
!>  Contains the main types for profile data
module ProfileTypes
    use PrecisionMod, only: MK, PROFILE_POLAR_KIND
    use MathConstants, only: NaN
    implicit none
    
    type T_ProfilePolar
        integer :: nValues !< length of all polar vectors
        real(MK) :: Re !< Reynolds number
        real(PROFILE_POLAR_KIND), dimension(:), pointer :: alpha => null() !< Angle of attack in degrees from -XX to XX
        real(PROFILE_POLAR_KIND), dimension(:), pointer :: CL    => null() !< Lift coefficients
        real(PROFILE_POLAR_KIND), dimension(:), pointer :: CD    => null() !< Drag coefficients
        real(PROFILE_POLAR_KIND), dimension(:), pointer :: CM    => null() !< Moment coefficients
    end type

    type T_ProfileGeometry
        logical :: bFlatBack = .false. !< Is it a Flat back airfoil
        ! input data
        integer :: n_in = -1 !< dimension of x_in and y_in below 
        real(MK), dimension(:), pointer :: x_in => null()
        real(MK), dimension(:), pointer :: y_in => null()
        ! normalized data, have to include the LE and TE points
        integer :: n_c = -1 !< dimension of x and y below 
        real(MK), dimension(:), pointer :: x_c => null() !< x/c geometry coordinates, LE is x=, TE is x=
        real(MK), dimension(:), pointer :: y_c => null() !< y/c geometry coordinates, Upper side(Suction) is mainly y>0
        ! Data in Body coordinate, scaled with chord, twisted. etc.
        integer :: n = -1 !< dimension of x_in and y_in below 
        real(MK), dimension(:), pointer :: x => null() !< x/c geometry coordinates, LE is x=, TE is x=
        real(MK), dimension(:), pointer :: y => null() !< y/c geometry coordinates, Upper side(Suction) is mainly y>0
        !
        real(MK) :: iLE !< index of LE point in x,y vectors
        real(MK) :: iTE !< index of TE point in x,y vectors
        ! "Linear theory variables"
        integer ::nMean_c= -1 !< dimension of x_mean_c and y_mean_c below
        real(MK),dimension(:),pointer :: x_mean_c=>null() !< x Coordinate mean chord line, going from LE to TE
        real(MK),dimension(:),pointer :: y_mean_c=>null() !< 
        real(MK),dimension(:),pointer :: thickness_mean_c =>null()!< 
        real(MK) :: camber=NaN
        real(MK) :: thickness_max=NaN
    end type


    ! hawc type 
!      Type Tprofdata
!          real(4) :: chord         =0.0d0                  ! Chord lenght of section
!          real(4) :: thickness     =0.0d0                  ! Thickness in % of chord
!          real(8),dimension(3):: vec_075to025 =[0.0d0,0.0d0,0.0d0] ! vector from C3/4 to C1/4 in [m]
!          real(4) :: prof_set      =0.0d0                  ! Aerodynamic profile set number for this section
!          integer :: nazi=360                             ! Number of profiles in interpolated profile coefficient arrays
!          real(8)  :: dazi=2.0d0*3.14159265359/360     ! distance between data (is set to 2*pi/nazi)
!          real(4),dimension(:),pointer :: CL,CD,CM         ! Interpolated profile coefficients
!      end Type Tprofdata
!  contains
            
end module ProfileTypes
