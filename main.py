import click

from midi_convert import convert_midi_to_scad, SCAD_TEMPLATE, InternalStructureType


def get_default_output_filename() -> str:
    click_context = click.get_current_context()
    midi_file = click_context.params.get('midi_file')
    if midi_file is not None:
        return f'{midi_file.name}.scad'
    return 'out.scad'


def deactivate_prompts(ctx, _, value):
    if value:
        for p in ctx.command.params:
            if isinstance(p, click.Option) and p.prompt is not None:
                p.prompt = None
    return value


@click.command()
@click.option('-q/--quiet', default=False, is_eager=True, expose_value=False, callback=deactivate_prompts)
@click.option('--midi-file', prompt='MIDI file to process', help='MIDI file path', type=click.File('rb'))
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
    '--internal-structure',
    help='Choose the internal structure type.',
    default=InternalStructureType.HOLLOW,
    type=click.Choice(list(map(str, InternalStructureType.__members__.keys())), case_sensitive=False),
)
def run(midi_file, output_file, notes_file, template, internal_structure) -> None:
    scad_file_contents = convert_midi_to_scad(
        midi_file=midi_file,
        available_notes_string=notes_file.read(),
        template=template,
        internal_structure_type=internal_structure,
    )
    output_file.write(scad_file_contents)


if __name__ == "__main__":
    run()
