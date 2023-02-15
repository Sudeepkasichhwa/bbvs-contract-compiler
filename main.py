import click
import py_compile
name_array = ['nabin']

def compile_to_bytecode():
    py_compile.compile('main.py')

@click.group()
@click.pass_context
def cli(ctx):
   pass

@cli.command()
@click.pass_context
def get_name_array(ctx):
    print(name_array)
    return name_array

@cli.command()
@click.option('--name')
@click.pass_context
def insert_name(ctx, name):
    name_array.append(name)
    print(name_array)
    compile_to_bytecode()

cli()
