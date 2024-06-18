import string
import typing


def render_template(
    template_filename: str,
    context: dict[str, typing.Any]
) -> str:
    with open(template_filename) as f:
        template = string.Template(f.read())
    return template.safe_substitute(context)


def render_multitrack(tracks: list[list[int]]) -> str:
    return '\n'.join([
        '[',
        *[f'  [{", ".join(map(str, track))}],' for track in tracks],
        f'];  // lines count: {len(tracks[0])}'
    ])


def render_indices(notes_mapping: dict[str, int]):
    return '\n'.join([
        '[',
        *[f'    [{i}, {i}],' for i in notes_mapping.values()],
        ']'
    ])
