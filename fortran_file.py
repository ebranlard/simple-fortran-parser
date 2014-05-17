#!/usr/bin/env python
from fortran_parse_tools import*

S_TYPE_TOOLS='Tools'


class FortranFile:
    def __init__(self,filename):
        self.filename=filename
        self.ModuleList=[]
    
    def read(self):
        with open(self.filename,'r') as f:
            print(self.filename)
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
                # always concatenate the end with the keyword
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



     

# def unique_list(l):
#     ulist = []
#     [ulist.append(x) for x in l if x not in ulist]
#     return ulist

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
                    print('Warning Mutiple options : Type %s - Module %s'%(t,m))
                m=m[0]
                #print('Solved Dependency: Type %s - Module %s'%(t,m))
            else:
                print('Warning: Unresolved Dependency: Type %s'%(t))

            self.type_depend_mod.append(m)

    def write_to_file(self,fout):
        fout.write('module %s\n'%self.name)
        self.UseStatements.write_to_file(fout,'')
        for t in self.TypeList:
            t.write_to_file(fout,self.indent)

        fout.write('end module %s\n'%self.name)

    def write_type_tools(self,fout):
        fout.write('module %s%s\n'%(self.name,S_TYPE_TOOLS))
        fout.write('    ! Module containing type: \n')
        fout.write('     use %s\n'%(self.name))
        # Resolved dependencies
        if len(self.type_depend_mod)>0:
            fout.write('    ! Friend modules: \n')
        for (m,t) in zip(self.type_depend_mod,self.type_dependencies):
            if m is not None:
                fout.write('     use %s%s\n'%(m,S_TYPE_TOOLS))
            else:
                fout.write('!     use %s%s\n'%(t,S_TYPE_TOOLS))

        fout.write('contains\n')
#         for t in self.TypeList:
#             t.write_type_tools(fout,self.indent)

        fout.write('end module %s%s\n'%(self.name,S_TYPE_TOOLS))
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

    def write_to_file(self,fout,indent):
        for s in self.statements:
            u='use '+s['module']
            if len(s['only_list'])>0:
                u+=', only: '
                for o in s['only_list']:
                    u+=o+', '
                u=u[:-2]

            fout.write('%s%s%s\n'%(indent,self.indent,u))

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

    # static data
    default_dict_=dict(built_in=True,type_raw='',type='',dimension_fixed=False,dimension='',pointer=False,allocatable=False,varname='',varvalue='')
    
    def __init__(self,name):
        # Raw data
        self.raw_lines=[]
        self.raw_name=name
        self.use_statements=''

        # Derived data
        self.pretty_name=''
        self.dependencies=[]
        self.components=[]

        # Misc 
        self.indent='    '

    def append(self,line):
        self.raw_lines.append(line)


    def analyse_raw_data(self):
        for l in self.raw_lines:
            d=self.default_dict_.copy()
            idx=l.find('::')
            if idx>0:
                attributes=l[:idx].strip()
                attributes_low=attributes.lower()
                vardef=l[idx+2:].strip()

                # Catching type
                d['type_raw']=attributes.split(',')[0].strip()
                if d['type_raw'].split('(')[0].lower()=='type':
                    d['built_in']=False
                    d['type']= d['type_raw'][d['type_raw'].index('(')+1:d['type_raw'].index(')')].strip()
                    self.dependencies.append(d['type'])

                else:
                    d['built_in']=True
                    d['type']= d['type_raw']


                d['varname']=vardef.split('=')[0].strip()
                if attributes_low.find('pointer')>0:
                    d['pointer']=True
                if attributes_low.find('allocatable')>0:
                    d['allocatable']=True

                # Trying to catch the value
                if d['pointer']:
                    s=vardef.split('>')
                    if len(s)>1:
                        d['varvalue']=s[1]
                elif not d['allocatable']:
                    s=vardef.split('=')
                    if len(s)>1:
                        d['varvalue']=s[1]


                # Catching the dimension
                idx=l.find('dimension')
                if idx>0:
                    dim_str=l[idx:]
                    dim_str=dim_str[dim_str.index('(')+1:dim_str.index(')')]
                    if dim_str.find(':')>0:
                        d['dimension_fixed']=False
                    else:
                        d['dimension_fixed']=True

                    d['dimension']=dim_str

                if d['pointer'] and len(d['varvalue'])==0:
                    print('Warning: type %s pointer %s not initialized to null'%(self.raw_name,d['varname']))

            else:
                print('Error, this script assumes definition with ::')


            #
            self.components.append(d)

    def write_to_file(self,fout,indent):
        fout.write('%stype %s\n'%(indent,self.raw_name))
        for d in self.components:
            attributes=d['type_raw'];
            if len(d['dimension'])>0:
                attributes+=', dimension(%s)'%d['dimension']

            if d['pointer']:
                attributes+=', pointer'
            if d['allocatable']:
                attributes+=', allocatable'
            
            attributes+=' :: '+d['varname']
            if len(d['varvalue'])>0:
                if d['pointer']:
                    attributes+=' =>'
                else:
                    attributes+=' = '
                attributes+=d['varvalue']




            fout.write('%s%s%s\n'%(indent,self.indent,attributes))
        fout.write('%send type\n'%indent)


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
