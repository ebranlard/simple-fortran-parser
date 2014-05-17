from __future__ import print_function
import re

def find_pos(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]



# Extracted from fissurroundedby developed for matlab2fortran
# looks if character s(p) is surrounded by the characters c1 and c2 
# returns a boolean , and the postion of these charactesrs
# [b p1 p2]=fissurroundedby('function [a b c]=issur([,])',10,'[',']')
# [b p1 p2]=fissurroundedby('function [a b c]=issur([,])',11,'[',']')
# [b p1 p2]=fissurroundedby('function [a b c]=issur([,])',10,'[',']')
# [b p1 p2]=fissurroundedby('function [''a b c'']=issur([,])',10,'''','''')
# [b p1 p2]=fissurroundedby('function [''a b c'']=issur([,])',12,'''','''')
# [b p1 p2]=fissurroundedby('(),()',4,'(',')')
def is_surrounded_by(s,p,c1,c2):
    p1=0;
    p2=0;
    ## stupid whiles
    # look backward
    notfound=True;
    i=p-1;
    while i>=0 and notfound:
        if c1!=c2 :
            # then if c2 is encountered we should break
            if s[i]==c2:
                break
        if s[i]==c1:
            notfound=False;
            p1=i;
        i=i-1;

    # look forward
    notfound=True;
    i=p+1;
    while i<len(s) and notfound:
        if c1!=c2 :
            # then if c1 is encountered we should break
            if s[i]==c1:
                break
        if s[i]==c2:
            notfound=False;
            p2=i;
        i=i+1;


    if p1==0 or p2==0:
        b=False; # not surrounded
    else:
        b=True;
    return(b,p1,p2)

# checks whether the position p in string s is wihtin some quotes
def is_in_quotes(s,p):
    # Quick and really dirty
    bInSingle=False
    bInDouble=False
    # We look before
    for i in range(p):
        if s[i]=='\'':
            if bInSingle:
                # That's a closing
                bInSingle=False
            elif bInDouble:
                # We are in double, ignore
                pass
            else:
                # That's an opening
                bInSingle=True
        if s[i]=='"':
            if bInDouble:
                # That's a closing
                bInDouble=False
            elif bInSingle:
                # We are in single, ignore double quotes
                pass
            else:
                # That's an opening
                bInDouble=True



            
    return(bInSingle or bInDouble)



if __name__ == "__main__":
    print(is_in_quotes("""0'""2'""",4))
#     (b,p1,p2)=is_surrounded_by(r'function [\'a b c\']=issur([,])',11,r'\'',r'\'')
#     print(b,p1,p2)
#     (b,p1,p2)=is_surrounded_by('dsfk[ & ] sdlkfj',6,'[',']')
#     print(b,p1,p2)
#     (b,p1,p2)=is_surrounded_by('function [a b c]=issur([,])',10,'[',']')
#     print(b,p1,p2)
#     (b,p1,p2)=is_surrounded_by('function [a b c]=issur([,])',11,'[',']')
#     print(b,p1,p2)
#     (b,p1,p2)=is_surrounded_by('function [a b c]=issur([,])',10,'[',']')
#     print(b,p1,p2)
#     (b,p1,p2)=is_surrounded_by('function [''a b c'']=issur([,])',12,r'\'',r'\'')
#     print(b,p1,p2)
#     (b,p1,p2)=is_surrounded_by('(),()',4,'(',')')
#     print(b,p1,p2)






