import click

a =['nabin']

@click.group()
@click.option('--greeting', '-g', help='name of the greeting')
@click.option('--name', prompt="your name")
@click.pass_context
def cli(ctx, greeting, name):
    click.echo(f'{greeting}, {name}')
    ctx.ensure_object(dict)
    ctx.obj['greeting'] = greeting
    ctx.obj['name'] = name


@cli.command()
# @click.option('--name')
@click.pass_context
def print_name(ctx):
    click.echo(f'{ctx.obj["greeting"]}, {ctx.obj["name"]}')
    ctx.forward(get_name,name = 'kasichhwa')
    # ctx.invoke(get_name)


@cli.command()
@click.pass_context
def get_name(ctx,name):
    print(ctx.obj["name"])
    print("from getname", name)


cli()
