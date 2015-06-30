#!/usr/bin/env python


# --------------------------------------------------------------------------------
# ---  PARAMS
# --------------------------------------------------------------------------------
Types=['integer','double precision','real','logical']
Dims =[1,0]




# --------------------------------------------------------------------------------
# ---  
# --------------------------------------------------------------------------------
import os
import sys
import glob

if len(sys.argv)>1:
    Files=sys.argv[1:]
else:
    Files=glob.glob('*.Template')


# print('Template files:')
# print(Files)

if len(Files)>0:

    filebase=Files[0].replace('.Template','')
    #
    for typ in Types:
        for dim in Dims:
            #
            TD=typ[0]+'%d'%dim
            TD=TD.upper()
            td=TD.lower()
            filename=filebase+TD+'.f90'
            if dim==0:
                TYPE_AND_DIM=typ
            else:
                TYPE_AND_DIM=typ+', dimension(n1)'
            #
            fr=open(Files[0],'r')
            fw=open(filename,'w')
            for l in fr.readlines():
                l=l.replace('<TD>',TD)
                l=l.replace('<N1>','n1')
                l=l.replace('<td>',td)
                l=l.replace('<TYPE_AND_DIM>',TYPE_AND_DIM)
                fw.write(l)
            fw.close()
            fr.close()




