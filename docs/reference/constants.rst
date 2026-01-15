.. _constants:

Physical and Numerical Constants
================================

This page documents the physical constants and numerical parameters defined in OSOAA.

.. contents:: Contents
   :local:
   :depth: 2

Overview
--------

OSOAA defines constants in the header file ``inc/OSOAA.h`` using C preprocessor ``#define`` statements. These constants control:

- Physical properties (depolarization factors, refractive indices)
- Numerical thresholds (convergence criteria, truncation limits)
- Array dimensions (maximum angles, scattering orders)
- Default values (file names, parameter settings)

Physical Constants
------------------

Molecular Depolarization Factors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CTE_MDF_AIR
^^^^^^^^^^^

**Molecular depolarization factor for air**

:Value: 0.0279
:Units: Dimensionless
:File: ``OSOAA_SOS_CORE.F``

Depolarization factor :math:`\\delta_{air}` accounts for molecular anisotropy in Rayleigh scattering by air molecules.

**Cabannes line factor for air:**

.. math::

   \\rho_{air} = \\frac{6(1-\\delta_{air})}{3+7\\delta_{air}} = \\frac{6(1-0.0279)}{3+7(0.0279)} \\approx 1.8134

CTE_MDF_SEA
^^^^^^^^^^^

**Molecular depolarization factor for seawater**

:Value: 0.0906
:Units: Dimensionless
:File: ``OSOAA_SOS_CORE.F``

Depolarization factor :math:`\\delta_{sea}` for Rayleigh scattering by water molecules.

**Cabannes line factor for seawater:**

.. math::

   \\rho_{sea} = \\frac{6(1-\\delta_{sea})}{3+7\\delta_{sea}} = \\frac{6(1-0.0906)}{3+7(0.0906)} \\approx 1.5805

**Physical interpretation:** The depolarization factor quantifies how much linearly polarized light becomes depolarized during molecular scattering. Higher values indicate more depolarization.

Solar Radiation
~~~~~~~~~~~~~~~

CTE_SOLAR_DISC_SOLID_ANGLE
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Solar disc solid angle**

:Value: 6.8 × 10⁻⁵
:Units: steradians (sr)
:File: ``OSOAA_TRPHI.F``

Solid angle subtended by the solar disc at mean Earth-Sun distance.

**Calculation:**

.. math::

   \\Omega_{\\odot} = \\pi \\left(\\frac{R_{\\odot}}{d_{ES}}\\right)^2

Where:

- :math:`R_{\\odot}` = 6.96 × 10⁸ m (solar radius)
- :math:`d_{ES}` = 1.496 × 10¹¹ m (mean Earth-Sun distance)

**Usage:** Converting between radiance and irradiance for direct solar beam.

Refractive Indices
~~~~~~~~~~~~~~~~~~

Default seawater refractive index
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Value: ~1.34 (wavelength and temperature dependent)
:Usage: Sea surface interface calculations

**Typical values:**

- 550 nm, 20°C, 35 PSU: n = 1.340
- 400 nm: n ≈ 1.343
- 700 nm: n ≈ 1.338

**Temperature dependence:** dn/dT ≈ -1 × 10⁻⁴ K⁻¹

**Salinity dependence:** dn/dS ≈ 1.8 × 10⁻⁴ PSU⁻¹

Wavelength Range
~~~~~~~~~~~~~~~~

CTE_WAMIN
^^^^^^^^^

**Minimum wavelength for calculations**

:Value: 0.299 (299 nm)
:Units: micrometers
:File: ``OSOAA_MAIN.F``

Lower limit for wavelength in radiative transfer calculations. Corresponds to UV-B range.

**Valid wavelength range:** 299-1000 nm

- 299-400 nm: Ultraviolet (UV)
- 400-700 nm: Visible spectrum
- 700-1000 nm: Near-infrared (NIR)

Numerical Parameters
--------------------

Convergence Thresholds
~~~~~~~~~~~~~~~~~~~~~~

CTE_PH_SEUIL_CV_SG
^^^^^^^^^^^^^^^^^^

**Geometric series convergence threshold**

:Value: 0.005
:Units: Dimensionless (relative error)
:File: ``OSOAA_SOS_CORE.F``

Threshold to test convergence of geometric series in successive orders calculation.

**Convergence criterion:**

.. math::

   \\frac{|I^{(n)} - I^{(n-1)}|}{I^{(n-1)}} < 0.005

CTE_PH_SEUIL_SUMDIF
^^^^^^^^^^^^^^^^^^^

**Cumulative scattering stop threshold**

:Value: 0.001
:Units: Dimensionless (relative contribution)
:File: ``OSOAA_SOS_CORE.F``

Threshold to stop cumulative scattering when contribution becomes negligible.

**Stop criterion:**

.. math::

   \\frac{I^{(n)}}{\\sum_{k=0}^{n-1} I^{(k)}} < 0.001

CTE_PH_SEUIL_SF
^^^^^^^^^^^^^^^

**Fourier series truncation threshold**

:Value: 0.0002
:Units: Dimensionless
:File: ``OSOAA_SOS_CORE.F``

Threshold for stopping Fourier series expansion in azimuth.

**Truncation criterion:**

.. math::

   \\frac{|I_m|}{I_0} < 0.0002

Where :math:`I_m` is the m-th Fourier component.

Rotation Angle Thresholds
~~~~~~~~~~~~~~~~~~~~~~~~~

CTE_SEUIL_Z
^^^^^^^^^^^

**Rotation angle calculation threshold**

:Value: 0.001
:Units: Dimensionless
:File: ``OSOAA_TRPHI.F``

Threshold for calculating rotation angles in Stokes vector transformations.

CTE_SEUIL_EPSILON
^^^^^^^^^^^^^^^^^

**Small angle threshold**

:Value: 0.00001
:Units: Dimensionless
:File: ``OSOAA_TRPHI.F``

Threshold for treating angles as effectively zero to avoid numerical instability.

CTE_THRESHOLD_Q_U_NULL
^^^^^^^^^^^^^^^^^^^^^^

**Stokes parameter Q, U null threshold**

:Value: 1 × 10⁻⁹⁹
:Units: Dimensionless
:File: ``OSOAA_TRPHI.F``

Value below which Stokes parameters Q and U are set to zero to avoid numerical issues.

Surface Interface Thresholds
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CTE_THRESHOLD_GMAX
^^^^^^^^^^^^^^^^^^

**Maximum wave probability threshold**

:Value: 1 × 10⁻⁴⁰
:Units: Dimensionless
:File: ``OSOAA_SURF_MATRICES.F``

Maximum value of wave probability in Cox & Munk surface model.

CTE_THRESHOLD_DICHO
^^^^^^^^^^^^^^^^^^^

**Dichotomy threshold for incidence angles**

:Value: 1 × 10⁻¹⁰
:Units: Dimensionless
:File: ``OSOAA_SURF_MATRICES.F``

Convergence threshold for iterative solution of incidence angles at rough surface.

CTE_THRESHOLD_COSTHETAN
^^^^^^^^^^^^^^^^^^^^^^^

**Minimum cosine of wave normal angle**

:Value: 0.001
:Units: Dimensionless
:File: ``OSOAA_SURF_MATRICES.F``

Minimum value of cos(θₙ) for wave normal vector in air-sea coupled directions.

CTE_THRESHOLD_GEO_CONFIG
^^^^^^^^^^^^^^^^^^^^^^^^

**Geometric configuration threshold**

:Value: 1 × 10⁻¹⁵
:Units: Dimensionless
:File: ``OSOAA_SURF_MATRICES.F``

Threshold for estimating possible geometric configurations in transmission through surface.

CTE_PH_TEST
^^^^^^^^^^^

**GMIN/GMAX comparison factor**

:Value: 10000
:Units: Dimensionless
:File: ``OSOAA_SURF_MATRICES.F``

Factor used to compare minimum and maximum wave probabilities.

CTE_THRESHOLD_G_SMAX
^^^^^^^^^^^^^^^^^^^^

**Fourier expansion of wave probability threshold**

:Value: 0.0001
:Units: Dimensionless
:File: ``OSOAA_SURF_MATRICES.F``

Threshold for estimating maximum order of Fourier expansion of wave probability function.

Particle Truncation Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CTE_PH_SEUIL_TRONCA
^^^^^^^^^^^^^^^^^^^

**Phase function truncation threshold**

:Value: 0.1
:Units: Dimensionless
:File: ``OSOAA_PARTICLES_RAD.F``

Threshold for truncating forward scattering peak in phase functions.

Aerosol Truncation Angles
^^^^^^^^^^^^^^^^^^^^^^^^^

CTE_AER_MU1_TRONCA
""""""""""""""""""

:Value: 0.8 (corresponds to θ ≈ 36.9°)
:Units: Dimensionless (cos θ)

CTE_AER_MU2_TRONCA
""""""""""""""""""

:Value: 0.94 (corresponds to θ ≈ 20.0°)
:Units: Dimensionless (cos θ)

Angular range for phase function linearization when applying truncation to aerosol scattering.

Hydrosol Truncation Angles
^^^^^^^^^^^^^^^^^^^^^^^^^^

CTE_HYD_MU1_TRONCA
""""""""""""""""""

:Value: 0.85 (corresponds to θ ≈ 31.8°)
:Units: Dimensionless (cos θ)

CTE_HYD_MU2_TRONCA
""""""""""""""""""

:Value: 0.92 (corresponds to θ ≈ 23.1°)
:Units: Dimensionless (cos θ)

Angular range for phase function linearization when applying truncation to hydrosol scattering.

**Purpose:** Truncation removes the forward scattering peak which is difficult to resolve numerically while preserving total scattering.

Default Values
--------------

Scattering Orders
~~~~~~~~~~~~~~~~~

CTE_DEFAULT_IGMAX
^^^^^^^^^^^^^^^^^

**Default maximum number of scattering orders**

:Value: 100
:Units: Dimensionless (iteration count)
:File: ``OSOAA_MAIN.F``

Maximum number of successive orders iterations.

**Typical requirements:**

- Clear conditions: 20-50 orders
- Moderate turbidity: 50-100 orders
- High turbidity: 100-200 orders

Angular Discretization
~~~~~~~~~~~~~~~~~~~~~~

CTE_DEFAULT_NBMU_MIE
^^^^^^^^^^^^^^^^^^^^

**Default number of Gauss angles for Mie calculations**

:Value: 40
:Units: Number of angles (positive hemisphere)
:File: ``OSOAA_ANGLES.F``

CTE_DEFAULT_NBMU_LUM
^^^^^^^^^^^^^^^^^^^^

**Default number of Gauss angles for radiance calculations**

:Value: 48
:Units: Number of angles (positive hemisphere)
:File: ``OSOAA_ANGLES.F``

Fourier and Legendre Expansion Orders
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CTE_DEFAULT_OS_NB
^^^^^^^^^^^^^^^^^

**Default limit order for Legendre/Fourier expansion (radiance)**

:Value: 80
:Units: Dimensionless
:File: ``OSOAA_ANGLES.F``

Typically: ``CTE_DEFAULT_OS_NB = 2 × CTE_DEFAULT_NBMU_MIE``

CTE_DEFAULT_OS_NS
^^^^^^^^^^^^^^^^^

**Default limit order for Legendre expansion (Fresnel matrices)**

:Value: 96
:Units: Dimensionless
:File: ``OSOAA_ANGLES.F``

Typically: ``CTE_DEFAULT_OS_NS = 2 × CTE_DEFAULT_NBMU_LUM``

CTE_DEFAULT_OS_NM
^^^^^^^^^^^^^^^^^

**Default limit order for Fourier expansion (G function)**

:Value: 176
:Units: Dimensionless
:File: ``OSOAA_ANGLES.F``

Must satisfy: ``CTE_DEFAULT_OS_NM ≥ CTE_DEFAULT_OS_NB + CTE_DEFAULT_OS_NS``

Azimuthal Angles
~~~~~~~~~~~~~~~~

CTE_PH_NU
^^^^^^^^^

**Number of azimuthal angles**

:Value: 1024 (= 2¹⁰)
:Units: Number of angles
:File: ``OSOAA_SURF_MATRICES.F``

Number of azimuthal angles used in Fourier decomposition.

CTE_PH_NQ
^^^^^^^^^

**Exponent for azimuthal angle count**

:Value: 10
:Units: Dimensionless
:File: ``OSOAA_SURF_MATRICES.F``

Relationship: ``CTE_PH_NU = 2^CTE_PH_NQ = 2^10 = 1024``

Array Dimensions
----------------

Maximum Array Sizes
~~~~~~~~~~~~~~~~~~~

CTE_MIE_NBMU_MAX
^^^^^^^^^^^^^^^^

**Maximum number of angles for phase function tables**

:Value: 510
:Units: Number of angles (positive hemisphere)
:Files: ``OSOAA_AEROSOLS.F``, ``OSOAA_ANGLES.F``, ``OSOAA_HYDROSOLS.F``, ``OSOAA_MIE.F``, ``OSOAA_PARTICLES_RAD.F``

Must accommodate: ``CTE_DEFAULT_NBMU_MIE + CTE_NBMAX_USER_ANGLES``

CTE_NBMAX_USER_ANGLES
^^^^^^^^^^^^^^^^^^^^^

**Maximum number of user-defined angles**

:Value: 100
:Units: Number of angles
:File: ``OSOAA_ANGLES.F``

Maximum user-specified viewing angles that can be added to Gauss quadrature angles.

CTE_MIE_DIM
^^^^^^^^^^^

**Size of Mie calculation arrays**

:Value: 10000
:Units: Array dimension
:File: ``OSOAA_MIE.F``

Mie Calculation Limits
~~~~~~~~~~~~~~~~~~~~~~

Maximum Size Parameters for Aerosol Models
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

CTE_ALPHAMAX_WMO_DL
"""""""""""""""""""

:Value: 4000.0 (Dust-like)

CTE_ALPHAMAX_WMO_WS
"""""""""""""""""""

:Value: 50.0 (Water-soluble)

CTE_ALPHAMAX_WMO_OC
"""""""""""""""""""

:Value: 800.0 (Oceanic)

CTE_ALPHAMAX_WMO_SO
"""""""""""""""""""

:Value: 10.0 (Soot)

Maximum size parameter :math:`\\alpha_{max} = 2\\pi r_{max}/\\lambda` for Mie calculations in WMO aerosol models.

CTE_ALPHAMAX_SF_SR
""""""""""""""""""

:Value: 70.0 (Shettle & Fenn, rural)

CTE_ALPHAMAX_SF_SU
""""""""""""""""""

:Value: 90.0 (Shettle & Fenn, urban)

Maximum size parameters for Shettle & Fenn aerosol models.

Particle Size Distribution Limits
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CTE_DEFAULT_AER_JUNGE_RMAX
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Maximum radius for Junge aerosol distribution**

:Value: 50.0
:Units: micrometers (µm)
:File: ``OSOAA_MAIN.F``

CTE_DEFAULT_HYD_JUNGE_RMIN
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Minimum radius for Junge hydrosol distribution**

:Value: 0.01
:Units: micrometers (µm)
:File: ``OSOAA_MAIN.F``

CTE_DEFAULT_HYD_JUNGE_RMAX
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Maximum radius for Junge hydrosol distribution**

:Value: 200.0
:Units: micrometers (µm)
:File: ``OSOAA_MAIN.F``

CTE_JUNGE_SLOPE_COR
^^^^^^^^^^^^^^^^^^^

**Junge model slope correction**

:Value: 0.05
:Units: Dimensionless
:Files: ``OSOAA_AEROSOLS.F``, ``OSOAA_HYDROSOLS.F``

Corrective value for Junge model slope when user specifies the singular value ν = 3.

CTE_COEF_NRMAX
^^^^^^^^^^^^^^

**Size distribution cutoff ratio**

:Value: 0.002
:Units: Dimensionless
:Files: ``OSOAA_AEROSOLS.F``, ``OSOAA_HYDROSOLS.F``

Lowest value of size distribution ratio n(r)/N_max used to estimate limit size parameter for Mie calculations.

Default File Names
------------------

Output Files
~~~~~~~~~~~~

CTE_DEFAULT_FICSOS_RES_BIN
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Binary radiance result file (Fourier series)**

:Value: ``"LUM_SF.bin"``
:File: ``OSOAA_MAIN.F``

CTE_DEFAULT_FICSOS_RES_VS_VZA
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**ASCII radiance vs. viewing zenith angle file**

:Value: ``"LUM_vsVZA.txt"``
:File: ``OSOAA_MAIN.F``

Particle Property Files
~~~~~~~~~~~~~~~~~~~~~~~~

CTE_DEFAULT_FICGRANU_AER
^^^^^^^^^^^^^^^^^^^^^^^^

**Aerosol radiative properties file**

:Value: ``"PM_AER.txt"``
:File: ``OSOAA_MAIN.F``

CTE_DEFAULT_FICGRANU_PHYTO
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Phytoplankton radiative properties file**

:Value: ``"PM_PHYTO.txt"``
:File: ``OSOAA_MAIN.F``

CTE_DEFAULT_FICGRANU_MLP
^^^^^^^^^^^^^^^^^^^^^^^^

**Mineral-like particles radiative properties file**

:Value: ``"PM_MLP.txt"``
:File: ``OSOAA_MAIN.F``

Data Files
~~~~~~~~~~

CTE_AER_DATAWMO
^^^^^^^^^^^^^^^

**WMO particle model data file**

:Value: ``"Data_WMO_cor_2015_12_16"``
:File: ``OSOAA_AEROSOLS.F``

Contains modal radius, standard deviation, volumetric concentration, and refractive index for WMO aerosol models.

CTE_AER_DATASF
^^^^^^^^^^^^^^

**Shettle & Fenn size distribution data**

:Value: ``"Data_SF_cor_2015_12_16"``
:File: ``OSOAA_AEROSOLS.F``

CTE_AER_SR_SF, CTE_AER_LR_SF, CTE_AER_SU_SF, CTE_AER_LU_SF, CTE_AER_OM_SF
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Shettle & Fenn refractive index files**

:Values: Various filenames for different aerosol types (SR=Rural, SU=Urban, etc.)
:File: ``OSOAA_AEROSOLS.F``

CTE_FIC_BOT_SPECTRAL_DATA
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Seabed spectral reflectance data file**

:Value: ``"OSOAA_SEABED_REFLECTANCES.txt"``
:File: ``OSOAA_MAIN.F``

CTE_NB_WA_FIC_BOT
^^^^^^^^^^^^^^^^^

**Number of spectral data points in seabed file**

:Value: 91
:Units: Number of wavelengths
:File: ``OSOAA_MAIN.F``

Polarization Control
--------------------

CTE_POLAR_SWITCHED_OFF
^^^^^^^^^^^^^^^^^^^^^^

**Option to switch off polarization effects**

:Value: 0 (polarization enabled)
:Units: Dimensionless (flag)
:File: ``OSOAA_SOS_CORE.F``

- 0: Polarization calculations enabled (full vector RT)
- 1: Polarization switched off (scalar RT, faster)

**Note:** Setting to 1 significantly reduces computation time but loses polarization information.

Using Constants in OSOAA
-------------------------

Accessing Constants
~~~~~~~~~~~~~~~~~~~

Constants are defined in ``inc/OSOAA.h`` and compiled into the code. They cannot be changed at runtime without recompiling.

**To modify a constant:**

1. Edit ``inc/OSOAA.h``
2. Recompile OSOAA
3. Document changes in configuration files

Example Modifications
~~~~~~~~~~~~~~~~~~~~~

**Increase maximum scattering orders:**

.. code-block:: c

   // In inc/OSOAA.h
   #define CTE_DEFAULT_IGMAX 200  // Changed from 100

**Adjust convergence threshold for faster (less accurate) calculations:**

.. code-block:: c

   // In inc/OSOAA.h
   #define CTE_PH_SEUIL_SUMDIF  0.01  // Changed from 0.001

**Increase maximum user angles:**

.. code-block:: c

   // In inc/OSOAA.h
   #define CTE_NBMAX_USER_ANGLES 200  // Changed from 100
   
   // Must also increase:
   #define CTE_MIE_NBMU_MAX 710  // Was 510, now 510+200

Best Practices
--------------

When Modifying Constants
~~~~~~~~~~~~~~~~~~~~~~~~

1. **Document changes**: Keep a log of modified values
2. **Test thoroughly**: Verify convergence and accuracy
3. **Version control**: Tag code version with custom constants
4. **Performance**: Balance accuracy vs. computation time
5. **Memory**: Larger array dimensions increase memory usage

Common Modifications
~~~~~~~~~~~~~~~~~~~~

**For faster calculations:**

- Reduce ``CTE_DEFAULT_IGMAX``
- Increase convergence thresholds (``CTE_PH_SEUIL_*``)
- Reduce ``CTE_DEFAULT_NBMU_LUM``

**For higher accuracy:**

- Increase ``CTE_DEFAULT_IGMAX``
- Decrease convergence thresholds
- Increase ``CTE_DEFAULT_NBMU_LUM`` and ``CTE_DEFAULT_NBMU_MIE``

**For more viewing angles:**

- Increase ``CTE_NBMAX_USER_ANGLES``
- Correspondingly increase ``CTE_MIE_NBMU_MAX``

See Also
--------

- :ref:`parameter_reference` for input parameters
- :ref:`file_formats` for input/output file specifications
- ``inc/OSOAA.h`` source file for complete constant definitions
- Technical documentation for algorithm details
