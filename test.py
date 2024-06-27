import click

@click.command(
)
@click.option('--template-option', '-t', multiple=True, default=list)
def run(template_option):
    print(template_option)


run()
