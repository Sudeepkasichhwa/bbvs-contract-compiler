import click
import json
import py_compile
import sys

name_array = []
def load_json():
    f= open(r"C:\Users\acer\PycharmProjects\CLI\data.json")
    return json.load(f)
    print(json_data)
    f.close()
def write_json(new_data, file_name=r"C:\Users\acer\PycharmProjects\CLI\data.json"):
    # print(json.loads(new_data))
    with open(file_name,'r+') as file:
        file_data = json.load(file)
        file_data["name"].append(new_data)
        file.seek(0)
        json.dump(file_data,file,indent=4)
def initialize():
    json_data= load_json()
    for data in json_data['name']:
        name_array.append(data)
    print(json_data['name'])
def compile_to_bytecode():
    py_compile.compile('main.py')

@click.group()
@click.pass_context
def cli(ctx):
    initialize()

@cli.command()
@click.pass_context
def get_name_array(ctx):
    sys.stdout.write(json.dumps(name_array))
    return name_array

@cli.command()
@click.option('--name', nargs=2)
@click.pass_context
def insert_name(ctx, name):
    # key = ['candidat_id', 'name', 'image_url', 'post']
    # dict = {}
    # for i in range(len(name)):
    #     dict[key[i]]= name
    #
    # print(dict)
    print(name)
    print({'name':name[0],'age':name[1]})
    # name_array.append(name)
    write_json({'name':name[0],'age':name[1]})

    print(name_array)
    # compile_to_bytecode()

cli()
