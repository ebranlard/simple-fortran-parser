#!/usr/bin/env python
#############################################################
# symlink:
#############################################################
# Description : use ./SCRIPT -h for help and description
# Written by : Emmanuel Branlard
# Date : May 2014
# Dependencies : python
# License : Feel free to modify and adapt it
#############################################################
from __future__ import print_function
import os, re
from fortran_file import*
import sys
import argparse



DESCRIPTION="""Description:

   Example: 
       $fortran_type_gen file1.f90 file2.f90
    """

def main(argv):
    # Configure argument parser
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,description=DESCRIPTION)
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('files', nargs='+', help='List of files')
    args = parser.parse_args(argv)
    files=args.files

    for filename in files:
#         (head,filebase)=os.path.split(f)
        (filebase,extension)=os.path.splitext(filename)
        filename_out=filebase+'Tools'+extension
        process_file(filename,filename_out)

def process_file(filename,filename_out):
    with open(filename,'r') as f:
        F=FortranFile(filename);
        F.read()
        F.write_type_tools()

#                 m.to_file(fout2)
# 
#             for l in L:
#                 fout.write(l+'\n')



if __name__ == "__main__":
    #main(sys.argv[1:])
    main(['test/WingTypes.f90'])

