from __future__ import print_function
from parsing_tools import*
import re
from stderr import eprint

# split an expression looking for comment and continuation sign
def line_not_supported_warning(line):
    l=line.join(' ')
    if len(l)>0:
        if l.find('&!')>0:
            eprint('Warning: the following line can raise possible issue, since continuation with comments are not supported:')
            eprint(line)




# Bind fortran multiple lines
def bind_lines(lines):
    parsed_lines=[];
    bCat=False
    line_cat=[];
    #print('-----------------------------------------------------')
    #print(''.join(lines))
    #print('-----------------------------------------------------')
    for line in lines:
        line_not_supported_warning(line)
        l=line.strip()
        # If it's a comment, we cancel all
        if len(l)>0:
            if l[0]=='!':
                if bCat:
                    eprint('Warning: Problematic line the previous line wants to concatenate with the current one')
                    eprint('Previous line: ',line_cat)
                    eprint('Current line: ',l)
                    parsed_lines.append(line_cat)
                    parsed_lines.append(l)
                else:
                    parsed_lines.append(l)
                bCat=False
                continue
        if bCat:
            # let's see if it's a fortran multiple line string
            ll=l
            if l[0]=='&':
                ll=l[1:]
            if ll[-1]=='&':
                ll=l[:-1]
                # we'll continue cating
                bCat=True
            else:
                bCat=False
            line_cat=line_cat+ll
            #print(' ')
            #print('line cat:',line_cat)
            #print('       l:',l)
            #print('      ll:',ll,'bCat',bCat)
            #print(' ')
        else:
            #  Initialization of line_cat
            bCat=False
            if len(l)>0:
                if l[-1]=='&':
                    bCat=True
                    line_cat=l[:-1]
                else:
                    line_cat=l
            else:
                line_cat=''
        if not bCat:
            if len(line_cat)>0:
                parsed_lines.append(line_cat)
#                 print(line_cat)

    return(parsed_lines)

# Remove fortran comments from lines
# The case of comment after multiple line string is not supported
def remove_comments(lines):
    parsed_lines=[];
    comments=[];
    for line in lines:
        line=line.strip()
        pos=find_pos(line,'!')
        comment=''
        l=line
        if len(pos)>0:
            if pos[0]==0:
                # Trivial case, the whole line is a comment
                l=[];
                
            else:
                # We neglect comments within string
                i=0
                bOK=False
                while i<len(pos):
                    if not is_in_quotes(line,pos[i]):
                        bOK=True
                        break
                    i=i+1


                if bOK:
                    comment=l[(pos[i]):]
                    l=l[:(pos[i])]
                
#                 else:
#                     print('Prolematic line:')
#                     print(line)

        if len(l)>0:
            parsed_lines.append(l)
            comments.append(comment)
    return(parsed_lines,comments)


if __name__ == "__main__":
    L="""
    mODULe WingTypes
        uSE PrecisionMod, only: MK
        iMPLICit none
    integer , dimension(4) :: II=(/0 ,&
        0,0,0/)

    chaRACter(lEn=32) :: string='! I''trick you &
    & or maybe not?'  ! That's a messed up "case!"
    
    tYPE T_patch
        iNteger :: FirstPanel
        iNteger :: nChord
        iNteger :: nSpan
        logical :: bEmit
        logical :: bThick
        ! Geometry 
        real(MK) :: Area_Patch
        real(MK), dimension(:), pointer :: Area_Stripe =>null()
        ! Loads 
        real(MK),dimension(:,:),pointer :: Cp  =>null()   !< Pressure coefficient
        real(MK),dimension(:,:),pointer :: StripeLoad  =>null()   !< Integrated Force over the "chord wise direction of the strip"
        real(MK),dimension(:,:),pointer :: StripeLoadPoint=>null()!< Point
        real(MK), dimension(:), pointer :: Cl_Urel_Span_Force=>null()
        real(MK), dimension(:), pointer :: Cl_2D_Span_KJ =>null()
        real(MK) :: Cl_2D_Wing_KJ
        real(MK) :: L_KJ
        ! NW Panels 
        integer, dimension(:), pointer :: INW => null() !< index of NW Panels attached to this patch (for now nSpan)
    end type

    """
    L = L.split('\n')
    L = bind_lines(L);
    L = remove_comments(L);
    for l in L:
        print(l)

    
    L1="integer , dimension(4) :: II=(/0 ,&"
    L2="character(len=32) :: string='! I''trick you &"
    L3="& or maybe not?'  ! That's a messed up 'case!'"
