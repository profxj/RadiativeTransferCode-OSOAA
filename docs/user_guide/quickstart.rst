Quick Start Guide
=================

This guide will help you run your first OSOAA simulation in minutes.

Prerequisites
-------------

Before starting, ensure you have:

1. OSOAA compiled and installed (see :doc:`installation`)
2. The executable ``OSOAA_MAIN.exe`` in the ``exe/`` directory
3. Basic understanding of radiative transfer concepts

Your First Simulation
---------------------

We'll simulate water-leaving radiance for a simple ocean-atmosphere scenario.

Step 1: Create Input File
~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a file named ``test_simulation.txt`` with the following minimal parameters::

    # OSOAA Test Simulation
    # Basic ocean-atmosphere scenario
    
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
    
    # ===== AEROSOLS =====
    AER.Model 0
    AER.DirMie ./data/aerosols/mie/
    AER.MMD.MRwa 1.45
    AER.MMD.MIwa 0.001
    AER.MMD.SDtype 2
    AER.MMD.SDradius 0.15
    AER.MMD.SDvar 0.6
    AER.AOTref 0.1
    AER.Waref 550.0
    AER.Angexp 1.0
    
    # ===== SEA PROFILE =====
    PROFILE.Sea.File PROFILE_SEA_DEFAULT.txt
    PROFILE.Sea.Depth 100.0
    
    # ===== HYDROSOLS =====
    HYD.Model 0
    HYD.DirMie ./data/hydrosols/mie/
    HYD.Chl 0.1
    HYD.ProfilChl 0
    
    # ===== SEA SURFACE =====
    SEA.Dir ./data/surface/
    SEA.Ind 1.334
    SEA.Type 1
    SEA.Wind 5.0
    
    # ===== OUTPUT FILES =====
    SOS.ResFile.Bin LUM_SF.bin
    OSOAA.ResFile.vsVZA LUM_vsVZA.txt
    OSOAA.ResFile.vsZ LUM_vsZ.txt
    OSOAA.ResFile.Advanced LUM_Advanced.txt

**Parameter Explanation**:

* ``OSOAA.Wa 550.0`` - Wavelength in nm (green light)
* ``ANG.Thetas 30.0`` - Solar zenith angle (degrees)
* ``AER.AOTref 0.1`` - Aerosol optical thickness
* ``HYD.Chl 0.1`` - Chlorophyll concentration (mg/m³)
* ``SEA.Wind 5.0`` - Wind speed (m/s)

Step 2: Prepare Data Directories
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create the required data directories::

    mkdir -p data/aerosols/mie
    mkdir -p data/hydrosols/mie
    mkdir -p data/surface

For this quick test, we'll use default files (OSOAA will use internal defaults).

Step 3: Run OSOAA
~~~~~~~~~~~~~~~~~

Execute the simulation::

    cd exe
    ./OSOAA_MAIN.exe < ../test_simulation.txt

Or using input redirection::

    exe/OSOAA_MAIN.exe < test_simulation.txt

Expected Output
~~~~~~~~~~~~~~~

You should see console output similar to::

    ========================================
    OSOAA V2.0 - Radiative Transfer Model
    ========================================
    
    Reading input parameters...
    Initializing angular grid...
    Computing atmospheric profile...
    Computing aerosol properties...
    Computing ocean profile...
    Computing hydrosol properties...
    Computing surface matrices...
    
    Starting successive orders calculation...
    Order 1... converged
    Order 2... converged
    Order 3... converged
    ...
    
    Writing output files...
    
    Simulation completed successfully!

Step 4: Check Results
~~~~~~~~~~~~~~~~~~~~~

After successful execution, you'll find output files in the ``exe/`` directory:

* ``LUM_vsVZA.txt`` - Radiance vs viewing zenith angle
* ``LUM_vsZ.txt`` - Radiance vs depth/altitude profile
* ``LUM_Advanced.txt`` - Detailed radiance components
* ``LUM_SF.bin`` - Binary file with Fourier series data

Viewing Results
---------------

Simple Text Inspection
~~~~~~~~~~~~~~~~~~~~~~

View the radiance vs viewing angle::

    cat LUM_vsVZA.txt

The file contains columns::

    # Viewing_Zenith_Angle(deg)  Radiance(W/m²/sr/nm)  Q  U  DoLP
    0.0     0.0124    0.0002   0.0001   0.015
    10.0    0.0129    0.0003   0.0001   0.018
    20.0    0.0141    0.0005   0.0002   0.024
    ...

Plotting Results (Python)
~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a Python script ``plot_results.py``::

    import numpy as np
    import matplotlib.pyplot as plt
    
    # Load data
    data = np.loadtxt('LUM_vsVZA.txt', skiprows=1)
    angles = data[:, 0]
    radiance = data[:, 1]
    
    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(angles, radiance, 'b-', linewidth=2)
    plt.xlabel('Viewing Zenith Angle (degrees)', fontsize=12)
    plt.ylabel('Radiance (W/m²/sr/nm)', fontsize=12)
    plt.title('Water-Leaving Radiance at 550 nm', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('radiance_vs_angle.png', dpi=300)
    plt.show()

Run it::

    python plot_results.py

Understanding the Results
-------------------------

Key Observations
~~~~~~~~~~~~~~~~

1. **Radiance magnitude**: Typical values range from 0.01-0.1 W/m²/sr/nm
2. **Angular dependence**: Radiance varies with viewing angle
3. **Polarization**: Q and U components show polarization effects
4. **Degree of Linear Polarization (DoLP)**: Typically 1-5%

Physical Interpretation
~~~~~~~~~~~~~~~~~~~~~~~

The simulated radiance represents:

* **Direct transmission**: Sunlight transmitted through atmosphere and water
* **Atmospheric scattering**: Light scattered by molecules and aerosols
* **Water scattering**: Light scattered by water and particles
* **Surface reflection**: Fresnel reflection and wave-slope effects

Common Issues and Solutions
----------------------------

Issue 1: Missing Data Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Error**::

    ERROR: Cannot open file: ./data/aerosols/mie/...

**Solution**: Either create proper data directories or use OSOAA's internal defaults by 
removing the directory paths from the input file.

Issue 2: Convergence Problems
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Error**::

    WARNING: Convergence not achieved after maximum iterations

**Solution**: 

* Increase maximum scattering orders
* Adjust convergence thresholds
* Check input parameters for physical validity

Issue 3: Memory Errors
~~~~~~~~~~~~~~~~~~~~~~~

**Error**::

    ERROR: Memory allocation failed

**Solution**:

* Reduce angular grid resolution
* Decrease number of vertical levels
* Close other applications to free RAM

Modifying the Simulation
-------------------------

Experiment by changing key parameters:

Change Chlorophyll Concentration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    HYD.Chl 1.0     # Higher phytoplankton content

Change Solar Angle
~~~~~~~~~~~~~~~~~~

::

    ANG.Thetas 60.0  # Lower sun (higher zenith angle)

Change Wind Speed
~~~~~~~~~~~~~~~~~

::

    SEA.Wind 10.0   # Rougher sea surface

Add Aerosol Load
~~~~~~~~~~~~~~~~

::

    AER.AOTref 0.5  # Higher aerosol optical thickness

Batch Simulations
-----------------

To run multiple simulations, create a script:

Bash Script Example
~~~~~~~~~~~~~~~~~~~

Create ``run_batch.sh``::

    #!/bin/bash
    
    # Run simulations for different chlorophyll values
    for chl in 0.01 0.1 1.0 10.0; do
        echo "Running simulation for Chl = $chl mg/m³"
        
        # Modify input file
        sed "s/HYD.Chl .*/HYD.Chl $chl/" test_simulation.txt > temp_input.txt
        
        # Run OSOAA
        ./exe/OSOAA_MAIN.exe < temp_input.txt
        
        # Rename output
        mv exe/LUM_vsVZA.txt results/LUM_vsVZA_chl${chl}.txt
    done
    
    echo "All simulations completed!"

Make it executable and run::

    chmod +x run_batch.sh
    ./run_batch.sh

Next Steps
----------

Now that you've run your first simulation:

* :doc:`input_parameters` - Learn about all available parameters
* :doc:`running_osoaa` - Advanced simulation techniques
* :doc:`output_files` - Detailed output file formats
* :doc:`../examples/basic_simulation` - More example scenarios

Tips for Success
----------------

1. **Start simple**: Use default parameters initially
2. **Validate results**: Compare with known cases
3. **Document parameters**: Keep notes on what you've changed
4. **Check convergence**: Ensure iterations converged
5. **Backup results**: Save output files with descriptive names
6. **Plot data**: Visualize to understand behavior
