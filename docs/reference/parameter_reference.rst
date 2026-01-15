.. _parameter_reference:

Parameter Reference
===================

This page provides a comprehensive reference for all input parameters used in OSOAA simulations.

.. contents:: Contents
   :local:
   :depth: 2

Parameter File Format
---------------------

OSOAA reads parameters from ASCII text files with the following format::

    # Comment lines start with #
    PARAMETER_NAME value
    
    # Blank lines are ignored
    ANOTHER_PARAMETER value

**Rules:**

- One parameter per line
- Parameter name and value separated by whitespace
- Comments begin with ``#``
- Case-sensitive parameter names
- Numeric values use decimal point (e.g., ``1.5`` not ``1,5``)

**Notation:**

- ``*`` = Required parameter
- ``(default: X)`` = Optional parameter with default value X

Wavelength and Geometry
-----------------------

Wavelength Parameters
~~~~~~~~~~~~~~~~~~~~~

OSOAA.Wa *
^^^^^^^^^^

**Wavelength for monochromatic radiance calculation**

:Type: Float
:Units: nanometers (nm)
:Range: 299-1000 nm
:Example: ``OSOAA.Wa 550.0``

The wavelength at which to perform the radiative transfer calculation. OSOAA performs monochromatic calculations. For multi-spectral results, run multiple simulations at different wavelengths.

**Common ocean color wavelengths:**

- 412 nm: Blue (SeaWiFS, MODIS)
- 443 nm: Blue (SeaWiFS, MODIS)
- 490 nm: Blue-green (SeaWiFS, MODIS)
- 550 nm: Green (reference wavelength)
- 670 nm: Red (SeaWiFS, MODIS)
- 865 nm: Near-infrared (atmospheric correction)

Solar Geometry
~~~~~~~~~~~~~~

ANG.Thetas *
^^^^^^^^^^^^

**Solar zenith angle**

:Type: Float
:Units: degrees
:Range: 0-90°
:Example: ``ANG.Thetas 30.0``

Angle between the sun direction and the vertical (zenith).

**Typical values:**

- 0°: Sun at zenith (overhead, noon at equator)
- 30°: Typical mid-latitude afternoon
- 45°: Mid-morning or mid-afternoon
- 60°: Low sun angle, early morning or late afternoon
- 75°: Near sunrise/sunset (may cause convergence issues)

.. warning::
   Solar zenith angles > 75° may cause numerical instability and slow convergence.

Viewing Geometry
~~~~~~~~~~~~~~~~

OSOAA.View.Phi *
^^^^^^^^^^^^^^^^

**Relative azimuth angle between sun and viewing direction**

:Type: Float
:Units: degrees
:Range: 0-180°
:Example: ``OSOAA.View.Phi 90.0``

The azimuthal angle difference between the sun and viewing directions.

**Scattering geometry:**

- 0°: Forward scattering (viewing in sun direction)
- 90°: Cross-sun viewing (perpendicular to sun)
- 180°: Backscattering (viewing opposite to sun, sun glint region)

OSOAA.View.Level *
^^^^^^^^^^^^^^^^^^

**Vertical level type for output**

:Type: Integer
:Values:
  - 1 = Altitude (in atmosphere)
  - -1 = Depth (in ocean)
:Example: ``OSOAA.View.Level -1``

Specifies whether the output altitude/depth (OSOAA.View.Z) is in the atmosphere or ocean.

OSOAA.View.Z *
^^^^^^^^^^^^^^

**Altitude or depth for radiance output**

:Type: Float
:Units: kilometers (atmosphere) or meters (ocean)
:Range: 
  - Altitude: 0 to PROFILE.Atm.Ztoa
  - Depth: 0 to PROFILE.Sea.Depth
:Example: ``OSOAA.View.Z 0.0``

The vertical position where radiance output is requested.

**Common choices:**

- ``0.0`` with ``Level 1``: Just above sea surface (upwelling radiance)
- ``0.0`` with ``Level -1``: Just below sea surface (transmitted radiance)
- ``-0.0`` with ``Level -1``: Subsurface radiance (water-leaving radiance)
- ``-10.0`` with ``Level -1``: 10 meters depth

Angular Discretization
~~~~~~~~~~~~~~~~~~~~~~

ANG.Rad.NbGauss *
^^^^^^^^^^^^^^^^^

**Number of Gauss-Legendre quadrature points**

:Type: Integer
:Range: 10-50 (typically 16-24)
:Example: ``ANG.Rad.NbGauss 24``

Number of zenith angles for Gauss quadrature integration in radiative transfer calculations. Higher values increase accuracy but also computation time.

**Recommendations:**

- 16: Fast calculations, moderate accuracy
- 24: Good balance (recommended)
- 32: High accuracy applications
- 48: Very high accuracy (research)

ANG.Rad.UserAngFile
^^^^^^^^^^^^^^^^^^^

**User-defined angular directions file**

:Type: String (filename)
:Example: ``ANG.Rad.UserAngFile MY_ANGLES.txt``

Optional file specifying additional viewing angles for output. Format::

    # Zenith angle (degrees)
    0.0
    30.0
    45.0
    60.0

ANG.Phi.Nb *
^^^^^^^^^^^^

**Number of azimuthal angles for Fourier series**

:Type: Integer
:Default: 1024
:Example: ``ANG.Phi.Nb 1024``

Number of azimuthal angles used in Fourier decomposition of the radiance field. Defined in ``inc/OSOAA.h`` as ``CTE_PH_NU``.

Atmospheric Parameters
----------------------

Atmospheric Profile
~~~~~~~~~~~~~~~~~~~

PROFILE.Atm.File
^^^^^^^^^^^^^^^^

**Atmospheric profile data file**

:Type: String (filename)
:Example: ``PROFILE.Atm.File MY_ATMOSPHERE.txt``
:Default: ``PROFILE_ATM_US76.txt`` (U.S. Standard Atmosphere 1976)

Specifies vertical profiles of temperature, pressure, and molecular density.

PROFILE.Atm.Ztoa *
^^^^^^^^^^^^^^^^^^

**Top of atmosphere altitude**

:Type: Float
:Units: kilometers
:Range: 50-120 km
:Default: 120.0
:Example: ``PROFILE.Atm.Ztoa 100.0``

Upper boundary of the atmospheric domain. Standard value is 100-120 km (thermosphere).

PROFILE.Atm.Zmin
^^^^^^^^^^^^^^^^

**Minimum atmospheric altitude for calculations**

:Type: Float
:Units: kilometers
:Default: 0.0 (sea surface)
:Example: ``PROFILE.Atm.Zmin 0.0``

PROFILE.Atm.StdAtm
^^^^^^^^^^^^^^^^^^

**Use standard atmosphere model**

:Type: Integer
:Values:
  - 0 = User-defined profile
  - 1 = U.S. Standard Atmosphere 1976
:Default: 1
:Example: ``PROFILE.Atm.StdAtm 1``

Molecular Atmosphere
~~~~~~~~~~~~~~~~~~~~

PROFILE.Atm.MOT *
^^^^^^^^^^^^^^^^^

**Molecular optical thickness**

:Type: Float
:Range: 0.0-0.5 (typically)
:Example: ``PROFILE.Atm.MOT 0.15``

Total Rayleigh scattering optical thickness of the atmosphere at the specified wavelength.

**Typical values at sea level:**

- 412 nm: ~0.30
- 550 nm: ~0.10
- 865 nm: ~0.02

**Scaling:** MOT varies approximately as λ⁻⁴ (Rayleigh scattering law).

PROFILE.Atm.HR
^^^^^^^^^^^^^^

**Rayleigh scattering scale height**

:Type: Float
:Units: kilometers
:Default: 8.0
:Example: ``PROFILE.Atm.HR 8.0``

Scale height for exponential decay of molecular density with altitude:

.. math::

   \\rho(z) = \\rho_0 \\exp(-z/H_R)

PROFILE.Atm.Tlay
^^^^^^^^^^^^^^^^

**Number of atmospheric layers**

:Type: Integer
:Range: 20-200
:Default: 50
:Example: ``PROFILE.Atm.Tlay 50``

Number of vertical layers in atmospheric discretization. More layers increase accuracy and computation time.

Aerosol Parameters
------------------

Aerosol Model Selection
~~~~~~~~~~~~~~~~~~~~~~~

AER.Model *
^^^^^^^^^^^

**Aerosol model type**

:Type: Integer
:Values:
  - 0 = Mono-modal size distribution (LND or Junge)
  - 1 = WMO multi-modal model
  - 2 = Shettle & Fenn bi-modal model
  - 3 = Log-normal bi-modal distribution
  - 4 = Phase functions from external file
:Example: ``AER.Model 0``

Determines which aerosol model to use for atmospheric scattering.

Aerosol Optical Properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~

AER.AOTref *
^^^^^^^^^^^^

**Aerosol optical thickness at reference wavelength**

:Type: Float
:Range: 0.0-2.0
:Example: ``AER.AOTref 0.1``

Total aerosol optical depth (extinction) at the reference wavelength.

**Typical values:**

- 0.02-0.05: Very clean (remote ocean)
- 0.05-0.1: Clean maritime
- 0.1-0.3: Average conditions
- 0.3-0.8: Hazy/polluted
- 0.8-2.0: Very turbid (dust storms, smoke)

AER.Waref
^^^^^^^^^

**Reference wavelength for AOT**

:Type: Float
:Units: nanometers
:Default: Same as OSOAA.Wa
:Example: ``AER.Waref 550.0``

Wavelength at which AOTref is specified. Used with Angström exponent to compute AOT at other wavelengths.

AER.Angexp
^^^^^^^^^^

**Angström exponent for spectral AOT dependence**

:Type: Float
:Range: 0.0-2.5
:Default: 1.0
:Example: ``AER.Angexp 1.0``

Describes wavelength dependence of aerosol optical thickness:

.. math::

   \\tau_{aer}(\\lambda) = \\tau_{ref} \\left(\\frac{\\lambda_{ref}}{\\lambda}\\right)^\\alpha

**Typical values:**

- 0.0-0.5: Large particles (maritime aerosols, dust)
- 0.5-1.0: Mixed aerosols
- 1.0-1.5: Average aerosols
- 1.5-2.5: Small particles (urban pollution, biomass burning)

AER.HR
^^^^^^

**Aerosol scale height**

:Type: Float
:Units: kilometers
:Default: 2.0
:Example: ``AER.HR 2.0``

Scale height for exponential decay of aerosol concentration with altitude.

**Typical values:**

- 1.0 km: Dust, pollution (confined to boundary layer)
- 2.0 km: Average aerosols
- 3.0-4.0 km: Elevated layers, biomass burning

Mono-Modal Aerosol (Model=0)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

AER.MMD.MRwa *
^^^^^^^^^^^^^^

**Real part of aerosol refractive index**

:Type: Float
:Range: 1.3-1.6
:Example: ``AER.MMD.MRwa 1.45``

Real component of complex refractive index: n = MRwa + i·MIwa

**Common values:**

- 1.33: Water droplets
- 1.40: Water-soluble aerosols
- 1.45: Average aerosols
- 1.50: Dust
- 1.53: Mineral dust
- 1.55: Urban aerosols

AER.MMD.MIwa *
^^^^^^^^^^^^^^

**Imaginary part of aerosol refractive index**

:Type: Float
:Range: 0.0-0.05
:Example: ``AER.MMD.MIwa 0.005``

Imaginary component determining absorption.

**Typical values:**

- 0.0: Non-absorbing (pure scattering)
- 0.001-0.005: Weakly absorbing (maritime aerosols)
- 0.005-0.01: Moderately absorbing (dust)
- 0.01-0.02: Absorbing (pollution)
- 0.02-0.05: Strongly absorbing (soot, black carbon)

AER.MMD.SDtype *
^^^^^^^^^^^^^^^^

**Size distribution type**

:Type: Integer
:Values:
  - 1 = Junge power law distribution
  - 2 = Log-normal distribution
:Example: ``AER.MMD.SDtype 2``

**Junge distribution:**

.. math::

   n(r) \\propto r^{-\\nu}

**Log-normal distribution:**

.. math::

   n(r) = \\frac{N}{\\sqrt{2\\pi}\\sigma r} \\exp\\left[-\\frac{(\\ln r - \\ln r_0)^2}{2\\sigma^2}\\right]

AER.MMD.SDradius *
^^^^^^^^^^^^^^^^^^

**Characteristic radius of size distribution**

:Type: Float
:Units: micrometers (µm)
:Range: 0.01-10.0
:Example: ``AER.MMD.SDradius 0.15``

- **For log-normal**: Median radius (r₀)
- **For Junge**: Reference radius

**Typical values:**

- 0.05-0.15 µm: Urban pollution, fine mode
- 0.2-0.5 µm: Average aerosols
- 0.5-2.0 µm: Coarse mode, dust
- 2.0-10.0 µm: Sea salt, large dust

AER.MMD.SDvar *
^^^^^^^^^^^^^^^

**Size distribution variance**

:Type: Float
:Range: 0.3-0.8
:Example: ``AER.MMD.SDvar 0.6``

- **For log-normal**: Standard deviation of ln(r), typically σ = 0.4-0.7
- **For Junge**: Slope parameter ν, typically 3-4

Bi-Modal Log-Normal Aerosol (Model=3)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fine Mode Parameters
^^^^^^^^^^^^^^^^^^^^

AER.BMD.VCF *
"""""""""""""

**Volume concentration fraction of fine mode**

:Type: Float
:Range: 0.0-1.0
:Example: ``AER.BMD.VCF 0.7``

Fraction of total aerosol volume in fine mode. Coarse mode fraction = 1 - VCF.

AER.BMD.MRFM *, AER.BMD.MIFM *
""""""""""""""""""""""""""""""

**Refractive index of fine mode (real and imaginary)**

:Type: Float
:Example: ``AER.BMD.MRFM 1.40``, ``AER.BMD.MIFM 0.001``

AER.BMD.RADFM *, AER.BMD.VARFM *
""""""""""""""""""""""""""""""""

**Median radius and variance of fine mode**

:Type: Float
:Units: µm (radius)
:Example: ``AER.BMD.RADFM 0.1``, ``AER.BMD.VARFM 0.6``

Coarse Mode Parameters
^^^^^^^^^^^^^^^^^^^^^^

AER.BMD.MRCM *, AER.BMD.MICM *
""""""""""""""""""""""""""""""

**Refractive index of coarse mode (real and imaginary)**

:Type: Float
:Example: ``AER.BMD.MRCM 1.53``, ``AER.BMD.MICM 0.008``

AER.BMD.RADCM *, AER.BMD.VARCM *
""""""""""""""""""""""""""""""""

**Median radius and variance of coarse mode**

:Type: Float
:Units: µm (radius)
:Example: ``AER.BMD.RADCM 1.0``, ``AER.BMD.VARCM 0.7``

WMO Aerosol Model (Model=1)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

AER.WMO.Model *
^^^^^^^^^^^^^^^

**WMO aerosol type**

:Type: Integer
:Values:
  - 1 = Maritime
  - 2 = Continental
  - 3 = Urban
  - 4 = Tropospheric
:Example: ``AER.WMO.Model 1``

Pre-defined multi-modal aerosol models from World Meteorological Organization.

AER.WMO.DL, AER.WMO.WS, AER.WMO.OC, AER.WMO.SO
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Component optical thicknesses**

:Type: Float
:Example: ``AER.WMO.DL 0.05`` (Dust-like)

Individual contributions to total AOT from different aerosol components:

- **DL**: Dust-like
- **WS**: Water-soluble
- **OC**: Oceanic
- **SO**: Soot

Shettle & Fenn Model (Model=2)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

AER.SF.Model *
^^^^^^^^^^^^^^

**Shettle & Fenn aerosol type**

:Type: Integer
:Values:
  - 1 = Maritime (different humidity levels)
  - 2 = Coastal
  - 3 = Tropospheric
  - 4 = Urban
:Example: ``AER.SF.Model 1``

AER.SF.RH
^^^^^^^^^

**Relative humidity for hygroscopic growth**

:Type: Float
:Units: percent
:Range: 0-99
:Default: 70
:Example: ``AER.SF.RH 80.0``

Affects aerosol size and refractive index through water uptake.

External Phase Function (Model=4)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

AER.ExtData *
^^^^^^^^^^^^^

**External phase function data file**

:Type: String (filename)
:Example: ``AER.ExtData MY_AEROSOL_PHASE.txt``

File containing measured or pre-computed phase function and optical properties.

**Format:**

- Scattering angles
- Phase function values
- Single scattering albedo
- Phase matrix elements (for polarization)

Aerosol File Paths
~~~~~~~~~~~~~~~~~~

AER.DirMie *
^^^^^^^^^^^^

**Directory for Mie calculation files**

:Type: String (path)
:Example: ``AER.DirMie ./data/aerosols/mie/``

Directory where Mie scattering tables are stored or generated.

AER.Log, AER.MieLog
^^^^^^^^^^^^^^^^^^^

**Log file names**

:Type: String (filename)
:Example: ``AER.Log AER_LOG.txt``

AER.ResFile.IOP
^^^^^^^^^^^^^^^

**Output file for aerosol IOPs**

:Type: String (filename)
:Example: ``AER.ResFile.IOP AER_IOP_550nm.txt``

File to store computed inherent optical properties.

Ocean Parameters
----------------

Ocean Profile
~~~~~~~~~~~~~

PROFILE.Sea.File
^^^^^^^^^^^^^^^^

**Ocean profile data file**

:Type: String (filename)
:Example: ``PROFILE.Sea.File MY_OCEAN_PROFILE.txt``
:Default: ``PROFILE_SEA_DEFAULT.txt``

Specifies vertical profiles of temperature, salinity, and optical properties.

PROFILE.Sea.Depth *
^^^^^^^^^^^^^^^^^^^

**Maximum ocean depth**

:Type: Float
:Units: meters
:Range: 10-1000
:Example: ``PROFILE.Sea.Depth 100.0``

Depth of the ocean domain. Should be sufficient to capture euphotic zone or region of interest.

**Typical values:**

- 50-100 m: Coastal waters
- 100-200 m: Shelf waters, euphotic zone
- 200+ m: Open ocean (most light absorbed by ~200 m)

PROFILE.Sea.Tlay
^^^^^^^^^^^^^^^^

**Number of ocean layers**

:Type: Integer
:Range: 10-100
:Default: 30
:Example: ``PROFILE.Sea.Tlay 30``

Vertical discretization of ocean. Finer layers near surface recommended.

Hydrosol Parameters
-------------------

Hydrosol Model Selection
~~~~~~~~~~~~~~~~~~~~~~~~

HYD.Model *
^^^^^^^^^^^

**Hydrosol model type**

:Type: Integer
:Values:
  - 0 = Mono-modal size distribution
  - 1 = Bio-optical model (chlorophyll-based)
  - 2 = Mineral-like particles
  - 3 = Combined bio-optical + minerals
  - 4 = External phase functions
  - 5 = User-defined absorption and scattering coefficients
:Example: ``HYD.Model 1``

Bio-Optical Model (Model=1)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

HYD.BioOpt.Chl *
^^^^^^^^^^^^^^^^

**Chlorophyll-a concentration**

:Type: Float
:Units: mg/m³
:Range: 0.01-50
:Example: ``HYD.BioOpt.Chl 0.5``

Chlorophyll-a concentration drives phytoplankton absorption and scattering.

**Typical values:**

- 0.01-0.1: Oligotrophic (open ocean)
- 0.1-1.0: Mesotrophic
- 1.0-10.0: Eutrophic (coastal, productive)
- 10.0-50.0: Highly eutrophic (bloom conditions)

HYD.BioOpt.ProfileType
^^^^^^^^^^^^^^^^^^^^^^

**Chlorophyll vertical profile type**

:Type: Integer
:Values:
  - 0 = Homogeneous
  - 1 = Gaussian (subsurface maximum)
  - 2 = User-defined profile
:Example: ``HYD.BioOpt.ProfileType 1``

HYD.BioOpt.Zmax
^^^^^^^^^^^^^^^

**Depth of chlorophyll maximum** (for Gaussian profile)

:Type: Float
:Units: meters
:Range: 10-100
:Example: ``HYD.BioOpt.Zmax 50.0``

HYD.BioOpt.Width
^^^^^^^^^^^^^^^^

**Width of chlorophyll maximum** (for Gaussian profile)

:Type: Float
:Units: meters
:Example: ``HYD.BioOpt.Width 20.0``

Yellow Substance (CDOM)
~~~~~~~~~~~~~~~~~~~~~~~~

HYD.YS.abs440 *
^^^^^^^^^^^^^^^

**Yellow substance absorption at 440 nm**

:Type: Float
:Units: m⁻¹
:Range: 0.0-1.0
:Example: ``HYD.YS.abs440 0.05``

CDOM (Colored Dissolved Organic Matter) absorption coefficient at reference wavelength.

**Typical values:**

- 0.0-0.02: Oligotrophic open ocean
- 0.02-0.1: Coastal waters
- 0.1-0.5: Estuaries, river-influenced
- 0.5-2.0: High-CDOM rivers, wetlands

HYD.YS.Swa
^^^^^^^^^^

**Yellow substance spectral slope**

:Type: Float
:Units: nm⁻¹
:Default: 0.014
:Example: ``HYD.YS.Swa 0.014``

Exponential decay coefficient for wavelength dependence:

.. math::

   a_{YS}(\\lambda) = a_{YS}(440) \\exp[-S(\\lambda - 440)]

Mineral-Like Particles
~~~~~~~~~~~~~~~~~~~~~~

HYD.MLP.Csed *
^^^^^^^^^^^^^^

**Sediment concentration**

:Type: Float
:Units: g/m³
:Range: 0.0-100
:Example: ``HYD.MLP.Csed 1.0``

Concentration of suspended mineral particles.

**Typical values:**

- 0.1-1.0: Clear coastal waters
- 1.0-10.0: Turbid coastal waters
- 10.0-100.0: Very turbid (estuaries, resuspension events)

HYD.MLP.MRwa, HYD.MLP.MIwa *
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Refractive index of minerals**

:Type: Float
:Example: ``HYD.MLP.MRwa 1.15``, ``HYD.MLP.MIwa 0.001``

User-Defined IOPs (Model=5)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

HYD.UserIOP.File *
^^^^^^^^^^^^^^^^^^

**User-defined IOP data file**

:Type: String (filename)
:Example: ``HYD.UserIOP.File MY_IOPS.txt``

File containing measured absorption and scattering coefficients versus depth.

**Format:**

::

    # Depth(m)  a_total(m^-1)  b_total(m^-1)  bb_total(m^-1)
    0.0         0.05           0.3            0.01
    10.0        0.06           0.32           0.011
    20.0        0.065          0.35           0.012

Hydrosol File Paths
~~~~~~~~~~~~~~~~~~~

HYD.DirMie, HYD.Log, HYD.ResFile.IOP
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Similar to aerosol file parameters, for hydrosol calculations.

Sea Surface Parameters
----------------------

Surface Model
~~~~~~~~~~~~~

SOS.Surface.Model *
^^^^^^^^^^^^^^^^^^^

**Sea surface model type**

:Type: Integer
:Values:
  - 0 = Flat surface (Fresnel reflection)
  - 1 = Rough surface (Cox & Munk wind-wave model)
:Example: ``SOS.Surface.Model 1``

Rough Surface (Model=1)
~~~~~~~~~~~~~~~~~~~~~~~

SOS.Surface.Wind *
^^^^^^^^^^^^^^^^^^

**Wind speed at 10 m height**

:Type: Float
:Units: m/s
:Range: 0-20
:Example: ``SOS.Surface.Wind 5.0``

Wind speed drives wave development in Cox & Munk model.

**Beaufort scale:**

- 0-1 m/s: Calm
- 1-3 m/s: Light breeze
- 3-5 m/s: Gentle breeze
- 5-8 m/s: Moderate breeze
- 8-11 m/s: Fresh breeze
- 11+ m/s: Strong breeze to gale

SOS.Surface.WaveNum
^^^^^^^^^^^^^^^^^^^

**Number of wave slope classes**

:Type: Integer
:Default: 20
:Example: ``SOS.Surface.WaveNum 20``

Discretization of wave slope probability distribution. Higher values increase accuracy and computation time.

SOS.Surface.SlopeVar
^^^^^^^^^^^^^^^^^^^^

**Variance of wave slopes**

:Type: Float
:Example: ``SOS.Surface.SlopeVar 0.003``

Can be specified directly or computed from wind speed via Cox & Munk relationships.

Water Refractive Index
~~~~~~~~~~~~~~~~~~~~~~

SOS.Surface.RefracIndex
^^^^^^^^^^^^^^^^^^^^^^^

**Real refractive index of seawater**

:Type: Float
:Default: 1.34 (typical for 550 nm, 20°C, 35 PSU)
:Example: ``SOS.Surface.RefracIndex 1.34``

Depends on wavelength, temperature, and salinity.

Radiative Transfer Parameters
-----------------------------

Successive Orders Method
~~~~~~~~~~~~~~~~~~~~~~~~

OSOAA.ResFile.LUM_SF
^^^^^^^^^^^^^^^^^^^^

**Binary output file for Fourier series**

:Type: String (filename)
:Default: ``LUM_SF.bin``
:Example: ``OSOAA.ResFile.LUM_SF RADIANCE_FOURIER.bin``

OSOAA.ResFile.LUM_VZA
^^^^^^^^^^^^^^^^^^^^^

**ASCII output file for radiance vs. viewing angle**

:Type: String (filename)
:Default: ``LUM_vsVZA.txt``
:Example: ``OSOAA.ResFile.LUM_VZA RADIANCE_VS_ANGLE.txt``

Convergence Parameters
~~~~~~~~~~~~~~~~~~~~~~

SOS.IGMAX
^^^^^^^^^

**Maximum number of scattering orders**

:Type: Integer
:Default: 100
:Range: 10-200
:Example: ``SOS.IGMAX 50``

Maximum iterations in successive orders of scattering. Calculation stops when convergence is reached or IGMAX is exceeded.

**Guidelines:**

- Clear atmosphere/ocean: 20-50 orders sufficient
- Turbid conditions: 50-100 orders
- Very turbid or multiple scattering dominant: 100-200 orders

SOS.ResFile.LOG
^^^^^^^^^^^^^^^

**Log file for successive orders calculations**

:Type: String (filename)
:Default: ``LOG_OSOAA.txt``
:Example: ``SOS.ResFile.LOG CALCULATION_LOG.txt``

Contains convergence information and iteration details.

Output Control Parameters
--------------------------

Output Options
~~~~~~~~~~~~~~

OSOAA.ResFile.UP
^^^^^^^^^^^^^^^^

**Output file for upwelling radiance**

:Type: String (filename)
:Example: ``OSOAA.ResFile.UP RADIANCE_UP.txt``

OSOAA.ResFile.DOWN
^^^^^^^^^^^^^^^^^^

**Output file for downwelling radiance**

:Type: String (filename)
:Example: ``OSOAA.ResFile.DOWN RADIANCE_DOWN.txt``

OSOAA.ResFile.POLUP
^^^^^^^^^^^^^^^^^^^

**Output file for upwelling polarization**

:Type: String (filename)
:Example: ``OSOAA.ResFile.POLUP POLARIZATION_UP.txt``

Contains Stokes parameters Q, U, V and degree of linear polarization (DoLP).

OSOAA.ResFile.POLDOWN
^^^^^^^^^^^^^^^^^^^^^

**Output file for downwelling polarization**

:Type: String (filename)
:Example: ``OSOAA.ResFile.POLDOWN POLARIZATION_DOWN.txt``

Example Parameter Files
-----------------------

Basic Ocean Color Simulation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    # Basic ocean color simulation at 550 nm
    # Solar geometry: 30° zenith, nadir viewing
    
    # Wavelength and geometry
    OSOAA.Wa 550.0
    ANG.Thetas 30.0
    OSOAA.View.Phi 0.0
    OSOAA.View.Level -1
    OSOAA.View.Z -0.0
    
    # Angular discretization
    ANG.Rad.NbGauss 24
    
    # Atmosphere
    PROFILE.Atm.MOT 0.1
    AER.Model 0
    AER.AOTref 0.1
    AER.Angexp 1.0
    AER.MMD.MRwa 1.45
    AER.MMD.MIwa 0.001
    AER.MMD.SDtype 2
    AER.MMD.SDradius 0.15
    AER.MMD.SDvar 0.6
    
    # Ocean
    PROFILE.Sea.Depth 100.0
    HYD.Model 1
    HYD.BioOpt.Chl 0.5
    HYD.YS.abs440 0.05
    
    # Sea surface
    SOS.Surface.Model 1
    SOS.Surface.Wind 5.0

Turbid Coastal Waters
~~~~~~~~~~~~~~~~~~~~~

::

    # Turbid coastal simulation
    
    OSOAA.Wa 550.0
    ANG.Thetas 45.0
    OSOAA.View.Phi 90.0
    OSOAA.View.Level -1
    OSOAA.View.Z -0.0
    
    # Higher AOT for coastal haze
    PROFILE.Atm.MOT 0.15
    AER.Model 3
    AER.AOTref 0.3
    
    # Bi-modal aerosol
    AER.BMD.VCF 0.6
    AER.BMD.MRFM 1.40
    AER.BMD.MIFM 0.005
    AER.BMD.RADFM 0.1
    AER.BMD.VARFM 0.6
    AER.BMD.MRCM 1.50
    AER.BMD.MICM 0.01
    AER.BMD.RADCM 1.0
    AER.BMD.VARCM 0.7
    
    # Turbid water
    PROFILE.Sea.Depth 50.0
    HYD.Model 3
    HYD.BioOpt.Chl 5.0
    HYD.MLP.Csed 10.0
    HYD.YS.abs440 0.2
    
    # Rough surface
    SOS.Surface.Model 1
    SOS.Surface.Wind 8.0

See Also
--------

- :ref:`constants` for physical constants used in calculations
- :ref:`file_formats` for input/output file formats
- :ref:`faq` for common parameter questions
