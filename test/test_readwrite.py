#!/usr/bin/env python
from __future__ import print_function
import os, sys, inspect
import unittest

MyDir=os.path.dirname(__file__)
pythonpath=os.path.realpath(os.path.abspath(os.path.join('../'+MyDir)))
sys.path.insert(0, pythonpath)

from fortran_file import*


import unittest
def loc(path):
    return os.path.join(MyDir,path)

class Test(unittest.TestCase):
    def test_read(self):
        pass
#         F=FortranFile(loc('_TODO/MathUtils.f90'))
#         F.write('_TODO/MathUtils_gen.f90')
#         F=FortranFile(loc('_TODO/MatlabFunctions.f90'))
#         F.write('_TODO/MatlabFunctions_gen.f90')
#         F=FortranFile(loc('_TODO/ProjLibVpm_m2p.f90'))
#         F.write('_TODO/ProjLibVpm_m2p_gen.f90')
#         F=FortranFile(loc('_TODO/ProjLibVpm_p2m.f90'))
#         F.write('_TODO/ProjLibVpm_p2m_gen.f90')
#         F=FortranFile(loc('_TODO/VectorAnalysisStrides.f90'))
#         F.write('_TODO/VectorAnalysisStrides_gen.f90')
#         F=FortranFile(loc('_TODO/Wind.f90'))
#         F.write('_TODO/Wind.f90')
#         F=FortranFile(loc('_TODO/fft.f90'))
#         F.write('_TODO/fft_gen.f90')

if __name__ == '__main__':
    unittest.main()
