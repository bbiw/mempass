
import pkg_resources
import click

@click.command()
def cli():
    click.echo('hello')
    sp = pkg_resources.resource_string(__name__,'lists/special.txt')
    print(sp.splitlines())
