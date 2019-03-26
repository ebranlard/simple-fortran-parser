#!/usr/bin/env python

from __future__ import print_function
import os, sys, inspect
import unittest

MyDir=os.path.dirname(__file__)
pythonpath=os.path.realpath(os.path.abspath(os.path.join('../'+MyDir)))
sys.path.insert(0, pythonpath)

from fortran_file import*

def main():
    def loc(path):
        return os.path.join(MyDir,path)

    print(MyDir)

    F=FortranFile(loc('Interface.f90'))
    F.read()
    F.write               (loc('Interface_gen.f90'))
    F.write_signatures    (loc('Interface.h'))
    F.write_signatures_def(loc('Interface.def'))

    F=FortranFile(loc('ProfileTypes.f90'))
    F.read()
    F.write(loc('ProfileTypes_gen.f90'))
    F.write_type_tools(loc('ProfileAutoTools.f90'))

    # Regenerating files
    F=FortranFile(loc('ProfileTypes_gen.f90'))
    F.read()
    F.write(loc('ProfileTypes_gen_gen.f90'))

    F=FortranFile(loc('Interface_gen.f90'))
    F.read()
    F.write(loc('Interface_gen_gen.f90'))
    #F.write()
    #F.write_type_tools()
    #F.write_signatures_def()

import unittest
class Test(unittest.TestCase):
    def test_all(self):
        main()

if __name__ == '__main__':
    main()
