#!/usr/bin/env python
#############################################################
# fortran_to_c: classes and tools to convert fortran to c
#############################################################
# Description: 
# Written by : Emmanuel Branlard
# Date : October 2014
# Dependencies : python
# License : Feel free to modify and adapt it
#############################################################



def fortran_type_to_c(ftype):
    if ftype=='':
        C_TYPE='void*'
    else:
        # nasty non generic case
        tp=ftype.lower()
        if tp.find('integer')>=0:
            C_TYPE='int*'
        elif tp.find('character')>=0:
            C_TYPE='const char*'
        elif tp.find('real')>=0:
            C_TYPE='float*'
            if tp.find('double'):
                C_TYPE='double*'
        else:
            C_TYPE='TODO'

    return(C_TYPE)

def fortran_returntype_to_c(ftype):
    if ftype=='':
        C_TYPE='void'
    else:
        # nasty non generic case
        tp=ftype.lower()
        if tp.find('integer')>=0:
            C_TYPE='int'
        elif tp.find('real')>=0:
            C_TYPE='float'
            if tp.find('double'):
                C_TYPE='double'
        else:
            C_TYPE='TODO'

    return(C_TYPE)

