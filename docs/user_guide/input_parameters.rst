Input Parameters
================

This comprehensive guide describes all input parameters for OSOAA simulations.

Parameter File Format
---------------------

Basic Structure
~~~~~~~~~~~~~~~

OSOAA reads parameters from a plain text file with the following format::

    # Comment lines start with #
    PARAMETER_NAME value
    
    # Blank lines are ignored
    ANOTHER_PARAMETER value

Rules:

* One parameter per line
* Parameter name and value separated by whitespace
* Comments begin with ``#``
* Case-sensitive parameter names
* Numeric values use decimal point (e.g., ``1.5`` not ``1,5``)

Required vs Optional
~~~~~~~~~~~~~~~~~~~~

* **Required parameters**: Must be specified for simulation to run
* **Optional parameters**: Have default values if not specified

Parameters are marked as:

* ``*`` = Required
* ``(default: X)`` = Optional with default value X

Wavelength Parameters
---------------------

OSOAA.Wa *
~~~~~~~~~~

**Wavelength for radiance calculation**

:Type: Float
:Units: nanometers (nm)
:Range: 299-1000 nm
:Example: ``OSOAA.Wa 550.0``

Specifies the wavelength at which to perform the radiative transfer calculation.

.. note::
   OSOAA performs monochromatic calculations. For multi-spectral results, 
   run multiple simulations at different wavelengths.

**Typical values**:

* 412 nm - Blue (common ocean color band)
* 443 nm - Blue
* 490 nm - Blue-green
* 550 nm - Green
* 670 nm - Red
* 865 nm - Near-infrared

Geometric Conditions
--------------------

Viewing Geometry
~~~~~~~~~~~~~~~~

OSOAA.View.Phi *
^^^^^^^^^^^^^^^^

**Relative azimuth angle between sun and viewing direction**

:Type: Float
:Units: degrees
:Range: 0-180°
:Example: ``OSOAA.View.Phi 90.0``

* 0° = Forward scattering (sun direction)
* 90° = Cross-sun viewing
* 180° = Backscattering (opposite sun)

OSOAA.View.Level *
^^^^^^^^^^^^^^^^^^

**Vertical level type for output**

:Type: Integer
:Values:
  * 1 = Altitude (in atmosphere)
  * -1 = Depth (in ocean)
:Example: ``OSOAA.View.Level -1``

OSOAA.View.Z *
^^^^^^^^^^^^^^

**Altitude or depth for radiance output**

:Type: Float
:Units: kilometers (atmosphere) or meters (ocean)
:Range: 
  * Altitude: 0 to PROFILE.Atm.Ztoa
  * Depth: 0 to PROFILE.Sea.Depth
:Example: ``OSOAA.View.Z 0.0``

Common values:

* ``0.0`` with ``Level 1`` = Sea surface (above water)
* ``-0.0`` with ``Level -1`` = Just below water surface
* ``-10.0`` with ``Level -1`` = 10 meters depth

Solar Geometry
~~~~~~~~~~~~~~

ANG.Thetas *
^^^^^^^^^^^^

**Solar zenith angle**

:Type: Float
:Units: degrees
:Range: 0-90°
:Example: ``ANG.Thetas 30.0``

* 0° = Sun at zenith (overhead)
* 30° = Typical mid-latitude afternoon
* 60° = Low sun angle
* 90° = Sunrise/sunset (not recommended)

.. warning::
   Very large solar zenith angles (>75°) may cause convergence issues.

Angular Discretization
~~~~~~~~~~~~~~~~~~~~~~

ANG.Rad.NbGauss *
^^^^^^^^^^^^^^^^^

**Number of Gauss angles for radiance calculations**

:Type: Integer
:Range: 20-100
:Example: ``ANG.Rad.NbGauss 40``

Higher values give better accuracy but increase computation time.

**Recommendations**:

* Quick tests: 20-30
* Standard simulations: 40-50
* High accuracy: 60-80

ANG.Rad.UserAngFile
^^^^^^^^^^^^^^^^^^^

**File with user-defined viewing angles**

:Type: String (filename)
:Example: ``ANG.Rad.UserAngFile MY_ANGLES.txt``
:Default: ``ANGLE_RAD_DEFAULT.txt``

File format (one angle per line)::

    0.0
    10.0
    20.0
    30.0
    ...

ANG.Rad.ResFile
^^^^^^^^^^^^^^^

**Output file for angular grid information**

:Type: String (filename)
:Example: ``ANG.Rad.ResFile ANGLES_RAD.txt``
:Default: ``ANGLES_RAD.txt``

ANG.Mie.NbGauss *
^^^^^^^^^^^^^^^^^

**Number of Gauss angles for phase functions**

:Type: Integer
:Range: 50-200
:Example: ``ANG.Mie.NbGauss 83``

More angles give better integration of phase functions.

ANG.Mie.UserAngFile
^^^^^^^^^^^^^^^^^^^

**Additional angles for phase function calculations**

:Type: String (filename)
:Optional: Yes

Atmospheric Profile
-------------------

Profile File
~~~~~~~~~~~~

PROFILE.Atm.File
^^^^^^^^^^^^^^^^

**Atmospheric profile data file**

:Type: String (filename)
:Example: ``PROFILE.Atm.File PROFILE_ATM_DEFAULT.txt``
:Default: Standard atmosphere profile

File format::

    # Altitude(km)  Pressure(hPa)  Temperature(K)  Density(kg/m³)
    0.0    1013.25    288.15    1.225
    1.0    898.74     281.65    1.112
    ...

PROFILE.Atm.Pressure *
^^^^^^^^^^^^^^^^^^^^^^

**Surface pressure**

:Type: Float
:Units: hectoPascals (hPa or mb)
:Range: 900-1050 hPa
:Example: ``PROFILE.Atm.Pressure 1013.25``

Standard sea level: 1013.25 hPa

PROFILE.Atm.HR *
^^^^^^^^^^^^^^^^

**Rayleigh scattering scale height**

:Type: Float
:Units: kilometers
:Range: 6-10 km
:Example: ``PROFILE.Atm.HR 8.0``

Standard atmosphere: 8.0 km

PROFILE.Atm.Ha *
^^^^^^^^^^^^^^^^

**Aerosol scale height**

:Type: Float
:Units: kilometers
:Range: 1-4 km
:Example: ``PROFILE.Atm.Ha 2.0``

Typical value: 2.0 km (boundary layer aerosols)

PROFILE.Atm.MO3 *
^^^^^^^^^^^^^^^^^

**Ozone content**

:Type: Float
:Units: atm-cm
:Range: 0.2-0.5
:Example: ``PROFILE.Atm.MO3 0.3``

Standard atmosphere: 0.3 atm-cm

PROFILE.Atm.Ztoa *
^^^^^^^^^^^^^^^^^^

**Top of atmosphere altitude**

:Type: Float
:Units: kilometers
:Range: 20-100 km
:Example: ``PROFILE.Atm.Ztoa 60.0``

Standard: 60 km (sufficient for most applications)

Aerosol Parameters
------------------

Aerosol Model Selection
~~~~~~~~~~~~~~~~~~~~~~~

AER.Model *
^^^^^^^^^^^

**Aerosol model type**

:Type: Integer
:Values:
  * 0 = Mono-modal size distribution (LND or Junge)
  * 1 = WMO multi-modal model
  * 2 = Shettle & Fenn bi-modal model
  * 3 = Log-normal bi-modal distribution
  * 4 = Phase functions from external file
:Example: ``AER.Model 0``

Aerosol Files
~~~~~~~~~~~~~

AER.DirMie *
^^^^^^^^^^^^

**Directory for aerosol Mie calculation files**

:Type: String (path)
:Example: ``AER.DirMie /data/osoaa/aerosols/mie/``

AER.MieLog
^^^^^^^^^^

**Log file for aerosol Mie calculations**

:Type: String (filename)
:Example: ``AER.MieLog AER_MIE_LOG.txt``
:Default: ``AER_MIE_LOG.txt``

AER.Log
^^^^^^^

**Log file for aerosol radiative properties**

:Type: String (filename)
:Example: ``AER.Log AER_LOG.txt``
:Default: ``AER_LOG.txt``

AER.ResFile.IOP
^^^^^^^^^^^^^^^

**Output file for aerosol inherent optical properties**

:Type: String (filename)
:Example: ``AER.ResFile.IOP AER_IOP.txt``

Aerosol Optical Properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~

AER.AOTref *
^^^^^^^^^^^^

**Aerosol optical thickness at reference wavelength**

:Type: Float
:Range: 0.0-2.0
:Example: ``AER.AOTref 0.1``

Typical values:

* 0.05 = Clean maritime
* 0.1 = Average conditions
* 0.3 = Hazy
* 1.0 = Very turbid

AER.Waref
^^^^^^^^^

**Reference wavelength for AOT**

:Type: Float
:Units: nanometers
:Example: ``AER.Waref 550.0``
:Default: Same as OSOAA.Wa

AER.Angexp
^^^^^^^^^^

**Angström exponent for spectral AOT**

:Type: Float
:Range: 0.0-2.5
:Example: ``AER.Angexp 1.0``

Relates AOT at different wavelengths:

.. math::

   \\tau(\\lambda) = \\tau_{ref} \\left(\\frac{\\lambda_{ref}}{\\lambda}\\right)^\\alpha

Typical values:

* 0.5 = Large particles (maritime)
* 1.0 = Average
* 1.5-2.0 = Small particles (urban, biomass burning)

Mono-Modal Aerosol (Model=0)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

AER.MMD.MRwa *
^^^^^^^^^^^^^^

**Real part of refractive index**

:Type: Float
:Range: 1.3-1.6
:Example: ``AER.MMD.MRwa 1.45``

Common values:

* 1.40 = Water-soluble
* 1.45 = Average
* 1.53 = Mineral dust

AER.MMD.MIwa *
^^^^^^^^^^^^^^

**Imaginary part of refractive index**

:Type: Float
:Range: 0.0-0.05
:Example: ``AER.MMD.MIwa 0.001``

* 0.0 = Non-absorbing
* 0.001 = Weakly absorbing
* 0.01 = Moderately absorbing (dust)
* 0.05 = Strongly absorbing (soot)

AER.MMD.SDtype *
^^^^^^^^^^^^^^^^

**Size distribution type**

:Type: Integer
:Values:
  * 1 = Junge power law
  * 2 = Log-normal distribution
:Example: ``AER.MMD.SDtype 2``

AER.MMD.SDradius *
^^^^^^^^^^^^^^^^^^

**Characteristic radius**

:Type: Float
:Units: micrometers (µm)
:Range: 0.01-10 µm
:Example: ``AER.MMD.SDradius 0.15``

For log-normal: median radius  
For Junge: reference radius

AER.MMD.SDvar *
^^^^^^^^^^^^^^^

**Size distribution variance**

:Type: Float
:Units: dimensionless
:Example: ``AER.MMD.SDvar 0.6``

For log-normal: standard deviation of ln(r)

Ocean Profile Parameters
-------------------------

PROFILE.Sea.File
~~~~~~~~~~~~~~~~

**Ocean profile data file**

:Type: String (filename)
:Example: ``PROFILE.Sea.File MY_OCEAN_PROFILE.txt``
:Default: ``PROFILE_SEA_DEFAULT.txt``

PROFILE.Sea.Depth *
~~~~~~~~~~~~~~~~~~~

**Maximum ocean depth**

:Type: Float
:Units: meters
:Range: 10-1000 m
:Example: ``PROFILE.Sea.Depth 100.0``

Hydrosol Parameters
-------------------

HYD.Model *
~~~~~~~~~~~

**Hydrosol model type**

:Type: Integer
:Values:
  * 0 = Bio-optical model (chlorophyll-based)
  * 1 = Phase functions from external file
:Example: ``HYD.Model 0``

HYD.DirMie *
~~~~~~~~~~~~

**Directory for hydrosol Mie files**

:Type: String (path)
:Example: ``HYD.DirMie /data/osoaa/hydrosols/mie/``

HYD.Chl *
~~~~~~~~~

**Chlorophyll-a concentration**

:Type: Float
:Units: mg/m³
:Range: 0.01-100 mg/m³
:Example: ``HYD.Chl 0.1``

Typical values:

* 0.03-0.1 = Oligotrophic (clear ocean)
* 0.1-1.0 = Mesotrophic
* 1.0-10 = Eutrophic (coastal)
* >10 = Hyper-eutrophic (algal bloom)

HYD.ProfilChl
~~~~~~~~~~~~~

**Chlorophyll vertical profile type**

:Type: Integer
:Values:
  * 0 = Homogeneous (constant with depth)
  * 1 = Gaussian profile (deep chlorophyll maximum)
  * 2 = Custom profile from file
:Example: ``HYD.ProfilChl 0``
:Default: 0

Sea Surface Parameters
----------------------

SEA.Dir *
~~~~~~~~~

**Directory for surface property files**

:Type: String (path)
:Example: ``SEA.Dir /data/osoaa/surface/``

SEA.Log
~~~~~~~

**Log file for surface calculations**

:Type: String (filename)
:Example: ``SEA.Log SEA_LOG.txt``
:Default: ``SEA_LOG.txt``

SEA.Ind *
~~~~~~~~~

**Refractive index of seawater**

:Type: Float
:Range: 1.33-1.35
:Example: ``SEA.Ind 1.334``

Standard value: 1.334 (at 550 nm, 20°C)

SEA.Type *
~~~~~~~~~~

**Sea surface type**

:Type: Integer
:Values:
  * 0 = Flat surface (Fresnel)
  * 1 = Rough surface (Cox & Munk)
:Example: ``SEA.Type 1``

SEA.Wind
~~~~~~~~

**Wind speed** (required if SEA.Type=1)

:Type: Float
:Units: m/s
:Range: 0-20 m/s
:Example: ``SEA.Wind 5.0``

Affects surface roughness via Cox & Munk model.

SEA.BotType
~~~~~~~~~~~

**Bottom type** (for shallow water)

:Type: Integer
:Values:
  * 0 = No bottom (deep water)
  * 1 = Black bottom
  * 2 = Clean coral sand
  * 3 = Green algae
  * 4 = Brown algae
  * 5 = Red algae
:Example: ``SEA.BotType 0``
:Default: 0

Output File Parameters
----------------------

SOS.Log
~~~~~~~

**Log file for radiative transfer core**

:Type: String (filename)
:Example: ``SOS.Log SOS_LOG.txt``

SOS.ResFile.Bin *
~~~~~~~~~~~~~~~~~

**Binary output file (Fourier series)**

:Type: String (filename)
:Example: ``SOS.ResFile.Bin LUM_SF.bin``

OSOAA.ResFile.vsVZA *
~~~~~~~~~~~~~~~~~~~~~

**Radiance vs viewing zenith angle**

:Type: String (filename)
:Example: ``OSOAA.ResFile.vsVZA LUM_vsVZA.txt``

OSOAA.ResFile.vsZ
~~~~~~~~~~~~~~~~~

**Radiance vs altitude/depth profile**

:Type: String (filename)
:Example: ``OSOAA.ResFile.vsZ LUM_vsZ.txt``

OSOAA.ResFile.Advanced
~~~~~~~~~~~~~~~~~~~~~~

**Advanced output (all components)**

:Type: String (filename)
:Example: ``OSOAA.ResFile.Advanced LUM_Advanced.txt``

Parameter Validation
--------------------

OSOAA performs validation checks:

* Required parameters are present
* Values are within valid ranges
* File paths exist
* Physical consistency (e.g., AOT ≥ 0)

Common Validation Errors
~~~~~~~~~~~~~~~~~~~~~~~~~

**Missing required parameter**::

    ERROR: Required parameter OSOAA.Wa not specified

**Out of range**::

    ERROR: ANG.Thetas = 95.0 exceeds maximum 90.0

**Invalid file path**::

    ERROR: Cannot access directory: /invalid/path/

Best Practices
--------------

1. **Start with defaults**: Use provided example files
2. **Document changes**: Comment your modifications
3. **Validate physics**: Ensure parameters make physical sense
4. **Check consistency**: Related parameters should be compatible
5. **Test incrementally**: Change one parameter at a time

Example Complete Input File
----------------------------

See :doc:`../examples/basic_simulation` for full working examples.

Next Steps
----------

* :doc:`running_osoaa` - Learn how to execute simulations
* :doc:`output_files` - Understand the results
* :doc:`../reference/parameter_reference` - Complete parameter tables
