Hydrosol Models Tutorial
========================

This tutorial explores ocean particle models (hydrosols) in OSOAA, including phytoplankton, mineral particles, and yellow substance, and their effects on water-leaving radiance.

Overview
--------

OSOAA provides several hydrosol models:

* **Model 0**: Chlorophyll-based bio-optical model
* **Model 1**: Mineral-like particle model
* **Model 2**: Combined chlorophyll + minerals
* **Model 5**: Custom inherent optical properties (IOPs)

These models affect:

* Absorption coefficient: a(λ, z)
* Scattering coefficient: b(λ, z)
* Phase function: P(Θ)
* Backscattering ratio: b_b/b

Learning Objectives
-------------------

After this tutorial, you will be able to:

* Configure chlorophyll-based simulations
* Add mineral particle contributions
* Implement yellow substance absorption
* Use custom IOPs from measurements
* Interpret hydrosol effects on ocean color
* Simulate vertical profile variations

Tutorial 1: Chlorophyll-Based Model
-----------------------------------

The most common approach for ocean color applications.

Oligotrophic Waters
~~~~~~~~~~~~~~~~~~~

Ultra-clean open ocean with very low chlorophyll.

Input file ``oligo_water.txt``::

    # Oligotrophic Water Simulation
    # Very low chlorophyll concentration
    
    OSOAA.Wa 443.0
    
    # Geometric conditions
    OSOAA.View.Phi 0.0
    OSOAA.View.Level 1
    OSOAA.View.Z -0.0
    ANG.Thetas 30.0
    ANG.Rad.NbGauss 40
    ANG.Rad.UserAngFile ANGLE_RAD_DEFAULT.txt
    ANG.Rad.ResFile ANGLES_RAD.txt
    ANG.Mie.NbGauss 83
    
    # Atmospheric profile
    PROFILE.Atm.File PROFILE_ATM_DEFAULT.txt
    PROFILE.Atm.Pressure 1013.25
    PROFILE.Atm.HR 8.0
    PROFILE.Atm.Ha 2.0
    PROFILE.Atm.MO3 0.3
    PROFILE.Atm.Ztoa 60.0
    
    # Clean maritime aerosols
    AER.Model 0
    AER.MMD.MRwa 1.38
    AER.MMD.MIwa 0.0001
    AER.MMD.SDtype 2
    AER.MMD.SDradius 0.5
    AER.MMD.SDvar 0.7
    AER.AOTref 0.05
    AER.Waref 550.0
    AER.Angexp 0.5
    
    # Sea profile
    PROFILE.Sea.File PROFILE_SEA_DEFAULT.txt
    PROFILE.Sea.Depth 100.0
    
    # ===== HYDROSOL MODEL: Chlorophyll only =====
    HYD.Model 0
    HYD.DirMie ./data/hydrosols/mie/
    
    # Very low chlorophyll (oligotrophic)
    HYD.Chl 0.01             # mg/m³ (South Pacific Gyre)
    HYD.ProfilChl 0          # Homogeneous profile
    
    # Yellow substance (minimal in open ocean)
    HYD.abs.Yellow 0.005     # Absorption at 440 nm (m⁻¹)
    HYD.slope.Yellow 0.015   # Spectral slope (nm⁻¹)
    
    # Sea surface
    SEA.Dir ./data/surface/
    SEA.Ind 1.334
    SEA.Type 1
    SEA.Wind 3.0
    
    # Output
    SOS.ResFile.Bin LUM_SF_oligo.bin
    OSOAA.ResFile.vsVZA LUM_vsVZA_oligo.txt
    OSOAA.ResFile.Advanced LUM_Advanced_oligo.txt

**Characteristics**:

* Chl < 0.03 mg/m³
* Secchi depth > 30 m
* Strong blue color
* Maximum clarity
* Rayleigh scattering dominates

Mesotrophic Waters
~~~~~~~~~~~~~~~~~~

Moderate productivity, typical coastal waters::

    HYD.Chl 0.5              # mg/m³ (coastal ocean)
    HYD.abs.Yellow 0.02      # Slightly more CDOM

**Characteristics**:

* Chl = 0.1-1.0 mg/m³
* Secchi depth 10-20 m
* Blue-green color
* Balanced optical properties

Eutrophic Waters
~~~~~~~~~~~~~~~~

High productivity, nutrient-rich waters::

    HYD.Chl 10.0             # mg/m³ (productive coastal/upwelling)
    HYD.abs.Yellow 0.05      # Higher CDOM from biological activity

**Characteristics**:

* Chl > 3 mg/m³
* Secchi depth < 5 m
* Green to yellow-green color
* Strong chlorophyll absorption

Chlorophyll Series
~~~~~~~~~~~~~~~~~~

Run simulations across trophic gradient::

    #!/bin/bash
    
    # Chlorophyll concentrations spanning ocean types
    CHL_VALUES=(0.01 0.03 0.1 0.3 1.0 3.0 10.0 30.0)
    
    for chl in "${CHL_VALUES[@]}"; do
        echo "Running Chl = $chl mg/m³"
        sed "s/HYD.Chl .*/HYD.Chl $chl/" oligo_water.txt > temp_chl${chl}.txt
        sed -i "s/oligo/chl${chl}/g" temp_chl${chl}.txt
        cd exe/
        ./OSOAA_MAIN.exe < ../temp_chl${chl}.txt
        cd ..
    done

Analysis Script
~~~~~~~~~~~~~~~

::

    import numpy as np
    import matplotlib.pyplot as plt
    
    chl_values = [0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0]
    radiance_443 = []
    radiance_555 = []
    
    for chl in chl_values:
        try:
            data = np.loadtxt(f'exe/LUM_vsVZA_chl{chl}.txt', skiprows=5)
            idx = np.argmin(np.abs(data[:, 0]))
            radiance_443.append(data[idx, 1])
        except:
            radiance_443.append(np.nan)
    
    # Plot
    plt.figure(figsize=(10, 6))
    plt.semilogx(chl_values, radiance_443, 'o-', linewidth=2, markersize=8)
    plt.xlabel('Chlorophyll-a (mg/m³)', fontsize=12)
    plt.ylabel('Lwn at 443 nm (W/m²/sr/nm)', fontsize=12)
    plt.title('Water-Leaving Radiance vs. Chlorophyll', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.show()

**Expected Behavior**:

* Blue radiance (443 nm) decreases with Chl
* Green radiance (555 nm) peaks at moderate Chl
* Maximum radiance shifts from blue to green

Tutorial 2: Mineral Particle Model
----------------------------------

Simulate mineral-rich waters (coastal, riverine influence).

Configuration
~~~~~~~~~~~~~

Input file ``mineral_particles.txt``::

    # Mineral Particle Simulation
    # Coastal water with suspended sediments
    
    OSOAA.Wa 550.0
    
    # [Standard geometric and atmospheric setup]
    
    # ===== HYDROSOL MODEL: Mineral particles =====
    HYD.Model 1
    HYD.DirMie ./data/hydrosols/mie/
    
    # Mineral particle properties
    HYD.MRL.MRwa 1.15        # Real refractive index (suspended sediment)
    HYD.MRL.MIwa 0.001       # Imaginary part (weakly absorbing)
    HYD.MRL.SDtype 2         # Log-normal distribution
    HYD.MRL.SDradius 2.0     # Median radius (µm) - larger than phytoplankton
    HYD.MRL.SDvar 0.8        # Broad size distribution
    
    # Mineral concentration
    HYD.MRL.Csed 5.0         # Suspended sediment concentration (g/m³)
    
    # Vertical profile (homogeneous)
    HYD.ProfilMRL 0
    
    # Yellow substance
    HYD.abs.Yellow 0.05      # Often correlated with riverine input
    HYD.slope.Yellow 0.015
    
    # [Sea surface and output as before]

**Key Parameters**:

* **MRwa = 1.15**: Typical for quartz, clay minerals
* **MIwa = 0.001**: Weakly absorbing
* **SDradius = 2.0 µm**: Larger than phytoplankton (0.5-1.0 µm)
* **Csed**: Mass concentration of suspended sediments

Sediment Load Effects
~~~~~~~~~~~~~~~~~~~~~

Test different sediment concentrations::

    #!/bin/bash
    
    # Sediment loads: 1, 5, 10, 20 g/m³
    for sed in 1 5 10 20; do
        echo "Running Csed = $sed g/m³"
        sed "s/HYD.MRL.Csed .*/HYD.MRL.Csed $sed.0/" mineral_particles.txt > temp_sed${sed}.txt
        sed -i "s/mineral_particles/sed${sed}/g" temp_sed${sed}.txt
        ./OSOAA_MAIN.exe < temp_sed${sed}.txt
    done

**Expected Behavior**:

* Increased backscattering
* Flatter spectral shape
* Reduced water penetration
* Higher turbidity

Physical Interpretation
~~~~~~~~~~~~~~~~~~~~~~~

**Low sediment (< 2 g/m³)**:

* Clear coastal water
* Sediment resuspension from bottom
* Moderate visibility

**Medium sediment (2-10 g/m³)**:

* Turbid coastal water
* River plumes
* Poor visibility

**High sediment (> 10 g/m³)**:

* Very turbid water
* Near-shore, estuarine
* Very poor visibility
* Dominant scattering

Tutorial 3: Combined Chlorophyll + Minerals
-------------------------------------------

Realistic coastal waters with both biological and mineral contributions.

Configuration
~~~~~~~~~~~~~

Input file ``coastal_water.txt``::

    # Coastal Water with Phytoplankton and Sediments
    
    OSOAA.Wa 550.0
    
    # [Standard setup]
    
    # ===== HYDROSOL MODEL: Combined =====
    HYD.Model 2
    HYD.DirMie ./data/hydrosols/mie/
    
    # Phytoplankton (biological component)
    HYD.Chl 1.0              # mg/m³ (moderate productivity)
    HYD.ProfilChl 0
    
    # Mineral particles (terrigenous component)
    HYD.MRL.MRwa 1.15
    HYD.MRL.MIwa 0.001
    HYD.MRL.SDtype 2
    HYD.MRL.SDradius 2.0
    HYD.MRL.SDvar 0.8
    HYD.MRL.Csed 3.0         # g/m³ (coastal turbidity)
    HYD.ProfilMRL 0
    
    # Yellow substance (CDOM from rivers and biology)
    HYD.abs.Yellow 0.1       # High CDOM
    HYD.slope.Yellow 0.017
    
    # [Rest as before]

Scenarios
~~~~~~~~~

**Case 1: River Plume**

High sediment, moderate Chl, high CDOM::

    HYD.Chl 2.0
    HYD.MRL.Csed 10.0
    HYD.abs.Yellow 0.5

**Case 2: Upwelling Zone**

High Chl, low sediment, low CDOM::

    HYD.Chl 15.0
    HYD.MRL.Csed 0.5
    HYD.abs.Yellow 0.02

**Case 3: Coastal Eutrophic**

High Chl, moderate sediment, moderate CDOM::

    HYD.Chl 8.0
    HYD.MRL.Csed 4.0
    HYD.abs.Yellow 0.15

Comparison
~~~~~~~~~~

::

    #!/bin/bash
    
    # River plume
    sed 's/HYD.Chl .*/HYD.Chl 2.0/' coastal_water.txt > temp_river.txt
    sed -i 's/HYD.MRL.Csed .*/HYD.MRL.Csed 10.0/' temp_river.txt
    sed -i 's/HYD.abs.Yellow .*/HYD.abs.Yellow 0.5/' temp_river.txt
    sed -i 's/coastal_water/river_plume/g' temp_river.txt
    ./OSOAA_MAIN.exe < temp_river.txt
    
    # Upwelling
    sed 's/HYD.Chl .*/HYD.Chl 15.0/' coastal_water.txt > temp_upwell.txt
    sed -i 's/HYD.MRL.Csed .*/HYD.MRL.Csed 0.5/' temp_upwell.txt
    sed -i 's/HYD.abs.Yellow .*/HYD.abs.Yellow 0.02/' temp_upwell.txt
    sed -i 's/coastal_water/upwelling/g' temp_upwell.txt
    ./OSOAA_MAIN.exe < temp_upwell.txt

Tutorial 4: Yellow Substance (CDOM)
-----------------------------------

Colored Dissolved Organic Matter absorption effects.

CDOM Model
~~~~~~~~~~

CDOM absorption follows an exponential spectral model:

.. math::

   a_{CDOM}(\\lambda) = a_{CDOM}(\\lambda_0) \\exp[-S(\\lambda - \\lambda_0)]

where:

* a_CDOM(440) is the absorption at 440 nm reference
* S is the spectral slope (typically 0.010-0.020 nm⁻¹)

Configuration
~~~~~~~~~~~~~

::

    # Different CDOM levels
    
    # Oligotrophic open ocean (minimal CDOM)
    HYD.abs.Yellow 0.005
    HYD.slope.Yellow 0.015
    
    # Coastal water (moderate CDOM)
    HYD.abs.Yellow 0.05
    HYD.slope.Yellow 0.017
    
    # River-influenced (high CDOM)
    HYD.abs.Yellow 0.5
    HYD.slope.Yellow 0.018
    
    # Boreal lakes (very high CDOM)
    HYD.abs.Yellow 2.0
    HYD.slope.Yellow 0.020

CDOM Series
~~~~~~~~~~~

::

    #!/bin/bash
    
    # CDOM absorption at 440 nm
    CDOM_VALUES=(0.005 0.01 0.02 0.05 0.1 0.2 0.5 1.0)
    
    for cdom in "${CDOM_VALUES[@]}"; do
        echo "Running CDOM = $cdom m⁻¹"
        sed "s/HYD.abs.Yellow .*/HYD.abs.Yellow $cdom/" oligo_water.txt > temp_cdom${cdom}.txt
        sed -i "s/oligo/cdom${cdom}/g" temp_cdom${cdom}.txt
        ./OSOAA_MAIN.exe < temp_cdom${cdom}.txt
    done

**Effects of CDOM**:

* Strong absorption in blue (400-500 nm)
* Exponentially decreasing toward red
* Reduces blue radiance significantly
* Shifts peak from blue to green
* No scattering contribution

Tutorial 5: Vertical Profiles
-----------------------------

Simulate depth-varying chlorophyll distributions.

Profile Types
~~~~~~~~~~~~~

OSOAA supports several profile shapes:

* **ProfilChl = 0**: Homogeneous (constant with depth)
* **ProfilChl = 1**: Gaussian profile (Deep Chlorophyll Maximum)
* **ProfilChl = 2**: Custom profile from file

Gaussian Profile (DCM)
~~~~~~~~~~~~~~~~~~~~~~

Deep Chlorophyll Maximum is common in stratified waters::

    HYD.Model 0
    HYD.Chl 0.2              # Surface chlorophyll (mg/m³)
    HYD.ProfilChl 1          # Gaussian profile
    
    # Gaussian parameters
    HYD.Chlprof.zmax 50.0    # Depth of maximum (m)
    HYD.Chlprof.Cmax 1.5     # Maximum Chl at DCM (mg/m³)
    HYD.Chlprof.sig 20.0     # Width of Gaussian (m)

**Physical Interpretation**:

* Surface: 0.2 mg/m³ (nutrient-depleted)
* DCM at 50 m: 1.5 mg/m³ (optimal light + nutrients)
* Gaussian width: 20 m (gradual transition)

Profile Equation
~~~~~~~~~~~~~~~~

.. math::

   Chl(z) = Chl_{surf} + (Chl_{max} - Chl_{surf}) \\exp\\left[-\\frac{(z - z_{max})^2}{2\\sigma^2}\\right]

Scenarios
~~~~~~~~~

**Shallow coastal DCM**::

    HYD.Chlprof.zmax 20.0
    HYD.Chlprof.Cmax 3.0
    HYD.Chlprof.sig 10.0

**Deep ocean DCM**::

    HYD.Chlprof.zmax 80.0
    HYD.Chlprof.Cmax 0.8
    HYD.Chlprof.sig 15.0

**Intense bloom layer**::

    HYD.Chlprof.zmax 10.0
    HYD.Chlprof.Cmax 20.0
    HYD.Chlprof.sig 5.0

Custom Profile
~~~~~~~~~~~~~~

For measured profiles, create a file ``chl_profile.txt``::

    # Depth (m)  Chlorophyll (mg/m³)
    0.0          0.15
    5.0          0.18
    10.0         0.25
    20.0         0.50
    30.0         0.80
    40.0         1.20
    50.0         1.50
    60.0         1.30
    70.0         0.90
    80.0         0.50
    90.0         0.30
    100.0        0.20

Configure::

    HYD.ProfilChl 2
    HYD.ProfilChlFile chl_profile.txt

Tutorial 6: Custom IOPs
-----------------------

Use measured inherent optical properties.

Motivation
~~~~~~~~~~

For validation or specific case studies, you may have:

* In-situ measurements of absorption
* Scattering coefficients from instruments
* Custom phase functions

Configuration
~~~~~~~~~~~~~

::

    # Custom IOP model
    HYD.Model 5
    
    # Absorption profile file
    HYD.abs.File absorption_profile.txt
    
    # Scattering profile file
    HYD.scat.File scattering_profile.txt
    
    # Phase function file (optional)
    HYD.phase.File phase_function.txt

File Formats
~~~~~~~~~~~~

**Absorption profile** (``absorption_profile.txt``)::

    # Depth (m)  Total absorption (m⁻¹)
    0.0          0.050
    10.0         0.055
    20.0         0.065
    30.0         0.080
    40.0         0.070
    50.0         0.055

**Scattering profile** (``scattering_profile.txt``)::

    # Depth (m)  Total scattering (m⁻¹)  Backscattering ratio
    0.0          0.15                    0.015
    10.0         0.18                    0.016
    20.0         0.25                    0.018
    30.0         0.30                    0.020
    40.0         0.22                    0.017
    50.0         0.16                    0.015

**Phase function** (optional, ``phase_function.txt``)::

    # Scattering angle (deg)  Phase function
    0.0                        100.0
    10.0                       25.0
    20.0                       8.5
    30.0                       4.2
    ...
    180.0                      0.5

Best Practices
--------------

Choosing Hydrosol Models
~~~~~~~~~~~~~~~~~~~~~~~~

1. **Use Model 0 (Chl-based)** for:
   
   * Standard ocean color applications
   * Open ocean case 1 waters
   * Phytoplankton-dominated systems

2. **Use Model 1 (Minerals)** for:
   
   * Sediment transport studies
   * Coastal erosion impacts
   * River plume tracking

3. **Use Model 2 (Combined)** for:
   
   * Realistic coastal simulations
   * Case 2 waters
   * Mixed optically complex waters

4. **Use Model 5 (Custom)** for:
   
   * Validation against field measurements
   * Unusual water types
   * Research on specific locations

Typical Parameter Ranges
~~~~~~~~~~~~~~~~~~~~~~~~

**Chlorophyll**:

* Ultra-oligotrophic: 0.01-0.03 mg/m³
* Oligotrophic: 0.03-0.1 mg/m³
* Mesotrophic: 0.1-1.0 mg/m³
* Eutrophic: 1.0-10 mg/m³
* Hyper-eutrophic: > 10 mg/m³

**Sediment concentration**:

* Clear water: < 1 g/m³
* Slight turbidity: 1-5 g/m³
* Moderate turbidity: 5-20 g/m³
* High turbidity: 20-100 g/m³
* Extreme turbidity: > 100 g/m³

**CDOM absorption at 440 nm**:

* Open ocean: 0.005-0.02 m⁻¹
* Coastal: 0.02-0.2 m⁻¹
* River-influenced: 0.2-1.0 m⁻¹
* Lakes/estuaries: 1.0-5.0 m⁻¹

Common Mistakes
---------------

1. **Unit confusion**:
   
   * Chlorophyll: mg/m³ (not µg/L, though numerically equal)
   * Sediment: g/m³ (not mg/L)
   * Absorption: m⁻¹ (not cm⁻¹)

2. **Unrealistic combinations**:
   
   * High Chl with very high CDOM (usually correlated but not extreme)
   * Zero sediment with high turbidity

3. **Profile inconsistencies**:
   
   * DCM deeper than total depth
   * Negative concentrations

4. **Neglecting CDOM**:
   
   * Even open ocean has some CDOM (~0.005 m⁻¹)

Validation
----------

Compare with field measurements::

    # For oligotrophic waters at 443 nm:
    # Expected Rrs: 0.004-0.008 sr⁻¹
    # Expected bb/(a+bb): 0.3-0.5
    
    # For eutrophic waters at 555 nm:
    # Expected Rrs: 0.005-0.015 sr⁻¹
    # Expected bb/(a+bb): 0.1-0.3

Analysis Tools
--------------

Remote Sensing Reflectance
~~~~~~~~~~~~~~~~~~~~~~~~~~

Calculate Rrs from Lwn::

    import numpy as np
    
    # Convert Lwn to Rrs
    # Rrs = Lwn / Ed(0+)
    # Approximate Ed(0+) for clear sky, SZA=30°
    Ed_0plus = 1.5  # W/m²/nm at 550 nm
    
    Lwn = 0.05  # From OSOAA output
    Rrs = Lwn / Ed_0plus
    print(f"Rrs = {Rrs:.4f} sr⁻¹")

Diffuse Attenuation
~~~~~~~~~~~~~~~~~~~

From vertical profile output::

    import numpy as np
    
    # Load vertical profile
    data = np.loadtxt('LUM_vsZ.txt', skiprows=5)
    depth = data[:, 0]
    Ed = data[:, 1]  # Downwelling irradiance
    
    # Calculate Kd
    Kd = -np.gradient(np.log(Ed), depth)
    
    # Average over euphotic zone
    idx_eu = depth <= 3.0  # First 3 meters
    Kd_mean = np.mean(Kd[idx_eu])
    print(f"Kd = {Kd_mean:.3f} m⁻¹")

Next Steps
----------

* :doc:`rough_surface` - Combine hydrosols with surface effects
* :doc:`custom_profiles` - Advanced vertical structure
* :doc:`../science/ocean_model` - Theoretical background
* :doc:`../reference/parameter_reference` - Complete parameter listing

Further Reading
---------------

* Morel, A. and Maritorena, S. (2001) "Bio-optical properties of oceanic waters"
* Babin et al. (2003) "Variations in the light absorption coefficients of phytoplankton, nonalgal particles, and dissolved organic matter"
* Gordon, H.R. and Morel, A. (1983) "Remote assessment of ocean color for interpretation of satellite visible imagery"
* IOCCG Report Series - "Remote Sensing of Inherent Optical Properties"
