#!/usr/bin/env python
from fortran_parse_tools import*

S_TYPE_TOOLS='AutoTools'

TOOLS=[
        {'interface':'init'     , 'routines':['init_inout']} ,
        {'interface':'term'     , 'routines':['term_inout']} ,
        {'interface':'write'    , 'routines':['term_inout']} ,
        {'interface':'read'     , 'routines':['term_inout']} ,
        ]


class FortranFile:
    def __init__(self,filename):
        self.filename=filename
        self.ModuleList=[]

    def read(self):
        with open(self.filename,'r') as f:
            #print(self.filename)
            # Cleaning up input file
            L = bind_lines(f.readlines());
            L = remove_comments(L);

            # --------------------------------------------------------------------------------
            # --- Extracting types
            # --------------------------------------------------------------------------------
            self.ModuleList=[]
            bIsInType=False
            bIsInModule=False
            m=None
            t=None
            for l in L:
                # always concatenate end with the keyword
                if l[0:4].lower()=='end ':
                    l='end'+l[4:]

                words=l.split(' ')
                if words[0].lower()=='module':
                    # This is a new module
                    m=(FortranModule(words[1]))
                    bIsInModule=True
                if words[0].lower()=='endmodule':
                    self.ModuleList.append(m)
                    bIsInModule=False
                elif words[0].lower()=='use':
                    m.UseStatements.append(l)
                elif words[0].lower()=='type':
                    # Creating a new type
                    t=FortranType(words[1])
                    bIsInType=True
                elif words[0].lower()=='endtype':
                    m.TypeList.append(t)
                    bIsInType=False
                else:
                    if bIsInType:
                        t.append(l)


            # --------------------------------------------------------------------------------
            # --- Analyse raw data
            # --------------------------------------------------------------------------------
            for m in self.ModuleList:
                m.analyse_raw_data()
#                     for l in t.raw_lines:
#                         print(l)

    def write(self,filename_out=''):
        import os
        if filename_out=='':
            (filebase,extension)=os.path.splitext(self.filename)
            filename_out=filebase+'_gen'+extension
        with open(filename_out,'w') as f:
            for m in self.ModuleList:
                m.write_to_file(f)

    def write_type_tools(self,filename_out=''):
        import os
        if filename_out=='':
            (filebase,extension)=os.path.splitext(self.filename)
            filename_out=filebase+S_TYPE_TOOLS+extension
        with open(filename_out,'w') as f:
            for m in self.ModuleList:
                m.write_type_tools(f)






class FortranModule:

    def __init__(self,name):
        self.name=name

        # UseStatement
        self.UseStatements=FortranUseStatements()
        # Types
        self.TypeList=[]
        self.type_dependencies=[]
        self.type_depend_mod=[]
        # Interfaces
        # Variables
        # Methods
        # Misc
        self.indent='    '

    def analyse_raw_data(self):
        #print('MODULE: '+self.name)

        # --------------------------------------------------------------------------------
        # ---  Analysying sub elements
        # --------------------------------------------------------------------------------
        # Analyse Types
        for t in self.TypeList:
            #print('TYPE: '+t.raw_name)
            t.analyse_raw_data()
            self.type_dependencies.append(t.dependencies)

        self.UseStatements.analyse_raw_data()

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
                    print('Warning Multiple options : Type %s - Module %s'%(t,m))
                m=m[0]
                #print('Solved Dependency: Type %s - Module %s'%(t,m))
            else:
                print('Warning: Unresolved Dependency: Type %s'%(t))

            self.type_depend_mod.append(m)

    def write_to_file(self,f):
        f.write('module %s\n'%self.name)
        self.UseStatements.write_to_file(f,'')
        for t in self.TypeList:
            t.write_to_file(f,self.indent)

        f.write('end module %s\n'%self.name)

    def write_type_tools(self,f):
        f.write('module %s%s\n'%(self.name,S_TYPE_TOOLS))
        f.write('    ! Module containing type: \n')
        f.write('    use %s\n'%(self.name))
        # Resolved dependencies
        if len(self.type_depend_mod)>0:
            f.write('    ! Friend modules: \n')
        for (m,t) in zip(self.type_depend_mod,self.type_dependencies):
            if m is not None:
                f.write('    use %s%s\n'%(m,S_TYPE_TOOLS))
            else:
                f.write('!    use %s%s\n'%(t,S_TYPE_TOOLS))

        f.write('    implicit none\n\n')
        f.write('    private\n\n')


        # --------------------------------------------------------------------------------
        # ---  Interfaces and public attributes
        # --------------------------------------------------------------------------------
        for t in self.TypeList:
            for tool in TOOLS:
                if len(tool['interface'])>0:
                    f.write('    interface %s_%s; module procedure &\n'%(t.pretty_name,tool['interface']))
                    for (routine_name,i) in zip(tool['routines'],range(len(tool['routines']))):
                        end_line=',&'
                        if i==len(tool['routines'])-1:
                            end_line=''
                        f.write('          %s_%s%s\n'%(t.pretty_name,routine_name,end_line))
                    f.write('    end interface %s_%s\n'%(t.pretty_name,tool['interface']))
            for tool in TOOLS:
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
        for t in self.TypeList:
            for tool in TOOLS:
                if len(tool['interface'])>0:
                    func_call='t.write_tool_%s(f)'%tool['interface']
                    eval(func_call)
#                 t.write_type_tools(f,self.indent)

        f.write('end module %s%s\n'%(self.name,S_TYPE_TOOLS))


class FortranUseStatements:

    # static data
    default_dict_=dict(module='',only_list=[])

    def __init__(self,line=[]):
        self.raw_lines=line
        self.statements=[]
        self.indent='    '

    def append(self,line):
        self.raw_lines.append(line)

    def analyse_raw_data(self):
        for l in self.raw_lines:
            d=self.default_dict_.copy()
            sp=l.split(':')
            if len(sp)>1:
                d['only_list']=sp[1].strip().split(',')

            d['module']=sp[0].replace(',',' ').replace('  ',' ').split(' ')[1].strip()

            self.statements.append(d)

    def write_to_file(self,f,indent):
        for s in self.statements:
            u='use '+s['module']
            if len(s['only_list'])>0:
                u+=', only: '
                for o in s['only_list']:
                    u+=o+', '
                u=u[:-2]

            f.write('%s%s%s\n'%(indent,self.indent,u))

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





class FortranType:

    default_dict_=dict(built_in=True,type_raw='',type='',dimension_fixed=False,dimension='',pointer=False,allocatable=False,varname='',varvalue='')

    def __init__(self,name):
        # Raw data
        self.raw_lines=[]
        self.raw_name=name

        # Derived data
        # Main Data
        self.pretty_name=self.pretty_type(name)
        self.dependencies=[]
        self.Declarations=[]

        # Misc
        self.indent='    '

    def append(self,line):
        self.raw_lines.append(line)
        self.Declarations.append(FortranTypeDeclaration(line))

    def analyse_raw_data(self):
        for d in self.Declarations:
            if not d['built_in']:
                self.dependencies.append(d['type'])

    def write_to_file(self,f,indent=''):
        f.write('%stype %s\n'%(indent,self.raw_name))
        for d in self.Declarations:
            d.write_to_file(f,indent+self.indent)
        f.write('%send type\n'%indent)
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


    def _getRoutine1p(self,name):
        FS=FortranSubroutine(self.pretty_name+name)
        FS.append_arg('type(%s), pointer :: %s '%(self.raw_name,'X'))
        return(FS)

    def _getRoutine1io(self,name):
        FS=FortranSubroutine(self.pretty_name+name)
        FS.append_arg('type(%s), intent(inout) :: %s '%(self.raw_name,'X'))
        return(FS)

    def _getRoutine1i(self,name):
        FS=FortranSubroutine(self.pretty_name+name)
        FS.append_arg('type(%s), intent(in) :: %s '%(self.raw_name,'X'))
        return(FS)

    def _getRoutine1o(self,name):
        FS=FortranSubroutine(self.pretty_name+name)
        FS.append_arg('type(%s), intent(out) :: %s '%(self.raw_name,'X'))
        return(FS)


    # --------------------------------------------------------------------------------
    # ---  TOOLS Writter
    # --------------------------------------------------------------------------------
    def write_tool_init(self,f):
#         FS=self._getRoutine1p('_init_pointer')
#         for d in self.Declarations:
#             FS.corpus.append(d.get_init('X%'))
#         FS.write_to_file(f)

        FS=self._getRoutine1io('_init_inout')
        for d in self.Declarations:
            FS.corpus.append(d.get_init('X%'))
        FS.write_to_file(f)

    def write_tool_term(self,f):
#         FS=self._getRoutine1p('_term_pointer')
#         for d in self.Declarations:
#             FS.corpus.append(d.get_term('X%'))
#         FS.write_to_file(f)

        FS=self._getRoutine1io('_term_inout')
        for d in self.Declarations:
            FS.corpus.append(d.get_term('X%'))
        FS.write_to_file(f)

#         FS.name=FS.name.replace('pointer','inout')
#         FS.write_to_file_inout(f)


    def write_tool_write(self,f):
#         FS=self._getRoutine1p('_write_pointer')
#         FS.append_arg('integer, intent(in) :: iunit')
#         FS.corpus.append('if (associated(X)) then')
#         for d in self.Declarations:
#             FS.corpus.append(d.get_write('X%'))
#         FS.corpus.append('endif')
#         FS.write_to_file(f)

        FS=self._getRoutine1i('_write_inout')
        FS.append_arg('integer, intent(in) :: iunit')
        for d in self.Declarations:
            FS.corpus.append(d.get_write('X%'))
        FS.write_to_file(f)


    def write_tool_read(self,f):
#         FS=self._getRoutine1p('_read_pointer')
#         FS.append_arg('integer, intent(in) :: iunit')
#         FS.corpus.append('logical :: bPresent')
#         FS.corpus.append('integer :: n1')
#         FS.corpus.append('integer :: n2')
#         FS.corpus.append('integer :: n3')
#         FS.corpus.append('integer :: n4')
#         FS.corpus.append('if (associated(X)) then')
#         for d in self.Declarations:
#             FS.corpus.append(d.get_read('X%'))
#         FS.corpus.append('endif')
#         FS.write_to_file(f)

        FS=self._getRoutine1o('_read_inout')
        FS.append_arg('integer, intent(in) :: iunit')
        FS.corpus.append('logical :: bPresent')
        FS.corpus.append('integer :: n1')
        FS.corpus.append('integer :: n2')
        FS.corpus.append('integer :: n3')
        FS.corpus.append('integer :: n4')
        for d in self.Declarations:
            FS.corpus.append(d.get_read('X%'))
        FS.write_to_file(f)





class FortranMethod(object):
    def __init__(self,name):
        self.name=name
        self.type='method'
        self.arglist_str=''
        self.arglist_raw=[]
        self.arglist=[]
        self.corpus=[]
        self.indent='    '

    def append_arg(self,arg):
        self.arglist_raw.append(arg)
        d=FortranArgument(arg)
        self.arglist.append(d)
        if len(self.arglist_str)==0:
            self.arglist_str=d['varname']
        else:
            self.arglist_str+=','+d['varname']

    def write_to_file(self,f,indent='    '):
        f.write('%s%s %s(%s)\n'%(indent,self.type,self.name,self.arglist_str))
        for d in self.arglist:
            d.write_to_file(f,indent+self.indent)
        for l in self.corpus:
            if len(l)>0:
                for ll in l.split('\n'):
                    f.write('%s%s\n'%(indent+self.indent,ll))
        f.write('%send %s %s\n\n'%(indent,self.type,self.name))

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

class FortranDeclaration(dict):
    def __init__(self,l):
        super(FortranDeclaration,self).__init__(built_in=True,\
                type_raw='',\
                type='',\
                pretty_type='',\
                dimension_fixed=False,\
                dimension='',\
                ndimensions=0,\
                pointer=False,\
                allocatable=False,\
                intent='',\
                varname='',\
                varvalue='')
        self.IsArgument=False
        self.IsTypeDeclaration=False


        # --------------------------------------------------------------------------------
        # --- Converting declaration line to a dictionary
        # --------------------------------------------------------------------------------
        idx=l.find('::')
        if idx>0:
            attributes=l[:idx].strip()
            attributes_low=attributes.lower()
            vardef=l[idx+2:].strip()

            # Catching type
            self['type_raw']=attributes.split(',')[0].strip()
            if self['type_raw'].split('(')[0].lower()=='type':
                self['built_in']=False
                self['type']= self['type_raw'][self['type_raw'].index('(')+1:self['type_raw'].index(')')].strip()
                self['pretty_type']= FortranType.pretty_type(self['type'])
                #self.dependencies.append(self['type'])

            else:
                self['built_in']=True
                self['type']= self['type_raw']
                self['pretty_type']= self['type'].split('(')[0].lower()


            self['varname']=vardef.split('=')[0].strip()
            if attributes_low.find('pointer')>0:
                self['pointer']=True
            if attributes_low.find('allocatable')>0:
                self['allocatable']=True

            # Trying to catch the value
            if self['pointer']:
                s=vardef.split('>')
                if len(s)>1:
                    self['varvalue']=s[1]
            elif not self['allocatable']:
                s=vardef.split('=')
                if len(s)>1:
                    self['varvalue']=s[1]


            # Catching the dimension
            idx=l.find('dimension')
            if idx>0:
                dim_str=l[idx:]
                dim_str=dim_str[dim_str.index('(')+1:dim_str.index(')')]
                if dim_str.find(':')>0:
                    self['dimension_fixed']=False
                else:
                    self['dimension_fixed']=True

                self['dimension']=dim_str
                self['ndimensions']=self['dimension'].count(',')+1

            if self['pointer'] and len(self['varvalue'])==0 and self.IsTypeDeclaration:
                print('Warning: %s not initialized to null'%(self['varname']))
        else:
            print('Error, this script assumes definition with ::')


    def write_to_file(self,f,indent='    '):
        attributes=self['type_raw'];
        if len(self['dimension'])>0:
            attributes+=', dimension(%s)'%self['dimension']
        if self['pointer']:
            attributes+=', pointer'
        if self['allocatable']:
            attributes+=', allocatable'
        attributes+=' :: '+self['varname']
        if len(self['varvalue'])>0:
            if self['pointer']:
                attributes+=' =>'
            else:
                attributes+=' = '
            attributes+=self['varvalue']
        f.write('%s%s\n'%(indent,attributes))

    def get_term(self,preffix=''):
        term=''
        varname=preffix+self['varname']
        if self['built_in']:
            if self['pointer']:
                term='if (associated(%s)) deallocate(%s)'%(varname,varname)
            if self['allocatable']:
                term='if (allocated(%s)) deallocate(%s)'%(varname,varname)
        else:
            if self['pointer']:
                term='if (associated(%s)) call %s_term(%s)'%(varname,self['pretty_type'],varname)
            if self['allocatable']:
                term='if (allocated(%s)) call %s_term(%s)'%(varname,self['pretty_type'],varname)
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
#             if self['pointer']:
#                 write='if (associated(%s)) call %s_write(%s)'%(varname,self['pretty_type'],varname)
#             elif self['allocatable']:
#                 write='if (allocated(%s)) call %s_write(%s)'%(varname,self['pretty_type'],varname)
#             else:
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
                    read+='    read(iunit)n%d\n'%(i+1)
                    ns+='n%d,'%(i+1)
                ns=ns[:-1]
                read+='    allocate(%s(%s))\n'%(varname,ns)
                read+='    read(iunit)%s\n'%varname
                read+='endif'
            else:
                read='read(iunit)%s'%(varname)
        else:
#             if self['pointer']:
#                 read='if (associated(%s)) call %s_read(%s)'%(varname,self['pretty_type'],varname)
#             elif self['allocatable']:
#                 read='if (allocated(%s)) call %s_read(%s)'%(varname,self['pretty_type'],varname)
#             else:
            read='call %s_read(%s,iunit)'%(self['pretty_type'],varname)
        return(read)

class FortranArgument(FortranDeclaration):
    def __init__(self,l):
        super(FortranArgument,self).__init__(l)
        self.IsArgument=True

class FortranTypeDeclaration(FortranDeclaration):
    def __init__(self,l):
        super(FortranTypeDeclaration,self).__init__(l)
        self.IsTypeDeclaration=True


if __name__ == "__main__":
    F=FortranFile('test/WingTypes.f90')
    F.read()
    F.write()
    F.write_type_tools()
    F=FortranFile('test/ObjectInfoTypes.f90')
    F.read()
    F.write()
    F.write_type_tools()
    F=FortranFile('test/ProfileTypes.f90')
    F.read()
    F.write()
    F.write_type_tools()
