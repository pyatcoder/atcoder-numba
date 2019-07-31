import sys
import importlib
import gzip
import base64
import os
import re
import queue
import runpy
import numba
from numba.pycc import CC

config = {
    'module_name': 'numba_modules',
    'suffix': '_aot',
    'example': 'in_1.txt'
}


def aot_compile(file_name):
    """

    :param file_name:
    :return:
    """
    cc = CC(config['module_name'])
    func = []
    signatures = []
    if os.path.exists(config['example']):
        f = os.open(config['example'], os.O_RDONLY)
        stdin_bk = os.dup(0)
        os.dup2(f, 0)
        try:
            module = runpy.run_module(file_name, run_name="__main__")
            for k in module:
                e = module[k]
                if type(e) == numba.targets.registry.CPUDispatcher \
                        and e.nopython_signatures:
                    cc.export(k, e.nopython_signatures[0])(e)
                    func.append(k)
                    signatures.append(str(e.nopython_signatures[0]))
            auto_jit = True
        finally:
            os.dup2(stdin_bk, 0)
            os.close(f)
    else:
        module = importlib.import_module(file_name)
        for dir_ in dir(module):
            e = eval('module.' + dir_)
            if type(e) == numba.targets.registry.CPUDispatcher \
                    and e.nopython_signatures:
                cc.export(dir_, e.nopython_signatures[0])(e)
                func.append(dir_)
                signatures.append(str(e.nopython_signatures[0]))
        auto_jit = False

    cc.output_dir = os.curdir
    if func:
        cc.compile()
    return cc, func, signatures, auto_jit


def signature_info(f_out, func, signatures):
    for f, s in zip(func, signatures):
        f_out.write("# {}: {}\n".format(f, s))


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
    f_out.write("atcoder={\n")
    f_out.write("    'name': '{}',\n".format(cc.name))
    f_out.write("    'file': '{}',\n".format(cc.output_file))
    f_out.write("    'func': {},\n".format(func))
    f_out.write("    'gz': {}\n".format(str(asc)))
    f_out.write("}\n")
    f_out.write("import gzip, base64\n")
    f_out.write("gz = gzip.decompress(base64.b64decode(atcoder['gz']))\n")
    f_out.write("with open(atcoder['file'], 'wb') as f:\n")
    f_out.write("    f.write(gz)\n")


def edit_code(file_name, cc, func, signatures, auto_jit):
    """
    :param cc:
    :param func:
    :param signatures
    :param file_name:
    :return:
    """
    code_flag = True
    que = queue.Queue()
    mode = 0  # 0 通常、1 関数内、2 デコレータ
    pattern_numba = re.compile(r"from(\s+)numba|import(\s+)numba")
    pattern_decorator = re.compile(r"@")
    pattern_def = re.compile(r"def(\s+)")
    pattern_empty = re.compile(r"\s*\n$")
    pattern_comment = re.compile(r"\s*#")
    pattern_indent = re.compile(r"\s+")

    def get_func_name(s):
        m = re.match(r"def(\s+)(\w+)", s)
        return m.group(2)

    def write_func_info(s):
        nonlocal code_flag
        nonlocal mode
        func_name = get_func_name(s)
        if func_name in func:
            if code_flag:
                if auto_jit:
                    signature_info(f_out, func, signatures)
                if sys.argv[1] == "embed":
                    attach_module(f_out, cc, func)
                f_out.write("from {} import {}\n".format(cc.name, ', '.join(func)))
                code_flag = False
            if mode == 2:
                while not que.empty():
                    t = que.get()
                    if pattern_decorator.match(t):
                        f_out.write('# ' + t)
                    else:
                        f_out.write(t)
            f_out.write('# ' + s)
            mode = 1
        else:
            if mode == 2:
                while not que.empty():
                    t = que.get()
                    f_out.write(t)
            f_out.write(s)
            mode = 0

    with open(file_name + '.py', 'r') as f_in:
        with open(file_name + config['suffix'] + '.py', 'w') as f_out:
            for line in f_in:
                if mode == 0:
                    if pattern_numba.match(line):
                        f_out.write('# ' + line)
                    elif pattern_decorator.match(line):
                        mode = 2
                        que.put(line)
                    elif pattern_def.match(line):
                        write_func_info(line)
                    else:
                        f_out.write(line)
                elif mode == 1:
                    if pattern_empty.match(line):
                        f_out.write('\n')
                    elif pattern_comment.match(line):
                        f_out.write(line)
                    elif pattern_indent.match(line):
                        f_out.write('# ' + line)
                    else:
                        mode = 0
                        f_out.write(line)
                elif mode == 2:
                    if pattern_decorator.match(line) or\
                            pattern_empty.match(line) or\
                            pattern_comment.match(line):
                        que.put(line)
                    elif pattern_def.match(line):
                        write_func_info(line)
                    else:
                        while not que.empty():
                            t = que.get()
                            f_out.write(t)
                        f_out.write(line)
                        mode = 0


def usage_message():
    print("Usage:")
    print("{} compile inputs -- Ahead-of-time compilation ".format(sys.argv[0]))
    print("{} embed inputs -- Create code for submit to Atcoder".format(sys.argv[0]))


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("compile", "embed"):
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
    cc, func, signatures, auto_jit = aot_compile(file_name)
    edit_code(file_name, cc, func, signatures, auto_jit)


if __name__ == '__main__':
    main()