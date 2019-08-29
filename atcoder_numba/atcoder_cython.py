import sys
import os
import gzip
import base64
import subprocess


cc_suffix = '_cc'
exe_name = 'a.out'


def write_code(dir_, filename, s):
    with open('{}/{}{}.py'.format(dir_, filename, cc_suffix), 'w') as f:
        f.write('import subprocess\n')
        f.write('import gzip, base64, os\n')
        f.write('import stat\n\n')

        f.write('gz = {}\n'.format(s))
        f.write('bin = gzip.decompress(base64.b64decode(gz))\n')
        f.write('p = os.path.dirname(__file__)\n')
        f.write('pymain = os.path.join(p, "{}")\n'.format(exe_name))
        f.write('with open(pymain, "wb") as f:\n')
        f.write('    f.write(bin)\n')
        f.write('os.chmod(pymain, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)\n')
        f.write('if p == "":\n')
        f.write('    pymain = "./" + pymain\n')
        f.write('subprocess.call(pymain)\n')


def make_compile(dir_, filename):
    minor = sys.version_info[1]
    cmd = "cython -3 --embed {}/{}.pyx -o {}/{}.c".format(dir_, filename, dir_, filename)
    subprocess.call(cmd.split())
    cmd = "gcc -O3 -fPIC -I/usr/include/python3.{}m {}/{}.c -lpython3.7m -o {}/{}".format(minor, dir_, filename, dir_, filename)
    subprocess.call(cmd.split())


def main():
    path_ = os.path.abspath(sys.argv[-1])
    dir_ = os.path.dirname(path_)
    filename = os.path.splitext(os.path.basename(path_))[0]
    make_compile(dir_, filename)
    with open('{}/{}'.format(dir_, filename), 'rb') as f_bin:
        so = f_bin.read()
    gz = gzip.compress(so)
    asc = base64.b64encode(gz)
    write_code(dir_, filename, str(asc))
    sys.exit(0)

