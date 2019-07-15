import sys
import importlib
import gzip
import base64
import os
import re
import numba
from numba.pycc import CC

config = {
    'module_name': 'numba_modules',
    'suffix': '_aot'
}


def aot_compile(file_name):
    """

    :param file_name:
    :return:
    """
    cc = CC(config['module_name'])
    func = []
    module = importlib.import_module(file_name)
    for dir_ in dir(module):
        e = eval('module.' + dir_)
        if type(e) == numba.targets.registry.CPUDispatcher \
                and e.nopython_signatures:
            cc.export(dir_, e.nopython_signatures[0])(e)
            func.append(dir_)

    cc.output_dir = os.curdir
    if func:
        cc.compile()
    return cc, func


def attach_module(f_out, cc, func):
    """

    :param f_out:
    :param cc:
    :param func:
    :return:
    """
    with open(cc.output_file, 'rb') as f_bin:
        so = f_bin.read()
    gz = gzip.compress(so)
    asc = base64.b64encode(gz)
    f_out.write("    atcoder={\n")
    f_out.write("        'name': '{}',\n".format(cc.name))
    f_out.write("        'file': '{}',\n".format(cc.output_file))
    f_out.write("        'func': {},\n".format(func))
    f_out.write("        'gz': {}\n".format(str(asc)))
    f_out.write("    }\n")
    f_out.write("    import gzip, base64\n")
    f_out.write("    gz = gzip.decompress(base64.b64decode(atcoder['gz']))\n")
    f_out.write("    with open(atcoder['file'], 'wb') as f:\n")
    f_out.write("        f.write(gz)\n")


def edit_code(cc, func, file_name):
    """
    :param cc:
    :param func:
    :param file_name:
    :return:
    """
    with open(file_name + '.py', 'r') as f_in:
        with open(file_name + config['suffix'] + '.py', 'w') as f_out:
            pattern_numba = re.compile(r"from(\s+)numba|import(\s+)numba|@numba|@jit|@njit")
            pattern_main = re.compile(r"if(\s+)__name__(\s+)==(\s)[\"\']__main__[\"\'](\s)*:")
            for line in f_in:
                if pattern_numba.match(line):
                    f_out.write('# ' + line)
                else:
                    f_out.write(line)
                if pattern_main.match(line):
                    if sys.argv[1] == "submit" and func:
                        attach_module(f_out, cc, func)
                    if func:
                        f_out.write("    from {} import {}\n".format(cc.name, ', '.join(func)))


def usage_message():
    print("Usage:")
    print("{} compile inputs -- Ahead-of-time compilation ".format(sys.argv[0]))
    print("{} submit inputs -- Create code for submit to Atcoder".format(sys.argv[0]))


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("compile", "submit"):
        usage_message()
        sys.exit(-1)

    if len(sys.argv) < 3:
        usage_message()
        print("atcoder-numba: error: the following arguments are required: inputs")
        sys.exit(-1)

    path_ = os.path.abspath(sys.argv[-1])
    dir_ = os.path.dirname(path_)
    os.chdir(dir_)
    sys.path.insert(0, dir_)
    file_name = os.path.splitext(os.path.basename(path_))[0]
    cc, func = aot_compile(file_name)
    edit_code(cc, func, 'main')


if __name__ == '__main__':
    main()