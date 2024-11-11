import io
import os
import pathlib
import tempfile

import gradio
from subprocess import Popen, PIPE
from midi_convert import convert_midi_to_scad, InternalStructureType

temporary_directory = tempfile.TemporaryDirectory()

OPENSCAD_BINARY = os.getenv('OPENSCAD_BINARY', 'openscad')
with open('examples/notes.txt') as f:
    DEFAULT_NOTES = f.read()


def run_openscad(input_filename, output_filename):
    process = Popen(
        [OPENSCAD_BINARY, '-o', output_filename, input_filename, '--export-format', 'stl'],
        stdout=PIPE,
        stderr=PIPE,
    )
    process.communicate()


def run_app(midi_bytes, notes, internal_structure_type):
    scad_file = tempfile.NamedTemporaryFile(dir=temporary_directory.name, mode='w', delete=False)
    stl_file = tempfile.NamedTemporaryFile(delete=False, dir=temporary_directory.name, suffix='.stl')
    scad_file_contents = convert_midi_to_scad(
        midi_file=io.BytesIO(midi_bytes),
        available_notes_string=notes,
        internal_structure_type=internal_structure_type,
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

examples_root = pathlib.Path(__file__).parent.joinpath("examples")

examples = [
    [
        str(examples_root.joinpath("potatoes_and_molasses.mid")),
        DEFAULT_NOTES,
        'RIBS',
    ],
]


iface = gradio.Interface(
    fn=run_app,
    title='MIDI to Music Box',
    description='''
    This app allows you to convert MIDI files to printable 3D model of the music box drum. 
    Tutorial is available on the [GitHub](https://github.com/PashaWNN/midi_to_music_box)
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
        gradio.Dropdown(
            label='Internal structure type',
            choices=[
                (v.value.title(), v) for _, v in
                InternalStructureType.__members__.items()
            ],
            value=InternalStructureType.HOLLOW.value.title(),
        )
    ],
    outputs=[gradio.Model3D()],
    examples=examples,
    allow_flagging='never',
).launch(debug=True, show_error=True)
