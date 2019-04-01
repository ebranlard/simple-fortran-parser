module ProfileAutoTools
    ! Module containing type: 
    use ProfileTypes
    implicit none

    private

    interface profilepolar_init; module procedure &
          profilepolar_init_0
    end interface profilepolar_init
    interface profilepolar_initp; module procedure &
          profilepolar_initp_0,&
          profilepolar_initp_1
    end interface profilepolar_initp
    interface profilepolar_term; module procedure &
          profilepolar_term_0
    end interface profilepolar_term
    interface profilepolar_termp; module procedure &
          profilepolar_termp_0,&
          profilepolar_termp_1
    end interface profilepolar_termp
    interface profilepolar_write; module procedure &
          profilepolar_write_0
    end interface profilepolar_write
    interface profilepolar_writep; module procedure &
          profilepolar_writep_0,&
          profilepolar_writep_1
    end interface profilepolar_writep
    interface profilepolar_read; module procedure &
          profilepolar_read_0
    end interface profilepolar_read
    interface profilepolar_readp; module procedure &
          profilepolar_readp_0,&
          profilepolar_readp_1
    end interface profilepolar_readp
    public :: profilepolar_init
    public :: profilepolar_initp
    public :: profilepolar_term
    public :: profilepolar_termp
    public :: profilepolar_write
    public :: profilepolar_writep
    public :: profilepolar_read
    public :: profilepolar_readp

    interface profilegeometry_init; module procedure &
          profilegeometry_init_0
    end interface profilegeometry_init
    interface profilegeometry_initp; module procedure &
          profilegeometry_initp_0,&
          profilegeometry_initp_1
    end interface profilegeometry_initp
    interface profilegeometry_term; module procedure &
          profilegeometry_term_0
    end interface profilegeometry_term
    interface profilegeometry_termp; module procedure &
          profilegeometry_termp_0,&
          profilegeometry_termp_1
    end interface profilegeometry_termp
    interface profilegeometry_write; module procedure &
          profilegeometry_write_0
    end interface profilegeometry_write
    interface profilegeometry_writep; module procedure &
          profilegeometry_writep_0,&
          profilegeometry_writep_1
    end interface profilegeometry_writep
    interface profilegeometry_read; module procedure &
          profilegeometry_read_0
    end interface profilegeometry_read
    interface profilegeometry_readp; module procedure &
          profilegeometry_readp_0,&
          profilegeometry_readp_1
    end interface profilegeometry_readp
    public :: profilegeometry_init
    public :: profilegeometry_initp
    public :: profilegeometry_term
    public :: profilegeometry_termp
    public :: profilegeometry_write
    public :: profilegeometry_writep
    public :: profilegeometry_read
    public :: profilegeometry_readp

contains
    subroutine profilepolar_init_0(X)
        ! Arguments declaration
        type(T_ProfilePolar), intent(inout) :: X
        ! Corpus
        X%alpha =>  null()
        X%CL =>  null()
        X%CD =>  null()
        X%CM =>  null()
    end subroutine

    subroutine profilepolar_initp_0(X)
        ! Arguments declaration
        type(T_ProfilePolar), pointer :: X
        ! Corpus
        if (associated(X)) then
        X%alpha =>  null()
        X%CL =>  null()
        X%CD =>  null()
        X%CM =>  null()
        endif
    end subroutine

    subroutine profilepolar_initp_1(X)
        ! Arguments declaration
        type(T_ProfilePolar), dimension(:), pointer :: X
        ! Variable declaration
        integer :: iX
        ! Corpus
        if (associated(X)) then
            do iX=1,size(X)
                call profilepolar_init(X(iX))
            enddo
        endif
    end subroutine

    subroutine profilepolar_term_0(X)
        ! Arguments declaration
        type(T_ProfilePolar), intent(inout) :: X
        ! Corpus
        if (associated(X%alpha)) deallocate(X%alpha)
        if (associated(X%CL)) deallocate(X%CL)
        if (associated(X%CD)) deallocate(X%CD)
        if (associated(X%CM)) deallocate(X%CM)
    end subroutine

    subroutine profilepolar_termp_0(X)
        ! Arguments declaration
        type(T_ProfilePolar), pointer :: X
        ! Corpus
        if (associated(X)) then
        if (associated(X%alpha)) deallocate(X%alpha)
        if (associated(X%CL)) deallocate(X%CL)
        if (associated(X%CD)) deallocate(X%CD)
        if (associated(X%CM)) deallocate(X%CM)
            deallocate(X)
        endif
    end subroutine

    subroutine profilepolar_termp_1(X)
        ! Arguments declaration
        type(T_ProfilePolar), dimension(:), pointer :: X
        ! Variable declaration
        integer :: iX
        ! Corpus
        if (associated(X)) then
            do iX=1,size(X)
                call profilepolar_term(X(iX))
            enddo
            deallocate(X)
        endif
    end subroutine

    subroutine profilepolar_write_0(X,iunit)
        ! Arguments declaration
        type(T_ProfilePolar), intent(in) :: X
        integer, intent(in) :: iunit
        ! Corpus
        write(iunit)X%nValues
        write(iunit)X%Re
        write(iunit)associated(X%alpha)
if (associated(X%alpha)) then
    write(iunit)size(X%alpha,1)
write(iunit)X%alpha
endif
        write(iunit)associated(X%CL)
if (associated(X%CL)) then
    write(iunit)size(X%CL,1)
write(iunit)X%CL
endif
        write(iunit)associated(X%CD)
if (associated(X%CD)) then
    write(iunit)size(X%CD,1)
write(iunit)X%CD
endif
        write(iunit)associated(X%CM)
if (associated(X%CM)) then
    write(iunit)size(X%CM,1)
write(iunit)X%CM
endif
    end subroutine

    subroutine profilepolar_writep_0(X,iunit)
        ! Arguments declaration
        type(T_ProfilePolar), pointer :: X
        integer, intent(in) :: iunit
        ! Corpus
        write(iunit)associated(X)
        if (associated(X)) then
        write(iunit)X%nValues
        write(iunit)X%Re
        write(iunit)associated(X%alpha)
if (associated(X%alpha)) then
    write(iunit)size(X%alpha,1)
write(iunit)X%alpha
endif
        write(iunit)associated(X%CL)
if (associated(X%CL)) then
    write(iunit)size(X%CL,1)
write(iunit)X%CL
endif
        write(iunit)associated(X%CD)
if (associated(X%CD)) then
    write(iunit)size(X%CD,1)
write(iunit)X%CD
endif
        write(iunit)associated(X%CM)
if (associated(X%CM)) then
    write(iunit)size(X%CM,1)
write(iunit)X%CM
endif
        endif
    end subroutine

    subroutine profilepolar_writep_1(X,iunit)
        ! Arguments declaration
        type(T_ProfilePolar), dimension(:), pointer :: X
        integer, intent(in) :: iunit
        ! Variable declaration
        integer :: iX
        ! Corpus
        write(iunit)associated(X)
        if (associated(X)) then
            write(iunit)size(X)
            do iX=1,size(X)
                 call profilepolar_write(X(iX),iunit)
            enddo
        endif
    end subroutine

    subroutine profilepolar_read_0(X,iunit)
        ! Arguments declaration
        type(T_ProfilePolar), intent(out) :: X
        integer, intent(in) :: iunit
        ! Variable declaration
        logical :: bPresent
        integer :: nd1
        ! Corpus
        read(iunit)X%nValues
        read(iunit)X%Re
        read(iunit)bPresent
if (bPresent) then
    read(iunit)nd1
    allocate(X%alpha(nd1))
    read(iunit)X%alpha
endif
        read(iunit)bPresent
if (bPresent) then
    read(iunit)nd1
    allocate(X%CL(nd1))
    read(iunit)X%CL
endif
        read(iunit)bPresent
if (bPresent) then
    read(iunit)nd1
    allocate(X%CD(nd1))
    read(iunit)X%CD
endif
        read(iunit)bPresent
if (bPresent) then
    read(iunit)nd1
    allocate(X%CM(nd1))
    read(iunit)X%CM
endif
    end subroutine

    subroutine profilepolar_readp_0(X,iunit)
        ! Arguments declaration
        type(T_ProfilePolar), pointer :: X
        integer, intent(in) :: iunit
        ! Variable declaration
        logical :: bPresent
        integer :: nd1
        ! Corpus
        read(iunit)bPresent
        if (bPresent) then
        allocate(X)
        read(iunit)X%nValues
        read(iunit)X%Re
        read(iunit)bPresent
if (bPresent) then
    read(iunit)nd1
    allocate(X%alpha(nd1))
    read(iunit)X%alpha
endif
        read(iunit)bPresent
if (bPresent) then
    read(iunit)nd1
    allocate(X%CL(nd1))
    read(iunit)X%CL
endif
        read(iunit)bPresent
if (bPresent) then
    read(iunit)nd1
    allocate(X%CD(nd1))
    read(iunit)X%CD
endif
        read(iunit)bPresent
if (bPresent) then
    read(iunit)nd1
    allocate(X%CM(nd1))
    read(iunit)X%CM
endif
        endif
    end subroutine

    subroutine profilepolar_readp_1(X,iunit)
        ! Arguments declaration
        type(T_ProfilePolar), dimension(:), pointer :: X
        integer, intent(in) :: iunit
        ! Variable declaration
        integer :: iX
        logical :: bPresent
        integer :: nd1
        ! Corpus
        read(iunit)bPresent
        if (bPresent) then
            read(iunit)nd1
            if(associated(X).and. size(X)/=nd1) then
                 print*,"ERROR X wrong size"
                 STOP
            endif
            if(.not. associated(X)) then
                 allocate(X(nd1))
            endif
            do iX=1,nd1
                 call profilepolar_read(X(iX),iunit)
            enddo
        endif
    end subroutine

    subroutine profilegeometry_init_0(X)
        ! Arguments declaration
        type(T_ProfileGeometry), intent(inout) :: X
        ! Corpus
        X%bFlatBack = .false.
        X%n_in = -1
        X%x_in =>  null()
        X%y_in =>  null()
        X%n_c = -1
        X%x_c =>  null()
        X%y_c =>  null()
        X%n = -1
        X%x =>  null()
        X%y =>  null()
        X%nMean_c = -1
        X%x_mean_c =>  null()
        X%y_mean_c =>  null()
        X%thickness_mean_c =>  null()
        X%camber = NaN
        X%thickness_max = NaN
    end subroutine

    subroutine profilegeometry_initp_0(X)
        ! Arguments declaration
        type(T_ProfileGeometry), pointer :: X
        ! Corpus
        if (associated(X)) then
        X%bFlatBack = .false.
        X%n_in = -1
        X%x_in =>  null()
        X%y_in =>  null()
        X%n_c = -1
        X%x_c =>  null()
        X%y_c =>  null()
        X%n = -1
        X%x =>  null()
        X%y =>  null()
        X%nMean_c = -1
        X%x_mean_c =>  null()
        X%y_mean_c =>  null()
        X%thickness_mean_c =>  null()
        X%camber = NaN
        X%thickness_max = NaN
        endif
    end subroutine

    subroutine profilegeometry_initp_1(X)
        ! Arguments declaration
        type(T_ProfileGeometry), dimension(:), pointer :: X
        ! Variable declaration
        integer :: iX
        ! Corpus
        if (associated(X)) then
            do iX=1,size(X)
                call profilegeometry_init(X(iX))
            enddo
        endif
    end subroutine

    subroutine profilegeometry_term_0(X)
        ! Arguments declaration
        type(T_ProfileGeometry), intent(inout) :: X
        ! Corpus
        X%bFlatBack = .false. ! reinit - to avoid unused variable message
        X%n_in = -1 ! reinit - to avoid unused variable message
        if (associated(X%x_in)) deallocate(X%x_in)
        if (associated(X%y_in)) deallocate(X%y_in)
        X%n_c = -1 ! reinit - to avoid unused variable message
        if (associated(X%x_c)) deallocate(X%x_c)
        if (associated(X%y_c)) deallocate(X%y_c)
        X%n = -1 ! reinit - to avoid unused variable message
        if (associated(X%x)) deallocate(X%x)
        if (associated(X%y)) deallocate(X%y)
        X%nMean_c = -1 ! reinit - to avoid unused variable message
        if (associated(X%x_mean_c)) deallocate(X%x_mean_c)
        if (associated(X%y_mean_c)) deallocate(X%y_mean_c)
        if (associated(X%thickness_mean_c)) deallocate(X%thickness_mean_c)
        X%camber = NaN ! reinit - to avoid unused variable message
        X%thickness_max = NaN ! reinit - to avoid unused variable message
    end subroutine

    subroutine profilegeometry_termp_0(X)
        ! Arguments declaration
        type(T_ProfileGeometry), pointer :: X
        ! Corpus
        if (associated(X)) then
        X%bFlatBack = .false. ! reinit - to avoid unused variable message
        X%n_in = -1 ! reinit - to avoid unused variable message
        if (associated(X%x_in)) deallocate(X%x_in)
        if (associated(X%y_in)) deallocate(X%y_in)
        X%n_c = -1 ! reinit - to avoid unused variable message
        if (associated(X%x_c)) deallocate(X%x_c)
        if (associated(X%y_c)) deallocate(X%y_c)
        X%n = -1 ! reinit - to avoid unused variable message
        if (associated(X%x)) deallocate(X%x)
        if (associated(X%y)) deallocate(X%y)
        X%nMean_c = -1 ! reinit - to avoid unused variable message
        if (associated(X%x_mean_c)) deallocate(X%x_mean_c)
        if (associated(X%y_mean_c)) deallocate(X%y_mean_c)
        if (associated(X%thickness_mean_c)) deallocate(X%thickness_mean_c)
        X%camber = NaN ! reinit - to avoid unused variable message
        X%thickness_max = NaN ! reinit - to avoid unused variable message
            deallocate(X)
        endif
    end subroutine

    subroutine profilegeometry_termp_1(X)
        ! Arguments declaration
        type(T_ProfileGeometry), dimension(:), pointer :: X
        ! Variable declaration
        integer :: iX
        ! Corpus
        if (associated(X)) then
            do iX=1,size(X)
                call profilegeometry_term(X(iX))
            enddo
            deallocate(X)
        endif
    end subroutine

    subroutine profilegeometry_write_0(X,iunit)
        ! Arguments declaration
        type(T_ProfileGeometry), intent(in) :: X
        integer, intent(in) :: iunit
        ! Corpus
        write(iunit)X%bFlatBack
        write(iunit)X%n_in
        write(iunit)associated(X%x_in)
if (associated(X%x_in)) then
    write(iunit)size(X%x_in,1)
write(iunit)X%x_in
endif
        write(iunit)associated(X%y_in)
if (associated(X%y_in)) then
    write(iunit)size(X%y_in,1)
write(iunit)X%y_in
endif
        write(iunit)X%n_c
        write(iunit)associated(X%x_c)
if (associated(X%x_c)) then
    write(iunit)size(X%x_c,1)
write(iunit)X%x_c
endif
        write(iunit)associated(X%y_c)
if (associated(X%y_c)) then
    write(iunit)size(X%y_c,1)
write(iunit)X%y_c
endif
        write(iunit)X%n
        write(iunit)associated(X%x)
if (associated(X%x)) then
    write(iunit)size(X%x,1)
write(iunit)X%x
endif
        write(iunit)associated(X%y)
if (associated(X%y)) then
    write(iunit)size(X%y,1)
write(iunit)X%y
endif
        write(iunit)X%iLE
        write(iunit)X%iTE
        write(iunit)X%nMean_c
        write(iunit)associated(X%x_mean_c)
if (associated(X%x_mean_c)) then
    write(iunit)size(X%x_mean_c,1)
write(iunit)X%x_mean_c
endif
        write(iunit)associated(X%y_mean_c)
if (associated(X%y_mean_c)) then
    write(iunit)size(X%y_mean_c,1)
write(iunit)X%y_mean_c
endif
        write(iunit)associated(X%thickness_mean_c)
if (associated(X%thickness_mean_c)) then
    write(iunit)size(X%thickness_mean_c,1)
write(iunit)X%thickness_mean_c
endif
        write(iunit)X%camber
        write(iunit)X%thickness_max
    end subroutine

    subroutine profilegeometry_writep_0(X,iunit)
        ! Arguments declaration
        type(T_ProfileGeometry), pointer :: X
        integer, intent(in) :: iunit
        ! Corpus
        write(iunit)associated(X)
        if (associated(X)) then
        write(iunit)X%bFlatBack
        write(iunit)X%n_in
        write(iunit)associated(X%x_in)
if (associated(X%x_in)) then
    write(iunit)size(X%x_in,1)
write(iunit)X%x_in
endif
        write(iunit)associated(X%y_in)
if (associated(X%y_in)) then
    write(iunit)size(X%y_in,1)
write(iunit)X%y_in
endif
        write(iunit)X%n_c
        write(iunit)associated(X%x_c)
if (associated(X%x_c)) then
    write(iunit)size(X%x_c,1)
write(iunit)X%x_c
endif
        write(iunit)associated(X%y_c)
if (associated(X%y_c)) then
    write(iunit)size(X%y_c,1)
write(iunit)X%y_c
endif
        write(iunit)X%n
        write(iunit)associated(X%x)
if (associated(X%x)) then
    write(iunit)size(X%x,1)
write(iunit)X%x
endif
        write(iunit)associated(X%y)
if (associated(X%y)) then
    write(iunit)size(X%y,1)
write(iunit)X%y
endif
        write(iunit)X%iLE
        write(iunit)X%iTE
        write(iunit)X%nMean_c
        write(iunit)associated(X%x_mean_c)
if (associated(X%x_mean_c)) then
    write(iunit)size(X%x_mean_c,1)
write(iunit)X%x_mean_c
endif
        write(iunit)associated(X%y_mean_c)
if (associated(X%y_mean_c)) then
    write(iunit)size(X%y_mean_c,1)
write(iunit)X%y_mean_c
endif
        write(iunit)associated(X%thickness_mean_c)
if (associated(X%thickness_mean_c)) then
    write(iunit)size(X%thickness_mean_c,1)
write(iunit)X%thickness_mean_c
endif
        write(iunit)X%camber
        write(iunit)X%thickness_max
        endif
    end subroutine

    subroutine profilegeometry_writep_1(X,iunit)
        ! Arguments declaration
        type(T_ProfileGeometry), dimension(:), pointer :: X
        integer, intent(in) :: iunit
        ! Variable declaration
        integer :: iX
        ! Corpus
        write(iunit)associated(X)
        if (associated(X)) then
            write(iunit)size(X)
            do iX=1,size(X)
                 call profilegeometry_write(X(iX),iunit)
            enddo
        endif
    end subroutine

    subroutine profilegeometry_read_0(X,iunit)
        ! Arguments declaration
        type(T_ProfileGeometry), intent(out) :: X
        integer, intent(in) :: iunit
        ! Variable declaration
        logical :: bPresent
        integer :: nd1
        ! Corpus
        read(iunit)X%bFlatBack
        read(iunit)X%n_in
        read(iunit)bPresent
if (bPresent) then
    read(iunit)nd1
    allocate(X%x_in(nd1))
    read(iunit)X%x_in
endif
        read(iunit)bPresent
if (bPresent) then
    read(iunit)nd1
    allocate(X%y_in(nd1))
    read(iunit)X%y_in
endif
        read(iunit)X%n_c
        read(iunit)bPresent
if (bPresent) then
    read(iunit)nd1
    allocate(X%x_c(nd1))
    read(iunit)X%x_c
endif
        read(iunit)bPresent
if (bPresent) then
    read(iunit)nd1
    allocate(X%y_c(nd1))
    read(iunit)X%y_c
endif
        read(iunit)X%n
        read(iunit)bPresent
if (bPresent) then
    read(iunit)nd1
    allocate(X%x(nd1))
    read(iunit)X%x
endif
        read(iunit)bPresent
if (bPresent) then
    read(iunit)nd1
    allocate(X%y(nd1))
    read(iunit)X%y
endif
        read(iunit)X%iLE
        read(iunit)X%iTE
        read(iunit)X%nMean_c
        read(iunit)bPresent
if (bPresent) then
    read(iunit)nd1
    allocate(X%x_mean_c(nd1))
    read(iunit)X%x_mean_c
endif
        read(iunit)bPresent
if (bPresent) then
    read(iunit)nd1
    allocate(X%y_mean_c(nd1))
    read(iunit)X%y_mean_c
endif
        read(iunit)bPresent
if (bPresent) then
    read(iunit)nd1
    allocate(X%thickness_mean_c(nd1))
    read(iunit)X%thickness_mean_c
endif
        read(iunit)X%camber
        read(iunit)X%thickness_max
    end subroutine

    subroutine profilegeometry_readp_0(X,iunit)
        ! Arguments declaration
        type(T_ProfileGeometry), pointer :: X
        integer, intent(in) :: iunit
        ! Variable declaration
        logical :: bPresent
        integer :: nd1
        ! Corpus
        read(iunit)bPresent
        if (bPresent) then
        allocate(X)
        read(iunit)X%bFlatBack
        read(iunit)X%n_in
        read(iunit)bPresent
if (bPresent) then
    read(iunit)nd1
    allocate(X%x_in(nd1))
    read(iunit)X%x_in
endif
        read(iunit)bPresent
if (bPresent) then
    read(iunit)nd1
    allocate(X%y_in(nd1))
    read(iunit)X%y_in
endif
        read(iunit)X%n_c
        read(iunit)bPresent
if (bPresent) then
    read(iunit)nd1
    allocate(X%x_c(nd1))
    read(iunit)X%x_c
endif
        read(iunit)bPresent
if (bPresent) then
    read(iunit)nd1
    allocate(X%y_c(nd1))
    read(iunit)X%y_c
endif
        read(iunit)X%n
        read(iunit)bPresent
if (bPresent) then
    read(iunit)nd1
    allocate(X%x(nd1))
    read(iunit)X%x
endif
        read(iunit)bPresent
if (bPresent) then
    read(iunit)nd1
    allocate(X%y(nd1))
    read(iunit)X%y
endif
        read(iunit)X%iLE
        read(iunit)X%iTE
        read(iunit)X%nMean_c
        read(iunit)bPresent
if (bPresent) then
    read(iunit)nd1
    allocate(X%x_mean_c(nd1))
    read(iunit)X%x_mean_c
endif
        read(iunit)bPresent
if (bPresent) then
    read(iunit)nd1
    allocate(X%y_mean_c(nd1))
    read(iunit)X%y_mean_c
endif
        read(iunit)bPresent
if (bPresent) then
    read(iunit)nd1
    allocate(X%thickness_mean_c(nd1))
    read(iunit)X%thickness_mean_c
endif
        read(iunit)X%camber
        read(iunit)X%thickness_max
        endif
    end subroutine

    subroutine profilegeometry_readp_1(X,iunit)
        ! Arguments declaration
        type(T_ProfileGeometry), dimension(:), pointer :: X
        integer, intent(in) :: iunit
        ! Variable declaration
        integer :: iX
        logical :: bPresent
        integer :: nd1
        ! Corpus
        read(iunit)bPresent
        if (bPresent) then
            read(iunit)nd1
            if(associated(X).and. size(X)/=nd1) then
                 print*,"ERROR X wrong size"
                 STOP
            endif
            if(.not. associated(X)) then
                 allocate(X(nd1))
            endif
            do iX=1,nd1
                 call profilegeometry_read(X(iX),iunit)
            enddo
        endif
    end subroutine

end module ProfileAutoTools
