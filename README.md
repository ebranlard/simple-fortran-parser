[![Build Status](https://travis-ci.org/ebranlard/simple-fortran-parser.svg?branch=master)](https://travis-ci.org/ebranlard/simple-fortran-parser)

# Simple-fortran-parser

## Brief description
Tools for parsing a fortran file.

The main module: `fortran_file.py` : contains the different classes that correspond to a fortran file content (Modules, routines, declarations).

Different executable scripts are provided to perform operations on the fortran files (see next section).


## Usage and examples
The parser can be used to:
- rewrite a file (in a standardized way)
- write header files for bind(C) routines (for  dlls and shared objects)
- write def    files for bind(C) routines (for windows dll)
- Automatically write some tools for derived types (read/write)

Look (and make) in the test directory to see what the script can do.


## Generation of headers from fortran file
Usage:
```bash
python fortran_signature_gen.py File.f90
```
If the file `File.f90` has the following content:
```fortran
subroutine it_setTmax(t_max_in) BIND(C,name='it_setTmax')
    real(C_DOUBLE),intent(in) :: t_max_in;
    call setTmax(real(t_max_in,MK))
end subroutine
integer(C_INT) function it_time_increment() BIND(C,name='it_incrementtime')
    it_time_increment=12;
end function
```
this will generate the following header file
```c
void it_settmax(double* t_max_in);
int it_incrementtime();
```



## Limitations 
The script is not general. No parsing of the routine contents is done.
The parser is limited to verbose fortran 90 declarations of the kind:
```fortran    
    real(MK), dimension(:), intent(inout) :: A !<
```







