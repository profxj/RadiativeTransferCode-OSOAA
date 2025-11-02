.. _successive_orders:

Successive Orders Method
========================

This section describes the successive orders of scattering (SOS) method, the core numerical algorithm in OSOAA for solving the vector radiative transfer equation in coupled atmosphere-ocean systems.

.. contents:: Contents
   :local:
   :depth: 3

Introduction
------------

The successive orders of scattering method is a rigorous numerical technique for solving radiative transfer problems with multiple scattering. It provides an accurate and physically intuitive solution by decomposing the total radiance field into contributions from different scattering orders.

**Key Advantages:**

* **Physical interpretation**: Each term represents n scattering events
* **Controlled accuracy**: Convergence can be monitored and controlled
* **Flexible**: Applicable to arbitrary geometries and optical properties
* **Comprehensive**: Handles polarization naturally through Mueller matrix formalism

**Applications:**

* Coupled atmosphere-ocean radiative transfer
* Multiple scattering in turbid media
* Polarimetric remote sensing
* Validation of approximate methods

OSOAA implements the vector (polarized) successive orders method with Fourier decomposition in azimuth, optimized for atmosphere-ocean systems with rough surface interfaces.

Theoretical Foundation
----------------------

Radiative Transfer Equation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The vector radiative transfer equation (VRTE) describes the evolution of the Stokes vector **I** = (I, Q, U, V)^T along a ray:

.. math::

   \mu\frac{d\vec{I}(z,\mu,\phi)}{dz} = -\beta(z)\vec{I}(z,\mu,\phi) + \vec{S}(z,\mu,\phi)

Where:

* z = Vertical coordinate (altitude or depth)
* μ = cos(θ), cosine of zenith angle
* φ = Azimuth angle
* β(z) = Extinction coefficient [m⁻¹]
* **S** = Source function (scattering + emission)

**Source Function:**

The scattering source function is:

.. math::

   \vec{S}(z,\mu,\phi) = \frac{\beta_{sca}(z)}{4\pi}\int_0^{2\pi}\int_{-1}^{1} \mathbf{P}(z,\mu,\phi;\mu',\phi') \vec{I}(z,\mu',\phi') d\mu' d\phi'

Where:

* β_sca(z) = Scattering coefficient
* **P** = Phase matrix (4×4 for full polarization)
* Integration is over all incident directions (μ', φ')

**Boundary Conditions:**

* **Top of atmosphere (TOA)**: Solar irradiance at z = z_TOA
* **Bottom of ocean**: No upwelling from below (or specified bottom reflectance)
* **Surface interface**: Reflection and transmission matrices from Cox & Munk model

Order Decomposition
~~~~~~~~~~~~~~~~~~~

The total radiance field is expanded as a series:

.. math::

   \vec{I}_{total}(z,\mu,\phi) = \sum_{n=0}^{\infty} \vec{I}^{(n)}(z,\mu,\phi)

Where **I**^(n) is the contribution from exactly n scattering events.

**Physical Interpretation:**

* **n = 0**: Direct solar beam (unscattered)
* **n = 1**: Single scattering (photons scattered once)
* **n = 2**: Double scattering (photons scattered twice)
* **n ≥ 3**: Higher-order multiple scattering

Order 0: Direct Transmission
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The zeroth-order term represents direct solar radiation attenuated by extinction:

**In atmosphere (downwelling):**

.. math::

   \vec{I}^{(0)}(z,\mu,\phi) = \vec{F}_0 \delta(\mu - \mu_0)\delta(\phi - \phi_0) \exp\left[-\int_{z_{TOA}}^z \frac{\beta(z')}{\mu_0} dz'\right]

Where:

* **F**_0 = Extraterrestrial solar irradiance (Stokes vector)
* μ_0 = cos(θ_sun)
* φ_0 = Solar azimuth angle
* δ = Dirac delta function (directional source)

**Optical Depth:**

.. math::

   \tau(z) = \int_z^{z_{TOA}} \beta(z') dz'

**Transmitted Solar Beam:**

.. math::

   \vec{I}^{(0)}(z) = \vec{F}_0 \exp[-\tau(z)/\mu_0]

**In ocean (transmitted through surface):**

The solar beam is transmitted through the air-sea interface with:

* Refraction according to Snell's law
* Fresnel transmission coefficient
* Polarization transformation (Mueller matrix)

Order n ≥ 1: Multiple Scattering
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For scattering order n ≥ 1, the radiance is computed recursively:

.. math::

   \vec{I}^{(n)}(z,\mu,\phi) = \int_{V}\int_{4\pi} G(z,\mu,\phi; z',\mu',\phi') \vec{I}^{(n-1)}(z',\mu',\phi') d\Omega' dV'

Where G is the Green's function representing single-scattering from point (z', μ', φ') to (z, μ, φ).

**Single Scattering Operator:**

.. math::

   G(z,\mu,\phi; z',\mu',\phi') = \frac{\beta_{sca}(z')}{4\pi} \mathbf{P}(z',\Theta) \exp\left[-\int_{z'}^z \frac{\beta(s)}{|\mu|} ds\right]

Where Θ is the scattering angle determined by:

.. math::

   \cos\Theta = \mu\mu' + \sqrt{1-\mu^2}\sqrt{1-\mu'^2}\cos(\phi-\phi')

**Recursive Calculation:**

The key insight: if we know **I**^(n-1) everywhere, we can compute **I**^(n) by treating **I**^(n-1) as a source for single scattering.

Algorithm Implementation
------------------------

Computational Strategy
~~~~~~~~~~~~~~~~~~~~~~

**Step-by-Step Process:**

1. **Initialization:**
   
   * Set up vertical grid (atmosphere and ocean layers)
   * Set up angular grid (zenith and azimuth angles)
   * Compute optical properties at each level
   * Pre-compute surface reflection/transmission matrices

2. **Order 0 (Direct Beam):**
   
   * Calculate solar beam transmission through atmosphere
   * Apply surface transmission to ocean
   * Continue transmission through ocean layers
   * Accumulate: I_total = I^(0)

3. **Iteration Loop (n = 1, 2, 3, ...):**
   
   a. **Source function**: Use I^(n-1) to compute scattering source
   b. **Integrate RTE**: Solve for I^(n) with this source
   c. **Apply boundary conditions**: Surface reflection/transmission
   d. **Accumulate**: I_total += I^(n)
   e. **Check convergence**: If |I^(n)|/|I_total| < ε, stop
   f. **Update**: I_prev = I^(n), increment n

4. **Output:**
   
   * Final radiance field: I_total
   * Number of orders required
   * Convergence status

Pseudocode
~~~~~~~~~~

.. code-block:: text

   SUBROUTINE SUCCESSIVE_ORDERS(geometry, optical_properties, surface)
   
      ! Initialize
      I_total(:,:,:) = 0.0
      I_prev(:,:,:) = 0.0
      converged = FALSE
      order = 0
      
      ! Order 0: Direct transmission
      CALL COMPUTE_DIRECT_BEAM(I_direct)
      I_total = I_direct
      I_prev = I_direct
      
      ! Iterate over scattering orders
      DO order = 1, MAX_ORDERS
         
         ! Compute source function from previous order
         CALL COMPUTE_SOURCE_FUNCTION(I_prev, source)
         
         ! Solve RTE with this source
         CALL SOLVE_RTE_WITH_SOURCE(source, I_current)
         
         ! Apply surface boundary conditions
         CALL APPLY_SURFACE_BC(I_current, surface, I_current)
         
         ! Accumulate total radiance
         I_total = I_total + I_current
         
         ! Check convergence
         relative_change = NORM(I_current) / NORM(I_total)
         
         IF (relative_change < THRESHOLD) THEN
            converged = TRUE
            EXIT
         END IF
         
         ! Prepare for next iteration
         I_prev = I_current
         
      END DO
      
      IF (.NOT. converged) THEN
         PRINT *, "WARNING: Did not converge after ", MAX_ORDERS, " orders"
      END IF
      
      RETURN I_total, order, converged
   
   END SUBROUTINE

Source Function Computation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The source function at point (z, μ, φ) for order n is:

.. math::

   \vec{S}^{(n)}(z,\mu,\phi) = \frac{\beta_{sca}(z)}{4\pi}\int_0^{2\pi}\int_{-1}^{1} \mathbf{P}(z,\mu,\phi;\mu',\phi') \vec{I}^{(n-1)}(z,\mu',\phi') d\mu' d\phi'

**Numerical Implementation:**

1. **Angular discretization**: Replace integrals with quadrature sums:

   .. math::

      \vec{S}^{(n)}(z,\mu_i,\phi_j) = \frac{\beta_{sca}(z)}{4\pi} \sum_{k=1}^{N_\mu} \sum_{l=1}^{N_\phi} w_k w_l \mathbf{P}_{ikjl} \vec{I}^{(n-1)}(z,\mu_k,\phi_l)

2. **Phase matrix interpolation**: Pre-compute or interpolate **P** for required angles

3. **Vectorization**: Compute for all output angles simultaneously (efficient)

**Computational Cost:**

* O(N_z × N_μ² × N_φ²) operations per order
* Dominant computational burden in SOS method

Integration of RTE
~~~~~~~~~~~~~~~~~~

With the source function known, solve:

.. math::

   \mu\frac{d\vec{I}^{(n)}}{dz} = -\beta(z)\vec{I}^{(n)} + \vec{S}^{(n)}(z,\mu,\phi)

**Methods:**

1. **Discrete ordinates**: Solve along each discrete direction μ_i
2. **Upward sweep** (μ > 0): Integrate from bottom to top
3. **Downward sweep** (μ < 0): Integrate from top to bottom

**Formal Solution:**

For upward directions (μ > 0):

.. math::

   \vec{I}^{(n)}(z,\mu,\phi) = \vec{I}^{(n)}(z_0,\mu,\phi)e^{-\tau(z_0,z)/\mu} + \int_{z_0}^z \frac{\vec{S}^{(n)}(z',\mu,\phi)}{\mu} e^{-\tau(z',z)/\mu} dz'

**Numerical Integration:**

* Layer-by-layer integration
* Exponential attenuation factors
* Accumulation of source contributions

Surface Boundary Conditions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

At the air-sea interface (z = 0), apply reflection and transmission:

**Downward transmission (air → ocean):**

.. math::

   \vec{I}_{ocean}^{(n)}(0^-,\mu,\phi) = \int_0^{2\pi}\int_0^1 \mathbf{T}(\mu',\phi';\mu,\phi) \vec{I}_{atm}^{(n)}(0^+,\mu',\phi') d\mu' d\phi'

**Upward reflection (ocean → ocean):**

.. math::

   \vec{I}_{ocean,down}^{(n)}(0^-,\mu,\phi) = \int_0^{2\pi}\int_0^1 \mathbf{R}_{oo}(\mu',\phi';\mu,\phi) \vec{I}_{ocean,up}^{(n)}(0^-,\mu',\phi') d\mu' d\phi'

**Upward transmission (ocean → air):**

.. math::

   \vec{I}_{atm}^{(n)}(0^+,\mu,\phi) = \int_0^{2\pi}\int_0^1 \mathbf{T}_{oa}(\mu',\phi';\mu,\phi) \vec{I}_{ocean}^{(n)}(0^-,\mu',\phi') d\mu' d\phi'

**Downward reflection (air → air):**

.. math::

   \vec{I}_{atm,up}^{(n)}(0^+,\mu,\phi) = \int_0^{2\pi}\int_0^1 \mathbf{R}_{aa}(\mu',\phi';\mu,\phi) \vec{I}_{atm,down}^{(n)}(0^+,\mu',\phi') d\mu' d\phi'

Where:

* **T** = Transmission matrices (pre-computed for rough surface)
* **R** = Reflection matrices (air-air, ocean-ocean)
* Subscripts: atm = atmosphere, ocean = ocean, up/down = direction

**Implementation:**

These boundary conditions couple the atmosphere and ocean solutions, requiring careful handling of the interface at each order.

Convergence Criteria
--------------------

Convergence Tests
~~~~~~~~~~~~~~~~~

The iteration continues until the contribution from the latest order becomes negligible.

**Relative Convergence:**

.. math::

   \frac{\|\vec{I}^{(n)}\|}{\|\vec{I}_{total}\|} < \epsilon

Where ∥·∥ is an appropriate norm (e.g., L2 norm, maximum value).

**Typical Threshold:**

* ε = 0.001 (0.1% contribution): Standard accuracy
* ε = 0.0001 (0.01% contribution): High accuracy
* ε = 0.01 (1% contribution): Fast approximation

**Multiple Criteria:**

OSOAA may use multiple convergence tests:

1. **Absolute change**: |I^(n)| < ε_abs
2. **Relative change**: |I^(n)|/|I_total| < ε_rel
3. **Maximum location**: Convergence at critical locations (e.g., water-leaving radiance)

Convergence Behavior
~~~~~~~~~~~~~~~~~~~~

**Factors Affecting Convergence:**

1. **Optical Thickness:**
   
   * Thin media (τ < 1): 5-20 orders
   * Moderate (τ = 1-10): 20-50 orders
   * Thick (τ > 10): 50-100+ orders

2. **Single Scattering Albedo:**
   
   * Conservative scattering (ω_0 → 1): Slow convergence
   * Absorbing media (ω_0 < 0.8): Faster convergence

3. **Phase Function:**
   
   * Isotropic: Faster convergence
   * Forward-peaked: Slower convergence (more orders propagate)

4. **Geometry:**
   
   * Nadir viewing: Faster than oblique
   * Solar zenith angle: Higher SZA → more orders

**Typical Requirements:**

For OSOAA simulations:

* **Clear atmosphere, oligotrophic ocean**: 20-40 orders
* **Moderate turbidity**: 40-70 orders
* **High turbidity or clouds**: 70-150 orders

Geometric Series Acceleration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For optically thick media, higher orders can be approximated by a geometric series:

.. math::

   \sum_{k=N}^{\infty} I^{(k)} \approx \frac{I^{(N)}}{1 - r}

Where r is the estimated ratio I^(N)/I^(N-1).

**Application:**

If convergence is slow but orders show geometric decrease:

.. math::

   r = \frac{I^{(N)}}{I^{(N-1)}}

Then estimate:

.. math::

   I_{remaining} = \frac{I^{(N)}}{1-r}

**Caution:**

Only valid when:

* r < 1 (decreasing orders)
* r is approximately constant over recent orders
* Sufficient orders computed to establish pattern

Fourier Decomposition
---------------------

Azimuthal Expansion
~~~~~~~~~~~~~~~~~~~

Due to the cylindrical symmetry of the solar source, radiance can be expanded in Fourier series:

.. math::

   \vec{I}(z,\mu,\phi) = \sum_{m=0}^{M} \vec{I}^m(z,\mu)\cos[m(\phi-\phi_0)]

Where:

* m = Fourier mode (azimuthal order)
* φ_0 = Solar azimuth angle
* M = Truncation order

**Benefits:**

1. **Dimension reduction**: 3D → 2D problems (one per mode m)
2. **Computational efficiency**: Each mode solved independently
3. **Faster convergence**: Higher modes contribute less

Phase Matrix Expansion
~~~~~~~~~~~~~~~~~~~~~~

The phase matrix is similarly expanded:

.. math::

   \mathbf{P}(\mu,\phi;\mu',\phi') = \sum_{m=0}^{M} \mathbf{P}^m(\mu,\mu')\cos[m(\phi-\phi')]

Where **P**^m(μ,μ') is the m-th Fourier component.

**Scattering Angle:**

.. math::

   \cos\Theta = \mu\mu' + \sqrt{1-\mu^2}\sqrt{1-\mu'^2}\cos(\phi-\phi')

The phase function P(Θ) is expanded using addition theorem:

.. math::

   P(\Theta) = \sum_{m=0}^{\infty} (2-\delta_{0m})P^m(\mu)P^m(\mu')\cos[m(\phi-\phi')]

**Legendre Polynomial Expansion:**

Each Fourier mode is further expanded in Legendre polynomials:

.. math::

   P^m(\mu,\mu') = \sum_{l=m}^{L} \chi_l^m P_l^m(\mu)P_l^m(\mu')

Where:

* P_l^m = Associated Legendre polynomials
* χ_l^m = Expansion coefficients
* L = Legendre truncation order

Truncation Criteria
~~~~~~~~~~~~~~~~~~~

**Fourier Truncation:**

The series is truncated when:

.. math::

   \frac{\|\vec{I}^m\|}{\|\vec{I}^0\|} < \epsilon_F

**Typical Threshold:**

* ε_F = 0.0002 (CTE_PH_SEUIL_SF in OSOAA)

**Modes Required:**

* Rayleigh scattering: m = 0, 1, 2 (mainly)
* Aerosol scattering: m = 0-10 typical
* Rough surface: m = 0-20+ (depends on wind speed)

**Legendre Order:**

Must satisfy:

.. math::

   L \geq 2N_\mu

Where N_μ is the number of Gauss angles.

**OSOAA Defaults:**

* CTE_DEFAULT_OS_NB = 80 (radiance Legendre order)
* CTE_DEFAULT_OS_NS = 96 (surface Fresnel Legendre order)
* CTE_DEFAULT_OS_NM = 176 (total Fourier order)

Relationship: OS_NM ≥ OS_NB + OS_NS

Computational Efficiency
~~~~~~~~~~~~~~~~~~~~~~~~

**Savings:**

Without Fourier decomposition: O(N_μ² × N_φ²)
With Fourier decomposition: O(N_μ² × M) where M << N_φ

**Speedup:**

Typically 10-50× faster than full 3D calculation.

**Memory:**

Store radiance as I^m(z, μ) for each mode, rather than I(z, μ, φ) for all angles.

Implementation Details
----------------------

Angular Discretization
~~~~~~~~~~~~~~~~~~~~~~

**Gauss-Legendre Quadrature:**

Zenith angle integration uses Gauss-Legendre quadrature:

.. math::

   \int_{-1}^{1} f(\mu) d\mu \approx \sum_{i=1}^{N} w_i f(\mu_i)

Where:

* μ_i = Gauss abscissas (zeros of Legendre polynomial P_N)
* w_i = Gauss weights
* N = Number of quadrature points

**Properties:**

* Exact for polynomials of degree ≤ 2N-1
* Optimal for smooth integrands
* OSOAA typical: N = 20-80 angles per hemisphere

**User-Defined Angles:**

Additional viewing angles can be added:

* Not part of quadrature (no weights)
* Radiance interpolated or computed directly
* Used for specific output directions

**Azimuthal Angles:**

For Fourier mode computation:

* Uniform grid: φ_j = 2πj/N_φ, j = 0, ..., N_φ-1
* FFT for efficient Fourier transform
* Typical: N_φ = 64-256

Vertical Discretization
~~~~~~~~~~~~~~~~~~~~~~~

**Layer Structure:**

* Atmosphere: 30-100 layers, denser near surface
* Ocean: 20-50 layers, denser near surface
* Interface: Special handling at z = 0

**Optical Depth per Layer:**

Recommended: Δτ < 0.1-0.5 for accuracy

**Integration Methods:**

* Exponential factors: exp(-Δτ/μ)
* Trapezoidal or Simpson's rule for sources
* Careful handling of strong gradients

Fortran Implementation
~~~~~~~~~~~~~~~~~~~~~~

**Key Modules:**

Located in ``src/OSOAA_SOS.F`` and ``src/OSOAA_SOS_CORE.F``:

.. code-block:: fortran

   SUBROUTINE SOS_MAIN(...)
   ! Main successive orders control
   ! Manages iteration loop and convergence

   SUBROUTINE SOS_ITERATE_ORDER(ORDER, RADIANCE_IN, RADIANCE_OUT, ...)
   ! Computes n-th scattering order
   ! INPUT:  RADIANCE_IN  - I^(n-1)
   ! OUTPUT: RADIANCE_OUT - I^(n)

   SUBROUTINE SOS_COMPUTE_SOURCE(RADIANCE, SOURCE, ...)
   ! Computes scattering source function

   SUBROUTINE SOS_INTEGRATE_RTE(SOURCE, RADIANCE, ...)
   ! Integrates radiative transfer equation

   SUBROUTINE SOS_APPLY_SURFACE_BC(...)
   ! Applies surface boundary conditions

   SUBROUTINE SOS_ACCUMULATE(I_TOTAL, I_ORDER, ...)
   ! Accumulates contributions

   SUBROUTINE SOS_CHECK_CONVERGENCE(I_ORDER, I_TOTAL, CONVERGED, ...)
   ! Tests convergence criteria

**Data Structures:**

.. code-block:: fortran

   ! Radiance field: I(level, angle, Fourier mode, Stokes)
   REAL*8 :: RADIANCE(NZ, NMU, NFOURIER, 4)
   
   ! Source function
   REAL*8 :: SOURCE(NZ, NMU, NFOURIER, 4)
   
   ! Phase matrix
   REAL*8 :: PHASE_MATRIX(NMU, NMU, NFOURIER, 4, 4)

**Control Parameters:**

.. code-block:: fortran

   INTEGER :: IGMAX           ! Maximum scattering orders (default 100)
   REAL*8  :: CONV_THRESHOLD  ! Convergence threshold (default 0.001)
   INTEGER :: NFOURIER        ! Number of Fourier modes
   INTEGER :: NLEVELS         ! Number of vertical levels

Performance Optimization
------------------------

Computational Bottlenecks
~~~~~~~~~~~~~~~~~~~~~~~~~

**Time Distribution:**

1. **Surface matrix computation**: 30-50% (one-time cost)
2. **Source function**: 20-30% per order
3. **RTE integration**: 10-20% per order
4. **Boundary conditions**: 5-10% per order
5. **Overhead**: 5-10%

**Scaling:**

* With optical thickness: ~O(τ) orders required
* With angular resolution: O(N_μ²)
* With vertical resolution: O(N_z²)

Optimization Strategies
~~~~~~~~~~~~~~~~~~~~~~~

**1. Compiler Optimization:**

.. code-block:: makefile

   FFLAGS = -O3 -march=native -funroll-loops

**Performance gain:** 20-30%

**2. Angular Resolution:**

* Minimum adequate resolution (N_μ = 20-40)
* Higher for strongly peaked phase functions

**Trade-off:** Accuracy vs. speed

**3. Fourier Truncation:**

* Aggressive truncation (ε_F = 0.001 vs. 0.0001)
* Early termination of unnecessary modes

**Speedup:** 10-30%

**4. Vertical Resolution:**

* Coarser grid in optically thin regions
* Finer near interfaces and gradients

**5. Parallelization:**

Potential parallelization:

* Fourier modes (independent)
* Wavelengths (independent)
* Multiple geometries (independent)

**Implementation:** OpenMP or MPI

**6. Pre-computation:**

* Surface matrices (reuse for multiple runs)
* Phase matrices (store for wavelength series)
* Optical property tables

Memory Management
~~~~~~~~~~~~~~~~~

**Storage Requirements:**

.. math::

   Memory \approx N_z \times N_\mu \times N_m \times 4 \times 8 \text{ bytes}

**Example:**

* N_z = 100 levels
* N_μ = 40 angles
* N_m = 20 Fourier modes
* 4 Stokes parameters
* 8 bytes per double

Memory ≈ 100 × 40 × 20 × 4 × 8 = 2.56 MB (manageable)

**Large Simulations:**

For very fine resolution:

* Store on disk between orders
* Use sparse storage for Fourier modes
* Compress/decompress as needed

Output and Diagnostics
----------------------

Convergence Monitoring
~~~~~~~~~~~~~~~~~~~~~~

**SOS_LOG.txt Output:**

::

    ==========================================
    Successive Orders Calculation
    ==========================================
    
    Configuration:
      Maximum orders: 100
      Convergence threshold: 0.001
      Fourier modes: 20
      Gauss angles: 40
      
    Iteration Progress:
    
    Order  1: Relative change = 1.000000 (initial)
           Max location: z=0.0m, theta=30.0deg
           CPU time = 2.34 seconds
    
    Order  2: Relative change = 0.234567
           Max location: z=0.0m, theta=30.0deg
           CPU time = 2.56 seconds
    
    Order  3: Relative change = 0.056789
           Max location: z=0.0m, theta=30.0deg
           CPU time = 2.61 seconds
    
    [...]
    
    Order  8: Relative change = 0.000789 ** CONVERGED **
           Max location: z=0.0m, theta=30.0deg
           CPU time = 2.58 seconds
    
    Total CPU time: 20.45 seconds
    Total orders computed: 8
    Convergence status: SUCCESS

**Diagnostic Plots:**

Create plots of:

* Relative change vs. order number
* Cumulative radiance vs. order
* Contribution by Fourier mode

Radiance Field Output
~~~~~~~~~~~~~~~~~~~~~

**Binary File (LUM_SF.bin):**

Contains complete Fourier series for all levels and angles:

* I^m(z, μ) for each mode m
* All four Stokes parameters
* Can reconstruct full I(z, μ, φ)

**ASCII File (LUM_vsVZA.txt):**

Radiance vs. viewing zenith angle at specified level:

::

    # Viewing_Zenith_Angle(deg)  I  Q  U  V  DoLP
    0.0     0.0124    0.0002   0.0001  0.0000  0.015
    10.0    0.0129    0.0003   0.0001  0.0000  0.018
    20.0    0.0141    0.0005   0.0002  0.0000  0.024
    [...]

**Profile File (LUM_vsZ.txt):**

Radiance vs. depth/altitude for specified direction:

::

    # Depth(m)  I_down  Q_down  U_down  I_up  Q_up  U_up
    0.0        0.850    -0.120   0.003   0.012  0.002  0.000
    -5.0       0.780    -0.110   0.003   0.009  0.001  0.000
    -10.0      0.715    -0.100   0.002   0.007  0.001  0.000
    [...]

Validation and Testing
----------------------

Benchmark Problems
~~~~~~~~~~~~~~~~~~

**1. Rayleigh Scattering:**

* Pure molecular atmosphere
* Exact solutions available
* Test polarization treatment

**2. Isotropic Scattering:**

* Simple phase function
* Analytical solutions for thin media
* Validate integration accuracy

**3. Atmosphere-Ocean Interface:**

* Flat surface: Compare with analytical Fresnel
* Rough surface: Compare with Cox & Munk validation data

**4. Black Surface:**

* Ocean with no upwelling
* Test atmospheric radiative transfer alone

Inter-comparison Studies
~~~~~~~~~~~~~~~~~~~~~~~~

Compare OSOAA results with other radiative transfer codes:

* **VLIDORT**: Vector linearized discrete ordinate code
* **DISORT**: Discrete ordinate method
* **6S**: Second simulation of satellite signal
* **Hydrolight**: Underwater radiative transfer
* **Monte Carlo**: Statistical photon tracking

**Agreement:**

Typically within 1-5% for well-posed problems.

**Differences:**

* Numerical methods (discrete ordinate vs. Monte Carlo)
* Treatment of forward peak
* Surface models
* Angular resolution

Uncertainty Analysis
~~~~~~~~~~~~~~~~~~~~

**Sources of Uncertainty:**

1. **Angular discretization**: N_μ choice
   
   * Insufficient angles: 5-10% errors
   * Adequate resolution: <1% error

2. **Vertical discretization**: Layer thickness
   
   * Coarse layers: 2-5% errors
   * Fine layers: <1% error

3. **Fourier truncation**: Mode cutoff
   
   * Too few modes: 1-3% errors
   * Adequate modes: <0.5% error

4. **Convergence threshold**: ε choice
   
   * Loose convergence: 0.1-1% errors
   * Tight convergence: <0.1% error

5. **Truncation of forward peak**:
   
   * Impacts strongly peaked phase functions
   * Delta-Eddington: typically <2% error

**Total Uncertainty:**

Well-configured OSOAA: 2-5% radiometric accuracy

Best Practices
--------------

Configuration Guidelines
~~~~~~~~~~~~~~~~~~~~~~~~

**Angular Resolution:**

* **Minimum**: 20 Gauss angles (testing)
* **Standard**: 40-50 angles (production)
* **High accuracy**: 60-80 angles (validation)

**Fourier Modes:**

* Automatically determined by truncation criterion
* Typical: 10-20 modes for atmosphere-ocean
* More for rough surface with high winds

**Convergence:**

* Standard threshold: 0.001 (0.1%)
* High accuracy: 0.0001 (0.01%)
* Maximum orders: 100-150

**Vertical Resolution:**

* Euphotic zone: Δz = 1-5 m
* Deeper ocean: Δz = 5-20 m
* Atmosphere: Δz ~ 1-2 km

Computational Efficiency
~~~~~~~~~~~~~~~~~~~~~~~~

**For Parameter Studies:**

1. Pre-compute surface matrices once
2. Use moderate angular resolution
3. Standard convergence (ε = 0.001)
4. Reuse optical property tables

**For High-Accuracy Validation:**

1. High angular resolution (N_μ ≥ 60)
2. Tight convergence (ε = 0.0001)
3. Fine vertical grid
4. Check Fourier convergence

**For Operational Applications:**

1. Balance accuracy and speed
2. Validate configuration on subset
3. Use lookup tables if repeated geometries
4. Consider parallel execution

Troubleshooting
~~~~~~~~~~~~~~~

**Problem: Slow Convergence**

* **Cause**: High optical thickness, conservative scattering
* **Solution**: Increase IGMAX, check optical properties, consider geometric series acceleration

**Problem: Oscillating Convergence**

* **Cause**: Insufficient angular resolution, numerical instability
* **Solution**: Increase N_μ, check phase function truncation

**Problem: Wrong Radiance Magnitude**

* **Cause**: Incorrect optical properties, surface matrices, solar flux
* **Solution**: Validate IOPs, check units, verify surface calculation

**Problem: Strange Angular Patterns**

* **Cause**: Insufficient Fourier modes, angular aliasing
* **Solution**: Increase mode count, check truncation criterion

**Problem: Polarization Errors**

* **Cause**: Rotation angles, Mueller matrix errors, insufficient Fourier modes
* **Solution**: Validate phase matrices, check surface Mueller matrices, increase modes

See Also
--------

* :ref:`radiative_transfer` - Theoretical background
* :ref:`atmosphere_model` - Atmospheric scattering
* :ref:`ocean_model` - Ocean scattering
* :ref:`surface_interface` - Boundary conditions
* :ref:`parameter_reference` - Control parameters (SOS.IGMAX, etc.)
* :ref:`bibliography` - References (Lenoble 1993, Deuzé et al. 1989)

References
----------

**Primary References:**

* Lenoble, J. (ed.) (1993). *Atmospheric Radiative Transfer*. A. Deepak Publishing. (Standard reference on successive orders method)

* Chami, M. et al. (2015). "OSOAA: a vector radiative transfer model of coupled atmosphere-ocean system for a rough sea surface." *Optics Express* 23(21): 27829-27852. (OSOAA implementation)

**Additional Reading:**

* Deuzé, J. L. et al. (2000). "Estimate of the aerosol properties over the ocean with POLDER." *JGR* 105: 15329-15346. (Application of successive orders)

* Chandrasekhar, S. (1960). *Radiative Transfer*. Dover Publications. (Classic theoretical foundation)

* van de Hulst, H. C. (1980). *Multiple Light Scattering*. Academic Press. (Multiple scattering theory)

* Hovenier, J. W. et al. (2004). *Transfer of Polarized Light in Planetary Atmospheres*. Springer. (Polarized radiative transfer)
