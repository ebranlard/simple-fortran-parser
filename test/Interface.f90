!> 
module InterfaceLink
    use PrecisionMod, only: C_DOUBLE, C_INT, C_CHAR, MK
    use HerbiVorIO, only: log_error, log_info, log_warning
    use CStrings, only: cstring2fortran
    implicit none
contains
    subroutine io_term() BIND(C, name='io_term')
        use HerbiVor
        call herbivor_term();
    end subroutine

    !> Returns 1 if library has no error
    integer(C_INT) function check() BIND(C, name='check')
        use PrecisionMod, only: C_INT
        use HerbiVorErrorState, only: is_herbivor_in_error_state
        !
        check=int(1,C_INT)
        if(is_herbivor_in_error_state()) then
            check=int(0,C_INT);
            !print*,'Library in error state'
        endif
    end function

    !> Returns 1 if library has no error
    subroutine error_solved() BIND(C, name='error_solved')
        use HerbiVorErrorState, only: set_herbivor_error_state
        call set_herbivor_error_state(.false.)
    end subroutine

    !> Getting a string variable
    subroutine io_set_output_to_std(flag_c) BIND(C, name='io_set_output_to_std')
        use HerbiVorIO, only: set_output_to_std
        use PrecisionMod, only: C_INT
        !
        integer(C_INT),intent(in) :: flag_c   !< 1=output to std
        !
        call set_output_to_std(flag_c==1)
    end subroutine


    !> Setting a number variable
    subroutine io_set_var(svar_c,rval) BIND(C, name='io_set_var')
        use CStrings, only: cstring2fortran
        use HerbiVorIO, only: log_error, log_info
        use HerbiVorIO, only: bdebug_set_triggers
        use PrecisionMod, only: MK, C_DOUBLE, C_CHAR
        use MatlabFunctions, only: num2str
        use TimeTools, only: setdt, settmax
        use HerbiVorData ! The variables we will change are in this module
        use WindData, only: TurbPart
        use TimeInfoTools, only: set_action_time_var
        use StringUtils,       only: strsplit, T_SubStrings, substr_term
        character(kind=C_CHAR,len=1),dimension(*),intent(in) :: svar_c !< variable name
        real(C_DOUBLE),intent(in)              :: rval   !< variable value
        !
        character(64)                        :: svar   !< fortran string

        type(T_SubStrings) :: SubStrings
        call substr_term(SubStrings)
    end subroutine


    !> Getting HerbiVor version
    subroutine io_print_version() BIND(C, name='io_print_version')
        use HerbiVorLink, only: herbivor_print_version_no_log
        call herbivor_print_version_no_log()
    end subroutine

    !> Add a velocity field request with method v1 v2 v3 in global coord
    subroutine iv_user_vel_add_from_v1v2v3(v1,v2,v3,bComputeGrad,bPolar,n1,n2,n3) BIND(C,name='iv_user_vel_add_from_v1v2v3')
        use PrecisionMod, only: MK, C_DOUBLE, C_INT
        use UserVelocityFieldData, only: user_vel_add_from_v1v2v3
        integer(C_INT), intent(in)               :: n1,n2,n3
        real(C_DOUBLE), dimension(n1),intent(in) :: v1
        real(C_DOUBLE), dimension(n2),intent(in) :: v2
        real(C_DOUBLE), dimension(n3),intent(in) :: v3
        integer(C_INT), intent(in)               :: bComputeGrad
        integer(C_INT), intent(in)               :: bPolar
        !
        real(MK), dimension(:), allocatable :: v1_MK
        real(MK), dimension(:), allocatable :: v2_MK
        real(MK), dimension(:), allocatable :: v3_MK
        !
        allocate(v1_MK(n1)) ; v1_MK=real(v1,MK)
        allocate(v2_MK(n2)) ; v2_MK=real(v2,MK)
        allocate(v3_MK(n3)) ; v3_MK=real(v3,MK)
        call user_vel_add_from_v1v2v3(v1_MK,v2_MK,v3_MK,bComputeGrad==1,bPolar==1,int(n1),int(n2),int(n3))
    end subroutine

    !> Uses dt to increment time, returns 1 if time is successfully incremented
    integer(C_INT) function it_time_increment() BIND(C, name='it_incrementtime')
        use PrecisionMod, only: C_INT
        use TimeTools
        it_time_increment=0;
        if(time_increment()) it_IncrementTime=1;
    end function

    !!! Mutator Functions
    subroutine it_setTmax(t_max_in) BIND(C, name='it_setTmax')
        use PrecisionMod, only: MK, C_DOUBLE
        use TimeTools
        use HerbiVorData
        real(C_DOUBLE), intent(in) :: t_max_in
        call setTmax(real(t_max_in,MK))
        call settmax_herbivor(real(t_max_in,MK))
    end subroutine

    real(C_DOUBLE) function it_Time%dt() BIND(C, name='it_getdt')
        use PrecisionMod, only: C_DOUBLE
        use TimeTools
        it_getdt=real(Time%dt, C_DOUBLE);
    end function

    integer(C_INT) function it_Time%ntmax() BIND(C, name='it_getntmax')
        use PrecisionMod, only: C_INT
        use TimeTools
        it_getntmax=int(Time%ntmax,C_INT);
    end function

    !> Returns the size of the polar
    integer(C_INT) function ip_get_profile_polar_n(idb,iprof,ipol) result(n) BIND(C,name='ip_get_profile_polar_n')
        use ProfileData, only: ProfileDBInput, ProfileDBInterp
        use ProfileDatabaseTools, only: profile_database_polar_exists
        integer(C_INT), intent(in) :: idb !< 0 : input profile, 1, interp profile
        integer(C_INT), intent(in) :: iprof
        integer(C_INT), intent(in) :: ipol
        n=-1
        if(idb==0) then
            if(profile_database_polar_exists(ProfileDBInput,iprof,ipol)) n=ProfileDBInput%Profiles(iprof)%Polars(ipol)%nValues
        elseif(idb==1) then
            if(profile_database_polar_exists(ProfileDBInterp,iprof,ipol)) n=ProfileDBInterp%Profiles(iprof)%Polars(ipol)%nValues
        endif
        if(n==-1) call log_warning('Polar not found in database')
    end function
end module InterfaceLink
