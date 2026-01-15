Algorithms
==========

This section provides detailed descriptions of the key algorithms implemented in OSOAA.

Successive Orders of Scattering
-------------------------------

Overview
~~~~~~~~

The successive orders of scattering (SOS) method is the core algorithm in OSOAA. It solves the vector radiative transfer equation by decomposing the total radiance field into contributions from different scattering orders.

Mathematical Foundation
~~~~~~~~~~~~~~~~~~~~~~~

The total radiance field is expressed as:

.. math::

   I_{total}(\vec{r}, \vec{\Omega}) = \sum_{n=0}^{\infty} I^{(n)}(\vec{r}, \vec{\Omega})

Where:

* :math:`I^{(n)}` is the contribution from the :math:`n`-th scattering order
* :math:`\vec{r}` is the position vector
* :math:`\vec{\Omega}` is the direction vector

Order 0: Direct Transmission
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The zero-order term represents direct solar radiation attenuated through the atmosphere-ocean system:

.. math::

   I^{(0)}(\vec{r}, \vec{\Omega}) = I_0 \delta(\vec{\Omega} - \vec{\Omega}_0) \exp\left(-\int_0^r \beta_{ext}(s) ds\right)

Where:

* :math:`I_0` is the solar irradiance
* :math:`\vec{\Omega}_0` is the solar direction
* :math:`\beta_{ext}` is the extinction coefficient
* :math:`\delta` is the Dirac delta function

Order n ≥ 1: Multiple Scattering
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For scattering order :math:`n \geq 1`:

.. math::

   I^{(n)}(\vec{r}, \vec{\Omega}) = \int_V \int_{4\pi} \frac{\beta_{sca}(\vec{r}')}{4\pi} 
   \mathbf{P}(\vec{r}', \vec{\Omega}' \rightarrow \vec{\Omega}) I^{(n-1)}(\vec{r}', \vec{\Omega}') 
   \exp(-\tau_{r',r}) d\Omega' dV'

Where:

* :math:`\beta_{sca}` is the scattering coefficient
* :math:`\mathbf{P}` is the phase matrix (4×4 for polarization)
* :math:`\tau_{r',r}` is the optical depth between points :math:`r'` and :math:`r`

Algorithm Implementation
~~~~~~~~~~~~~~~~~~~~~~~~

**Pseudocode**:

.. code-block:: text

   Initialize:
      I_total = 0
      I_prev = 0
      
   // Order 0: Direct transmission
   I_0 = ComputeDirectTransmission()
   I_total = I_0
   I_prev = I_0
   
   // Iterate over scattering orders
   for n = 1 to MAX_ORDERS:
      
      // Compute n-th order contribution
      I_n = ComputeScatteringOrder(n, I_prev)
      
      // Accumulate
      I_total = I_total + I_n
      
      // Check convergence
      rel_change = |I_n| / |I_total|
      
      if rel_change < THRESHOLD:
         convergence = TRUE
         break
      
      I_prev = I_n
   
   return I_total, n, convergence

**Convergence Criteria**:

The iteration stops when:

.. math::

   \frac{|I^{(n)}|}{|I_{total}|} < \epsilon

Typical values: :math:`\epsilon = 0.001` to 0.0001

**Implementation Details**:

Located in ``src/OSOAA_SOS.F`` and ``src/OSOAA_SOS_CORE.F``:

.. code-block:: fortran

   SUBROUTINE SOS_ITERATE_ORDER(ORDER, RADIANCE_IN, RADIANCE_OUT,
  &                              CONVERGED, ...)
   ! Computes the n-th order of scattering
   ! Uses previous order as source function

Optimization Techniques
~~~~~~~~~~~~~~~~~~~~~~~

1. **Geometric Series Acceleration**

   For optically thick media, higher orders can be approximated:
   
   .. math::
   
      \sum_{n=N}^{\infty} I^{(n)} \approx \frac{I^{(N)}}{1 - r}
   
   Where :math:`r` is the estimated geometric ratio.

2. **Fourier Decomposition in Azimuth**

   The radiance is decomposed as:
   
   .. math::
   
      I(\theta, \phi) = \sum_{m=0}^{M} I_m(\theta) \cos[m(\phi - \phi_0)]
   
   This reduces 3D problem to a series of 2D problems.

3. **Truncation of Forward Peak**

   For strongly forward-scattering phase functions, the forward peak is truncated 
   and treated with delta-Eddington approximation.

Mie Scattering Calculations
---------------------------

Purpose
~~~~~~~

Compute scattering properties of spherical particles (aerosols and hydrosols) 
using Mie theory.

Mie Coefficients
~~~~~~~~~~~~~~~~

The Mie solution expands electromagnetic fields in series of vector spherical harmonics:

.. math::

   a_n = \frac{\psi_n(mx)\psi'_n(x) - m\psi'_n(mx)\psi_n(x)}
              {\psi_n(mx)\xi'_n(x) - m\psi'_n(mx)\xi_n(x)}

.. math::

   b_n = \frac{m\psi_n(mx)\psi'_n(x) - \psi'_n(mx)\psi_n(x)}
              {m\psi_n(mx)\xi'_n(x) - \psi'_n(mx)\xi_n(x)}

Where:

* :math:`x = 2\pi r/\lambda` is the size parameter
* :math:`m = n_{particle}/n_{medium}` is the relative refractive index
* :math:`\psi_n`, :math:`\xi_n` are Riccati-Bessel functions
* :math:`\psi'_n`, :math:`\xi'_n` are their derivatives

Number of Terms
^^^^^^^^^^^^^^^

The series is truncated at:

.. math::

   n_{max} = x + 4x^{1/3} + 2

This ensures convergence to machine precision for most cases.

Scattering Cross Sections
~~~~~~~~~~~~~~~~~~~~~~~~~

**Scattering cross section**:

.. math::

   C_{sca} = \frac{2\pi}{k^2} \sum_{n=1}^{n_{max}} (2n+1)(|a_n|^2 + |b_n|^2)

**Extinction cross section**:

.. math::

   C_{ext} = \frac{2\pi}{k^2} \sum_{n=1}^{n_{max}} (2n+1)\text{Re}(a_n + b_n)

**Absorption cross section**:

.. math::

   C_{abs} = C_{ext} - C_{sca}

Where :math:`k = 2\pi/\lambda` is the wave number.

Phase Function
~~~~~~~~~~~~~~

The scattering phase function is computed from angular functions:

.. math::

   p(\cos\Theta) = \frac{1}{2k^2C_{sca}}(|S_1(\Theta)|^2 + |S_2(\Theta)|^2)

Where the scattering amplitude functions are:

.. math::

   S_1(\Theta) = \sum_{n=1}^{n_{max}} \frac{2n+1}{n(n+1)}(a_n \pi_n + b_n \tau_n)

.. math::

   S_2(\Theta) = \sum_{n=1}^{n_{max}} \frac{2n+1}{n(n+1)}(a_n \tau_n + b_n \pi_n)

With angular functions:

.. math::

   \pi_n(\cos\Theta) = \frac{P_n^1(\cos\Theta)}{\sin\Theta}

.. math::

   \tau_n(\cos\Theta) = \frac{dP_n^1(\cos\Theta)}{d\Theta}

Where :math:`P_n^1` are associated Legendre polynomials.

Phase Matrix Elements
~~~~~~~~~~~~~~~~~~~~~

The complete Mueller matrix for single scattering:

.. math::

   \mathbf{M}(\Theta) = \frac{1}{k^2 r^2} \begin{pmatrix}
   \frac{1}{2}(|S_2|^2 + |S_1|^2) & \frac{1}{2}(|S_2|^2 - |S_1|^2) & 0 & 0 \\
   \frac{1}{2}(|S_2|^2 - |S_1|^2) & \frac{1}{2}(|S_2|^2 + |S_1|^2) & 0 & 0 \\
   0 & 0 & \text{Re}(S_2 S_1^*) & \text{Im}(S_2 S_1^*) \\
   0 & 0 & -\text{Im}(S_2 S_1^*) & \text{Re}(S_2 S_1^*)
   \end{pmatrix}

Implementation
~~~~~~~~~~~~~~

Located in ``src/OSOAA_MIE.F``:

.. code-block:: fortran

   SUBROUTINE MIE_COEFFICIENTS(SIZE_PARAM, REF_INDEX, NMAX, AN, BN)
   ! Computes Mie coefficients a_n and b_n
   
   SUBROUTINE MIE_CROSS_SECTIONS(SIZE_PARAM, REF_INDEX, AN, BN, 
  &                                NMAX, C_SCA, C_EXT, C_ABS)
   ! Computes scattering, extinction, absorption cross sections
   
   SUBROUTINE MIE_PHASE_FUNCTION(ANGLES, NANG, AN, BN, NSTOP,
  &                               PHASE_FUNC, PHASE_MATRIX)
   ! Computes phase function and Mueller matrix elements

Size Distribution Integration
-----------------------------

Polydisperse Particles
~~~~~~~~~~~~~~~~~~~~~~

Real aerosols and hydrosols have distributions of particle sizes. The bulk 
optical properties are obtained by integrating over the size distribution:

.. math::

   \beta_{ext}(\lambda) = \int_0^{\infty} C_{ext}(r, \lambda) n(r) dr

Where :math:`n(r)` is the particle number density per unit size interval.

Log-Normal Distribution
~~~~~~~~~~~~~~~~~~~~~~~

Most commonly used size distribution:

.. math::

   n(r) = \frac{N}{\sqrt{2\pi}\sigma r} \exp\left[-\frac{(\ln r - \ln r_0)^2}{2\sigma^2}\right]

Where:

* :math:`N` is the total number density
* :math:`r_0` is the median radius
* :math:`\sigma` is the standard deviation of :math:`\ln r`

Junge Power Law
~~~~~~~~~~~~~~~

Alternative distribution for aerosols:

.. math::

   n(r) = Cr^{-\nu}

Where:

* :math:`C` is a normalization constant
* :math:`\nu` is the power law exponent (typically 3-4)

Numerical Integration
~~~~~~~~~~~~~~~~~~~~~

**Algorithm**:

1. Convert to logarithmic radius grid:
   
   .. math::
   
      x = \ln r, \quad dx = dr/r

2. Use Gauss-Legendre quadrature:
   
   .. math::
   
      \int_0^{\infty} f(r) n(r) dr \approx \sum_{i=1}^{N_q} w_i f(r_i) n(r_i) r_i

3. Choose appropriate radius range: :math:`r_{min}` to :math:`r_{max}`

**Implementation**:

.. code-block:: fortran

   SUBROUTINE INTEGRATE_SIZE_DISTRIBUTION(N_FUNC, SIZE_DIST,
  &                                        CROSS_SECTIONS, ...)
   ! Integrates single-particle properties over size distribution

Typical parameters:

* :math:`N_q = 40-80` quadrature points
* :math:`r_{min} = 0.01` µm, :math:`r_{max} = 100` µm

Cox & Munk Sea Surface Model
----------------------------

Wave Slope Statistics
~~~~~~~~~~~~~~~~~~~~~

The probability density function of wave slopes follows a bivariate Gaussian:

.. math::

   P(Z_x, Z_y) = \frac{1}{2\pi\sigma_c\sigma_u} 
   \exp\left[-\frac{1}{2}\left(\frac{Z_x^2}{\sigma_c^2} + \frac{Z_y^2}{\sigma_u^2}\right)\right]

Where:

* :math:`Z_x`, :math:`Z_y` are cross-wind and up-wind slope components
* :math:`\sigma_c^2 = 0.003 + 0.00512 \cdot U` (cross-wind variance)
* :math:`\sigma_u^2 = 0.00316 \cdot U` (up-wind variance)
* :math:`U` is the wind speed at 10 m height (m/s)

Reflection/Transmission Calculation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For each geometry (incident direction :math:`\vec{\Omega}_i`, transmitted direction :math:`\vec{\Omega}_t`):

1. **Find wave normal**: Solve for normal vector :math:`\vec{n}` satisfying Snell's law:
   
   .. math::
   
      n_{air}\sin\theta_i = n_{water}\sin\theta_t

2. **Compute Fresnel coefficients**: For parallel and perpendicular polarizations:
   
   .. math::
   
      R_{\parallel} = \left|\frac{n_2\cos\theta_i - n_1\cos\theta_t}{n_2\cos\theta_i + n_1\cos\theta_t}\right|^2
   
   .. math::
   
      R_{\perp} = \left|\frac{n_1\cos\theta_i - n_2\cos\theta_t}{n_1\cos\theta_i + n_2\cos\theta_t}\right|^2

3. **Weight by probability**: Multiply by :math:`P(Z_x, Z_y)`

4. **Integrate over all wave orientations**:
   
   .. math::
   
      R(\theta_i, \theta_t, \phi) = \int_{-\infty}^{\infty} \int_{-\infty}^{\infty} 
      R_{Fresnel}(\vec{n}) P(Z_x, Z_y) dZ_x dZ_y

Shadowing and Masking
~~~~~~~~~~~~~~~~~~~~~

Geometric shadowing reduces reflectance at grazing angles. The shadowing function :math:`S` 
is computed from wave slope statistics and geometry.

.. math::

   R_{effective} = R \cdot S(\theta_i, \theta_t)

Implementation
~~~~~~~~~~~~~~

Located in ``src/OSOAA_SURF_MATRICES.F``:

.. code-block:: fortran

   SUBROUTINE INTEGRATE_WAVE_FACETS(THETA_I, THETA_T, PHI,
  &                                  SIGMA_C, SIGMA_U,
  &                                  REFL_MATRIX, TRANS_MATRIX)

The integration uses:

* 1024 azimuthal angles (``CTE_PH_NU``)
* Dichotomy method to find valid wave normals
* Threshold ``CTE_THRESHOLD_GMAX = 1.0e-40`` for minimum probability

Angular Discretization
----------------------

Gauss-Legendre Quadrature
~~~~~~~~~~~~~~~~~~~~~~~~~~

For accurate integration of the radiative transfer equation, angular integrals are 
computed using Gauss-Legendre quadrature.

**Quadrature points** :math:`\mu_i` and **weights** :math:`w_i` satisfy:

.. math::

   \int_{-1}^{1} f(\mu) d\mu \approx \sum_{i=1}^{N} w_i f(\mu_i)

The points are zeros of the Legendre polynomial :math:`P_N(\mu)`, and weights are:

.. math::

   w_i = \frac{2}{(1-\mu_i^2)[P'_N(\mu_i)]^2}

Algorithm
~~~~~~~~~

**Recursive calculation** of Legendre polynomials:

.. math::

   P_0(\mu) = 1

.. math::

   P_1(\mu) = \mu

.. math::

   (n+1)P_{n+1}(\mu) = (2n+1)\mu P_n(\mu) - n P_{n-1}(\mu)

**Newton-Raphson iteration** to find zeros:

.. math::

   \mu_{i+1} = \mu_i - \frac{P_N(\mu_i)}{P'_N(\mu_i)}

Implementation
~~~~~~~~~~~~~~

Located in ``src/OSOAA_ANGLES.F``:

.. code-block:: fortran

   SUBROUTINE ANGLES_GAUSS_LEGENDRE(N, X, W)
   ! Computes N Gauss-Legendre nodes X and weights W

Typical values: :math:`N = 40-80` for radiance calculations, :math:`N = 80-200` for 
phase function integration.

Coordinate Transformations
--------------------------

Stokes Vector Rotation
~~~~~~~~~~~~~~~~~~~~~~

When light propagates through different reference planes, the Stokes vector must be rotated.

**Rotation matrix**:

.. math::

   \mathbf{L}(\alpha) = \begin{pmatrix}
   1 & 0 & 0 & 0 \\
   0 & \cos 2\alpha & \sin 2\alpha & 0 \\
   0 & -\sin 2\alpha & \cos 2\alpha & 0 \\
   0 & 0 & 0 & 1
   \end{pmatrix}

Where :math:`\alpha` is the rotation angle between the two planes.

**Transformation**:

.. math::

   \vec{S}_{new} = \mathbf{L}(\alpha) \vec{S}_{old}

Rotation Angle Calculation
~~~~~~~~~~~~~~~~~~~~~~~~~~

Given two directions :math:`(\theta_1, \phi_1)` and :math:`(\theta_2, \phi_2)`, 
the rotation angle is computed using spherical trigonometry:

.. math::

   \cos\alpha = \frac{\cos\theta_2 - \cos\theta_1\cos\Theta}{\sin\theta_1\sin\Theta}

Where :math:`\Theta` is the scattering angle between the two directions.

Implementation
~~~~~~~~~~~~~~

Located in ``src/OSOAA_TRPHI.F``:

.. code-block:: fortran

   SUBROUTINE ROTATION_ANGLE(THETA1, PHI1, THETA2, PHI2, ALPHA)
   
   SUBROUTINE TRANSFORM_STOKES(STOKES_IN, ALPHA, STOKES_OUT)

Numerical Stability
-------------------

Several techniques ensure numerical stability:

Exponential Attenuation
~~~~~~~~~~~~~~~~~~~~~~~

For large optical depths, direct computation of :math:`\exp(-\tau)` can underflow. 
The code uses:

* Threshold checks: if :math:`\tau > \tau_{max}`, set :math:`\exp(-\tau) = 0`
* Logarithmic representation for intermediate calculations

Phase Function Normalization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The phase function is normalized to ensure:

.. math::

   \frac{1}{2}\int_{-1}^{1} P(\mu) d\mu = 1

Truncation of Phase Function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Strongly forward-scattering phase functions are truncated:

* For :math:`\mu > \mu_{truncate}` (e.g., 0.94), use delta-Eddington approximation
* Preserve total scattering and asymmetry parameter

Convergence Acceleration
~~~~~~~~~~~~~~~~~~~~~~~~

Multiple thresholds control convergence:

.. code-block:: c

   #define CTE_PH_SEUIL_CV_SG  0.005    // Geometric series
   #define CTE_PH_SEUIL_SUMDIF  0.001   // Cumulative difference
   #define CTE_PH_SEUIL_SF  0.0002      // Fourier series

Computational Complexity
------------------------

Time Complexity
~~~~~~~~~~~~~~~

For a simulation with:

* :math:`N_\theta` angular points
* :math:`N_z` vertical levels  
* :math:`N_{orders}` scattering orders

**Total complexity**: :math:`O(N_{orders} \times N_\theta^2 \times N_z^2)`

**Breakdown**:

* Mie calculations: :math:`O(N_r \times n_{max}^2)` where :math:`N_r` is number of radii
* Surface matrices: :math:`O(N_\theta^2 \times N_\phi)` where :math:`N_\phi = 1024`
* Each scattering order: :math:`O(N_\theta^2 \times N_z^2)`

Space Complexity
~~~~~~~~~~~~~~~~

**Memory usage**: :math:`O(N_\theta \times N_z \times 4)` for Stokes vectors

Typical allocation:

* Small: 20 angles, 50 levels → ~100 MB
* Medium: 50 angles, 100 levels → ~500 MB
* Large: 100 angles, 200 levels → ~2 GB

Parallelization Opportunities
-----------------------------

The code has several parallelizable components:

1. **Multiple wavelengths**: Independent calculations
2. **Multiple viewing geometries**: Independent calculations  
3. **Scattering orders**: Some dependencies, but parallelizable within each order
4. **Fourier terms**: Independent in azimuth decomposition

Current implementation is serial, but OpenMP directives could be added for:

.. code-block:: fortran

   !$OMP PARALLEL DO
   DO i = 1, N_angles
      ! Compute radiance for angle i
   END DO
   !$OMP END PARALLEL DO

Next Steps
----------

* :doc:`code_structure` - Code organization
* :doc:`performance` - Optimization and benchmarks
* :doc:`../science/radiative_transfer` - Theoretical background

See Also
--------

* :doc:`fortran_modules` - Module-level documentation
* :doc:`../examples/basic_simulation` - Example applications
