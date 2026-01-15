FORTRAN Modules
===============

This section documents the FORTRAN modules that comprise the OSOAA radiative transfer model.

Overview
--------

OSOAA consists of 12 main FORTRAN modules organized by functionality:

.. list-table:: OSOAA Module Structure
   :widths: 30 70
   :header-rows: 1

   * - Module
     - Purpose
   * - OSOAA_MAIN
     - Main program entry point and control flow
   * - OSOAA_ANGLES
     - Angular discretization and geometry
   * - OSOAA_AEROSOLS
     - Atmospheric aerosol properties
   * - OSOAA_HYDROSOLS
     - Ocean particle properties
   * - OSOAA_MIE
     - Mie scattering calculations
   * - OSOAA_PARTICLES_RAD
     - Particle radiative properties
   * - OSOAA_PROFILE
     - Vertical profiles (atmosphere and ocean)
   * - OSOAA_SURFACE
     - Sea surface properties
   * - OSOAA_SURF_MATRICES
     - Surface reflection/transmission matrices
   * - OSOAA_SOS
     - Successive orders of scattering method
   * - OSOAA_SOS_CORE
     - Core radiative transfer calculations
   * - OSOAA_TRPHI
     - Rotation angles and transformations

Module Dependencies
-------------------

The modules have the following dependency structure::

    OSOAA_MAIN
    ├── OSOAA_ANGLES
    ├── OSOAA_PROFILE
    ├── OSOAA_AEROSOLS
    │   ├── OSOAA_MIE
    │   └── OSOAA_PARTICLES_RAD
    ├── OSOAA_HYDROSOLS
    │   ├── OSOAA_MIE
    │   └── OSOAA_PARTICLES_RAD
    ├── OSOAA_SURFACE
    │   └── OSOAA_SURF_MATRICES
    │       └── OSOAA_TRPHI
    └── OSOAA_SOS
        ├── OSOAA_SOS_CORE
        └── OSOAA_TRPHI

All modules include the header file ``OSOAA.h`` which defines constants and parameters.

OSOAA_MAIN
----------

**File**: ``src/OSOAA_MAIN.F``

**Purpose**: Main program controlling the entire simulation workflow.

Key Functions
~~~~~~~~~~~~~

Program Flow
^^^^^^^^^^^^

1. **Initialization**
   
   * Read input parameters
   * Validate configuration
   * Initialize data structures

2. **Setup Phase**
   
   * Compute angular grids
   * Build atmospheric profile
   * Build ocean profile
   * Calculate aerosol properties
   * Calculate hydrosol properties
   * Compute surface matrices

3. **Radiative Transfer**
   
   * Execute successive orders method
   * Accumulate scattering contributions
   * Check convergence

4. **Output Generation**
   
   * Write radiance fields
   * Write polarization components
   * Generate result files

Key Variables
~~~~~~~~~~~~~

.. code-block:: fortran

   ! Wavelength
   REAL*8 :: WAVELENGTH
   
   ! Solar geometry
   REAL*8 :: THETA_SUN
   REAL*8 :: PHI_REL
   
   ! Viewing geometry
   REAL*8 :: THETA_VIEW
   REAL*8 :: Z_OUTPUT
   INTEGER :: LEVEL_TYPE
   
   ! Iteration control
   INTEGER :: IGMAX          ! Maximum scattering orders
   REAL*8 :: CONV_THRESHOLD  ! Convergence threshold

Constants Defined
~~~~~~~~~~~~~~~~~

From ``inc/OSOAA.h``:

.. code-block:: c

   #define CTE_DEFAULT_IGMAX 100          // Max iterations
   #define CTE_WAMIN 0.299                // Min wavelength (nm)
   #define CTE_DEFAULT_FICSOS_RES_BIN "LUM_SF.bin"
   #define CTE_DEFAULT_FICSOS_RES_VS_VZA "LUM_vsVZA.txt"

OSOAA_ANGLES
------------

**File**: ``src/OSOAA_ANGLES.F``

**Purpose**: Compute angular discretization grids for radiative transfer calculations.

Key Subroutines
~~~~~~~~~~~~~~~

ANGLES_GAUSS_LEGENDRE
^^^^^^^^^^^^^^^^^^^^^

Computes Gauss-Legendre quadrature points and weights for angular integration.

.. code-block:: fortran

   SUBROUTINE ANGLES_GAUSS_LEGENDRE(N, X, W)
   ! INPUT:
   !   N - Number of quadrature points
   ! OUTPUT:
   !   X(N) - Quadrature points (cosines of angles)
   !   W(N) - Quadrature weights

**Algorithm**: Uses recursive calculation of Legendre polynomials to determine 
Gauss quadrature nodes and weights for numerical integration over [-1, 1].

ANGLES_USER_DEFINED
^^^^^^^^^^^^^^^^^^^

Reads and processes user-specified viewing angles.

.. code-block:: fortran

   SUBROUTINE ANGLES_USER_DEFINED(FILENAME, NANG, ANGLES)
   ! INPUT:
   !   FILENAME - Path to angle file
   ! OUTPUT:
   !   NANG - Number of angles read
   !   ANGLES(NANG) - Array of viewing angles (degrees)

ANGLES_COMBINE
^^^^^^^^^^^^^^

Merges Gauss quadrature angles with user-defined angles.

Angular Grid Structure
~~~~~~~~~~~~~~~~~~~~~~

The angular discretization consists of:

1. **Gauss angles** for accurate integration
2. **User angles** for specific output directions
3. **Combined grid** sorted by angle

.. note::
   More Gauss points improve accuracy but increase computation time. 
   Typical values: 40-80 points.

OSOAA_AEROSOLS
--------------

**File**: ``src/OSOAA_AEROSOLS.F``

**Purpose**: Compute optical and microphysical properties of atmospheric aerosols.

Key Subroutines
~~~~~~~~~~~~~~~

AEROSOLS_MONO_MODAL
^^^^^^^^^^^^^^^^^^^

Calculates properties for mono-modal aerosol size distributions.

.. code-block:: fortran

   SUBROUTINE AEROSOLS_MONO_MODAL(DISTRIB_TYPE, RADIUS, VARIANCE,
  &                                MR, MI, WAVELENGTH, ...)
   ! INPUT:
   !   DISTRIB_TYPE - 1=Junge, 2=Log-normal
   !   RADIUS - Characteristic radius (µm)
   !   VARIANCE - Distribution variance
   !   MR, MI - Refractive index (real, imaginary)
   !   WAVELENGTH - Wavelength (nm)
   ! OUTPUT:
   !   Phase function, single scattering albedo, etc.

**Supported Distributions**:

* **Junge power law**: :math:`n(r) \\propto r^{-\\nu}`
* **Log-normal**: :math:`n(r) = \\frac{N}{\\sqrt{2\\pi}\\sigma r} \\exp\\left[-\\frac{(\\ln r - \\ln r_0)^2}{2\\sigma^2}\\right]`

AEROSOLS_BIMODAL
^^^^^^^^^^^^^^^^

Handles bi-modal log-normal distributions (fine + coarse modes).

.. code-block:: fortran

   SUBROUTINE AEROSOLS_BIMODAL(R_FINE, VAR_FINE, VC_FINE,
  &                             R_COARSE, VAR_COARSE, VC_COARSE,
  &                             MR_FINE, MI_FINE, MR_COARSE, MI_COARSE, ...)

**Physical Interpretation**: Separates aerosols into:

* **Fine mode**: Urban pollution, biomass burning (r < 0.5 µm)
* **Coarse mode**: Dust, sea salt (r > 0.5 µm)

AEROSOLS_WMO
^^^^^^^^^^^^

Implements WMO (World Meteorological Organization) standard aerosol models.

Available models:

1. Maritime
2. Continental
3. Urban
4. Tropospheric

AEROSOLS_SHETTLE_FENN
^^^^^^^^^^^^^^^^^^^^^

Shettle & Fenn aerosol models with humidity dependence.

Optical Properties Computed
~~~~~~~~~~~~~~~~~~~~~~~~~~~

For each aerosol model, the following are calculated:

* **Extinction coefficient** (:math:`\\beta_{ext}`)
* **Scattering coefficient** (:math:`\\beta_{sca}`)
* **Absorption coefficient** (:math:`\\beta_{abs}`)
* **Single scattering albedo** (:math:`\\omega_0 = \\beta_{sca}/\\beta_{ext}`)
* **Phase function** (:math:`P(\\Theta)`)
* **Phase matrix** (for polarization)

Truncation Strategy
~~~~~~~~~~~~~~~~~~~

From ``inc/OSOAA.h``:

.. code-block:: c

   #define CTE_AER_MU1_TRONCA 0.8    // First truncation threshold
   #define CTE_AER_MU2_TRONCA 0.94   // Second truncation threshold
   #define CTE_PH_SEUIL_TRONCA 0.1   // Truncation threshold

The phase function is truncated at forward angles to improve numerical stability 
while preserving total scattering.

OSOAA_HYDROSOLS
---------------

**File**: ``src/OSOAA_HYDROSOLS.F``

**Purpose**: Compute optical properties of ocean particles (phytoplankton and minerals).

Key Subroutines
~~~~~~~~~~~~~~~

HYDROSOLS_CHLOROPHYLL
^^^^^^^^^^^^^^^^^^^^^

Bio-optical model based on chlorophyll concentration.

.. code-block:: fortran

   SUBROUTINE HYDROSOLS_CHLOROPHYLL(CHL_CONCENTRATION, WAVELENGTH, ...)
   ! INPUT:
   !   CHL_CONCENTRATION - Chlorophyll-a (mg/m³)
   !   WAVELENGTH - Wavelength (nm)
   ! OUTPUT:
   !   Absorption coefficient, scattering coefficient, 
   !   backscattering ratio, phase function

**Empirical Relationships**:

* Absorption: :math:`a_{ph}(\\lambda) = A(\\lambda) \\cdot [Chl]^{B(\\lambda)}`
* Scattering: :math:`b_{bp}(\\lambda) = b_{bp}(550) \\cdot (\\lambda/550)^{-\\eta}`

HYDROSOLS_MINERAL
^^^^^^^^^^^^^^^^^

Mineral-like particle (suspended sediment) properties.

HYDROSOLS_YELLOW_SUBSTANCE
^^^^^^^^^^^^^^^^^^^^^^^^^^

Colored dissolved organic matter (CDOM) absorption.

.. math::

   a_{CDOM}(\\lambda) = a_{CDOM}(440) \\cdot \\exp[-S(\\lambda - 440)]

Where :math:`S \\approx 0.014` nm⁻¹ is the spectral slope.

Vertical Profiles
~~~~~~~~~~~~~~~~~

Three profile types:

1. **Homogeneous**: Constant with depth
   
   .. math::
   
      C(z) = C_0

2. **Gaussian**: Deep chlorophyll maximum
   
   .. math::
   
      C(z) = C_{bg} + C_{max} \\exp\\left[-\\frac{(z-z_{max})^2}{2\\sigma_z^2}\\right]

3. **Custom**: User-defined depth profile

Truncation Constants
~~~~~~~~~~~~~~~~~~~~

.. code-block:: c

   #define CTE_HYD_MU1_TRONCA 0.85   // Hydrosol truncation threshold 1
   #define CTE_HYD_MU2_TRONCA 0.92   // Hydrosol truncation threshold 2

OSOAA_MIE
---------

**File**: ``src/OSOAA_MIE.F``

**Purpose**: Mie theory calculations for spherical particles.

Key Subroutines
~~~~~~~~~~~~~~~

MIE_COEFFICIENTS
^^^^^^^^^^^^^^^^

Computes Mie scattering coefficients :math:`a_n` and :math:`b_n`.

.. code-block:: fortran

   SUBROUTINE MIE_COEFFICIENTS(X, M, NSTOP, AN, BN)
   ! INPUT:
   !   X - Size parameter (2πr/λ)
   !   M - Complex refractive index
   !   NSTOP - Maximum order
   ! OUTPUT:
   !   AN(NSTOP) - Scattering coefficients a_n
   !   BN(NSTOP) - Scattering coefficients b_n

**Size Parameter**:

.. math::

   x = \\frac{2\\pi r}{\\lambda}

MIE_CROSS_SECTIONS
^^^^^^^^^^^^^^^^^^

Calculates scattering and extinction cross sections.

.. math::

   C_{sca} = \\frac{2\\pi}{k^2} \\sum_{n=1}^{\\infty} (2n+1)(|a_n|^2 + |b_n|^2)

.. math::

   C_{ext} = \\frac{2\\pi}{k^2} \\sum_{n=1}^{\\infty} (2n+1)\\text{Re}(a_n + b_n)

MIE_PHASE_FUNCTION
^^^^^^^^^^^^^^^^^^

Computes scattering phase function and phase matrix.

.. code-block:: fortran

   SUBROUTINE MIE_PHASE_FUNCTION(ANGLES, NANG, AN, BN, NSTOP,
  &                               PHASE_FUNC, PHASE_MATRIX)
   ! OUTPUT:
   !   PHASE_FUNC(NANG) - Scalar phase function
   !   PHASE_MATRIX(4,4,NANG) - Mueller matrix elements

**Phase Matrix Elements**:

The Mueller matrix relates input and output Stokes vectors:

.. math::

   \\begin{pmatrix} I' \\\\ Q' \\\\ U' \\\\ V' \\end{pmatrix} = 
   \\frac{1}{k^2 r^2} \\begin{pmatrix}
   M_{11} & M_{12} & 0 & 0 \\\\
   M_{21} & M_{22} & 0 & 0 \\\\
   0 & 0 & M_{33} & M_{34} \\\\
   0 & 0 & -M_{43} & M_{44}
   \\end{pmatrix}
   \\begin{pmatrix} I \\\\ Q \\\\ U \\\\ V \\end{pmatrix}

OSOAA_PARTICLES_RAD
-------------------

**File**: ``src/OSOAA_PARTICLES_RAD.F``

**Purpose**: Compute radiative properties of particle ensembles.

Key Functions
~~~~~~~~~~~~~

Integration over Size Distribution
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: fortran

   SUBROUTINE INTEGRATE_SIZE_DISTRIBUTION(N_FUNC, SIZE_DIST,
  &                                        CROSS_SECTIONS, ...)
   ! Integrates single-particle properties over size distribution
   ! to obtain bulk optical properties

**Integration Method**: Gauss-Legendre quadrature over logarithmic radius grid.

Phase Function Normalization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ensures phase function normalization:

.. math::

   \\frac{1}{2}\\int_{-1}^{1} P(\\mu) d\\mu = 1

Where :math:`\\mu = \\cos\\Theta`.

Optical Depth Calculation
^^^^^^^^^^^^^^^^^^^^^^^^^

Computes optical depth through a layer:

.. math::

   \\tau = \\int \\beta_{ext}(z) dz

OSOAA_PROFILE
-------------

**File**: ``src/OSOAA_PROFILE.F``

**Purpose**: Manage vertical profiles of atmospheric and oceanic properties.

Key Subroutines
~~~~~~~~~~~~~~~

PROFILE_ATMOSPHERE
^^^^^^^^^^^^^^^^^^

Builds atmospheric vertical structure.

.. code-block:: fortran

   SUBROUTINE PROFILE_ATMOSPHERE(Z_LEVELS, N_LEVELS, PRESSURE,
  &                               TEMPERATURE, DENSITY, ...)
   ! Computes:
   ! - Pressure profile
   ! - Temperature profile
   ! - Air density profile
   ! - Rayleigh scattering profile
   ! - Aerosol optical depth profile

**Rayleigh Scattering**:

.. math::

   \\beta_R(z) = \\beta_R(0) \\exp(-z/H_R)

Where :math:`H_R = 8` km is the scale height.

PROFILE_OCEAN
^^^^^^^^^^^^^

Builds ocean vertical structure.

.. code-block:: fortran

   SUBROUTINE PROFILE_OCEAN(Z_LEVELS, N_LEVELS, CHLOROPHYLL,
  &                          MINERALS, CDOM, ...)
   ! Computes:
   ! - Chlorophyll profile
   ! - Mineral concentration profile
   ! - CDOM absorption profile
   ! - Total absorption coefficient
   ! - Total scattering coefficient
   ! - Total optical depth

PROFILE_COUPLING
^^^^^^^^^^^^^^^^

Handles interface between atmosphere and ocean at :math:`z = 0`.

Grid Discretization
~~~~~~~~~~~~~~~~~~~

The vertical grid uses:

* **Atmospheric layers**: Exponentially spaced, denser near surface
* **Ocean layers**: Logarithmically spaced, denser near surface
* **Total levels**: Typically 50-100 levels per medium

OSOAA_SURFACE
-------------

**File**: ``src/OSOAA_SURFACE.F``

**Purpose**: Compute sea surface optical properties.

Key Subroutines
~~~~~~~~~~~~~~~

SURFACE_FLAT
^^^^^^^^^^^^

Fresnel reflection and transmission for flat surface.

.. math::

   R_\\parallel = \\left|\\frac{n_1\\cos\\theta_t - n_2\\cos\\theta_i}{n_1\\cos\\theta_t + n_2\\cos\\theta_i}\\right|^2

.. math::

   R_\\perp = \\left|\\frac{n_1\\cos\\theta_i - n_2\\cos\\theta_t}{n_1\\cos\\theta_i + n_2\\cos\\theta_t}\\right|^2

SURFACE_ROUGH_COX_MUNK
^^^^^^^^^^^^^^^^^^^^^^

Cox & Munk wind-roughened surface model.

.. code-block:: fortran

   SUBROUTINE SURFACE_ROUGH_COX_MUNK(WIND_SPEED, THETA_I, THETA_T,
  &                                   PHI_REL, REFLECTANCE, ...)
   ! INPUT:
   !   WIND_SPEED - Wind speed at 10m (m/s)
   !   THETA_I - Incident zenith angle
   !   THETA_T - Transmitted zenith angle
   !   PHI_REL - Relative azimuth angle
   ! OUTPUT:
   !   REFLECTANCE - Directional reflectance
   !   TRANSMITTANCE - Directional transmittance

**Wave Slope Statistics**:

.. math::

   P(Z_x, Z_y) = \\frac{1}{2\\pi\\sigma_c\\sigma_u} 
   \\exp\\left[-\\frac{1}{2}\\left(\\frac{Z_x^2}{\\sigma_c^2} + \\frac{Z_y^2}{\\sigma_u^2}\\right)\\right]

Where:

* :math:`\\sigma_c^2 = 0.003 + 0.00512 \\cdot U` (cross-wind)
* :math:`\\sigma_u^2 = 0.00316 \\cdot U` (upwind)
* :math:`U` = wind speed (m/s)

OSOAA_SURF_MATRICES
-------------------

**File**: ``src/OSOAA_SURF_MATRICES.F``

**Purpose**: Compute reflection and transmission matrices for rough surface.

Key Components
~~~~~~~~~~~~~~

Wave Facet Integration
^^^^^^^^^^^^^^^^^^^^^^

Integrates over all possible wave slope orientations.

.. code-block:: fortran

   SUBROUTINE INTEGRATE_WAVE_FACETS(THETA_I, THETA_T, PHI,
  &                                  SIGMA_C, SIGMA_U,
  &                                  REFL_MATRIX, TRANS_MATRIX)

**Integration Domain**:

* Zenith angles of wave normal: 0-90°
* Azimuth angles: 0-360° (discretized into CTE_PH_NU points)

Geometric Configuration
^^^^^^^^^^^^^^^^^^^^^^^

Determines valid transmission/reflection geometries.

Constants:

.. code-block:: c

   #define CTE_THRESHOLD_GMAX 1.D-40          // Max wave probability
   #define CTE_THRESHOLD_DICHO 1.D-10         // Dichotomy threshold
   #define CTE_THRESHOLD_COSTHETAN 0.001      // Min cos(theta_n)
   #define CTE_THRESHOLD_GEO_CONFIG 1.D-15    // Geometry threshold
   #define CTE_PH_NU 1024                     // Azimuthal angles (2^10)
   #define CTE_PH_NQ 10                       // Exponent for NU

Mueller Matrix Assembly
^^^^^^^^^^^^^^^^^^^^^^^

Combines Fresnel coefficients with wave statistics to form complete Mueller matrices.

OSOAA_SOS
---------

**File**: ``src/OSOAA_SOS.F``

**Purpose**: Implement successive orders of scattering method.

Algorithm Overview
~~~~~~~~~~~~~~~~~~

The successive orders method splits the radiance field:

.. math::

   I_{total} = \\sum_{n=0}^{\\infty} I^{(n)}

Where :math:`I^{(n)}` is the contribution from the :math:`n`-th scattering order.

Order 0: Direct Transmission
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. math::

   I^{(0)} = I_0 \\exp(-\\tau)

Order n≥1: Multiple Scattering
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. math::

   I^{(n)}(\\vec{r}, \\vec{\\Omega}) = \\int_V \\int_{4\\pi} 
   P(\\vec{\\Omega}', \\vec{\\Omega}) I^{(n-1)}(\\vec{r}', \\vec{\\Omega}') 
   \\exp(-\\tau_{r',r}) d\\Omega' dV'

Key Subroutines
~~~~~~~~~~~~~~~

SOS_ITERATE_ORDER
^^^^^^^^^^^^^^^^^

Computes the n-th order of scattering.

.. code-block:: fortran

   SUBROUTINE SOS_ITERATE_ORDER(ORDER, RADIANCE_IN, RADIANCE_OUT,
  &                              CONVERGED, ...)
   ! INPUT:
   !   ORDER - Current scattering order
   !   RADIANCE_IN - Input radiance field from (n-1)
   ! OUTPUT:
   !   RADIANCE_OUT - Output radiance field for order n
   !   CONVERGED - Logical flag for convergence

**Convergence Criteria**:

.. math::

   \\frac{|I^{(n)} - I^{(n-1)}|}{I^{(n-1)}} < \\epsilon

Where :math:`\\epsilon` is the convergence threshold (typically 0.001).

SOS_ACCUMULATE
^^^^^^^^^^^^^^

Sums contributions from all orders.

SOS_FOURIER_DECOMPOSITION
^^^^^^^^^^^^^^^^^^^^^^^^^

Decomposes radiance into Fourier series in azimuth:

.. math::

   I(\\theta, \\phi) = \\sum_{m=0}^{M} I_m(\\theta) \\cos[m(\\phi - \\phi_0)]

Convergence thresholds from ``OSOAA.h``:

.. code-block:: c

   #define CTE_PH_SEUIL_CV_SG  0.005    // Geometric series
   #define CTE_PH_SEUIL_SUMDIF  0.001   // Cumulative scattering
   #define CTE_PH_SEUIL_SF  0.0002      // Fourier series

OSOAA_SOS_CORE
--------------

**File**: ``src/OSOAA_SOS_CORE.F``

**Purpose**: Core radiative transfer equation solution.

Physical Processes
~~~~~~~~~~~~~~~~~~

Molecular Depolarization
^^^^^^^^^^^^^^^^^^^^^^^^

Constants:

.. code-block:: c

   #define CTE_MDF_AIR 0.0279   // Air molecular depolarization
   #define CTE_MDF_SEA 0.0906   // Seawater molecular depolarization

**Cabannes Line Factor**:

.. math::

   \\rho = \\frac{6(1-\\delta)}{3+7\\delta}

Where :math:`\\delta` is the depolarization factor.

Source Function
^^^^^^^^^^^^^^^

The source function includes:

1. Direct solar beam attenuated by atmosphere/ocean
2. Single scattered radiance
3. Multiple scattered radiance (from previous orders)

Integration Methods
^^^^^^^^^^^^^^^^^^^

* **Angular integration**: Gauss-Legendre quadrature
* **Vertical integration**: Trapezoidal or Simpson's rule
* **Azimuthal integration**: Fourier decomposition

OSOAA_TRPHI
-----------

**File**: ``src/OSOAA_TRPHI.F``

**Purpose**: Coordinate transformations and rotation angles.

Key Subroutines
~~~~~~~~~~~~~~~

ROTATION_ANGLE
^^^^^^^^^^^^^^

Computes rotation angle for transforming Stokes parameters between coordinate systems.

.. code-block:: fortran

   SUBROUTINE ROTATION_ANGLE(THETA1, PHI1, THETA2, PHI2, ALPHA)
   ! Computes rotation angle ALPHA to transform from
   ! scattering plane (1) to scattering plane (2)

**Rotation Matrix**:

.. math::

   \\mathbf{L}(\\alpha) = \\begin{pmatrix}
   1 & 0 & 0 & 0 \\\\
   0 & \\cos 2\\alpha & \\sin 2\\alpha & 0 \\\\
   0 & -\\sin 2\\alpha & \\cos 2\\alpha & 0 \\\\
   0 & 0 & 0 & 1
   \\end{pmatrix}

TRANSFORM_STOKES
^^^^^^^^^^^^^^^^

Applies rotation to Stokes vector.

.. math::

   \\vec{S}' = \\mathbf{L}(\\alpha) \\vec{S}

Threshold:

.. code-block:: c

   #define CTE_SEUIL_Z 0.001   // Threshold for rotation angles

Summary
-------

The OSOAA FORTRAN modules work together to:

1. Discretize angular and vertical domains
2. Compute optical properties of aerosols and hydrosols
3. Calculate surface reflection/transmission
4. Solve radiative transfer equation using successive orders
5. Output radiance and polarization fields

For implementation details, see the source code and :doc:`algorithms` section.

Next Steps
----------

* :doc:`code_structure` - Overall code organization
* :doc:`algorithms` - Detailed algorithm descriptions
* :doc:`../science/radiative_transfer` - Theoretical background
