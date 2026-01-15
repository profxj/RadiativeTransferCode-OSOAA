Rough Surface Tutorial
======================

This tutorial explores the Cox & Munk sea surface model in OSOAA, demonstrating how wind-driven waves affect ocean color remote sensing through sun glint, shadowing, and wave-slope statistics.

Overview
--------

OSOAA provides two surface models:

* **Model 0**: Flat surface (Fresnel reflection only)
* **Model 1**: Rough surface (Cox & Munk wave-slope statistics)

The rough surface model accounts for:

* Wave-slope probability distribution
* Specular reflection (sun glint)
* Shadowing effects
* Multiple reflections
* Refraction through curved interface

This is critical for realistic ocean color simulations.

Learning Objectives
-------------------

After this tutorial, you will understand:

* Cox & Munk wave-slope model fundamentals
* Wind speed effects on radiance
* Sun glint patterns and avoidance
* Viewing geometry optimization
* Wind direction effects
* Combined surface and atmospheric effects

Tutorial 1: Flat vs. Rough Surface Comparison
---------------------------------------------

Understanding the baseline difference.

Flat Surface Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~

Input file ``flat_surface.txt``::

    # Flat Surface Simulation
    # No wave effects, pure Fresnel reflection
    
    OSOAA.Wa 550.0
    
    # Geometric conditions
    OSOAA.View.Phi 0.0       # Principal plane
    OSOAA.View.Level 1
    OSOAA.View.Z -0.0
    ANG.Thetas 30.0          # Solar zenith angle
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
    AER.AOTref 0.1
    AER.Waref 550.0
    AER.Angexp 0.5
    
    # Sea profile
    PROFILE.Sea.File PROFILE_SEA_DEFAULT.txt
    PROFILE.Sea.Depth 100.0
    
    # Hydrosols
    HYD.Model 0
    HYD.Chl 0.1
    HYD.ProfilChl 0
    HYD.abs.Yellow 0.02
    HYD.slope.Yellow 0.015
    
    # ===== SEA SURFACE: Flat =====
    SEA.Dir ./data/surface/
    SEA.Ind 1.334            # Refractive index of seawater
    SEA.Type 0               # Flat surface
    
    # Output
    SOS.ResFile.Bin LUM_SF_flat.bin
    OSOAA.ResFile.vsVZA LUM_vsVZA_flat.txt
    OSOAA.ResFile.Advanced LUM_Advanced_flat.txt

Rough Surface Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Input file ``rough_surface.txt`` (modify the above)::

    # ===== SEA SURFACE: Rough (Cox & Munk) =====
    SEA.Dir ./data/surface/
    SEA.Ind 1.334
    SEA.Type 1               # Rough surface
    SEA.Wind 5.0             # Wind speed (m/s)

Run Comparison
~~~~~~~~~~~~~~

::

    #!/bin/bash
    
    cd exe/
    
    # Flat surface
    ./OSOAA_MAIN.exe < ../flat_surface.txt
    
    # Rough surface
    ./OSOAA_MAIN.exe < ../rough_surface.txt
    
    cd ..

Analysis
~~~~~~~~

::

    import numpy as np
    import matplotlib.pyplot as plt
    
    # Load results
    flat = np.loadtxt('exe/LUM_vsVZA_flat.txt', skiprows=5)
    rough = np.loadtxt('exe/LUM_vsVZA_rough.txt', skiprows=5)
    
    # Plot comparison
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Total radiance
    ax1.plot(flat[:, 0], flat[:, 1], 'b-', linewidth=2, label='Flat')
    ax1.plot(rough[:, 0], rough[:, 1], 'r-', linewidth=2, label='Rough (5 m/s)')
    ax1.set_xlabel('Viewing Zenith Angle (degrees)', fontsize=12)
    ax1.set_ylabel('Radiance (W/m²/sr/nm)', fontsize=12)
    ax1.set_title('Total Radiance', fontsize=14)
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)
    
    # Difference
    ax2.plot(flat[:, 0], rough[:, 1] - flat[:, 1], 'g-', linewidth=2)
    ax2.set_xlabel('Viewing Zenith Angle (degrees)', fontsize=12)
    ax2.set_ylabel('Radiance Difference (W/m²/sr/nm)', fontsize=12)
    ax2.set_title('Rough - Flat', fontsize=14)
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=0, color='k', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.show()

**Expected Differences**:

* Near-nadir: Rough surface reduces radiance slightly (increased diffuse transmission)
* Off-nadir: Can show enhancement or reduction depending on glint geometry
* Overall: Rough surface "smooths" angular patterns

Tutorial 2: Wind Speed Effects
------------------------------

Exploring how wind speed affects wave-slope distribution.

Wind Speed Series
~~~~~~~~~~~~~~~~~

::

    #!/bin/bash
    
    # Wind speeds from calm to strong breeze
    WIND_VALUES=(0.5 2.0 5.0 8.0 12.0 15.0)
    
    for wind in "${WIND_VALUES[@]}"; do
        echo "Running wind speed = $wind m/s"
        sed "s/SEA.Wind .*/SEA.Wind $wind/" rough_surface.txt > temp_wind${wind}.txt
        sed -i "s/rough_surface/wind${wind}/g" temp_wind${wind}.txt
        cd exe/
        ./OSOAA_MAIN.exe < ../temp_wind${wind}.txt
        cd ..
    done

Beaufort Scale Reference
~~~~~~~~~~~~~~~~~~~~~~~~

* **0.5 m/s**: Calm (Beaufort 1)
* **2.0 m/s**: Light air (Beaufort 2)
* **5.0 m/s**: Gentle breeze (Beaufort 3)
* **8.0 m/s**: Moderate breeze (Beaufort 4)
* **12.0 m/s**: Fresh breeze (Beaufort 5)
* **15.0 m/s**: Strong breeze (Beaufort 6)

Physical Effects
~~~~~~~~~~~~~~~~

As wind speed increases:

* **Wave slope variance** increases (σ² ∝ Wind speed)
* **Glint area** expands (more facets reflecting sunlight)
* **Shadowing** becomes more important (waves block each other)
* **Multiple reflections** increase (light bounces between wave facets)
* **Effective Fresnel reflectance** changes

Visualization
~~~~~~~~~~~~~

::

    import numpy as np
    import matplotlib.pyplot as plt
    
    wind_values = [0.5, 2.0, 5.0, 8.0, 12.0, 15.0]
    colors = plt.cm.viridis(np.linspace(0, 1, len(wind_values)))
    
    plt.figure(figsize=(12, 6))
    
    for wind, color in zip(wind_values, colors):
        try:
            data = np.loadtxt(f'exe/LUM_vsVZA_wind{wind}.txt', skiprows=5)
            plt.plot(data[:, 0], data[:, 1], linewidth=2, 
                    label=f'{wind} m/s', color=color)
        except:
            pass
    
    plt.xlabel('Viewing Zenith Angle (degrees)', fontsize=12)
    plt.ylabel('Radiance (W/m²/sr/nm)', fontsize=12)
    plt.title('Wind Speed Effects on TOA Radiance', fontsize=14)
    plt.legend(fontsize=10, loc='best')
    plt.grid(True, alpha=0.3)
    plt.show()

**Expected Trends**:

* Higher wind → broader angular distribution
* Peak radiance may shift slightly
* Near-nadir less affected than off-nadir angles

Tutorial 3: Sun Glint Analysis
------------------------------

Understanding specular reflection and glint geometry.

Glint Geometry
~~~~~~~~~~~~~~

The specular reflection angle θ_spec is where:

.. math::

   \\theta_{spec} = \\arccos(|\\cos\\theta_s \\cos\\theta_v - \\sin\\theta_s \\sin\\theta_v \\cos\\phi|)

Where:

* θ_s = solar zenith angle
* θ_v = viewing zenith angle
* φ = relative azimuth angle

Glint Avoidance Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Input file ``glint_study.txt``::

    # Sun Glint Study
    # Varying viewing geometry to map glint pattern
    
    OSOAA.Wa 550.0
    
    # Solar geometry (fixed)
    ANG.Thetas 40.0          # 40° solar zenith
    
    # [Standard atmospheric, aerosol, hydrosol setup]
    
    # Sea surface with moderate wind
    SEA.Type 1
    SEA.Wind 7.0
    
    # Varying viewing geometry
    OSOAA.View.Phi 0.0       # Will vary this
    
    # [Output configuration]

Azimuth Sweep
~~~~~~~~~~~~~

::

    #!/bin/bash
    
    # Azimuth angles from 0° (principal plane) to 180° (backscatter)
    for phi in 0 30 60 90 120 150 180; do
        echo "Running azimuth angle = $phi degrees"
        sed "s/OSOAA.View.Phi .*/OSOAA.View.Phi $phi.0/" glint_study.txt > temp_phi${phi}.txt
        sed -i "s/glint_study/phi${phi}/g" temp_phi${phi}.txt
        cd exe/
        ./OSOAA_MAIN.exe < ../temp_phi${phi}.txt
        cd ..
    done

Glint Pattern Visualization
~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    
    phi_values = [0, 30, 60, 90, 120, 150, 180]
    
    # Create meshgrid
    VZA = None
    PHI = []
    RAD = []
    
    for phi in phi_values:
        try:
            data = np.loadtxt(f'exe/LUM_vsVZA_phi{phi}.txt', skiprows=5)
            if VZA is None:
                VZA = data[:, 0]
            
            for vza, rad in zip(data[:, 0], data[:, 1]):
                PHI.append(phi)
                RAD.append(rad)
        except:
            pass
    
    # Polar plot
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='polar')
    
    # Convert to radians
    phi_rad = np.deg2rad(PHI)
    
    # Scatter plot with color showing radiance
    scatter = ax.scatter(phi_rad, VZA, c=RAD, s=50, cmap='hot')
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_ylim(0, 70)
    ax.set_ylabel('Viewing Zenith Angle (degrees)', labelpad=30)
    ax.set_title('Sun Glint Pattern (SZA=40°, Wind=7 m/s)', pad=20, fontsize=14)
    
    cbar = plt.colorbar(scatter, ax=ax, pad=0.1)
    cbar.set_label('Radiance (W/m²/sr/nm)', fontsize=11)
    
    plt.show()

Glint Probability
~~~~~~~~~~~~~~~~~

Calculate probability of glint contamination::

    import numpy as np
    
    def glint_angle(sza, vza, phi):
        """Calculate angle from specular direction"""
        cos_glint = (np.cos(np.radians(sza)) * np.cos(np.radians(vza)) - 
                     np.sin(np.radians(sza)) * np.sin(np.radians(vza)) * 
                     np.cos(np.radians(phi)))
        return np.degrees(np.arccos(np.abs(cos_glint)))
    
    # Example: SZA=30°, VZA=20°, Phi=0°
    sza = 30
    vza = 20
    phi = 0
    
    theta_spec = glint_angle(sza, vza, phi)
    print(f"Angle from specular direction: {theta_spec:.1f}°")
    
    # Rule of thumb: glint significant if θ_spec < 20-30°

Tutorial 4: Optimal Viewing Geometries
--------------------------------------

Finding geometries that minimize surface effects.

Strategy
~~~~~~~~

1. **Maximize glint angle** (θ_spec > 30°)
2. **Avoid near-nadir** (Fresnel reflectance minimum)
3. **Consider polarization** (maximum perpendicular to principal plane)
4. **Balance signal-to-noise**

Geometry Optimization
~~~~~~~~~~~~~~~~~~~~~

::

    import numpy as np
    import matplotlib.pyplot as plt
    
    # Create geometry grid
    sza = 30  # Fixed solar angle
    vza_range = np.arange(0, 71, 5)
    phi_range = np.arange(0, 181, 10)
    
    VZA, PHI = np.meshgrid(vza_range, phi_range)
    
    # Calculate glint angle for each geometry
    cos_glint = (np.cos(np.radians(sza)) * np.cos(np.radians(VZA)) - 
                 np.sin(np.radians(sza)) * np.sin(np.radians(VZA)) * 
                 np.cos(np.radians(PHI)))
    GLINT_ANGLE = np.degrees(np.arccos(np.abs(cos_glint)))
    
    # Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Contour plot
    contour = ax1.contourf(PHI, VZA, GLINT_ANGLE, levels=20, cmap='RdYlGn')
    ax1.contour(PHI, VZA, GLINT_ANGLE, levels=[20, 30, 40], colors='black', linewidths=2)
    ax1.set_xlabel('Relative Azimuth (degrees)', fontsize=12)
    ax1.set_ylabel('Viewing Zenith Angle (degrees)', fontsize=12)
    ax1.set_title('Glint Angle Map (SZA=30°)', fontsize=14)
    cbar1 = plt.colorbar(contour, ax=ax1)
    cbar1.set_label('Angle from Specular (degrees)', fontsize=11)
    
    # Highlight safe zone (glint angle > 30°)
    safe_zone = GLINT_ANGLE > 30
    ax2.contourf(PHI, VZA, safe_zone.astype(float), levels=[0, 0.5, 1], 
                 colors=['red', 'green'], alpha=0.3)
    ax2.set_xlabel('Relative Azimuth (degrees)', fontsize=12)
    ax2.set_ylabel('Viewing Zenith Angle (degrees)', fontsize=12)
    ax2.set_title('Glint-Free Zone (green)', fontsize=14)
    
    plt.tight_layout()
    plt.show()

**Recommended Geometries**:

* **Ocean color**: Phi ≈ 90°, VZA = 40-50°
* **MODIS-like**: VZA ≈ ±55°, Phi ≈ 90°
* **SeaWiFS-like**: Nadir, but use glint flags
* **Multi-angle**: Multiple VZA at Phi ≈ 90°

Tutorial 5: Wind Direction Effects
----------------------------------

Cox & Munk model includes cross-wind and up-wind asymmetry.

Isotropic vs. Anisotropic
~~~~~~~~~~~~~~~~~~~~~~~~~~

The full Cox & Munk model accounts for:

* **Cross-wind variance** (σ_c²): Perpendicular to wind
* **Up-wind variance** (σ_u²): Parallel to wind
* Typical ratio: σ_c²/σ_u² ≈ 0.7-0.8

In OSOAA, specify wind speed and direction::

    SEA.Type 1
    SEA.Wind 10.0            # Wind speed (m/s)
    SEA.WindDir 45.0         # Wind direction (degrees from North)

Note: Most OSOAA configurations use isotropic approximation (wind direction optional).

Tutorial 6: Combined Surface and Atmospheric Effects
----------------------------------------------------

Realistic scenario with multiple scattering sources.

High Wind + High Aerosol
~~~~~~~~~~~~~~~~~~~~~~~~

Input file ``combined_effects.txt``::

    # Combined Surface and Atmospheric Effects
    # Rough sea under dusty atmosphere
    
    OSOAA.Wa 550.0
    
    ANG.Thetas 45.0          # Low sun angle
    OSOAA.View.Phi 90.0      # Cross-principal plane
    
    # [Standard geometric setup]
    
    # High aerosol load (dust event)
    AER.Model 0
    AER.MMD.MRwa 1.53        # Dust refractive index
    AER.MMD.MIwa 0.008
    AER.MMD.SDtype 2
    AER.MMD.SDradius 0.8     # Coarse dust
    AER.MMD.SDvar 0.8
    AER.AOTref 0.5           # Heavy aerosol loading
    AER.Waref 550.0
    AER.Angexp 0.3
    
    # Hydrosols (moderate)
    HYD.Model 0
    HYD.Chl 0.3
    
    # Rough sea (strong wind)
    SEA.Type 1
    SEA.Wind 12.0            # Strong breeze

Scenario Comparison
~~~~~~~~~~~~~~~~~~~

::

    #!/bin/bash
    
    # 1. Clean atmosphere + calm sea (baseline)
    sed 's/AER.AOTref .*/AER.AOTref 0.05/' combined_effects.txt > case1.txt
    sed -i 's/SEA.Wind .*/SEA.Wind 2.0/' case1.txt
    
    # 2. Clean atmosphere + rough sea
    sed 's/AER.AOTref .*/AER.AOTref 0.05/' combined_effects.txt > case2.txt
    sed -i 's/SEA.Wind .*/SEA.Wind 12.0/' case2.txt
    
    # 3. Dusty atmosphere + calm sea
    sed 's/AER.AOTref .*/AER.AOTref 0.5/' combined_effects.txt > case3.txt
    sed -i 's/SEA.Wind .*/SEA.Wind 2.0/' case3.txt
    
    # 4. Dusty atmosphere + rough sea (full combined)
    cp combined_effects.txt case4.txt
    
    for case in 1 2 3 4; do
        echo "Running case $case"
        cd exe/
        ./OSOAA_MAIN.exe < ../case${case}.txt
        cd ..
    done

Analysis
~~~~~~~~

::

    import numpy as np
    import matplotlib.pyplot as plt
    
    cases = {
        1: 'Clean atm + Calm sea',
        2: 'Clean atm + Rough sea',
        3: 'Dusty atm + Calm sea',
        4: 'Dusty atm + Rough sea'
    }
    
    plt.figure(figsize=(12, 7))
    
    for case, label in cases.items():
        try:
            data = np.loadtxt(f'exe/LUM_vsVZA_case{case}.txt', skiprows=5)
            plt.plot(data[:, 0], data[:, 1], linewidth=2, label=label, marker='o', markersize=4)
        except:
            pass
    
    plt.xlabel('Viewing Zenith Angle (degrees)', fontsize=12)
    plt.ylabel('TOA Radiance (W/m²/sr/nm)', fontsize=12)
    plt.title('Combined Atmospheric and Surface Effects', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.show()

**Expected Results**:

* Case 1 (baseline): Lowest radiance
* Case 2: Slightly modified angular shape
* Case 3: Strong atmospheric path radiance increase
* Case 4: Combined effects, highest radiance

Tutorial 7: Polarization and Rough Surface
-------------------------------------------

Surface roughness affects polarization differently than flat surfaces.

Configuration
~~~~~~~~~~~~~

::

    # Enable polarization output
    OSOAA.ResFile.Advanced LUM_Advanced_polar.txt
    
    # Rough surface
    SEA.Type 1
    SEA.Wind 6.0

Analysis
~~~~~~~~

::

    import numpy as np
    import matplotlib.pyplot as plt
    
    # Load advanced output with Stokes parameters
    data = np.loadtxt('exe/LUM_Advanced_polar.txt', skiprows=10)
    
    vza = data[:, 0]
    I = data[:, 1]  # Stokes I
    Q = data[:, 2]  # Stokes Q
    U = data[:, 3]  # Stokes U
    
    # Calculate degree of linear polarization
    DoLP = np.sqrt(Q**2 + U**2) / I * 100  # Percentage
    
    # Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    ax1.plot(vza, I, 'b-', linewidth=2)
    ax1.set_xlabel('Viewing Zenith Angle (degrees)', fontsize=12)
    ax1.set_ylabel('Total Radiance (W/m²/sr/nm)', fontsize=12)
    ax1.set_title('Stokes I', fontsize=14)
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(vza, DoLP, 'r-', linewidth=2)
    ax2.set_xlabel('Viewing Zenith Angle (degrees)', fontsize=12)
    ax2.set_ylabel('DoLP (%)', fontsize=12)
    ax2.set_title('Degree of Linear Polarization', fontsize=14)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

**Observations**:

* Rough surface reduces polarization near Brewster angle
* Maximum polarization shifts from flat surface case
* Overall DoLP typically 2-8% for ocean-atmosphere system

Performance Considerations
--------------------------

Computational Cost
~~~~~~~~~~~~~~~~~~

Rough surface calculations are ~3-10× slower than flat surface:

* Wave-slope integration requires nested loops
* Shadowing calculations add overhead
* Higher angular resolution needed for accuracy

Optimization Strategies
~~~~~~~~~~~~~~~~~~~~~~~

1. **Use flat surface for initial tests**
2. **Reduce angular resolution** for rough surface testing::

    ANG.Rad.NbGauss 24       # Lower resolution (faster)

3. **Test critical geometries only** (near glint)
4. **Parallel runs** for wind speed/geometry sweeps

Accuracy vs. Speed
~~~~~~~~~~~~~~~~~~

Recommended settings:

* **Quick test**: Flat surface, NbGauss = 24
* **Standard**: Rough surface, NbGauss = 40, Wind ≤ 10 m/s
* **High accuracy**: Rough surface, NbGauss = 60+, careful convergence checks

Best Practices
--------------

When to Use Flat Surface
~~~~~~~~~~~~~~~~~~~~~~~~

* **Initial testing** and parameter exploration
* **Very calm conditions** (Wind < 1 m/s)
* **Nadir-only viewing** (surface effects minimal)
* **Theoretical studies** focusing on water properties

When to Use Rough Surface
~~~~~~~~~~~~~~~~~~~~~~~~~

* **Realistic simulations** (typical ocean conditions)
* **Off-nadir geometries** (VZA > 10°)
* **Glint studies** and avoidance strategies
* **Multi-angle observations** (POLDER, MISR, etc.)
* **Validation** against satellite/field data

Wind Speed Selection
~~~~~~~~~~~~~~~~~~~~

Use realistic values:

* **Trade wind regions**: 5-8 m/s
* **Mid-latitudes**: 8-12 m/s
* **Storm conditions**: > 15 m/s
* **Calm conditions**: < 3 m/s

Common Mistakes
---------------

1. **Unrealistic wind speeds**:
   
   * Wind = 0 with SEA.Type = 1 (undefined)
   * Wind > 20 m/s (breaking wave effects not modeled)

2. **Ignoring geometry**:
   
   * Using rough surface but not checking glint angle
   * Principal plane observations without glint correction

3. **Insufficient angular resolution**:
   
   * NbGauss too low for rough surface (artifacts)

4. **Mixing models**:
   
   * Flat surface reflectance with rough surface calculations

Validation Against Measurements
-------------------------------

Sun Glint Observations
~~~~~~~~~~~~~~~~~~~~~~

Compare with sun glint observations (Cox & Munk 1954)::

    # Expected glint radiance enhancement
    # At θ_spec = 0° (perfect specular):
    # Enhancement ~ 100-1000× depending on wind speed
    # 
    # At θ_spec = 10°:
    # Enhancement ~ 10-50×

SeaWiFS/MODIS Comparisons
~~~~~~~~~~~~~~~~~~~~~~~~~

For validation:

* Use actual viewing geometries from satellite
* Match atmospheric conditions (AOT, wind)
* Apply spectral bands (400-700 nm range)
* Compare Lwn or Rrs

Expected Agreement
~~~~~~~~~~~~~~~~~~

* **Clear conditions**: Within 5-10%
* **Moderate AOT**: Within 10-20%
* **Glint areas**: Rougher agreement (20-50%)

Next Steps
----------

* :doc:`custom_profiles` - Vertical structure effects
* :doc:`../science/surface_interface` - Theoretical background
* :doc:`../reference/parameter_reference` - Complete parameters
* :doc:`../technical/performance` - Optimization techniques

Further Reading
---------------

* Cox, C. and Munk, W. (1954) "Measurement of the roughness of the sea surface from photographs of the sun's glitter"
* Zhang, H. and Wang, M. (2010) "Evaluation of sun glint models using MODIS measurements"
* Kay, S. et al. (2009) "Sun glint correction of high and low spatial resolution images of aquatic scenes"
* Harmel, T. and Chami, M. (2013) "Determination of sea surface wind speed using the polarimetric and multidirectional properties of satellite measurements"
