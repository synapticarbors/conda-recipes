from __future__ import print_function
from subprocess import check_output
import os
import sys
from collections import namedtuple

# Package object where npy flag specifies whether numpy is a dependency
P = namedtuple('P', ['name', 'npy'])

build_packages = [P('seaborn', True), 
                  P('mysql-connector-python', False)]

convert_packages = [P('rpy2', False)]

metapackages = []

shell = lambda cmd: check_output(cmd, shell=True, stderr=subprocess.STDOUT)

try:
    conda = os.environ['conda_build_app']
except KeyError:
    print('Set the environmental variable: conda_build_app')
    sys.exit(1)

def build(name):
    fn = shell('conda build --output %s' % name)
    if not exists(fn):
        out = shell('conda build %s' % name)
        print(out)

def convert(name):
    pass


print('Building conda packages')

for pkg in build_packages:
    if pkg.npy:
        for CONDA_NPY in ['18', '19']:
            os.environ['CONDA_NPY'] = CONDA_NPY
            build(pkg)
            del os.environ['CONDA_NPY']
    else:
        build(pkg)

