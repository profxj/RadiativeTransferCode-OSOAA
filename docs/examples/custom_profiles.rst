Custom Profiles Tutorial
========================

This tutorial demonstrates how to use custom vertical profiles in OSOAA, including atmospheric profiles, ocean profiles, and measured optical properties. This is essential for validation studies and specific case simulations.

Overview
--------

OSOAA allows custom profiles for:

* **Atmospheric profiles**: Temperature, pressure, molecular density, ozone
* **Aerosol profiles**: Vertical distribution of aerosol optical thickness
* **Ocean profiles**: Temperature, salinity, density
* **Chlorophyll profiles**: Measured or modeled phytoplankton distributions
* **Mineral profiles**: Suspended sediment vertical structure
* **IOP profiles**: Direct absorption and scattering measurements

These profiles override default parameterizations for maximum realism.

Learning Objectives
-------------------

After this tutorial, you will:

* Create atmospheric profile files
* Define custom chlorophyll vertical distributions
* Use measured IOP profiles
* Simulate deep chlorophyll maxima (DCM)
* Model river plumes and fronts
* Validate against field measurements

Tutorial 1: Custom Atmospheric Profile
--------------------------------------

For specific locations or conditions beyond standard atmosphere.

Profile File Format
~~~~~~~~~~~~~~~~~~~

Create ``custom_atmosphere.txt``::

    # Custom Atmospheric Profile
    # Altitude (km)  Temperature (K)  Pressure (hPa)  Molecular density  Ozone density
    0.0              288.15           1013.25          2.55e19            5.0e11
    1.0              281.65           902.0            2.27e19            5.5e11
    2.0              275.15           795.0            2.03e19            6.0e11
    5.0              255.65           540.0            1.45e19            8.0e11
    10.0             223.15           265.0            7.87e18            1.2e12
    15.0             216.65           121.0            3.72e18            2.5e12
    20.0             216.65           55.3             1.70e18            4.0e12
    30.0             226.65           12.0             3.50e17            6.0e12
    40.0             250.65           2.9              7.71e16            4.0e12
    50.0             270.65           0.8              1.97e16            1.5e12
    60.0             247.15           0.2              5.37e15            3.0e11

**Column Descriptions**:

1. **Altitude** (km): Height above sea level
2. **Temperature** (K): Atmospheric temperature
3. **Pressure** (hPa or mb): Air pressure
4. **Molecular density** (molecules/cm³): Air molecule number density
5. **Ozone density** (molecules/cm³): O₃ concentration

Configuration
~~~~~~~~~~~~~

Input file using custom atmosphere::

    # Use custom atmospheric profile
    PROFILE.Atm.File custom_atmosphere.txt
    
    # These parameters may be overridden by file:
    PROFILE.Atm.Pressure 1013.25     # Surface pressure
    PROFILE.Atm.HR 8.0               # Rayleigh scale height
    PROFILE.Atm.Ha 2.0               # Aerosol scale height
    PROFILE.Atm.MO3 0.3              # Ozone column (atm-cm)
    PROFILE.Atm.Ztoa 60.0            # Top of atmosphere

Physical Considerations
~~~~~~~~~~~~~~~~~~~~~~~

Ensure profile is physically consistent:

* Temperature decreases with altitude (lapse rate)
* Pressure decreases exponentially
* Molecular density follows ideal gas law: n = P/(kT)
* Ozone peaks in stratosphere (20-30 km)

Example: Tropical Atmosphere
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Warmer, higher tropopause::

    # Tropical profile
    0.0    300.0    1010.0    2.49e19    5.0e11
    1.0    293.0    898.0     2.22e19    5.5e11
    2.0    286.0    795.0     2.00e19    6.0e11
    5.0    263.0    540.0     1.42e19    8.0e11
    10.0   233.0    265.0     7.50e18    1.2e12
    15.0   205.0    121.0     3.90e18    2.5e12
    # ... (higher tropopause at ~17 km)

Example: Polar Atmosphere
~~~~~~~~~~~~~~~~~~~~~~~~~

Colder, lower tropopause::

    # Polar profile
    0.0    260.0    1013.0    2.72e19    5.0e11
    1.0    253.0    902.0     2.49e19    5.5e11
    2.0    246.0    795.0     2.26e19    6.0e11
    5.0    226.0    540.0     1.67e19    8.0e11
    10.0   213.0    265.0     8.70e18    1.2e12
    # ... (lower tropopause at ~8 km)

Tutorial 2: Gaussian Chlorophyll Profile (DCM)
----------------------------------------------

Deep Chlorophyll Maximum is common in stratified waters.

Configuration
~~~~~~~~~~~~~

::

    # Gaussian chlorophyll profile
    HYD.Model 0
    HYD.ProfilChl 1          # Gaussian profile type
    
    # Surface chlorophyll
    HYD.Chl 0.15             # mg/m³ (oligotrophic surface)
    
    # DCM parameters
    HYD.Chlprof.zmax 60.0    # Depth of maximum (m)
    HYD.Chlprof.Cmax 1.2     # Chlorophyll at DCM (mg/m³)
    HYD.Chlprof.sig 15.0     # Gaussian width (m)

Mathematical Form
~~~~~~~~~~~~~~~~~

The Gaussian profile is:

.. math::

   Chl(z) = Chl_{surf} + (Chl_{max} - Chl_{surf}) \\exp\\left[-\\frac{(z - z_{max})^2}{2\\sigma^2}\\right]

Scenarios
~~~~~~~~~

**Shallow Coastal DCM**::

    HYD.Chlprof.zmax 25.0    # Shallow DCM
    HYD.Chlprof.Cmax 3.0     # Strong DCM
    HYD.Chlprof.sig 10.0     # Narrow layer

**Deep Ocean DCM**::

    HYD.Chlprof.zmax 80.0    # Deep DCM
    HYD.Chlprof.Cmax 0.8     # Weak DCM
    HYD.Chlprof.sig 20.0     # Broad layer

**Multiple Maxima** (use custom profile for this)

Visualization
~~~~~~~~~~~~~

::

    import numpy as np
    import matplotlib.pyplot as plt
    
    def gaussian_chl_profile(z, chl_surf, z_max, chl_max, sigma):
        """Calculate Gaussian chlorophyll profile"""
        return chl_surf + (chl_max - chl_surf) * np.exp(-(z - z_max)**2 / (2 * sigma**2))
    
    # Depth array
    z = np.linspace(0, 150, 200)
    
    # Different scenarios
    shallow = gaussian_chl_profile(z, 0.15, 25, 3.0, 10)
    moderate = gaussian_chl_profile(z, 0.15, 60, 1.2, 15)
    deep = gaussian_chl_profile(z, 0.15, 80, 0.8, 20)
    
    # Plot
    plt.figure(figsize=(8, 10))
    plt.plot(shallow, z, 'r-', linewidth=2, label='Shallow Coastal')
    plt.plot(moderate, z, 'g-', linewidth=2, label='Moderate (Standard)')
    plt.plot(deep, z, 'b-', linewidth=2, label='Deep Ocean')
    plt.gca().invert_yaxis()
    plt.xlabel('Chlorophyll-a (mg/m³)', fontsize=12)
    plt.ylabel('Depth (m)', fontsize=12)
    plt.title('Gaussian Chlorophyll Profiles', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 3.5)
    plt.show()

Effects on Remote Sensing
~~~~~~~~~~~~~~~~~~~~~~~~~

Run simulations with different DCM depths::

    #!/bin/bash
    
    # DCM depth series
    for zmax in 20 40 60 80 100; do
        echo "Running DCM at depth = $zmax m"
        sed "s/HYD.Chlprof.zmax .*/HYD.Chlprof.zmax $zmax.0/" gaussian_profile.txt > temp_dcm${zmax}.txt
        sed -i "s/gaussian_profile/dcm${zmax}/g" temp_dcm${zmax}.txt
        cd exe/
        ./OSOAA_MAIN.exe < ../temp_dcm${zmax}.txt
        cd ..
    done

**Expected Results**:

* Shallow DCM (20 m): Strong influence on remote sensing
* Moderate DCM (60 m): Detectable in blue-green wavelengths
* Deep DCM (100 m): Minimal remote sensing signature

Tutorial 3: Custom Chlorophyll Profile File
--------------------------------------------

For measured or complex non-Gaussian profiles.

File Format
~~~~~~~~~~~

Create ``measured_chl_profile.txt``::

    # Measured Chlorophyll Profile
    # Station: ABC-123
    # Date: 2024-03-15
    # Location: 35.5°N, 25.3°W
    #
    # Depth (m)    Chlorophyll-a (mg/m³)
    0.0            0.18
    5.0            0.20
    10.0           0.25
    15.0           0.35
    20.0           0.50
    25.0           0.70
    30.0           0.95
    35.0           1.15
    40.0           1.28
    45.0           1.35
    50.0           1.30
    55.0           1.15
    60.0           0.95
    70.0           0.65
    80.0           0.45
    90.0           0.30
    100.0          0.22

**Requirements**:

* First column: Depth (m), increasing
* Second column: Chlorophyll concentration (mg/m³)
* Comments start with #
* At least 5-10 depth levels recommended

Configuration
~~~~~~~~~~~~~

::

    HYD.Model 0
    HYD.ProfilChl 2                    # Custom profile from file
    HYD.ProfilChlFile measured_chl_profile.txt

OSOAA will interpolate linearly between specified depths.

Example: Surface Bloom
~~~~~~~~~~~~~~~~~~~~~~

Create ``surface_bloom.txt``::

    # Surface bloom profile
    # High concentration near surface, rapid decrease
    0.0     15.0
    2.0     12.0
    5.0     8.0
    10.0    3.0
    15.0    1.5
    20.0    0.8
    30.0    0.4
    50.0    0.2
    100.0   0.1

Example: Subsurface Layers
~~~~~~~~~~~~~~~~~~~~~~~~~~

Create ``multiple_layers.txt``::

    # Two chlorophyll maxima
    0.0     0.3
    10.0    0.5
    20.0    1.5     # First maximum
    30.0    0.8
    40.0    0.6
    50.0    0.9
    60.0    1.8     # Second maximum (DCM)
    70.0    1.2
    80.0    0.7
    100.0   0.3

Example: River Plume
~~~~~~~~~~~~~~~~~~~~

Horizontal gradients represented as profiles::

    # Near-shore to offshore gradient
    # (depth represents offshore distance conceptually)
    0.0     3.0     # Very turbid near-shore
    2.0     2.5
    5.0     1.8
    10.0    1.0
    20.0    0.5
    50.0    0.2     # Oceanic background

Tutorial 4: Custom Ocean Profile
--------------------------------

Temperature and salinity affect refractive index and optical properties.

File Format
~~~~~~~~~~~

Create ``ocean_profile.txt``::

    # Custom Ocean Profile
    # Depth (m)  Temperature (°C)  Salinity (PSU)  Density (kg/m³)
    0.0          22.5              35.0            1024.0
    10.0         22.3              35.1            1024.2
    20.0         21.8              35.2            1024.5
    30.0         20.5              35.3            1025.0
    50.0         18.0              35.4            1025.8
    75.0         15.0              35.5            1026.5
    100.0        12.5              35.5            1027.0
    150.0        10.0              35.4            1027.3
    200.0        8.5               35.3            1027.5

Configuration
~~~~~~~~~~~~~

::

    PROFILE.Sea.File ocean_profile.txt
    PROFILE.Sea.Depth 200.0

Effects
~~~~~~~

Temperature and salinity affect:

* **Refractive index**: n ≈ 1.334 + f(T, S)
* **Rayleigh scattering**: β_sw ∝ n²
* **Density**: Affects layer structure
* **Absorption**: Temperature-dependent

Typical Values
~~~~~~~~~~~~~~

**Tropical Waters**::

    # Warm, salty, stratified
    0.0    28.0    36.0    1022.5
    50.0   25.0    36.5    1024.0
    100.0  20.0    36.0    1025.5

**Polar Waters**::

    # Cold, fresh, mixed
    0.0    2.0     33.0    1026.5
    50.0   1.5     33.2    1026.8
    100.0  1.0     33.5    1027.0

**Upwelling Zone**::

    # Cold water brought to surface
    0.0    15.0    34.5    1026.0
    20.0   14.0    34.8    1026.5
    50.0   12.0    35.0    1027.0

Tutorial 5: Combined Custom Profiles
------------------------------------

Using multiple custom profiles simultaneously.

Full Custom Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

Input file ``full_custom.txt``::

    # Full Custom Profile Simulation
    # All profiles from measurements
    
    OSOAA.Wa 443.0
    
    # Geometric conditions
    OSOAA.View.Phi 90.0
    OSOAA.View.Level 1
    OSOAA.View.Z -0.0
    ANG.Thetas 35.0
    ANG.Rad.NbGauss 40
    ANG.Rad.UserAngFile ANGLE_RAD_DEFAULT.txt
    ANG.Rad.ResFile ANGLES_RAD.txt
    ANG.Mie.NbGauss 83
    
    # ===== CUSTOM ATMOSPHERIC PROFILE =====
    PROFILE.Atm.File custom_atmosphere.txt
    PROFILE.Atm.Pressure 1015.0
    PROFILE.Atm.HR 8.0
    PROFILE.Atm.Ha 2.0
    PROFILE.Atm.MO3 0.28
    PROFILE.Atm.Ztoa 60.0
    
    # Aerosols (could also be custom vertical profile)
    AER.Model 0
    AER.MMD.MRwa 1.40
    AER.MMD.MIwa 0.002
    AER.MMD.SDtype 2
    AER.MMD.SDradius 0.3
    AER.MMD.SDvar 0.65
    AER.AOTref 0.15
    AER.Waref 550.0
    AER.Angexp 1.2
    
    # ===== CUSTOM OCEAN PROFILE =====
    PROFILE.Sea.File ocean_profile.txt
    PROFILE.Sea.Depth 150.0
    
    # ===== CUSTOM CHLOROPHYLL PROFILE =====
    HYD.Model 0
    HYD.ProfilChl 2
    HYD.ProfilChlFile measured_chl_profile.txt
    
    # Yellow substance
    HYD.abs.Yellow 0.03
    HYD.slope.Yellow 0.016
    
    # Sea surface
    SEA.Dir ./data/surface/
    SEA.Ind 1.334
    SEA.Type 1
    SEA.Wind 6.5
    
    # Output
    SOS.ResFile.Bin LUM_SF_custom.bin
    OSOAA.ResFile.vsVZA LUM_vsVZA_custom.txt
    OSOAA.ResFile.vsZ LUM_vsZ_custom.txt
    OSOAA.ResFile.Advanced LUM_Advanced_custom.txt

Tutorial 6: Custom IOP Profiles
-------------------------------

Most realistic validation using measured absorption and scattering.

Motivation
~~~~~~~~~~

For validation studies, use direct IOP measurements:

* From AC-9, AC-S instruments (absorption)
* From VSF meters (scattering)
* From CTD casts with bio-optical sensors

Absorption Profile
~~~~~~~~~~~~~~~~~~

Create ``absorption_profile.txt``::

    # Measured Total Absorption Coefficient
    # Station: DEF-456
    # Wavelength: 443 nm
    # Date: 2024-06-20
    #
    # Depth (m)    a_total (m⁻¹)
    0.0            0.045
    5.0            0.048
    10.0           0.052
    15.0           0.058
    20.0           0.070
    25.0           0.085
    30.0           0.095
    35.0           0.102
    40.0           0.105
    45.0           0.103
    50.0           0.095
    60.0           0.075
    70.0           0.060
    80.0           0.052
    100.0          0.047

Components (for reference, not used by OSOAA directly):

* a_w (pure water): 0.006 m⁻¹ at 443 nm
* a_ph (phytoplankton): variable
* a_CDOM: variable
* a_NAP (non-algal particles): variable

Scattering Profile
~~~~~~~~~~~~~~~~~~

Create ``scattering_profile.txt``::

    # Measured Scattering Coefficients
    # Wavelength: 443 nm
    #
    # Depth (m)    b_total (m⁻¹)    b_b (m⁻¹)
    0.0            0.180            0.0027
    5.0            0.195            0.0030
    10.0           0.220            0.0035
    15.0           0.260            0.0042
    20.0           0.315            0.0052
    25.0           0.380            0.0065
    30.0           0.425            0.0075
    35.0           0.450            0.0082
    40.0           0.460            0.0085
    45.0           0.455            0.0083
    50.0           0.420            0.0072
    60.0           0.340            0.0055
    70.0           0.275            0.0043
    80.0           0.230            0.0036
    100.0          0.200            0.0031

**Columns**:

1. Depth (m)
2. Total scattering coefficient b(λ, z) (m⁻¹)
3. Backscattering coefficient b_b(λ, z) (m⁻¹)

Note: Backscattering ratio b_b/b typically 0.01-0.02

Phase Function
~~~~~~~~~~~~~~

Optionally provide measured VSF (Volume Scattering Function)::

    # Measured Phase Function
    # Wavelength: 443 nm
    # Normalized to integrate to 4π
    #
    # Angle (deg)    P(Θ)
    0.0              120.0
    1.0              85.0
    2.0              62.0
    5.0              28.0
    10.0             12.5
    20.0             5.2
    30.0             2.8
    45.0             1.5
    60.0             0.9
    90.0             0.6
    120.0            0.5
    150.0            0.4
    180.0            0.4

Configuration
~~~~~~~~~~~~~

::

    # Custom IOP model
    HYD.Model 5
    
    # Provide measured profiles
    HYD.abs.File absorption_profile.txt
    HYD.scat.File scattering_profile.txt
    HYD.phase.File phase_function.txt    # Optional

OSOAA will:

* Interpolate profiles to its vertical grid
* Use provided absorption and scattering directly
* Calculate radiative transfer with measured IOPs

Tutorial 7: Validation Workflow
-------------------------------

Complete workflow for validating OSOAA against measurements.

Step 1: Gather Field Data
~~~~~~~~~~~~~~~~~~~~~~~~~

Collect:

* CTD profile (T, S, depth)
* Chlorophyll fluorescence profile
* IOP measurements (a, b, b_b)
* Incident irradiance (E_d)
* Water-leaving radiance (L_w)
* Meteorological data (wind, pressure)
* Sun angle, viewing geometry

Step 2: Create Profile Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    #!/bin/bash
    
    # Process field data into OSOAA format
    # (Assuming you have raw data files)
    
    # Convert CTD data
    python convert_ctd.py field_ctd_cast.csv > ocean_profile_validation.txt
    
    # Convert chlorophyll fluorescence
    python convert_chl.py field_chl_fluorescence.csv > chl_profile_validation.txt
    
    # Convert IOP data
    python convert_iop.py field_ac9_data.csv > absorption_validation.txt
    python convert_bb.py field_bb9_data.csv > scattering_validation.txt

Step 3: Configure OSOAA
~~~~~~~~~~~~~~~~~~~~~~~

Create ``validation_case.txt`` matching field conditions exactly::

    OSOAA.Wa 443.0           # Match radiometer wavelength
    
    ANG.Thetas 32.5          # Measured solar zenith angle
    OSOAA.View.Phi 135.0     # Measured relative azimuth
    
    # Measured atmospheric conditions
    PROFILE.Atm.Pressure 1018.5    # From weather station
    AER.AOTref 0.12                # From sun photometer
    
    # Custom profiles
    PROFILE.Sea.File ocean_profile_validation.txt
    HYD.ProfilChlFile chl_profile_validation.txt
    HYD.abs.File absorption_validation.txt
    HYD.scat.File scattering_validation.txt
    
    # Measured wind
    SEA.Wind 4.2             # From anemometer

Step 4: Run Simulation
~~~~~~~~~~~~~~~~~~~~~~

::

    cd exe/
    ./OSOAA_MAIN.exe < ../validation_case.txt
    cd ..

Step 5: Compare Results
~~~~~~~~~~~~~~~~~~~~~~~

::

    import numpy as np
    import matplotlib.pyplot as plt
    
    # Load OSOAA output
    osoaa = np.loadtxt('exe/LUM_vsVZA_validation.txt', skiprows=5)
    
    # Load field measurements
    field = np.loadtxt('field_radiance_measurements.txt')
    
    # Wavelengths
    wavelengths = [412, 443, 490, 510, 555, 670]
    
    # Plot comparison
    plt.figure(figsize=(10, 6))
    plt.plot(wavelengths, field[:, 1], 'o', markersize=10, label='Field Measurements')
    plt.plot(wavelengths, osoaa[:, 1], 's', markersize=8, label='OSOAA Simulation')
    plt.xlabel('Wavelength (nm)', fontsize=12)
    plt.ylabel('Water-leaving Radiance (W/m²/sr/nm)', fontsize=12)
    plt.title('Validation: OSOAA vs. Field Measurements', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.show()
    
    # Calculate statistics
    residual = osoaa[:, 1] - field[:, 1]
    rmse = np.sqrt(np.mean(residual**2))
    bias = np.mean(residual)
    rel_error = np.abs(residual / field[:, 1]) * 100
    
    print(f"RMSE: {rmse:.4f} W/m²/sr/nm")
    print(f"Bias: {bias:.4f} W/m²/sr/nm")
    print(f"Mean Relative Error: {np.mean(rel_error):.2f}%")

Best Practices
--------------

Profile Resolution
~~~~~~~~~~~~~~~~~~

* **Atmospheric**: 10-20 levels sufficient, finer near surface
* **Ocean**: 5-10 m resolution in upper 100 m
* **Chlorophyll**: Match optical depth scales (5-20 m)
* **IOPs**: Match instrument depth resolution

Consistency Checks
~~~~~~~~~~~~~~~~~~

1. **Chlorophyll vs. IOPs**: If using both, ensure consistency
2. **Temperature/Salinity**: Must be physically realistic
3. **Profile depth**: Extend beyond penetration depth
4. **Pressure/Altitude**: Check vertical coordinate consistency

Common Errors
~~~~~~~~~~~~~

1. **Wrong units**: Check m vs. km, mg/m³ vs. µg/L
2. **Depth ordering**: Must be monotonically increasing
3. **Missing data**: Gaps cause interpolation issues
4. **Unrealistic values**: Check for sensor errors in field data

Interpolation
~~~~~~~~~~~~~

OSOAA interpolates linearly between depths:

* Provide sufficient vertical resolution
* Avoid large gaps in data
* Extend profiles to simulation boundaries

Performance
~~~~~~~~~~~

Custom profiles have minimal performance impact:

* Files are read once at initialization
* Interpolation is fast
* Main cost is still radiative transfer calculation

Troubleshooting
---------------

Issue: Profile Not Applied
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptoms**: Results identical to default profiles

**Solutions**:

* Check file path and filename
* Verify file format (columns, units)
* Check for parsing errors in log files
* Ensure ProfilChl/ProfilMRL set correctly

Issue: Unrealistic Results
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptoms**: Very high/low radiance, NaN values

**Solutions**:

* Validate profile physically (no negative values)
* Check IOPs are reasonable (a, b > 0)
* Ensure proper units throughout
* Check depth ordering

Issue: Convergence Problems
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptoms**: Slow convergence or non-convergence

**Solutions**:

* Smooth noisy field data before input
* Check for extreme optical property values
* Ensure profile extends to sufficient depth
* Increase maximum iterations if needed

Advanced Topics
---------------

Aerosol Vertical Profiles
~~~~~~~~~~~~~~~~~~~~~~~~~

While less common, aerosol profiles can be customized:

* Modify ``PROFILE.Atm.Ha`` for scale height
* Or create custom aerosol extinction profiles
* Important for tropospheric layers, dust events

Time-Varying Profiles
~~~~~~~~~~~~~~~~~~~~~

For diurnal or tidal effects:

* Create multiple profile files
* Run series of simulations
* Interpolate/animate results

Coupled Bio-Physical Models
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Integrate OSOAA with ecosystem models:

* Export model output as OSOAA profiles
* Run OSOAA for remote sensing simulation
* Validate model with satellite data

Next Steps
----------

* :doc:`../science/ocean_model` - Theoretical background on IOPs
* :doc:`../reference/file_formats` - Detailed file specifications
* :doc:`../reference/parameter_reference` - Complete parameter list
* :doc:`basic_simulation` - Return to basic examples

Further Reading
---------------

* Gordon, H.R. (1989) "Can the Lambert-Beer law be applied to the diffuse attenuation coefficient?"
* Kirk, J.T.O. (2011) "Light and Photosynthesis in Aquatic Ecosystems" - Profiles and optical properties
* Cullen, J.J. (2015) "Subsurface Chlorophyll Maximum Layers" - DCM formation and characteristics
* Mobley, C.D. (1994) "Light and Water" - Radiative transfer with vertical structure
* Claustre, H. et al. (2008) "Bio-optical profiling floats as new observational tools"

Example: Complete Field Campaign
--------------------------------

Putting it all together for a realistic validation.

Campaign: Coastal Upwelling Study
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Location**: California Current (35°N, 122°W)

**Date**: July 15, 2024, 14:30 UTC

**Conditions**: Active upwelling, high productivity

Field Measurements
~~~~~~~~~~~~~~~~~~

1. CTD profile to 150 m
2. AC-9 absorption/attenuation
3. ECO BB9 backscattering
4. Fluorometer chlorophyll
5. CDOM fluorescence
6. HyperPro radiometry (E_d, L_u)
7. Weather station (P, T, wind)
8. Sun photometer (AOT)

Data Processing
~~~~~~~~~~~~~~~

Convert all measurements to OSOAA format, matching wavelength 443 nm.

OSOAA Configuration
~~~~~~~~~~~~~~~~~~~

Use all custom profiles, measured aerosols, exact geometry::

    # Complete field validation case
    OSOAA.Wa 443.0
    ANG.Thetas 28.3              # Measured SZA
    OSOAA.View.Phi 112.0         # Measured azimuth
    
    # Field conditions
    PROFILE.Atm.Pressure 1015.2
    AER.AOTref 0.08              # Sun photometer
    SEA.Wind 8.2                 # Anemometer
    
    # All custom profiles
    PROFILE.Atm.File field_atmosphere_20240715.txt
    PROFILE.Sea.File field_ocean_20240715.txt
    HYD.Model 5
    HYD.abs.File field_absorption_443nm_20240715.txt
    HYD.scat.File field_scattering_443nm_20240715.txt

Expected Agreement
~~~~~~~~~~~~~~~~~~

* Water-leaving radiance: Within 5-10%
* Remote sensing reflectance: Within 0.0005-0.001 sr⁻¹
* Spectral shape: Excellent match

This completes the custom profiles tutorial!
