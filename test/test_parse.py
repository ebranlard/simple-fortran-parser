#!/usr/bin/env python
from __future__ import print_function
import os, sys, inspect
import unittest

MyDir=os.path.dirname(__file__)
pythonpath=os.path.realpath(os.path.abspath(os.path.join('../'+MyDir)))
sys.path.insert(0, pythonpath)

from fortran_file import*


import unittest
class Test(unittest.TestCase):
    def assert_stringi(self,a,b):
        self.assert_string(a.lower(),b.lower())

    def assert_string(self,a,b):
        if a!=b:
            print('--------------------------------------------------')
            print('New>'+a+'<')
            print('--------------------------------------------------')
            print('Ref>'+b+'<')
            print('--------------------------------------------------')
            print('String written to files temp_ref and temp_new for comparison')
            print('--------------------------------------------------')
            with open('temp_ref','w') as f:
                f.write(b)
            with open('temp_new','w') as f:
                f.write(a)
        self.assertEqual(a,b)

# --------------------------------------------------------------------------------}
# --- Program 
# --------------------------------------------------------------------------------{
    def test_program(self):
        s="""program binary2Vtk
    use PrecisionMod
    implicit none
    real :: x
    integer :: i = 0
    x=x+i
contains
    subroutine f()
        write(*,*)'Hello'
    end subroutine
end program binary2Vtk"""
        F    = FortranFile(lines = s)
        sout = F.tostring(verbose = False)
        self.assert_string(sout,s)

# --------------------------------------------------------------------------------}
# --- Module 
# --------------------------------------------------------------------------------{
    def test_module(self):
        s="""module InterfaceLink
    use CStrings, only: cstring2fortran
    implicit none
contains
    subroutine io_term() BIND(C, name='io_term')
        use HerbiVor
        call herbivor_term();
    end subroutine
end module InterfaceLink"""
        F    = FortranFile(lines = s)
        sout = F.tostring(verbose = False)
        self.assert_string(sout,s)

        s="""module ProfileTypes
    use MathConstants, only: NaN
    implicit none
    type T_ProfilePolar
        integer :: nValues !< length of all polar vectors
        real(MK) :: Re !< Reynolds number
    end type
end module ProfileTypes"""
        F    = FortranFile(lines = s)
        sout = F.tostring(verbose = False)
        self.assert_string(sout,s)





    def test_function(self):
        # TODO Types before function
        # TODO result

#         s="""real(C_DOUBLE) function it_Time_dt() BIND(C,name='it_getdt')
#     use PrecisionMod, only: C_DOUBLE
#     use TimeTools
#     it_getdt=real(Time%dt, C_DOUBLE);
# end function"""
        s="""function it_Time_dt() BIND(C, name='it_getdt')
    use PrecisionMod, only: C_DOUBLE
    use TimeTools
    it_getdt=real(Time%dt, C_DOUBLE);
end function"""
        F    = FortranFile(lines   = s)
        sout = F.tostring(verbose = False)
        self.assert_string(s,sout)
# 
    def test_subroutine(self):
        # --- FortranFile - Subroutine outside of module:
        s="""subroutine io_term(x) BIND(C, name='io_term')
    use HerbiVor
    integer, intent(in) :: x
    integer :: y
    integer, pointer :: z
    call herbivor_term(y,z)
end subroutine"""
        F    = FortranFile(lines   = s)
        sout = F.tostring(verbose = False)
        self.assert_string(s,sout)

        # --- FortranMethod - Subroutine directly parsed
        #print('------------------------')
        M    = FortranMethod(raw_lines = s)
        sout = M.tostring(indent= '', verbose=False)
        self.assert_string(s,sout)

        #     import pdb
        #     pdb.set_trace()
        s="""subroutine profile_list_tostring(ProfileList,iunit_opt)
    type(T_RefProfile), pointer :: ProfileList
    integer, optional, intent(in) :: iunit_opt
    type(T_RefProfile), pointer :: CurrentProfile
    integer :: iprof
    character(len=56) :: prefix
    prefix=iprof+CurrentProfile
end subroutine"""
        M    = FortranMethod(raw_lines = s)
        sout = M.tostring(indent= '', verbose=False)
        self.assert_string(s,sout)
        #print(M.tostring())




# --------------------------------------------------------------------------------}
# ---  
# --------------------------------------------------------------------------------{
    def test_declaration(self):
        # Test types
        s='integer :: x'
        self.assert_string(FortranDeclaration(s).tostring().strip(),s)
        s='INTEGER :: x'
        self.assert_stringi(FortranDeclaration(s).tostring().strip(),s)
        s='type(MyType) :: x'
        self.assert_string(FortranDeclaration(s).tostring().strip(),s)

        # Test attributes
        s='character(len=12), INTENT(in) :: x'
        self.assert_stringi(FortranDeclaration(s).tostring().strip(),s)
        # Test attributes
        s='real(MK), dimension(:,:,:), target, optional, save, intent(inout) :: x'
        self.assert_string(FortranDeclaration(s).tostring().strip(),s)

        # Test init
        s='real(MK) :: x = 12'
        self.assert_string(FortranDeclaration(s).tostring().strip(),s)
        s='real(MK), pointer :: x =>null()'
        self.assert_string(FortranDeclaration(s).tostring().strip(),s)

        # Test advanced
        s='character(kind=C_CHAR,len=1), dimension(*), intent(in) :: x'
        self.assert_stringi(FortranDeclaration(s).tostring().strip(),s)

        s='real*8, dimension(n(1),n(2)) :: x'
        self.assert_stringi(FortranDeclaration(s).tostring().strip(),s)

# --------------------------------------------------------------------------------}
# ---  
# --------------------------------------------------------------------------------{
    def test_declarations(self):
        # test-multiline
        s='real(MK) :: x, y, z'
        s_ref='real(MK) :: x\nreal(MK) :: y\nreal(MK) :: z'
        self.assert_string(FortranDeclarations(s).tostring().strip(),s_ref)

        s='real :: a(3), b(:,:), c(n(1),n(2))'
        s_ref='real, dimension(3) :: a\nreal, dimension(:,:) :: b\nreal, dimension(n(1),n(2)) :: c'
        self.assert_string(FortranDeclarations(s).tostring().strip(),s_ref)


# --------------------------------------------------------------------------------}
# --- UseStatement 
# --------------------------------------------------------------------------------{
    def test_use(self):
        s='use MyMod'
        self.assert_string(FortranUseStatement(s).tostring().strip(),s)
        s='use MyMod, only: this, that ! comment'
        self.assert_string(FortranUseStatement(s).tostring().strip(),s)

# --------------------------------------------------------------------------------}
# --- Types
# --------------------------------------------------------------------------------{
    def test_type(self):
        s="""type T_ProfilePolar
    integer :: nValues !< length of all polar vectors
    real(MK) :: Re !< Reynolds number
end type"""
#         self.assert_string(FortranType(s).tostring().strip(),s)
        s="""Type TgetWindSpeedData
    real*8   ::    u_mean, &                          ! 10 min mean wind speed
        tint, &                            ! turbulence intensity
        wind_yaw_ang
        end type"""
        s_ref="""type TgetWindSpeedData
    real*8 :: u_mean ! 10 min mean wind speed turbulence intensity
    real*8 :: tint
    real*8 :: wind_yaw_ang
end type"""
        self.assert_string(FortranType(s).tostring().strip(),s_ref)




# --------------------------------------------------------------------------------}
# --- Entitiy
# --------------------------------------------------------------------------------{
    def test_entity(self):
        s='integer'
        self.assert_stringi(first_entity(s),s)

        s     = 'integer, pointer'
        s_ref = 'integer'
        self.assert_stringi(first_entity(s),s_ref)

        s     = 'integer(MK), pointer'
        s_ref = 'integer(MK)'
        self.assert_stringi(first_entity(s),s_ref)

        s     = 'integer, dimension(:)'
        s_ref = 'integer'
        self.assert_stringi(first_entity(s),s_ref)

        s     = 'integer(kind=1,len=2), pointer'
        s_ref = 'integer(kind=1,len=2)'
        self.assert_stringi(first_entity(s),s_ref)

        s     = 'dimension(n(1),n(2)), pointer'
        s_ref = 'dimension(n(1),n(2))'
        self.assert_stringi(first_entity(s),s_ref)



if __name__ == '__main__':
    unittest.main()

