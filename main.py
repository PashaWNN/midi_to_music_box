import click

from midi_convert import midi_to_music_score
from templates import render_template, render_track

SCAD_TEMPLATE = 'scadfile.scad.template'


def get_default_output_filename() -> str:
    click_context = click.get_current_context()
    return click_context.params.get('midi_file', 'out') + '.scad'


def deactivate_prompts(ctx, _, value):
    if value:
        for p in ctx.command.params:
            if isinstance(p, click.Option) and p.prompt is not None:
                p.prompt = None
    return value


@click.command()
@click.option('-q/--quiet', default=False, is_eager=True, expose_value=False, callback=deactivate_prompts)
@click.option('--midi-file', prompt='MIDI file to process', help='MIDI file path', type=click.Path(exists=True))
@click.option(
    '--notes-file', '--notes',
    prompt='Notes list file',
    help='Notes file path.',
    type=click.File('r'),
    default='notes.txt'
)
@click.option(
    '--output-file',
    prompt='Output filename',
    help='Output file path.',
    default=get_default_output_filename,
    type=click.File('w'),
)
@click.option(
    '--template',
    help='SCAD template to use.',
    default=SCAD_TEMPLATE,
    type=click.Path(exists=True),
)
@click.option(
    '--disable-ribs',
    help='Disable ribs generation. May be useful for faster printing while experimenting.',
    default=False,
    type=click.BOOL,
    is_flag=True,
)
def run(midi_file, output_file, notes_file, template, disable_ribs) -> None:
    available_notes = notes_file.read().splitlines()
    music_score = midi_to_music_score(midi_file, available_notes=available_notes)
    scad_context = {
        'musicScore': render_track(music_score.as_track()),
        'enableRibs': 'false' if disable_ribs else 'true',
    }
    scad_file_contents = render_template(template, context=scad_context)
    output_file.write(scad_file_contents)


if __name__ == "__main__":
    run()
