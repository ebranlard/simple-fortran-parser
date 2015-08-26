# Simple-fortran-parser

## Brief description
Tools for parsing a fortran file.

Main file: "fortran_file.py" : contains the different classes that correspond to a fortran file content (Modules, routines, declarations).


## Usage and examples
The parser can be used to:
- rewrite a file (in a standardized way)
- write header files for bind(C) routines (for  dlls and shared objects)
- write def    files for bind(C) routines (for windows dll)
- Automatically write some tools for derived types (read/write)

Look (and make) in the test directory to see what the script can do.


## Limitations (a lot) 
The script is not fully general. No parsing of the routine contents is done.
The parser is limited to verbose fortran 90 declarations of the kind:
    
    real(MK), dimension(:), intent(inout) :: A !<







