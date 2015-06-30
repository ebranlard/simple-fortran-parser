#!/usr/bin/env python

from __future__ import print_function
import os, sys, inspect
pythonpath=os.path.realpath(os.path.abspath('../'))
sys.path.insert(0, pythonpath)

from fortran_file import*

if __name__ == "__main__":
    F=FortranFile('Interface.f90')
    F.read()
    F.write('Interface_gen.f90')
    F.write_signatures('Interface.h')
    F.write_signatures_def('Interface.def')

    F=FortranFile('ProfileTypes.f90')
    F.read()
    F.write('ProfileTypes_gen.f90')
    F.write_type_tools('ProfileAutoTools.f90')

    # Regenerating files
    F=FortranFile('ProfileTypes_gen.f90')
    F.read()
    F.write('ProfileTypes_gen_gen.f90')

    F=FortranFile('Interface_gen.f90')
    F.read()
    F.write('Interface_gen_gen.f90')
    #F.write()
    #F.write_type_tools()
    #F.write_signatures_def()
