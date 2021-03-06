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



# --------------------------------------------------------------------------------
# ---  Main program
# --------------------------------------------------------------------------------
DESCRIPTION="""Description:

   Example:
       $fortran_type_gen file1.f90 file2.f90
    """

def main(argv):
    # Configure argument parser
    try:
        import argparse
        bHasArgParse=True
    except Exception:
        bHasArgParse=False

    if bHasArgParse:
        parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,description=DESCRIPTION)
        parser.add_argument('--version', action='version', version='%(prog)s 1.0')
        parser.add_argument('files', nargs='+', help='List of files')
        args = parser.parse_args(argv)
        files=args.files
    else:
        files=argv

    # Looping on files and processing them
    for filename in files:
        filename_out=get_type_tool_filename(filename)
        process_file(filename,filename_out)

def process_file(filename,filename_out):
    with open(filename,'r') as f:
        f=FortranFile(filename);
        f.write_type_tools(filename_out)


if __name__ == "__main__":
    main(sys.argv[1:])
#     main(['test/WingTypes.f90','test/ObjectInfoTypes.f90','test/ProfileTypes.f90'])
#     main(['test/WingTypes.f90'])
