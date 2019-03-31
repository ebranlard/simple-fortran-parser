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
    ! An addition is going to happen
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
    public :: tata
    type(T_ProfilePolar), save :: prof
    private
end module ProfileTypes"""
        F    = FortranFile(lines = s)
        sout = F.tostring(verbose = False)
        self.assert_string(sout,s)
        s="""module ProfileTypes
    use MathConstants, only: NaN
    implicit none
    type T_ProfilePolar
        integer :: nValues !< length of all polar vectors
        real(MK) :: Re !< Reynolds number
        real(PROFILE_POLAR_KIND), dimension(:), pointer :: alpha => null() !< Angle of attack in degrees from -XX to XX
    end type
end module ProfileTypes"""
        F    = FortranFile(lines = s)
        sout = F.tostring(verbose = False)
        self.assert_string(sout,s)


    def test_function(self):
        # TODO result
        s="""pure elemental real(C_DOUBLE) function it_Time_dt() result(aa) BIND(C, name='it_getdt')
    use PrecisionMod, only: C_DOUBLE
    use TimeTools
    aa=real(Time%dt, C_DOUBLE);
end function"""
        F    = FortranFile(lines   = s)
        sout = F.tostring(verbose = False)
        self.assert_string(s,sout)
#         s="""function it_Time_dt() BIND(C, name='it_getdt')
#     use PrecisionMod, only: C_DOUBLE
#     use TimeTools
#     it_getdt=real(Time%dt, C_DOUBLE);
# end function"""
#         F    = FortranFile(lines   = s)
#         sout = F.tostring(verbose = False)
#         self.assert_string(s,sout)

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
        M    = FortranMethod(raw_lines = s)
        sout = M.tostring(indent= '', verbose=False)
        self.assert_string(s,sout)
        #
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
        #
        # --- FortranMethod - Subroutine with ^
        s="""subroutine profile_list_tostring(ProfileList &
            ,iunit_opt &
            )
    real, intent(in) :: ProfileList
    integer, intent(inout) :: iunit_opt
    iunit_opt=iunit_opt+ProfileList
end subroutine"""
        s_ref="""subroutine profile_list_tostring(ProfileList,iunit_opt)
    real, intent(in) :: ProfileList
    integer, intent(inout) :: iunit_opt
    iunit_opt=iunit_opt+ProfileList
end subroutine"""
        M    = FortranMethod(raw_lines = s)
        sout = M.tostring(indent= '', verbose=False)
        self.assert_string(sout,s_ref)




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
        s='real(MK), pointer :: x => null()'
        self.assert_string(FortranDeclaration(s).tostring().strip(),s)
        s='complex(kind=MK), dimension(8) :: data = (/1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0/)'
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
        self.assert_string(FortranType(s).tostring().strip(),s)
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

        s="""type T_ProfileGeometry
    logical :: bFlatBack = .false. !< Is it a Flat back airfoil
    ! input data
    integer :: n_in = -1 !< dimension of x_in and y_in below
    real(MK), dimension(:), pointer :: x_in => null()
end type"""
        self.assert_string(FortranType(s).tostring().strip(),s)


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

        # Split
        s     = 'dimension(n(1),n(2)), pointer'
        self.assertEqual(split_entities(s),['dimension(n(1),n(2))','pointer'])

        s     = 'dimension(n(1),n(2)), pointer'

        s='real(MK), dimension(:,:,:), target, optional, save, intent(inout)'
        self.assertEqual(split_entities(s),['real(MK)','dimension(:,:,:)','target','optional','save','intent(inout)'])

        s='x => null(), a,q(3,4), c(:,:),v(N(1),:)'
        self.assertEqual(split_entities(s),['x => null()','a','q(3,4)','c(:,:)','v(N(1),:)'])
        s='data = (/1.0, 1.0/), n=1'
        self.assertEqual(split_entities(s),['data = (/1.0, 1.0/)','n=1'])

        # Not really what we would want
        s='pure int(CI) function( x, n(1) )'
        self.assertEqual(split_entities(s),['pure int(CI)','function( x, n(1) )'])

# --------------------------------------------------------------------------------}
# --- Split comments
# --------------------------------------------------------------------------------{
    def test_split(self):
        s=''
        self.assertEqual(split_comment(s),('',''))
        s='  hello'
        self.assertEqual(split_comment(s),('  hello',''))
        s='!'
        self.assertEqual(split_comment(s),('','!'))
        s='! hi '
        self.assertEqual(split_comment(s),('','! hi'))
        s='hello ! hi'
        self.assertEqual(split_comment(s),('hello','! hi'))
        s='  hello ! hi'
        self.assertEqual(split_comment(s),('  hello','! hi'))
        s='hello="!not" ! hi'
        self.assertEqual(split_comment(s),('hello="!not"','! hi'))

# --------------------------------------------------------------------------------}
# --- Indent 
# --------------------------------------------------------------------------------{
    def test_indent(self):
        s=''
        self.assertEqual(reindent(s,'    '),'    ')
        s='aa'
        self.assertEqual(reindent(s,'    '),'    aa')
        s='    aa'
        self.assertEqual(reindent(s,'    '),'    aa')
        s='        aa'
        self.assertEqual(reindent(s,'    '),'        aa')


# --------------------------------------------------------------------------------}
# --- Bind lines 
# --------------------------------------------------------------------------------{
    def test_bind(self):
        s="""a ! b"""
        (L,C)=bind_lines_with_comments(s.split('\n'))
        self.assertEqual(L[0],'a')
        self.assertEqual(C[0],'! b')
        s="""aa &   ! my com
bb  """
        (L,C)=bind_lines_with_comments(s.split('\n'))
        self.assertEqual(L[0],'aa bb')
        self.assertEqual(C[0],'! my com')

        # TODO string continuation
        s="""s="aa"&   ! my com
&"bb"  """
        (L,C)=bind_lines_with_comments(s.split('\n'))
        self.assertEqual(L[0],'s="aa""bb"')
        self.assertEqual(C[0],'! my com')


if __name__ == '__main__':
    unittest.main()

