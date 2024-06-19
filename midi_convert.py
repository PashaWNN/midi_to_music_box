import mido

NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
OCTAVES = list(range(11))
NOTES_IN_OCTAVE = len(NOTES)


def number_to_note(number: int) -> str:
    octave = number // NOTES_IN_OCTAVE - 1
    assert octave in OCTAVES, 'Invalid octave number'
    assert 0 <= number <= 127, 'Invalid MIDI note number'
    note = NOTES[number % NOTES_IN_OCTAVE]

    return f'{note}{octave}'


def _indices(lst: list, element, start: int = 0) -> list[int]:
    """Get all indices of an element in a list."""
    result = []
    offset = -1
    while True:
        try:
            offset = lst.index(element, offset + 1)
        except ValueError:
            return result
        result.append(offset + start)


class NoteNumberGetter:
    """
    This class allows to get note number by note character
    So that some note is available at different numbers, different number is returned each time.
    """
    def __init__(self, available_notes: list[str]) -> None:
        self._notes_mapping = {
            **{
                note: (_indices(available_notes, note, start=1), -1)
                for note in available_notes
            }
        }

    def get_note_number(self, note: str) -> int:
        note_numbers, last_used_index = self._notes_mapping[note]
        last_used_index = (last_used_index + 1) % len(note_numbers)
        note_number = note_numbers[last_used_index]
        self._notes_mapping[note] = (note_numbers, last_used_index)
        return note_number


class MusicScore:
    def __init__(self, score: list[list[str]], available_notes: list[str]):
        self._score = score
        self._note_number_getter = NoteNumberGetter(available_notes)

    def _get_note_number(self, note: str) -> int:
        return self._note_number_getter.get_note_number(note)

    def as_track(self) -> list[list[int]]:
        """
        MusicScore representation for SCAD script.
        Contains a list of lists, in which each list represents a single quant containing note numbers.
        """
        track = []
        for note_track in self._score:
            track.append(list(map(lambda note: self._get_note_number(note), note_track)))
        return track


def get_midi_time_quant(midi_file: mido.MidiFile) -> int:
    """
    Get the time quant to generate correct sequence for music box.
    This function has a limitation: only one time quant could be used for a music box,
    so first note_off time that differs from zero is used (i. e. first note duration is used)
    """
    for track in midi_file.tracks:
        for message in track:
            if message.type == 'note_off' and message.time > 0:
                return message.time
    raise ValueError('Could not find any note with valid time in MIDI file.')


def midi_to_music_score(midi_filename: str, available_notes: list[str]) -> MusicScore:
    midi_file = mido.MidiFile(midi_filename)
    score = [[]]
    time_quant = get_midi_time_quant(midi_file)
    for track in midi_file.tracks:
        for message in track:
            if message.type not in ('note_on', 'note_off'):
                continue
            elapsed = message.time // time_quant
            score.extend([] for _ in range(elapsed))
            if message.type == 'note_on':
                current_frame = score[-1]
                note = number_to_note(message.note)
                if note not in available_notes:
                    raise ValueError(f'MIDI file contains notes that are not available in music box: {note}.')
                current_frame.append(note)
    return MusicScore(score, available_notes)
