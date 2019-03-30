#!/usr/bin/env python
#############################################################
# fortran_file: classes to read/parse/write a fortran file
#############################################################
# Description: 
# Written by : Emmanuel Branlard
# Date : May 2014
# Dependencies : python
# License : Feel free to modify and adapt it
#############################################################

# --------------------------------------------------------------------------------
# --- Notes 
# --------------------------------------------------------------------------------
# - Declarations are detected with "::"
# - Comments might be messed up due to long line merging. see remove_comments 


# --------------------------------------------------------------------------------
# ---  
# --------------------------------------------------------------------------------
from __future__ import print_function
import sys 
import re
import os

from fortran_parse_tools import*
from fortran_to_c import*
from stderr import eprint



# The routines of the tools are written by the method write_tools_[INTERFACE] of the class FortranType
# e.g.  FortranType.write_tool_init,  FortranType.write_tool_term
#
# These methods then calls FortranDeclaration.get_init  for each of the declarations of the type
TOOLS=[
        {'interface':'init'     , 'routines':['0']} ,
        {'interface':'initp'    , 'routines':['0','1']} ,
        {'interface':'term'     , 'routines':['0']} ,
        {'interface':'termp'    , 'routines':['0','1']} ,
        {'interface':'write'    , 'routines':['0']} ,
        {'interface':'writep'   , 'routines':['0','1']} ,
        {'interface':'read'     , 'routines':['0']} ,
        {'interface':'readp'    , 'routines':['0','1']} ,
        ]
TOOLS_INPUT=[
        {'interface':'set_var'  , 'routines':['s','v']} , # Only for input types
        ]


# --------------------------------------------------------------------------------
# ---  THIS IS WHERE THE CHOICE OF A NAME TAKE PLACE
# --------------------------------------------------------------------------------
S_TYPE_TOOLS='AutoTools'
def get_type_tool_filename(filename):
    (filebase,extension)=os.path.splitext(filename)
    filename_out=filebase.replace('Types','')+S_TYPE_TOOLS+extension
    return(filename_out)

def get_type_tool_module(module):
    module_out=module.replace('Types','')+S_TYPE_TOOLS
    return(module_out)


# --------------------------------------------------------------------------------
# ---  FortranFile class
# --------------------------------------------------------------------------------
class FortranFile:
    def __init__(self,filename=None,lines=None):
        self.filename=filename
        self.Modules=[]
        self.Routines=[] # standalone routines

        if self.filename is not None:
            if os.path.exists(self.filename):
                self.read()
        elif lines is not None:
            self.parse(lines)
        else:
            pass

    def read(self):
        # Reading file
        with open(self.filename,'r') as f:
            self.parse(f.readlines())

    def parse(self,Lines):
        if type(Lines) is not list:
            Lines=Lines.split('\n')
        L = bind_lines(Lines);
        (L,comments) = remove_comments(L);
        #print('\n'.join(L))
        # --------------------------------------------------------------------------------
        # --- Extracting Modules, types and Use Statements,
        #  really nasty I should have extracted modules only and then pass it around...
        # --------------------------------------------------------------------------------
        self.Modules=[]
        self.Routines=[]
        bIsInType       = False
        bIsInMethod     = False
        bIsInStandalone = False
        bIsInModule     = False
        m  = None
        s  = None
        ss = None
        t  = None
        for (l,c) in zip(L,comments):
            # always concatenate end with the keyword
            if l[0:4].lower()=='end ':
                l='end'+l[4:]

            words=l.replace('  ',' ').split(' ')
            words_low=l.lower().split(' ')
            if words[0].lower()=='module':
                # This is a new module
                m=(FortranModule(words[1]))
                bIsInModule=True
            elif words[0].lower()=='endmodule':
                self.Modules.append(m)
                bIsInModule=False

            if 'subroutine' in words_low or 'function' in words_low :
                # This is a new subroutine
                s=(FortranMethod(raw_name=l))
                bIsInMethod=True
                if not bIsInModule:
                    bIsInStandalone=True
                    #print('Starting a standalone routine!',l)
            elif words[0].lower()=='endsubroutine':
                if bIsInModule:
                    m.MethodList.append(s) 
                    bIsInMethod=False
                elif bIsInStandalone:
                    self.Routines.append(s)
                else:
                    eprint('Error, subroutine not in modules or not standalone!')
                    sys.exit(-1)
            elif words[0].lower()=='endfunction':
                if bIsInModule:
                    m.MethodList.append(s)
                    bIsInMethod=False
                else:
                    eprint('Error, subroutines not in modules not handled yet')
            elif words[0].lower()=='use':
                if (not bIsInModule) and (not bIsInStandalone):
                    eprint('Error, use statements found outside of module or subroutine!')
                    eprint('    line:  ',l)
                else:
                    if not bIsInMethod :
                        m.UseStatements.append(l,c)
                    else:
                        s.append_raw(l,c)

            elif words[0].lower()=='type':
                if not bIsInMethod:
                    if l.find('save')>0 or l.find('::')>0:
                        # TODO: type (XXX), save :: myvar  (in a module declaration)
                        eprint('Warning: type attributes declaration not yet supported: '+l)
                    else:
                         # Creating a new type
                        t=FortranType(words[1])
                        bIsInType=True
                else:
                    s.append_raw(l,c)
            elif words[0].lower()=='endtype':
                m.TypeList.append(t)
                bIsInType=False
            else:
                if bIsInType:
                    t.append(l,c)
                elif bIsInMethod:
                    s.append_raw(l,c)
                #else:
                #    print('Discarded line:',l)

        if bIsInModule:
            raise Exception('No end of module found')

        # --------------------------------------------------------------------------------
        # --- Analyse raw data
        # --------------------------------------------------------------------------------
        for m in self.Modules:
            m.analyse_raw_data()
        for s in self.Routines:
            s.analyse_raw_data()
#                     for l in t.raw_lines:
#                         print(l)

    def tostring(self,verbose=True):
        """ File to string """
        s=''
        # Modules
        for i,m in enumerate(self.Modules):
            s+=m.tostring()
            if i<len(self.Modules)-1:
                s+='\n'
        # Spacing between modules and standalone routines
        if len(self.Routines)>0 and len(s)>0:
            s+='\n'
        # Standalone subroutines (no indent)
        for i,r in enumerate(self.Routines):
            s+=r.tostring(indent='',verbose=verbose)
            if i<len(self.Routines)-1:
                s+='\n'+'\n'
        return s


    def write(self,filename_out=''):
        if filename_out=='':
            (filebase,extension)=os.path.splitext(self.filename)
            filename_out=filebase+'_gen'+extension
        with open(filename_out,'w') as f:
            for m in self.Modules:
                m.write_to_file(f)
        #    f=open(filename_out,'w')
        #elif filename_out=='STDOUT':
        #    f=sys.stdout
        #else:
        #    f=open(filename_out,'w')

        #for m in self.Modules:
        #    m.write_to_file(f)

    def write_type_tools(self,filename_out=''):
        if filename_out=='':
            filename_out=get_type_tool_filename(self.filename)
        with open(filename_out,'w') as f:
            for m in self.Modules:
                m.write_type_tools(f)


    def write_signatures(self,filename_out='',verbose=False):
        if filename_out=='':
            (filebase,extension)=os.path.splitext(self.filename)
            filename_out=filebase+'.h'
        elif filename_out=='STDOUT':
            f=sys.stdout
        else:
            f=open(filename_out,'w')
        if verbose:
            f.write('// --- Signatures from file: '+self.filename+'\n')
        for m in self.Modules:
            m.write_signatures(f,verbose)
        if f is not sys.stdout:
            f.close()


    def write_signatures_def(self,filename_out=''):
        if filename_out=='':
            (filebase,extension)=os.path.splitext(self.filename)
            filename_out=filebase+'.def'
        if filename_out=='STDOUT':
            f=sys.stdout
        else:
            f=open(filename_out,'w')
        if len(self.Modules)>1:
            raise(Exception('More than one module'))
        else:
            m=self.Modules[0]
            libname=m.name
            if len(m.name)>9:
                if m.name[0:9]=='Interface':
                    libname=m.name[9:];
                    libname=libname.lower()
            #f.write('LIBRARY lib%s.dll\n'%libname)
            #f.write('EXPORTS\n')
            m.write_signatures_def(f)
        if f is not sys.stdout:
            f.close()




class FortranModule:
    def __init__(self,name):
        self.name=name

        # UseStatement
        self.UseStatements=FortranUseStatements(line=[])
        # Types
        self.TypeList=[]
        self.type_dependencies=[]
        self.type_depend_mod=[]
        # Interfaces
        # Variables
        # Methods
        self.MethodList=[]
        # Misc
        self.indent='    '

    def analyse_raw_data(self):
        # Types
        #print('MODULE: '+self.name)

        # --------------------------------------------------------------------------------
        # ---  Analysying sub elements
        # --------------------------------------------------------------------------------
        # Analyse Types
        for t in self.TypeList:
            #print('TYPE: '+t.raw_name)
            t.analyse_raw_data()
            self.type_dependencies.append(t.dependencies)

        # Analyse use statements
        self.UseStatements.analyse_raw_data()
        
        # Analyse Methods
        for m in self.MethodList:
            #print('Analysing raw input for Method: '+m.name+m.raw_name)
            m.analyse_raw_data()


        # --------------------------------------------------------------------------------
        # --- Type Dependencies
        # --------------------------------------------------------------------------------
        # Analyse Types dependencies at module level
        D=self.type_dependencies;
        D=[x.lower() for y in D for x in y if x is not None ]
        # Removing duplicates
        D2=[]
        [D2.append(x) for x in D if x not in D2];
        # Removing dependencies from types that are in our module
        D3=[t.raw_name.lower() for t in self.TypeList ]
        D2=[x for x in D2 if x not in D3];

        self.type_dependencies=D2;
        # --------------------------------------------------------------------------------
        # ---  Attempting to resolve dependencies
        # --------------------------------------------------------------------------------
        for t in self.type_dependencies:
            # Attempt 1: explicit include
            mod_found=self.UseStatements.find_in_only_list(t)
            if mod_found is None:
                # Attempt 2: finding in module name
                # removing any extra character from type name
                t2=t
                if t[0].lower()=='t':
                    t2=t2[1:]
                if t2[0].lower()=='_':
                    t2=t2[1:]
                mod_found=self.UseStatements.find_in_module_name(t2)

                pass
            m=mod_found
            if m is not None:
                if len(m)>1:
                    eprint('Warning Multiple options : Type %s - Module %s'%(t,m))
                m=m[0]
                #eprint('Solved Dependency: Type %s - Module %s'%(t,m))
            else:
                eprint('Warning: Unresolved Dependency: Type %s'%(t))

            self.type_depend_mod.append(m)

    def tostring(self):
        """ Module to string """
        s=''
        s+='module %s\n'%self.name
        # Use statements
        s+=self.UseStatements.tostring(indent=self.indent)
        s+='%simplicit none\n'%self.indent
        ## Types
        for i,t in enumerate(self.TypeList):
            s+=t.tostring(self.indent)
            if i<len(self.TypeList)-1:
                s+='\n'

        ## Subroutines 
        if len(self.MethodList)>0:
            s+='contains\n'
            for m in self.MethodList:
                s+=m.tostring(indent=self.indent)+'\n'+'\n'
        s+='end module %s'%self.name
        return s

    def write_to_file(self,f):
        f.write(self.tostring())

    def write_signatures(self,f,verbose=False):
        if verbose:
            f.write('// Signatures from module %s\n'%self.name)
        for s in self.MethodList:
            if(s.bind_name!=''):
                s.write_signature(f,verbose)

    def write_signatures_def(self,f):
        for s in self.MethodList:
            if(s.bind_name!=''):
                s.write_signature_def(f)

    def write_type_tools(self,f):
        f.write('module %s\n'%get_type_tool_module(self.name))
        f.write('    ! Module containing type: \n')
        f.write('    use %s\n'%(self.name))
        # Resolved dependencies
        if len(self.type_depend_mod)>0:
            f.write('    ! Friend modules: \n')
        for (m,t) in zip(self.type_depend_mod,self.type_dependencies):
            if m is not None:
                f.write('    use %s\n'%(get_type_tool_module(m)))
            else:
                f.write('!    use %s\n'%(get_type_tool_module(t)))

        f.write('    implicit none\n\n')
        f.write('    private\n\n')


        # --------------------------------------------------------------------------------
        # ---  Interfaces and public attributes
        # --------------------------------------------------------------------------------
        for t in self.TypeList:
            if(t.pretty_name.lower().find('inputs')>0):
                TOOLS_LOC=TOOLS+TOOLS_INPUT
            else:
                TOOLS_LOC=TOOLS

            for tool in TOOLS_LOC:
                if len(tool['interface'])>0:
                    f.write('    interface %s_%s; module procedure &\n'%(t.pretty_name,tool['interface']))
                    for (routine_name,i) in zip(tool['routines'],range(len(tool['routines']))):
                        end_line=',&'
                        if i==len(tool['routines'])-1:
                            end_line=''
                        f.write('          %s_%s_%s%s\n'%(t.pretty_name,tool['interface'],routine_name,end_line))
                    f.write('    end interface %s_%s\n'%(t.pretty_name,tool['interface']))
            for tool in TOOLS_LOC:
                if len(tool['interface'])>0:
                    f.write('    public :: %s_%s\n'%(t.pretty_name,tool['interface']))
                else:
                    for routine_name in tool['routines']:
                        f.write('    public :: %s_%s\n'%(t.pretty_name,routine_name))

            f.write('\n')




        f.write('contains\n')


        # --------------------------------------------------------------------------------
        # ---  Functions
        # --------------------------------------------------------------------------------
        # The functions of the tools are written by the method write_tools_[INTERFACE] of the class FortranType
        for t in self.TypeList:
            if(t.pretty_name.lower().find('inputs')>0):
                TOOLS_LOC=TOOLS+TOOLS_INPUT
            else:
                TOOLS_LOC=TOOLS
            for tool in TOOLS_LOC:
                if len(tool['interface'])>0:
                    routines=tool['routines'];
                    func_call='t.write_tool_%s(f,routines)'%tool['interface']
                    eval(func_call)
#                 t.write_type_tools(f,self.indent)

        f.write('end module %s\n'%get_type_tool_module(self.name))


# --------------------------------------------------------------------------------}
# --- Fortran Use Statement
# --------------------------------------------------------------------------------{
class FortranUseStatements:
    def __init__(self,line=[],comments=[]):
        self.raw_lines=line
        self.comments=comments
        self.statements=[]
        self.indent='    '
        # static data

    def append(self,line,comment=''):
        self.raw_lines.append(line)
        self.comments.append(comment)

    def analyse_raw_data(self):
        for l in self.raw_lines:
            #d=self.default_dict_.copy()
            d=dict(module='',only_list=[])
            sp=l.split(':')
            if len(sp)>1:
                d['only_list']=sp[1].replace(' ','').split(',')

            d['module']=sp[0].replace(',',' ').replace('  ',' ').split(' ')[1].strip()

            self.statements.append(d)

    def tostring(self,indent=''):
        """ Use statement to string """
        s='' 
        for st in self.statements:
            u='use '+st['module']
            if len(st['only_list'])>0:
                u+=', only: '
                for o in st['only_list']:
                    u+=o+', '
                u=u[:-2]
            s+=indent + u +'\n'
        return s

    def __repr__(self):
        return self.tostring()

    def write_to_file(self,f,indent):
        f.write(self.tostring(indent))

    def find_in_only_list(self,t):
        found=None
        for s in self.statements:
            if len(s['only_list'])>0:
                found=[o for o in s['only_list'] if o.lower()==t.lower() ]
                if len(found)>0:
                    found=[s['module']]
                    break
                else:
                    found=None

        return found

    def find_in_module_name(self,t):
        found=[o['module'] for o in self.statements if o['module'].lower().find(t.lower())>=0 ]
        if len(found)==0:
            found=None
        return found





# --------------------------------------------------------------------------------}
# --- Fortran Type 
# --------------------------------------------------------------------------------{
class FortranType:
    def __init__(self,name):
        # Raw data
        self.raw_lines=[]
        self.raw_name=name

        # Derived data
        self.bRecursive=False
        # Main Data
        self.pretty_name=self.pretty_type(name)
        self.dependencies=[]
        self.Declarations=[]

        # Misc
        self.indent='    '

    def append(self,line,comment=''):
        self.raw_lines.append(line)
        self.Declarations.append(FortranDeclaration(line,comment,inType=True))

    def analyse_raw_data(self):
        for d in self.Declarations:
            if not d['built_in']:
                self.dependencies.append(d['type'])
                if d['type']==self.raw_name:
                    eprint('Info: The following type is recursive:'+ d['type'])
                    self.bRecursive=True

    def tostring(self,indent=''):
        """ Type to string"""
        s=''
        s+='%stype %s\n'%(indent,self.raw_name)
        for d in self.Declarations:
            s+=d.tostring(indent+self.indent)+'\n'
        s+=indent+'end type\n'
        return s

    def write_to_file(self,f,indent=''):
        f.write(self.tostring(indent))

    # --------------------------------------------------------------------------------
    # ---  TOOLS
    # --------------------------------------------------------------------------------
    @staticmethod
    def pretty_type(name):
        pretty_name=name
        if pretty_name[0].lower()=='t':
            pretty_name=pretty_name[1:]
        if pretty_name[0].lower()=='_':
            pretty_name=pretty_name[1:]
        return(pretty_name.lower())


    def _getRoutine0p(self,name):
        FS=FortranSubroutine(self.pretty_name+name)
        FS.setRecusive(self.bRecursive)
        FS.append_arg('type(%s), pointer :: %s '%(self.raw_name,'X'))
        return(FS)
    def _getRoutine1p(self,name):
        FS=FortranSubroutine(self.pretty_name+name)
        FS.setRecusive(self.bRecursive)
        FS.append_arg('type(%s), dimension(:), pointer :: %s '%(self.raw_name,'X'))
        return(FS)

    def _getRoutine0io(self,name):
        FS=FortranSubroutine(self.pretty_name+name)
        FS.setRecusive(self.bRecursive)
        FS.append_arg('type(%s), intent(inout) :: %s '%(self.raw_name,'X'))
        return(FS)

    def _getRoutine0i(self,name):
        FS=FortranSubroutine(self.pretty_name+name)
        FS.setRecusive(self.bRecursive)
        FS.append_arg('type(%s), intent(in) :: %s '%(self.raw_name,'X'))
        return(FS)

    def _getRoutine0o(self,name):
        FS=FortranSubroutine(self.pretty_name+name)
        FS.setRecusive(self.bRecursive)
        FS.append_arg('type(%s), intent(out) :: %s '%(self.raw_name,'X'))
        return(FS)


    # --------------------------------------------------------------------------------
    # ---  TOOLS Writter
    # --------------------------------------------------------------------------------

    # Tools that write the initialization function of a derived type
    def write_tool_init(self,f,routines):
        bSimpleInOut=False
        if ('0' in routines) and not bSimpleInOut:
            FS=self._getRoutine0io('_init_0')
            for d in self.Declarations:
                FS.append_corpus(d.get_init('X%'))
            FS.write_to_file(f)
#         if ('inout' in routines) and bSimpleInOut:
#             FS=self._getRoutine0io('_init_inout')
#             FS.append_var('type(%s), pointer :: %s '%(self.raw_name,'pX'))
#             FS.append_corpus('pX=>X')
#             FS.append_corpus('call %s_%s(pX)'%(self.pretty_name,'init'))
#             FS.write_to_file(f)
    def write_tool_initp(self,f,routines):
        if ('0' in routines):
            FS=self._getRoutine0p('_initp_0')
            FS.append_corpus('if (associated(X)) then')
            for d in self.Declarations:
                FS.append_corpus(d.get_init('X%'))
            FS.append_corpus('endif')
            FS.write_to_file(f)
        if ('1' in routines):
            FS=self._getRoutine1p('_initp_1')
            FS.append_var('integer :: iX')
            FS.append_corpus('if (associated(X)) then')
            FS.append_corpus('    do iX=1,size(X)')
            FS.append_corpus('        call %s_%s(X(iX))'%(self.pretty_name,'init'))
            FS.append_corpus('    enddo')
            FS.append_corpus('endif')
            FS.write_to_file(f)

    # Tools that write the termination function of a derived type
    def write_tool_term(self,f,routines):
        FS=self._getRoutine0io('_term_0')
        for d in self.Declarations:
            FS.append_corpus(d.get_term('X%'))
        FS.write_to_file(f)
    def write_tool_termp(self,f,routines):
        FS=self._getRoutine0p('_termp_0')
        FS.append_corpus('if (associated(X)) then')
        for d in self.Declarations:
            FS.append_corpus(d.get_term('X%'))
        FS.append_corpus('    deallocate(X)')
        FS.append_corpus('endif')
        FS.write_to_file(f)

        if ('1' in routines):
            FS=self._getRoutine1p('_termp_1')
            FS.append_var('integer :: iX')
            FS.append_corpus('if (associated(X)) then')
            FS.append_corpus('    do iX=1,size(X)')
            FS.append_corpus('        call %s_%s(X(iX))'%(self.pretty_name,'term'))
            FS.append_corpus('    enddo')
            FS.append_corpus('    deallocate(X)')
            FS.append_corpus('endif')
            FS.write_to_file(f)

#         FS.name=FS.name.replace('pointer','0')
#         FS.write_to_file_inout(f)



    def write_tool_write(self,f,routines):
        FS=self._getRoutine0i('_write_0')
        FS.append_arg('integer, intent(in) :: iunit')
        for d in self.Declarations:
            FS.append_corpus(d.get_write('X%'))
        FS.write_to_file(f)

    def write_tool_writep(self,f,routines):
        FS=self._getRoutine0p('_writep_0')
        FS.append_arg('integer, intent(in) :: iunit')
        FS.append_corpus('write(iunit)associated(X)\n')
        FS.append_corpus('if (associated(X)) then')
        for d in self.Declarations:
            FS.append_corpus(d.get_write('X%'))
        FS.append_corpus('endif')
        FS.write_to_file(f)
        if ('1' in routines):
            FS=self._getRoutine1p('_writep_1')
            FS.append_arg('integer, intent(in) :: iunit')
            FS.append_var('integer :: iX')
            FS.append_corpus('write(iunit)associated(X)')
            FS.append_corpus('if (associated(X)) then')
            FS.append_corpus('    write(iunit)size(X)')
            FS.append_corpus('    do iX=1,size(X)')
            FS.append_corpus('         call %s_%s(X(iX),iunit)'%(self.pretty_name,'write'))
            FS.append_corpus('    enddo')
            FS.append_corpus('endif')
            FS.write_to_file(f)


    def write_tool_read(self,f,routines):
        # Writting routine name
        FS=self._getRoutine0o('_read_0')
        # Arguments
        FS.append_arg('integer, intent(in) :: iunit')
        # Variables
        FS.append_var('logical :: bPresent')
        # We need to we get the maximum number of dimensions of variables
        m=0
        for d in self.Declarations:
            if d['pointer'] or d['allocatable']:
                m=max((d['ndimensions'],m))

        if m>0 :
            FS.append_var('integer :: nd1')
        if m>1 :
            FS.append_var('integer :: nd2')
        if m>2 :
            FS.append_var('integer :: nd3')
        if m>3 :
            FS.append_var('integer :: nd4')
        # Reading type

        for d in self.Declarations:
            FS.append_corpus(d.get_read('X%'))
        FS.write_to_file(f)
    
    def write_tool_readp(self,f,routines):
        # Writting routine name
        FS=self._getRoutine0p('_readp_0')
        # Arguments
        FS.append_arg('integer, intent(in) :: iunit')
        # Variables
        FS.append_var('logical :: bPresent')
        # We need to we get the maximum number of dimensions of variables
        m=0
        for d in self.Declarations:
            if d['pointer'] or d['allocatable']:
                m=max((d['ndimensions'],m))

        if m>0 :
            FS.append_var('integer :: nd1')
        if m>1 :
            FS.append_var('integer :: nd2')
        if m>2 :
            FS.append_var('integer :: nd3')
        if m>3 :
            FS.append_var('integer :: nd4')
        FS.append_corpus('read(iunit)bPresent')
        FS.append_corpus('if (bPresent) then')
        FS.append_corpus('allocate(X)')
        for d in self.Declarations:
            FS.append_corpus(d.get_read('X%'))
        FS.append_corpus('endif')
        FS.write_to_file(f)
        if ('1' in routines):
            FS=self._getRoutine1p('_readp_1')
            FS.append_arg('integer, intent(in) :: iunit')
            FS.append_var('integer :: iX')
            FS.append_var('logical :: bPresent')
            FS.append_var('integer :: nd1')
            FS.append_corpus('read(iunit)bPresent')
            FS.append_corpus('if (bPresent) then')
            FS.append_corpus('    read(iunit)nd1')
            FS.append_corpus('    if(associated(X).and. size(X)/=nd1) then')
            FS.append_corpus('         print*,"ERROR X wrong size"')
            FS.append_corpus('         STOP')
            FS.append_corpus('    endif')
            FS.append_corpus('    if(.not. associated(X)) then')
#             FS.append_corpus('         print*,"allocating"')
            FS.append_corpus('         allocate(X(nd1))')
            FS.append_corpus('    endif')
            FS.append_corpus('    do iX=1,nd1')
            FS.append_corpus('         call %s_%s(X(iX),iunit)'%(self.pretty_name,'read'))
            FS.append_corpus('    enddo')
            FS.append_corpus('endif')
            FS.write_to_file(f)

    def write_tool_set_var(self,f,routines):
        #
        MAX_VAR_LENGTH=0
        for d in self.Declarations:
            MAX_VAR_LENGTH=max(len(d['varname']),MAX_VAR_LENGTH)

        if ('s' in routines):
            # Writting routine name
            FS=self._getRoutine0io('_set_var_s')
            # Use Statements
            FS.UseStatements.append('use StringUtils, only: strsplit, T_SubStrings, substr_term')
            FS.UseStatements.append('use Logging, only: log_info, log_error')
            FS.UseStatements.append('use MainIOData, only: bDEBUG')
            FS.UseStatements.analyse_raw_data()
            # Arguments
            FS.append_arg('character(len=*), intent(in) :: svar')
            FS.append_arg('character(len=*), intent(in) :: sval')
            # Variables
            FS.append_var('type(T_SubStrings) :: SubStrings')
            FS.append_corpus("if(bDEBUG) call log_info('Setting variable '//trim(svar)//' to '//trim(sval))")
            FS.append_corpus("call strsplit(trim(svar),SubStrings,'%',1)")

            #select case(SubStrings%s(1))
            FS.append_corpus("select case (SubStrings%s(1))")
            for d in self.Declarations:
                # Justifying variables
                dqsp="'%s'"%d['varname']
                dqsp=dqsp.ljust(MAX_VAR_LENGTH+2)
                dsp =d['varname'].ljust(MAX_VAR_LENGTH)
                #
                #print("%s %s"%(dqsp, d['type']))
                if d['type'].find('character')==0:
                    FS.append_corpus("case(%s); X%%%s = trim(sval)"%(dqsp,dsp))
                else:
                    # For derived types, we only accept "inputs" types
                    if (not d['built_in']):
                        if d['type'].lower().find('inputs')>0:
                            FS.append_corpus('case(%s)'%dqsp)
                            FS.append_corpus("    if (SubStrings%n/=2) call log_error('Impossible to set '//trim(svar))")
                            FS.append_corpus('    call %s_set_var(X%%%s,SubStrings%%s(2),svar)'%(d['pretty_type'],d['varname']))

            FS.append_corpus("case default")
            FS.append_corpus("    call log_error('Set %s Var: Invalid variable: '//trim(svar))"%self.pretty_name)
            FS.append_corpus("end select")
            FS.append_corpus("call substr_term(SubStrings)")
            FS.append_corpus("if(.false.)read(1)X ! just to avoid compiler warning if wariable not used")

            FS.write_to_file(f)
#                 type='',\ dimension='',\ ndimensions=0,\ pointer=False,\ allocatable=False,\
#                 intent='',\ varname='',\ varvalue='',\ comment='',\

        # --------------------------------------------------------------------------------
        # ---  
        # --------------------------------------------------------------------------------
        if ('v' in routines):
            # Writting routine name
            FS=self._getRoutine0io('_set_var_v')
            # Use Statements
            FS.UseStatements.append('use PrecisionMod, only: MK')
            FS.UseStatements.append('use StringUtils, only: strsplit, T_SubStrings, substr_term')
            FS.UseStatements.append('use Num2StrMod, only: num2str')
            FS.UseStatements.append('use Logging, only: log_info, log_error')
            FS.UseStatements.append('use MainIOData, only: bDEBUG')
            FS.UseStatements.analyse_raw_data()
            # Arguments
            FS.append_arg('character(len=*), intent(in) :: svar')
            FS.append_arg('real(MK),dimension(:) :: rvec')
            # Variables
            #FS.append_var('real(MK) :: rval')
            FS.append_var('type(T_SubStrings) :: SubStrings')
            FS.append_corpus("call strsplit(trim(svar),SubStrings,'%',1)")
            FS.append_corpus("if(bDEBUG) call log_info('Setting variable '//trim(svar)//' to '//num2str(rvec))")

            #select case(SubStrings%s(1))
            FS.append_corpus("select case (SubStrings%s(1))")
            for d in self.Declarations:
                dqsp="'%s'"%d['varname']
                dqsp=dqsp.ljust(MAX_VAR_LENGTH+2)
                dsp =d['varname'].ljust(MAX_VAR_LENGTH)
                if d['pointer'] or d['allocatable']:
                    eprint('Fortran File TODO',d)
                else:
                    if d['ndimensions']==0:
                        select_in='1'
                    elif d['ndimensions']==1:
                        select_in='1:%s'%d['dimension']
                    else:
                        eprint('Fortran File TODO more than one dimension for inputs')

                    if d['type']=='logical' :
                        FS.append_corpus("case(%s); X%%%s = int(rvec(%s))==1"%(dqsp,dsp,select_in))
                    elif d['type']=='integer':
                        FS.append_corpus("case(%s); X%%%s = int(rvec(%s))"%(dqsp,dsp,select_in))
                    elif d['type'][0:4]=='real':
                        FS.append_corpus("case(%s); X%%%s =     rvec(%s) "%(dqsp,dsp,select_in))
                    else:
                        # For derived types, we only accept "inputs" types
                        if (not d['built_in']):
                            if d['type'].lower().find('inputs')>0:
                                FS.append_corpus('case(%s)'%dqsp)
                                FS.append_corpus("    if (SubStrings%n/=2) call log_error('Impossible to set '//trim(svar))")
                                FS.append_corpus('    call %s_set_var(X%%%s,SubStrings%%s(2),rvec)'%(d['pretty_type'],d['varname']))
                            else:
                                eprint("Derived type skipped for inputs %s"%d['type'])


            FS.append_corpus("case default")
            FS.append_corpus("    call log_error('Set %s Var: Invalid variable: '//trim(svar))"%self.pretty_name)
            FS.append_corpus("end select")
            FS.append_corpus("call substr_term(SubStrings)")
            FS.append_corpus("if(.false.)read(1)X ! just to avoid compiler warning if wariable not used")
            FS.write_to_file(f)




# --------------------------------------------------------------------------------}
# --- Fortran Method 
# --------------------------------------------------------------------------------{
class FortranMethod(object):
    def __init__(self,name='',raw_name='',raw_lines=None):
        # A bit of a mess between name, raw_name and bind_name. I guess name and bind_name are the same.. I should get rid of raw_name. But replacement needs care for signature (C etc..)
        self.name=name
        self.raw_name=raw_name
        self.bind_name=''
        #
        self.result_name=''
        self.type='method'
        #
        self.raw_lines=[]
        self.raw_comment_lines=[] 
        self.arglist_str=''
        self.arglist_name_raw=[]
        self.arglist=FortranDeclarations([])
        self.varlist_str=''
        self.varlist_raw=[]
        self.varlist=[]
        self.corpus=[]
        self.indent='    '
        self.bRecursive=False
        self.return_type=''
        # UseStatement
        self.UseStatements=FortranUseStatements(line=[])

        if raw_lines is not None:
            if type(raw_lines) is not list:
                raw_lines=raw_lines.split('\n')
            L = bind_lines(raw_lines);
            (L,comments) = remove_comments(L);
            self.raw_name          = L[0]
            self.raw_lines         = L[1:-1]
            self.raw_comment_lines = comments[1:-1]
            self.analyse_raw_data()

    def append_raw(self,line,comment=''):
        self.raw_lines.append(line)
        self.raw_comment_lines.append(comment)
#         self.Declarations.append(FortranDeclaration(line,comment))

    def append_corpus(self,corpus):
        self.corpus.append(corpus)

    def append_var(self,decl,comment=''):
        if not isinstance(decl,FortranDeclaration):
            decl=FortranDeclaration(decl,comment)
        self.varlist.append(decl)

    def append_arg(self,decl,comment=''):
        if isinstance(decl,FortranDeclaration):
            decl.IsArgument=True
        else:
            decl=FortranDeclaration(decl,comment,argument=True)
        self.arglist.append(decl)
        if len(self.arglist_str)==0:
            self.arglist_str=decl['varname']
        else:
            self.arglist_str+=','+decl['varname']

    def analyse_raw_data(self):
        self.UseStatements=FortranUseStatements(line=[])
        # --------------------------------------------------------------------------------
        # ---  Analysing raw_name
        # --------------------------------------------------------------------------------
        #print('RawName:',self.raw_name)
        words=self.raw_name.lower().split(' ')
        for (w,i) in zip(words,range(len(words))):
            if w=='subroutine':
                self.type='subroutine'
                break
            if w=='function':
                self.type='function'
                break

        before_method = ' '.join(words[0:i]).strip()
        after_method  = ' '.join(words[i+1:]).strip()
        # Joining all, and replacing () with space and splitting
        # NOTE: some methods can have no parenthesis 
        after_method  = after_method.replace(' ','')
        after_method2 = after_method.replace('(',' ')
        after_method2 = after_method2.replace(')',' ')
        words=after_method2.split(' ')
        # Trying to catch a result 
#         if after_method.find('result(')
        self.name=words[0]
        if len(words)>1:
            if len(words[1])>0:
                self.arglist_name_raw=words[1].split(',')

        # --------------------------------------------------------------------------------
        # ---  Things after signature (i.e. bind and result) NASTY
        # --------------------------------------------------------------------------------
        self.result_name=''
        self.bind_name=''
        ### Trying to read bind and result
        bind_var=''
        for (w,i) in zip(words,range(len(words))):
            if w=='result':
                self.result_name=words[i+1]
            if w=='bind':
                bind_var=words[i+1]

        # Extracting bind name from bind words
        if bind_var!='':
            # WATCH OUT THIS IS NOT GENERAL!!!! is assumes a form: BIND(C,name='bind_name')
            names=bind_var.split('\'')
            self.bind_name=names[1]
            # Hmm... This below seems like a hack: overriding method name by bind name.. I guessed I used that for the signatures. Signatures should now use bind_name instead...
            self.name=names[1]
        # --------------------------------------------------------------------------------
        # ---  Special care for functions
        # --------------------------------------------------------------------------------
            ### Detection of 
        if self.type=='function':
            self.return_type=before_method.strip() # More handling required if recursive, pure, elemental, etc..
        
        # --------------------------------------------------------------------------------
        # ---  Analysing Use Statements, Argument, Variables and corpus
        # --------------------------------------------------------------------------------
        tmp_arg_list=[];
        tmp_arg_list_raw=[];
        tmp_arg_list_raw_comment=[];
        #
        tmp_ptr_list=[];
        tmp_ptr_list_raw=[];
        tmp_ptr_list_raw_comment=[];

        decl_lines    = []
        decl_comments = []

        for (line,comment) in zip(self.raw_lines,self.raw_comment_lines):
            l=line.strip()
            words=l.split(' ')
            # Detecting Use statement
            bUseStatement=words[0].lower()=='use'
            # Detecting declaration
            i_dots=l.find('::');
            bDeclaration=i_dots>0
            if bDeclaration:
                decl_lines.append(l)
                decl_comments.append(comment)
            elif bUseStatement:
                self.UseStatements.append(l)
                #print(l)
            else:
                self.append_corpus(l)
#             if pattern_intent_in.match(l):
#             pass


        # --------------------------------------------------------------------------------
        # --- Handling declarations, arguments variables
        # --------------------------------------------------------------------------------
        decl_stack = FortranDeclarations(lines=decl_lines,comments=decl_comments)
        # Looping on signature arguments, trying to find the matching declaration
        for arg_name in self.arglist_name_raw:
            bFound=False
            for i,d in enumerate(decl_stack):
               if d['varname'].lower()==arg_name.lower():
                   self.append_arg(d)
                   decl_stack.pop(i)
                   bFound=True
                   if len(d['intent'])<=0 and (not d['pointer']):
                       eprint('Warning: argument `{}` has no `intent` attributes in `{}`'.format(d['varname'],self.name))
                   break
            # If not found that's an error
            if not bFound:
                eprint('  ')
                eprint('Signature arguments:\n','   ',self.arglist_name_raw)
                eprint('Arguments: ')
                eprint(self.arglist)
                eprint('Remaining declarations: ')
                print(decl_stack)
                eprint('  ')
                eprint('Error: argument `%s` not found in the declaration list of `%s` '%(arg_name,self.name))
                eprint('       Did you use `intent` everywhere (except pointers)?')
                eprint(' ')
                sys.exit(-1)
        # --- Variables
        for d in decl_stack:
            self.append_var(d)
        # print(self.arglist)

        # --------------------------------------------------------------------------------
        # ---  Analysing use statements
        # --------------------------------------------------------------------------------
        self.UseStatements.analyse_raw_data()


    def setRecusive(self,bRecursive):
        self.bRecursive=bRecursive

    def remove_unused_var(self):
        self.varlist=[d for d in self.varlist if (any([(d['varname'] in x) for x in self.corpus]))]
#             for l in self.corpus:

    # Writting C signature equivalent to the current fortran method
    def write_signature(self,f,verbose=False):
        # 
        if verbose:
            f.write('//%s\n'%self.raw_name);
        if self.type=='subroutine':
            f.write('void ');
        else:
            f.write('%s '%fortran_returntype_to_c(self.return_type));

        # We use the bind_name for C signature
        f.write('%s('%self.bind_name);
        for (a,i) in zip(self.arglist,range(len(self.arglist))):
            C_TYPE=fortran_type_to_c(a['type'])
            f.write('%s '%C_TYPE);
            f.write('%s'%a['varname']);
            if i!= len(self.arglist)-1:
                f.write(', ');

        f.write(');\n');
    
    def write_signature_def(self,f):
        # We use the bind_name
        f.write('%s\n'%self.bind_name.lower());

#     def write_def(self,f):
#         f.write('//%s\n'%self.raw_name);
#         if self.type=='subroutine':
#             f.write('void ');
#         else:
#             f.write('%s '%fortran_type_to_c(self.return_type));
# 
#         f.write('%s('%self.name);
#         for (a,i) in zip(self.arglist,range(len(self.arglist))):
#             C_TYPE=fortran_type_to_c(a['type'])
#             f.write('%s '%C_TYPE);
#             f.write('%s'%a['varname']);
#             if i!= len(self.arglist):
#                 f.write(', ');
# 
#         f.write(');\n');

    def tostring(self,indent='    ',verbose=False):
        """ Routine to string """
        s=''
        s+=''
        # --------------------------------------------------------------------------------
        # --- Writting the fortran signature of the method
        # --------------------------------------------------------------------------------
        goodies_before=''
        goodies_after=''
        if self.bRecursive:
            goodies_before='recursive '
        else:
            if len('self.result_name')>0 and self.result_name!='':
                   goodies_after+=' result(%s)'%self.result_name
            if len('self.bind_name')>0 and self.bind_name!='':
                   goodies_after+=' BIND(C, name=\'%s\')'%self.bind_name

        s+='%s%s%s %s(%s)%s\n'%(indent,goodies_before,self.type,self.name,self.arglist_str,goodies_after)
        # --------------------------------------------------------------------------------
        # ---  Use statements
        # --------------------------------------------------------------------------------
        s+=self.UseStatements.tostring(self.indent+indent)
        # --------------------------------------------------------------------------------
        # ---  Arguments and variable declaration
        # --------------------------------------------------------------------------------
        # deleting unused variables
        self.remove_unused_var()

        if len(self.arglist)>0:
            if verbose:
                s+='%s! Arguments declaration\n'%(indent+self.indent)
            for d in self.arglist:
                s+=d.tostring(indent+self.indent)+'\n'

        if len(self.varlist)>0:
            if verbose:
                s+='%s! Variable declaration\n'%(indent+self.indent)
            for d in self.varlist:
                s+=d.tostring(indent+self.indent)+'\n'

        if len(self.corpus)>0:
            if verbose:
                s+='%s! Corpus\n'%(indent+self.indent)
            for l in self.corpus:
                if len(l)>0:
                    for ll in l.split('\n'):
                        s+='%s%s\n'%(indent+self.indent,ll)
        #f.write('%send %s %s\n\n'%(indent,self.type,self.name))
        s+='%send %s'%(indent,self.type)
        return s

    def write_to_file(self,f,indent='    '):
        s=self.tostring(indent)
        f.write(s)

    # A kind of hack
    def write_to_file_inout(self,f,indent='    '):
        f.write('%s%s %s(%s)\n'%(indent,self.type,self.name,self.arglist_str))
        for d in self.arglist:
            d['pointer']=False
            d.write_to_file(f,indent+self.indent)
#             f.write('%s%s\n'%(indent+self.indent,l))
        f.write('%send %s %s\n\n'%(indent,self.type,self.name))


class FortranSubroutine(FortranMethod):
    def __init__(self,name):
        super(FortranSubroutine,self).__init__(name)
        self.type='subroutine'


class FortranFunction(FortranMethod):
    def __init__(self,name):
        super(FortranFunction,self).__init__(name)
        self.type='function'

class FortranDeclarations(list):
    def __init__(self,Declarations=[],lines=None,comments=None):
        """ Initialize a list of declarations, Declarations is either:
             - a list of FortranDeclaration  
             - a list of strings
             - a string
        """
        raw_lines=None
        if type(Declarations) is list and (all([type(d) is FortranDeclaration for d in Declarations])):
                super(FortranDeclarations,self).__init__(Declarations)
        else:
            super(FortranDeclarations,self).__init__([])
            raw_lines=Declarations if len(Declarations)>0 else None

        if raw_lines is not None:
            if type(raw_lines) is not list:
                raw_lines=raw_lines.split('\n')
            lines = bind_lines(raw_lines);
            (lines,comments) = remove_comments(lines);
            
        if (lines is not None) and (type(lines) is not list):
            lines    = [lines]
            comments = [comments]

        if lines is not None:
            self.parse(lines,comments)


    def parse(self,lines,comments):
        """ parse lines of declaration """
        for l,comment in zip(lines,comments):
            i_dots=l.find('::');
            bDeclaration=i_dots>0
            if not bDeclaration:
                raise Exception('Only declarations with `::` supported')
            # --- handling several varaibles declared on one line
            l_before=l[0:i_dots].strip()
            l_after =l[i_dots+2:].strip()
            splits=l_after.split(',') 
            variables=[]
            tmp=''
            # handling declarations of the type :: a(1,2), b, M(:,:)
            bInPar=False
            for s in splits:
                no=s.count('(')
                nc=s.count(')')
                if no==nc+1:
                    tmp+=s+','
                    bInPar=True
                elif nc==no+1:
                    variables.append(tmp+s)
                    tmp=''
                    bInPar=False
                else:
                    if bInPar:
                        tmp+=s+','
                    else:
                        variables.append(s)
            #if len(splits)>0:
            #    print('Splits   : ',splits)
            #    print('Variables: ',variables)
            for var in variables:
                l_new=''
                # Old fashion declaration `a(5)`, to new fashion: `dimension(5) :: a` :
                io=var.find('(')
                ic=var.rfind(')')
                #print('var',var,io,ic)
                if io>0 and ic>0:
                    dim=var[io+1:ic]
                    if len(dim.strip())>0: # it could be x => null()
                        var=var[:io]
                        l_new = ', dimension('+dim+') '
                        #print(l_before+':: '+var)
                l_tmp=l_before+l_new+'::'+var.strip()
                #print(l_tmp)
                self.append(FortranDeclaration(l_tmp,comment))
                comment='' # only the first declaration gets the comment

    def tostring(self,indent=''):
        """ Declaration list to string """
        s=''
        for d in self:
            s+=d.tostring(indent)+'\n'
        return s

    def __repr__(self):
        return self.tostring()



class FortranDeclaration(dict):
    def __init__(self,l,comment='',inType=False,argument=False):
        super(FortranDeclaration,self).__init__(\
                built_in=True,\
                type_raw='',\
                type='',\
                pretty_type='',\
                dimension_fixed=False,\
                dimension='',\
                ndimensions=0,\
                pointer=False,\
                save=False,\
                optional=False,\
                allocatable=False,\
                intent='',\
                varname='',\
                varvalue='',\
                comment='',\
                alias=False)
        self.IsArgument=argument
        self.IsTypeDeclaration=inType


        # Small safety
        l=l.replace(';','');
        # --------------------------------------------------------------------------------
        # --- Converting declaration line to a dictionary
        # --------------------------------------------------------------------------------
        idx=l.find('::')
        if idx>0:
            attributes = l[:idx].strip()
            vardef     = l[idx+2:].strip()
            attr_clean = attributes.lower().replace(' ','').strip()

            # Catching variable name
            self['varname']=vardef.split('=')[0].strip()

            # Catching type
            if attr_clean.find('type(')==0:
                tr=attributes.split(',')[0].strip()
                self['type_raw']    = tr
                self['built_in']    = False
                self['type']        = tr[tr.index('(')+1:tr.index(')')].strip()
                self['pretty_type'] = FortranType.pretty_type(self['type'])
                #self.dependencies.append(self['type'])

            else:
                tr = first_entity(attributes)
                self['built_in']    = True
                self['type_raw']    = tr
                self['type']        = tr
                self['pretty_type'] = self['type'].split('(')[0]

            # Catching simple attributes: target, optinoal, pointer, save
            self['target']      = attr_clean.find(',target')>0
            self['optional']    = attr_clean.find(',optional')>0
            self['save']        = attr_clean.find(',save')>0
            self['pointer']     = attr_clean.find(',pointer')>0
            self['allocatable'] = attr_clean.find(',allocatable')>0

            # Trying to catch the value
            if self['pointer']:
                s=vardef.split('>')
                if len(s)>1:
                    self['varvalue']=s[1]
            elif not self['allocatable']:
                s=vardef.split('=')
                if len(s)>1:
                    self['varvalue']=s[1].strip()

            # Catching the dimension
            idx=attr_clean.find(',dimension')
            if idx>0:
                dim_str=attr_clean[idx+1:]
                dim_str = first_entity(dim_str)
                dim_str=dim_str[dim_str.find('(')+1:dim_str.rfind(')')]
                if dim_str.find(':')>0:
                    self['dimension_fixed']=False
                else:
                    self['dimension_fixed']=True

                self['dimension']   = dim_str
                self['ndimensions'] = self['dimension'].count(',')+1
            
            # Catching the intent
            idx=attr_clean.find(',intent')
            if idx>=0:
                intent_str=attr_clean[idx:]
                intent_str=intent_str[intent_str.index('(')+1:intent_str.index(')')]
                if intent_str.lower().strip()=='in':
                    self['intent']='in'
                elif intent_str.lower().strip()=='out':
                    self['intent']='out'
                else:
                    self['intent']='inout'

            if self['pointer'] and len(self['varvalue'])==0 and self.IsTypeDeclaration:
                eprint('Warning: %s not initialized to null'%(self['varname']))

            # Catching the comment
            if len(comment)>0:
                self['comment']=comment
                if comment.lower().find('alias')>=0:
                    #print(l+comment)
                    self['alias']=True
        else:
            eprint('Error, this script assumes definition with `::`, line:',l)

    def __repr__(self):
        return self.tostring()

    def tostring(self,indent=''):
        s=''
        attributes=self['type_raw'];
        if len(self['dimension'])>0:
            attributes+=', dimension(%s)'%self['dimension']
        if self['pointer']:
            attributes+=', pointer'
        if self['target']:
            attributes+=', target'
        if self['optional']:
            attributes+=', optional'
        if self['save']:
            attributes+=', save'
        if len(self['intent']):
            attributes+=', intent(%s)'%self['intent']
        if self['allocatable']:
            attributes+=', allocatable'
        attributes+=' :: '+self['varname']
        if len(self['varvalue'])>0:
            if self['pointer']:
                attributes+=' =>'
            else:
                attributes+=' = '
            attributes+=self['varvalue']

        if len(self['comment'])>0:
            attributes+=' '+self['comment']
        s+=indent+attributes
        return s

    def write_to_file(self,f,indent='    '):
        f.write(self.tostring(indent))

    def get_term(self,preffix=''):
        term=''
        varname=preffix+self['varname']
        if self['built_in']:
            if self['pointer']:
                term='if (associated(%s)) deallocate(%s)'%(varname,varname)
            elif self['allocatable']:
                term='if (allocated(%s)) deallocate(%s)'%(varname,varname)
            else:
                if len(self['varvalue'])>0:
                    # Adding an init 
                    term='%s = %s ! reinit - to avoid unused variable message'%(varname,self['varvalue'])
        else:
            if self['pointer']:
                if not self['alias']:
                    term='if (associated(%s)) call %s_termp(%s)'%(varname,self['pretty_type'],varname)
                else:
                    term='nullify(%s)'%varname
#                 term='if (associated(%s)) then\n    call %s_termp(%s)\n    deallocate(%s)\nendif'%(varname,self['pretty_type'],varname,varname)
            elif self['allocatable']:
                term='if (allocated(%s)) call %s_termp(%s)'%(varname,self['pretty_type'],varname)
#                 term='if (allocated(%s)) then\n    call %s_termp(%s)\n    deallocate(%s)\nendif'%(varname,self['pretty_type'],varname,varname)
            else:
                term='call %s_term(%s)'%(self['pretty_type'],varname)
        return(term)

    def get_init(self,preffix=''):
        init=''
        varname=preffix+self['varname']
        if self['built_in']:
            if len(self['varvalue'])>0:
                if self['pointer']:
                    init='%s => %s'%(varname,self['varvalue'])
                else:
                    init='%s = %s'%(varname,self['varvalue'])
        else:
            if self['pointer']:
                #init='call %s_initp(%s)'%(self['pretty_type'],varname)
                init='nullify(%s)'%(varname)
            elif self['allocatable']:
                init='call %s_initp(%s)'%(self['pretty_type'],varname)
            else:
                init='call %s_init(%s)'%(self['pretty_type'],varname)
        return(init)

    def get_write(self,preffix=''):
        write=''
        varname=preffix+self['varname']
        if self['built_in']:
            if self['pointer']:
                write+='write(iunit)associated(%s)\n'%varname
                write+='if (associated(%s)) then\n'%varname
                for i in range(self['ndimensions']):
                    write+='    write(iunit)size(%s,%d)\n'%(varname,i+1)
                write+='write(iunit)%s\n'%varname
                write+='endif'
            elif self['allocatable']:
                write+='write(iunit)allocated(%s)\n'%varname
                write+='if (allocated(%s)) then\n'%varname
                for i in range(self['ndimensions']):
                    write+='    write(iunit)size(%s,%d)\n'%(varname,i+1)

                write+='    write(iunit)%s\n'%varname
                write+='endif'
            else:
                write='write(iunit)%s'%varname
        else:
            if self['pointer']:
#                 write='if (associated(%s)) call %s_write(%s)'%(varname,self['pretty_type'],varname)
                write='call %s_writep(%s,iunit)'%(self['pretty_type'],varname)
            elif self['allocatable']:
#                 write='if (allocated(%s)) call %s_write(%s)'%(varname,self['pretty_type'],varname)
                write='call %s_writep(%s,iunit)'%(self['pretty_type'],varname)
            else:
                write='call %s_write(%s,iunit)'%(self['pretty_type'],varname)
        return(write)

    def get_read(self,preffix=''):
        read=''
        varname=preffix+self['varname']
        if self['built_in']:
            if self['pointer'] or self['allocatable']:
                read+='read(iunit)bPresent\n'
                read+='if (bPresent) then\n'
                ns=''
                for i in range(self['ndimensions']):
                    read+='    read(iunit)nd%d\n'%(i+1)
                    ns+='nd%d,'%(i+1)
                ns=ns[:-1]
                if self['ndimensions']==0:
                    read+='    allocate(%s)\n'%(varname)
                else:
                    read+='    allocate(%s(%s))\n'%(varname,ns)
                read+='    read(iunit)%s\n'%varname
                read+='endif'
            else:
                read='read(iunit)%s'%(varname)
        else:
            if self['pointer']:
#                 read='if (associated(%s)) call %s_read(%s)'%(varname,self['pretty_type'],varname)
                read='call %s_readp(%s,iunit)'%(self['pretty_type'],varname)
            elif self['allocatable']:
#                 read='if (allocated(%s)) call %s_read(%s)'%(varname,self['pretty_type'],varname)
                read='call %s_readp(%s,iunit)'%(self['pretty_type'],varname)
            else:
                read='call %s_read(%s,iunit)'%(self['pretty_type'],varname)
        return(read)
