Basic Simulation Tutorial
=========================

This tutorial walks you through creating and running basic OSOAA simulations, from simple clear water cases to more complex scenarios.

Learning Objectives
-------------------

By the end of this tutorial, you will be able to:

* Set up a minimal OSOAA simulation
* Understand key input parameters
* Run the simulation and interpret results
* Modify parameters to explore different scenarios
* Troubleshoot common issues

Tutorial 1: Clear Water with Minimal Aerosols
---------------------------------------------

This simplest case simulates a clear ocean with low chlorophyll and minimal atmospheric aerosols.

Input File Setup
~~~~~~~~~~~~~~~~

Create ``clear_water.txt``::

    # Clear Water Simulation
    # Minimal aerosol and chlorophyll
    
    # ===== WAVELENGTH =====
    OSOAA.Wa 550.0
    
    # ===== GEOMETRIC CONDITIONS =====
    OSOAA.View.Phi 0.0
    OSOAA.View.Level 1
    OSOAA.View.Z -0.0
    
    ANG.Thetas 30.0
    ANG.Rad.NbGauss 40
    ANG.Rad.UserAngFile ANGLE_RAD_DEFAULT.txt
    ANG.Rad.ResFile ANGLES_RAD.txt
    ANG.Mie.NbGauss 83
    
    # ===== ATMOSPHERIC PROFILE =====
    PROFILE.Atm.File PROFILE_ATM_DEFAULT.txt
    PROFILE.Atm.Pressure 1013.25
    PROFILE.Atm.HR 8.0
    PROFILE.Atm.Ha 2.0
    PROFILE.Atm.MO3 0.3
    PROFILE.Atm.Ztoa 60.0
    
    # ===== AEROSOLS (Minimal) =====
    AER.Model 0
    AER.DirMie ./data/aerosols/mie/
    AER.MMD.MRwa 1.40
    AER.MMD.MIwa 0.001
    AER.MMD.SDtype 2
    AER.MMD.SDradius 0.15
    AER.MMD.SDvar 0.5
    AER.AOTref 0.05
    AER.Waref 550.0
    AER.Angexp 1.0
    
    # ===== SEA PROFILE =====
    PROFILE.Sea.File PROFILE_SEA_DEFAULT.txt
    PROFILE.Sea.Depth 100.0
    
    # ===== HYDROSOLS (Low Chlorophyll) =====
    HYD.Model 0
    HYD.DirMie ./data/hydrosols/mie/
    HYD.Chl 0.03
    HYD.ProfilChl 0
    
    # ===== SEA SURFACE (Calm) =====
    SEA.Dir ./data/surface/
    SEA.Ind 1.334
    SEA.Type 1
    SEA.Wind 2.0
    
    # ===== OUTPUT FILES =====
    SOS.ResFile.Bin LUM_SF_clear.bin
    OSOAA.ResFile.vsVZA LUM_vsVZA_clear.txt
    OSOAA.ResFile.vsZ LUM_vsZ_clear.txt
    OSOAA.ResFile.Advanced LUM_Advanced_clear.txt

Key Parameters
~~~~~~~~~~~~~~

* **Chlorophyll**: 0.03 mg/m³ (oligotrophic waters)
* **AOT**: 0.05 (very clean atmosphere)
* **Wind speed**: 2.0 m/s (calm sea)
* **Solar zenith angle**: 30° (midday conditions)

Run the Simulation
~~~~~~~~~~~~~~~~~~

Execute::

    cd exe/
    ./OSOAA_MAIN.exe < ../clear_water.txt

Expected Runtime
~~~~~~~~~~~~~~~~

* **Typical**: 5-15 minutes on modern CPU
* **Memory**: ~500 MB

Expected Results
~~~~~~~~~~~~~~~~

The output file ``LUM_vsVZA_clear.txt`` will contain radiance vs. viewing zenith angle. Expected characteristics:

* **Water-leaving radiance**: ~0.02-0.05 W/m²/sr/nm
* **Peak near nadir**: Maximum radiance at viewing angles near 0°
* **Blue-green color**: Maximum radiance in blue-green wavelengths (if run at multiple wavelengths)
* **Low polarization**: DoLP < 2%

Visualization
~~~~~~~~~~~~~

Plot the results using Python::

    import numpy as np
    import matplotlib.pyplot as plt
    
    # Load data
    data = np.loadtxt('LUM_vsVZA_clear.txt', skiprows=5)
    vza = data[:, 0]  # Viewing zenith angle
    I = data[:, 1]    # Stokes I (total intensity)
    
    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(vza, I, 'b-', linewidth=2)
    plt.xlabel('Viewing Zenith Angle (degrees)', fontsize=12)
    plt.ylabel('Radiance (W/m²/sr/nm)', fontsize=12)
    plt.title('Clear Water Radiance at 550 nm', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.show()

Tutorial 2: Varying Chlorophyll Concentration
---------------------------------------------

This tutorial explores how phytoplankton concentration affects water-leaving radiance.

Chlorophyll Series
~~~~~~~~~~~~~~~~~~

Run simulations for chlorophyll values: 0.01, 0.1, 1.0, 10.0 mg/m³

Create a bash script ``run_chl_series.sh``::

    #!/bin/bash
    
    # Array of chlorophyll values
    CHL_VALUES=(0.01 0.1 1.0 10.0)
    
    for chl in "${CHL_VALUES[@]}"; do
        echo "Running simulation for Chl = $chl mg/m³"
        
        # Copy base input file
        cp clear_water.txt temp_chl_${chl}.txt
        
        # Modify chlorophyll value
        sed -i "s/HYD.Chl .*/HYD.Chl $chl/" temp_chl_${chl}.txt
        
        # Update output filenames
        sed -i "s/LUM_SF_clear.bin/LUM_SF_chl${chl}.bin/" temp_chl_${chl}.txt
        sed -i "s/LUM_vsVZA_clear.txt/LUM_vsVZA_chl${chl}.txt/" temp_chl_${chl}.txt
        sed -i "s/LUM_vsZ_clear.txt/LUM_vsZ_chl${chl}.txt/" temp_chl_${chl}.txt
        sed -i "s/LUM_Advanced_clear.txt/LUM_Advanced_chl${chl}.txt/" temp_chl_${chl}.txt
        
        # Run simulation
        cd exe/
        ./OSOAA_MAIN.exe < ../temp_chl_${chl}.txt
        cd ..
        
        echo "Completed Chl = $chl mg/m³"
    done
    
    echo "All simulations completed!"

Make executable and run::

    chmod +x run_chl_series.sh
    ./run_chl_series.sh

Expected Behavior
~~~~~~~~~~~~~~~~~

As chlorophyll increases from 0.01 to 10.0 mg/m³:

* **Magnitude**: Radiance increases in green (520-570 nm)
* **Spectral shape**: Blue radiance decreases, green increases
* **Color shift**: From blue (oligotrophic) to green (eutrophic)
* **Absorption**: Increased absorption in blue and red wavelengths

Physical Interpretation
~~~~~~~~~~~~~~~~~~~~~~~

* **Low Chl (0.01 mg/m³)**: Ultra-oligotrophic (open ocean gyres)
  
  * Deep Secchi depth (>30 m)
  * Strong Rayleigh scattering dominates
  * Blue color

* **Medium Chl (0.1-1.0 mg/m³)**: Mesotrophic (coastal waters)
  
  * Moderate Secchi depth (10-20 m)
  * Balance between scattering and absorption
  * Blue-green color

* **High Chl (10 mg/m³)**: Eutrophic (productive coastal waters)
  
  * Shallow Secchi depth (<5 m)
  * Strong chlorophyll absorption
  * Green color

Tutorial 3: Multi-Wavelength Simulation
---------------------------------------

Simulate the full visible spectrum from 400-700 nm.

Wavelength Loop Script
~~~~~~~~~~~~~~~~~~~~~~

Create ``run_spectrum.sh``::

    #!/bin/bash
    
    # Wavelength range: 400-700 nm in 25 nm steps
    for wl in {400..700..25}; do
        echo "Running wavelength $wl nm"
        
        # Modify input file
        sed "s/OSOAA.Wa .*/OSOAA.Wa $wl.0/" clear_water.txt > temp_wl_${wl}.txt
        sed -i "s/AER.Waref .*/AER.Waref $wl.0/" temp_wl_${wl}.txt
        sed -i "s/LUM_SF_clear.bin/LUM_SF_wl${wl}.bin/" temp_wl_${wl}.txt
        sed -i "s/LUM_vsVZA_clear.txt/LUM_vsVZA_wl${wl}.txt/" temp_wl_${wl}.txt
        
        # Run
        cd exe/
        ./OSOAA_MAIN.exe < ../temp_wl_${wl}.txt
        cd ..
    done

Combine Results
~~~~~~~~~~~~~~~

Python script to combine spectral results::

    import numpy as np
    import matplotlib.pyplot as plt
    import glob
    
    # Wavelengths
    wavelengths = np.arange(400, 725, 25)
    
    # Storage for radiance at nadir
    radiance_nadir = []
    
    # Load each wavelength
    for wl in wavelengths:
        try:
            data = np.loadtxt(f'exe/LUM_vsVZA_wl{wl}.txt', skiprows=5)
            # Get nadir value (VZA ≈ 0)
            idx_nadir = np.argmin(np.abs(data[:, 0]))
            radiance_nadir.append(data[idx_nadir, 1])
        except:
            radiance_nadir.append(np.nan)
    
    # Plot spectrum
    plt.figure(figsize=(12, 6))
    plt.plot(wavelengths, radiance_nadir, 'o-', linewidth=2, markersize=8)
    plt.xlabel('Wavelength (nm)', fontsize=12)
    plt.ylabel('Nadir Radiance (W/m²/sr/nm)', fontsize=12)
    plt.title('Water-Leaving Radiance Spectrum', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.xlim(390, 710)
    plt.show()

Tutorial 4: Viewing Geometry Effects
------------------------------------

Explore how radiance changes with viewing direction.

Azimuth Angle Series
~~~~~~~~~~~~~~~~~~~~

Modify ``OSOAA.View.Phi`` from 0° to 180° to simulate different azimuth angles::

    #!/bin/bash
    
    # Azimuth angles: 0, 45, 90, 135, 180 degrees
    for phi in 0 45 90 135 180; do
        echo "Running azimuth angle = $phi degrees"
        
        sed "s/OSOAA.View.Phi .*/OSOAA.View.Phi $phi.0/" clear_water.txt > temp_phi_${phi}.txt
        sed -i "s/LUM_vsVZA_clear.txt/LUM_vsVZA_phi${phi}.txt/" temp_phi_${phi}.txt
        
        cd exe/
        ./OSOAA_MAIN.exe < ../temp_phi_${phi}.txt
        cd ..
    done

Physical Meaning
~~~~~~~~~~~~~~~~

* **Phi = 0°**: Principal plane (sun, surface normal, and sensor aligned)
* **Phi = 90°/270°**: Cross-principal plane
* **Phi = 180°**: Backscattering direction (sun behind sensor)

Expected Patterns
~~~~~~~~~~~~~~~~~

* **Maximum radiance**: Often near sun glint direction (depends on surface roughness)
* **Minimum radiance**: In backscattering geometry
* **Polarization**: Maximum in perpendicular plane (Phi ≈ 90°)

Tutorial 5: Solar Zenith Angle Effects
--------------------------------------

Simulate different times of day by varying solar zenith angle.

Solar Angle Series
~~~~~~~~~~~~~~~~~~

::

    #!/bin/bash
    
    # Solar zenith angles: 0, 30, 60, 70 degrees
    for sza in 0 30 60 70; do
        echo "Running SZA = $sza degrees"
        
        sed "s/ANG.Thetas .*/ANG.Thetas $sza.0/" clear_water.txt > temp_sza_${sza}.txt
        sed -i "s/LUM_vsVZA_clear.txt/LUM_vsVZA_sza${sza}.txt/" temp_sza_${sza}.txt
        
        cd exe/
        ./OSOAA_MAIN.exe < ../temp_sza_${sza}.txt
        cd ..
    done

Physical Interpretation
~~~~~~~~~~~~~~~~~~~~~~~

* **SZA = 0°**: Sun at zenith (noon, tropics)
  
  * Shortest atmospheric path
  * Maximum irradiance
  * Minimal atmospheric effects

* **SZA = 30°**: Mid-morning/afternoon
  
  * Typical remote sensing geometry
  * Moderate atmospheric path

* **SZA = 60°**: Early morning/late afternoon
  
  * Longer atmospheric path
  * Increased Rayleigh scattering
  * Stronger polarization

* **SZA = 70°**: Near sunrise/sunset
  
  * Very long atmospheric path
  * Strong atmospheric contribution
  * Lower radiance levels

Common Issues and Solutions
---------------------------

Issue: "Cannot open file" Errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem**: Missing data directories for Mie calculations.

**Solution 1** (Recommended): Remove directory specifications to use internal defaults::

    # Comment out or remove these lines:
    # AER.DirMie ./data/aerosols/mie/
    # HYD.DirMie ./data/hydrosols/mie/
    # SEA.Dir ./data/surface/

**Solution 2**: Create data directories::

    mkdir -p data/aerosols/mie
    mkdir -p data/hydrosols/mie
    mkdir -p data/surface

Issue: Convergence Warnings
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem**: "WARNING: Convergence not achieved"

**Solutions**:

1. Increase angular resolution::

    ANG.Rad.NbGauss 60  # Higher resolution

2. Increase maximum iterations (in code compilation)

3. Check for unrealistic parameter combinations

Issue: Very Long Runtime
~~~~~~~~~~~~~~~~~~~~~~~~

**Problem**: Simulation takes hours instead of minutes.

**Possible causes**:

* High angular resolution
* Rough surface with high wind speed
* Many vertical levels

**Solutions**:

* Reduce ``ANG.Rad.NbGauss`` to 24-30 for testing
* Use flat surface (``SEA.Type 0``) initially
* Simplify vertical profiles

Issue: Unexpected Results
~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem**: Radiance values seem incorrect.

**Checks**:

1. Verify wavelength is correctly set
2. Check chlorophyll units (mg/m³, not µg/L)
3. Ensure realistic parameter ranges
4. Compare with published ocean color data

Validation Exercise
-------------------

Compare your results with expected values from ocean color literature.

Clear Water at 550 nm
~~~~~~~~~~~~~~~~~~~~~

For clear water (Chl = 0.03 mg/m³), nadir viewing, SZA = 30°:

* **Expected Lwn**: ~0.02-0.04 W/m²/sr/nm at 550 nm
* **Blue/Green ratio**: Lwn(443)/Lwn(555) ≈ 0.8-1.2

If your results differ significantly:

1. Check input parameters carefully
2. Verify atmospheric conditions
3. Ensure proper output file interpretation

Next Steps
----------

Now that you've mastered basic simulations, try:

* :doc:`aerosol_models` - Explore different aerosol types
* :doc:`hydrosol_models` - Advanced ocean optical properties
* :doc:`rough_surface` - Sea surface effects
* :doc:`custom_profiles` - Use measured vertical profiles

Additional Resources
--------------------

* :doc:`../user_guide/quickstart` - Quick reference
* :doc:`../user_guide/input_parameters` - Complete parameter list
* :doc:`../reference/parameter_reference` - Parameter details
* :doc:`../reference/faq` - Frequently asked questions

Tips for Success
----------------

1. **Start simple**: Begin with clear water, flat surface, low aerosols
2. **One parameter at a time**: Change only one variable when testing
3. **Document settings**: Keep detailed notes on parameter choices
4. **Validate results**: Compare with published ocean color data
5. **Use scripts**: Automate parameter sweeps for efficiency
6. **Check logs**: Always review log files for warnings
7. **Save configurations**: Keep successful input files for reference
