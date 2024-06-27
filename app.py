import io
import os
import tempfile

import gradio
from subprocess import Popen, PIPE
from midi_convert import convert_midi_to_scad

temporary_directory = tempfile.TemporaryDirectory()

OPENSCAD_BINARY = os.getenv('OPENSCAD_BINARY', 'openscad')
with open('notes.txt') as f:
    DEFAULT_NOTES = f.read()


def run_openscad(input_filename, output_filename):
    process = Popen(
        [OPENSCAD_BINARY, '-o', output_filename, input_filename, '--export-format', 'stl'],
        stdout=PIPE,
        stderr=PIPE,
    )
    process.communicate()


def run_app(midi_bytes, notes, disable_ribs):
    scad_file = tempfile.NamedTemporaryFile(dir=temporary_directory.name, mode='w')
    stl_file = tempfile.NamedTemporaryFile(delete=False, dir=temporary_directory.name, suffix='.stl')
    scad_file_contents = convert_midi_to_scad(
        midi_file=io.BytesIO(midi_bytes),
        available_notes_string=notes,
        disable_ribs=disable_ribs,
    )
    scad_file.write(scad_file_contents)
    scad_file.flush()
    run_openscad(input_filename=scad_file.name, output_filename=stl_file.name)
    return stl_file.name


article = '''
    <p style='text-align: center'>
    <a href='https://github.com/PashaWNN/midi_to_music_box'>GitHub page (with tutorial)</a> | 
    <a href='https://habr.com/ru/articles/824136/'>Article (in Russian)</a>
    </p>
'''


iface = gradio.Interface(
    fn=run_app,
    title='MIDI to Music Box',
    description='''
    This app allows you to convert MIDI files to printable 3D model of the music box drum. 
    More on that in the README.md
    ''',
    inputs=[
        gradio.File(label='MIDI file', file_types=['.mid'], type='binary'),
        gradio.TextArea(
            label='Available notes',
            placeholder=(
                f'All available notes, from lowest to highest. There must be 18 of them. Example:\n{DEFAULT_NOTES}'
            ),
        ),
    ],
    additional_inputs=[
        gradio.Checkbox(label='Disable inner ribs generation')
    ],
    outputs=[gradio.Model3D()],
    allow_flagging='never',
).launch(debug=True, show_error=True)
