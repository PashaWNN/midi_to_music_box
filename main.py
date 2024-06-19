import sys
from midi_convert import midi_to_music_score
from templates import render_template, render_multitrack

SCAD_TEMPLATE = 'scadfile.scad.template'
NOTES_FILE = 'notes.txt'


def load_notes() -> list[str]:
    with open(NOTES_FILE) as f:
        return f.read().splitlines()


def run(*args) -> None:
    if len(args) < 2:
        raise ValueError("You didn't specify input file")
    input_filename = args[1]
    if len(args) > 2:
        output_filename = args[2]
    else:
        output_filename = args[1] + '.scad'
    available_notes = load_notes()
    music_score = midi_to_music_score(input_filename, available_notes=available_notes)
    scad_context = {
        'musicScore': render_multitrack(music_score.as_track()),
    }
    scad_file = render_template(SCAD_TEMPLATE, context=scad_context)
    with open(output_filename, 'w') as f:
        f.write(scad_file)


if __name__ == "__main__":
    run(*sys.argv)
