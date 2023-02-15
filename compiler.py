import py_compile


def compile_to_bytecode():
    py_compile.compile('main.py')


if __name__ == '__main__':
    print('im runnning')
    compile_to_bytecode()
