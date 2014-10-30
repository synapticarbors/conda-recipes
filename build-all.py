from __future__ import print_function
import subprocess
from subprocess import check_output
import os
import sys
import glob
from collections import namedtuple

# Package object where npy flag specifies whether numpy is a dependency
P = namedtuple('P', ['name', 'npy'])

build_packages = [P('seaborn', True), 
                  P('mysql-connector-python', False)]

convert_packages = [P('rpy2_gohlke', False)]

metapackages = [P('eq-metapackage', False)]

shell = lambda cmd: check_output(cmd, shell=True, stderr=subprocess.STDOUT)

try:
    conda = os.environ['conda_app']
except KeyError:
    print('Set the environmental variable: conda_app')
    sys.exit(1)


def build(name):
    fn = shell('{conda} build --output {name}'.format(conda=conda, name=name))
    fn = fn.strip()
    print(fn)
    if not os.path.exists(fn):
        out = shell('{conda} build {name}'.format(conda=conda, name=name))
        print(out)

    return fn

def convert(name):
    exe_file = glob.glob(os.path.join(name, '*.exe'))[0]
    fn = shell('{conda} convert --dry-run {exe_file}'.format(conda=conda, exe_file=exe_file))
    fn = os.path.abspath(fn.replace('Wrote:', '').strip())
    print(fn)
    if not os.path.exists(fn):
        out = shell('{conda} convert {exe_file}'.format(conda=conda, exe_file=exe_file))
        print(out)

    return fn


for pkg in build_packages:
    print(pkg.name)
    if pkg.npy:
        for CONDA_NPY in ['18', '19']:
            os.environ['CONDA_NPY'] = CONDA_NPY
            fn = build(pkg.name)
            del os.environ['CONDA_NPY']
    else:
        fn = build(pkg.name)


for pkg in convert_packages:
    print(pkg.name)
    if pkg.npy:
        for CONDA_NPY in ['18', '19']:
            os.environ['CONDA_NPY'] = CONDA_NPY
            fn = convert(pkg.name)
            del os.environ['CONDA_NPY']
    else:
        fn = convert(pkg.name)

for pkg in metapackages:
    print(pkg.name)
    if pkg.npy:
        for CONDA_NPY in ['18', '19']:
            os.environ['CONDA_NPY'] = CONDA_NPY
            fn = build(pkg.name)
            del os.environ['CONDA_NPY']
    else:
        fn = build(pkg.name)

