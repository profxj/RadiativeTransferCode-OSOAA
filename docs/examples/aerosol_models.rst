Aerosol Models Tutorial
=======================

This tutorial demonstrates how to use different aerosol models in OSOAA to simulate various atmospheric conditions and their effects on ocean color remote sensing.

Overview
--------

OSOAA provides several aerosol model options:

* **Model 0**: Mono-modal distribution (Junge or log-normal)
* **Model 1**: Bi-modal log-normal distribution
* **Model 2**: WMO standard models (Maritime, Continental, Urban, Tropospheric)
* **Model 3**: Shettle & Fenn models with humidity dependence
* **Model 5**: Custom aerosol phase function

Each model is suited for different atmospheric conditions and research objectives.

Learning Objectives
-------------------

After completing this tutorial, you will:

* Understand different aerosol size distributions
* Configure WMO and Shettle & Fenn models
* Simulate various aerosol types (maritime, urban, dust)
* Analyze aerosol effects on water-leaving radiance
* Choose appropriate models for your research

Tutorial 1: Mono-Modal Log-Normal Distribution
----------------------------------------------

The most flexible option for custom aerosol properties.

Maritime Aerosols
~~~~~~~~~~~~~~~~~

Typical oceanic conditions with sea salt aerosols.

Input file ``maritime_aerosol.txt``::

    # Maritime Aerosol Simulation
    # Sea salt particles with hygroscopic properties
    
    OSOAA.Wa 550.0
    
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
    
    # ===== AEROSOL MODEL: Mono-modal =====
    AER.Model 0
    AER.DirMie ./data/aerosols/mie/
    
    # Maritime aerosol properties
    AER.MMD.MRwa 1.38        # Real refractive index (sea salt)
    AER.MMD.MIwa 0.0001      # Imaginary part (weakly absorbing)
    AER.MMD.SDtype 2         # Log-normal distribution
    AER.MMD.SDradius 0.5     # Median radius (µm) - coarse
    AER.MMD.SDvar 0.7        # Variance (broad distribution)
    
    # Optical depth
    AER.AOTref 0.1           # Clean maritime atmosphere
    AER.Waref 550.0
    AER.Angexp 0.5           # Low Angstrom exponent (large particles)
    
    # Sea profile
    PROFILE.Sea.File PROFILE_SEA_DEFAULT.txt
    PROFILE.Sea.Depth 100.0
    
    # Hydrosols (clean water)
    HYD.Model 0
    HYD.Chl 0.1
    HYD.ProfilChl 0
    
    # Sea surface
    SEA.Dir ./data/surface/
    SEA.Ind 1.334
    SEA.Type 1
    SEA.Wind 5.0
    
    # Output
    SOS.ResFile.Bin LUM_SF_maritime.bin
    OSOAA.ResFile.vsVZA LUM_vsVZA_maritime.txt
    OSOAA.ResFile.Advanced LUM_Advanced_maritime.txt

**Key Parameters**:

* **MRwa = 1.38**: Typical for hydrated sea salt
* **MIwa = 0.0001**: Nearly non-absorbing
* **SDradius = 0.5 µm**: Coarse mode sea salt
* **Angexp = 0.5**: Weak wavelength dependence (large particles)

Urban Aerosols
~~~~~~~~~~~~~~

Urban pollution with fine mode particles.

Modify the maritime file::

    # Urban aerosol properties
    AER.MMD.MRwa 1.53        # Higher refractive index (carbon, sulfates)
    AER.MMD.MIwa 0.01        # Moderately absorbing
    AER.MMD.SDtype 2         # Log-normal
    AER.MMD.SDradius 0.15    # Median radius (µm) - fine mode
    AER.MMD.SDvar 0.6        # Narrower distribution
    
    AER.AOTref 0.3           # More turbid urban atmosphere
    AER.Angexp 1.5           # High Angstrom exponent (small particles)

**Key Differences**:

* Smaller particles (0.15 vs 0.5 µm)
* More absorbing (MIwa = 0.01 vs 0.0001)
* Higher AOT (0.3 vs 0.1)
* Larger Angstrom exponent (1.5 vs 0.5)

Mineral Dust
~~~~~~~~~~~~

Desert dust transported over ocean::

    # Mineral dust properties
    AER.MMD.MRwa 1.53        # Refractive index (silicates)
    AER.MMD.MIwa 0.008       # Weakly absorbing (hematite content)
    AER.MMD.SDtype 2         # Log-normal
    AER.MMD.SDradius 0.8     # Coarse particles
    AER.MMD.SDvar 0.8        # Broad size distribution
    
    AER.AOTref 0.5           # Dust outbreak
    AER.Angexp 0.3           # Very low Angstrom exponent

**Characteristics**:

* Large particles (0.8 µm)
* Broad size distribution
* High optical thickness during events
* Low Angstrom exponent

Comparison Script
~~~~~~~~~~~~~~~~~

Run all three scenarios::

    #!/bin/bash
    
    # Maritime
    ./OSOAA_MAIN.exe < maritime_aerosol.txt
    
    # Urban (modify and run)
    sed 's/AER.MMD.MRwa 1.38/AER.MMD.MRwa 1.53/' maritime_aerosol.txt > temp.txt
    sed -i 's/AER.MMD.MIwa 0.0001/AER.MMD.MIwa 0.01/' temp.txt
    sed -i 's/AER.MMD.SDradius 0.5/AER.MMD.SDradius 0.15/' temp.txt
    sed -i 's/AER.AOTref 0.1/AER.AOTref 0.3/' temp.txt
    sed -i 's/AER.Angexp 0.5/AER.Angexp 1.5/' temp.txt
    sed -i 's/maritime/urban/g' temp.txt
    ./OSOAA_MAIN.exe < temp.txt
    
    # Dust
    sed 's/AER.MMD.SDradius 0.5/AER.MMD.SDradius 0.8/' maritime_aerosol.txt > temp.txt
    sed -i 's/AER.MMD.MIwa 0.0001/AER.MMD.MIwa 0.008/' temp.txt
    sed -i 's/AER.AOTref 0.1/AER.AOTref 0.5/' temp.txt
    sed -i 's/AER.Angexp 0.5/AER.Angexp 0.3/' temp.txt
    sed -i 's/maritime/dust/g' temp.txt
    ./OSOAA_MAIN.exe < temp.txt

Tutorial 2: Bi-Modal Distribution
---------------------------------

Realistic representation with separate fine and coarse modes.

Configuration
~~~~~~~~~~~~~

Input file ``bimodal_aerosol.txt``::

    # Bi-Modal Aerosol Distribution
    # Separate fine (pollution) and coarse (sea salt) modes
    
    OSOAA.Wa 550.0
    
    # [Same geometric and atmospheric setup as before]
    
    # ===== AEROSOL MODEL: Bi-modal =====
    AER.Model 1
    AER.DirMie ./data/aerosols/mie/
    
    # Fine mode (urban pollution, biomass burning)
    AER.BMD.MRwa.FM 1.45     # Real refractive index
    AER.BMD.MIwa.FM 0.02     # Absorbing (soot, organic carbon)
    AER.BMD.SDradius.FM 0.1  # Small particles (µm)
    AER.BMD.SDvar.FM 0.5     # Narrow distribution
    AER.BMD.VolC.FM 0.3      # Volume concentration fraction
    
    # Coarse mode (sea salt, dust)
    AER.BMD.MRwa.CM 1.38     # Real refractive index
    AER.BMD.MIwa.CM 0.0001   # Non-absorbing (sea salt)
    AER.BMD.SDradius.CM 0.5  # Large particles (µm)
    AER.BMD.SDvar.CM 0.7     # Broad distribution
    AER.BMD.VolC.CM 0.7      # Volume concentration fraction
    
    # Total optical depth
    AER.AOTref 0.2
    AER.Waref 550.0
    AER.Angexp 1.0           # Composite Angstrom exponent
    
    # [Rest of parameters same as before]

**Physical Interpretation**:

* **Fine mode**: r < 0.5 µm, strongly absorbing, from combustion
* **Coarse mode**: r > 0.5 µm, non-absorbing, from mechanical processes
* **Volume fractions**: VolC.FM + VolC.CM should equal 1.0

Scenarios
~~~~~~~~~

**Clean Marine Boundary Layer**::

    AER.BMD.VolC.FM 0.1      # 10% fine mode
    AER.BMD.VolC.CM 0.9      # 90% coarse mode (sea salt dominant)
    AER.AOTref 0.08

**Polluted Coastal Area**::

    AER.BMD.VolC.FM 0.6      # 60% fine mode
    AER.BMD.VolC.CM 0.4      # 40% coarse mode
    AER.AOTref 0.35

**Mixed Continental Outflow**::

    AER.BMD.VolC.FM 0.5      # Equal contribution
    AER.BMD.VolC.CM 0.5
    AER.AOTref 0.25

Tutorial 3: WMO Standard Models
-------------------------------

Pre-defined aerosol models from World Meteorological Organization.

Available Models
~~~~~~~~~~~~~~~~

1. **Maritime** (Model 1): Open ocean, sea salt dominant
2. **Continental** (Model 2): Rural continental areas
3. **Urban** (Model 3): Industrial and urban pollution
4. **Tropospheric** (Model 4): Background stratospheric aerosols

Maritime Model
~~~~~~~~~~~~~~

Input file ``wmo_maritime.txt``::

    # WMO Maritime Model
    
    OSOAA.Wa 550.0
    
    # [Standard geometric setup]
    
    # ===== AEROSOL MODEL: WMO =====
    AER.Model 2
    
    # WMO Maritime model
    AER.WMO.Model 1
    
    # Composition (volume fractions, must sum to 1.0)
    AER.WMO.DL 0.0           # Dust-like particles
    AER.WMO.WS 0.95          # Water-soluble (sea salt)
    AER.WMO.OC 0.05          # Oceanic particles
    AER.WMO.SO 0.0           # Soot
    
    # Optical depth
    AER.AOTref 0.1
    AER.Waref 550.0
    AER.Angexp 0.5

**Component Description**:

* **WS (Water-soluble)**: Sea salt, hygroscopic
* **OC (Oceanic)**: Organic sea spray
* **DL (Dust-like)**: Mineral particles
* **SO (Soot)**: Black carbon

Continental Model
~~~~~~~~~~~~~~~~~

::

    AER.WMO.Model 2
    
    # Continental composition
    AER.WMO.DL 0.3           # Dust from soil
    AER.WMO.WS 0.5           # Water-soluble compounds
    AER.WMO.OC 0.0           # No oceanic
    AER.WMO.SO 0.2           # Soot from combustion
    
    AER.AOTref 0.2
    AER.Angexp 1.2

Urban Model
~~~~~~~~~~~

::

    AER.WMO.Model 3
    
    # Urban composition
    AER.WMO.DL 0.2           # Resuspended dust
    AER.WMO.WS 0.4           # Sulfates, nitrates
    AER.WMO.OC 0.0           # Minimal oceanic
    AER.WMO.SO 0.4           # High soot content
    
    AER.AOTref 0.4
    AER.Angexp 1.5

Comparison
~~~~~~~~~~

Run all WMO models::

    #!/bin/bash
    
    for model in 1 2 3 4; do
        echo "Running WMO Model $model"
        sed "s/AER.WMO.Model .*/AER.WMO.Model $model/" wmo_maritime.txt > temp_wmo_${model}.txt
        sed -i "s/maritime/wmo${model}/g" temp_wmo_${model}.txt
        ./OSOAA_MAIN.exe < temp_wmo_${model}.txt
    done

Tutorial 4: Shettle & Fenn Models
---------------------------------

Aerosol models with explicit humidity dependence.

Configuration
~~~~~~~~~~~~~

Input file ``shettle_fenn.txt``::

    # Shettle & Fenn Aerosol Model
    
    OSOAA.Wa 550.0
    
    # [Standard setup]
    
    # ===== AEROSOL MODEL: Shettle & Fenn =====
    AER.Model 3
    
    # Model selection
    AER.SF.Model 1           # 1=Maritime, 2=Coastal, 3=Urban, 4=Tropospheric
    
    # Relative humidity (critical parameter)
    AER.SF.RH 70.0           # Percent (0-99%)
    
    # Optical depth
    AER.AOTref 0.15
    AER.Waref 550.0
    AER.Angexp 0.8

Available Models
~~~~~~~~~~~~~~~~

1. **Maritime** (AER.SF.Model = 1): Open ocean
2. **Coastal** (AER.SF.Model = 2): Coastal regions
3. **Urban** (AER.SF.Model = 3): Cities
4. **Tropospheric** (AER.SF.Model = 4): Free troposphere

Humidity Effects
~~~~~~~~~~~~~~~~

Aerosol properties change with relative humidity::

    #!/bin/bash
    
    # Test different humidity levels for maritime aerosols
    for rh in 50 70 80 90 95; do
        echo "Running RH = $rh%"
        sed "s/AER.SF.RH .*/AER.SF.RH $rh.0/" shettle_fenn.txt > temp_rh${rh}.txt
        sed -i "s/shettle_fenn/SF_rh${rh}/g" temp_rh${rh}.txt
        ./OSOAA_MAIN.exe < temp_rh${rh}.txt
    done

**Expected Behavior**:

* **Low RH (50%)**: Dry particles, smaller size, less scattering
* **High RH (95%)**: Hygroscopic growth, larger particles, increased scattering
* **Refractive index**: Decreases with increasing humidity (more water)

Physical Interpretation
~~~~~~~~~~~~~~~~~~~~~~~

At high humidity (>80%):

* Sea salt particles absorb water and swell
* Particle radius can double
* Scattering coefficient increases significantly
* Optical depth at constant number concentration increases

Tutorial 5: Aerosol Optical Thickness Sensitivity
-------------------------------------------------

Explore how AOT affects ocean color signals.

AOT Series
~~~~~~~~~~

::

    #!/bin/bash
    
    # AOT values from very clean to very turbid
    AOT_VALUES=(0.02 0.05 0.1 0.2 0.3 0.5 0.8)
    
    for aot in "${AOT_VALUES[@]}"; do
        echo "Running AOT = $aot"
        sed "s/AER.AOTref .*/AER.AOTref $aot/" maritime_aerosol.txt > temp_aot${aot}.txt
        sed -i "s/maritime/aot${aot}/g" temp_aot${aot}.txt
        ./OSOAA_MAIN.exe < temp_aot${aot}.txt
    done

Analysis
~~~~~~~~

Compare water-leaving radiance vs. AOT::

    import numpy as np
    import matplotlib.pyplot as plt
    
    aot_values = [0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 0.8]
    radiance = []
    
    for aot in aot_values:
        data = np.loadtxt(f'LUM_vsVZA_aot{aot}.txt', skiprows=5)
        idx = np.argmin(np.abs(data[:, 0]))  # Nadir
        radiance.append(data[idx, 1])
    
    plt.figure(figsize=(10, 6))
    plt.plot(aot_values, radiance, 'o-', linewidth=2, markersize=10)
    plt.xlabel('Aerosol Optical Thickness', fontsize=14)
    plt.ylabel('Water-Leaving Radiance (W/m²/sr/nm)', fontsize=14)
    plt.title('Impact of Aerosol Loading at 550 nm', fontsize=16)
    plt.grid(True, alpha=0.3)
    plt.show()

**Expected Trend**:

* Water-leaving radiance decreases with increasing AOT
* Atmospheric path radiance increases
* At very high AOT (>0.5), atmospheric signal dominates

Tutorial 6: Angstrom Exponent Effects
-------------------------------------

The Angstrom exponent describes spectral variation of AOT.

Spectral AOT
~~~~~~~~~~~~

AOT varies with wavelength:

.. math::

   \\tau_{aer}(\\lambda) = \\tau_{aer}(\\lambda_0) \\left(\\frac{\\lambda}{\\lambda_0}\\right)^{-\\alpha}

where α is the Angstrom exponent.

Simulations
~~~~~~~~~~~

Compare different particle sizes::

    #!/bin/bash
    
    # Small particles (urban): α ≈ 1.5-2.0
    # Average: α ≈ 1.0
    # Large particles (maritime): α ≈ 0.5
    # Very large (dust): α ≈ 0.2-0.3
    
    for angexp in 0.3 0.5 1.0 1.5 2.0; do
        echo "Running Angstrom exponent = $angexp"
        sed "s/AER.Angexp .*/AER.Angexp $angexp/" maritime_aerosol.txt > temp_ang${angexp}.txt
        sed -i "s/maritime/ang${angexp}/g" temp_ang${angexp}.txt
        ./OSOAA_MAIN.exe < temp_ang${angexp}.txt
    done

Physical Meaning
~~~~~~~~~~~~~~~~

* **High α (1.5-2.0)**: Small particles
  
  * Strong spectral variation
  * τ(400nm) >> τ(700nm)
  * Typical of pollution

* **Low α (0.3-0.5)**: Large particles
  
  * Weak spectral variation
  * τ(400nm) ≈ τ(700nm)
  * Typical of sea salt, dust

Best Practices
--------------

Choosing the Right Model
~~~~~~~~~~~~~~~~~~~~~~~~

1. **Use WMO models** when:
   
   * Simulating standard atmospheric conditions
   * Comparing with historical studies
   * Need reproducible results

2. **Use Shettle & Fenn** when:
   
   * Humidity is a critical factor
   * Simulating coastal areas with variable RH
   * Need explicit hygroscopic effects

3. **Use mono-modal** when:
   
   * You have specific aerosol measurements
   * Custom refractive indices needed
   * Research on specific aerosol types

4. **Use bi-modal** when:
   
   * Simulating realistic mixed aerosols
   * Separating fine/coarse mode contributions
   * Validating multi-angle polarimeters

Parameter Selection Guidelines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Refractive Index**:

* Maritime (sea salt): MR = 1.38-1.40, MI < 0.001
* Urban (mixed): MR = 1.45-1.53, MI = 0.01-0.03
* Dust: MR = 1.53, MI = 0.005-0.01
* Soot: MR = 1.75, MI = 0.4-0.5

**Size Distribution**:

* Fine mode: r = 0.05-0.2 µm, σ = 0.4-0.6
* Accumulation mode: r = 0.2-0.5 µm, σ = 0.5-0.7
* Coarse mode: r = 0.5-2.0 µm, σ = 0.6-0.8

**AOT at 550 nm**:

* Very clean: < 0.05
* Clean: 0.05-0.15
* Moderate: 0.15-0.35
* Turbid: 0.35-0.6
* Very turbid: > 0.6

Common Mistakes
---------------

1. **Unrealistic combinations**:
   
   * High AOT with low Angstrom exponent AND small radius
   * Maritime aerosols with high absorption

2. **Volume fractions**:
   
   * In bi-modal or WMO models, fractions must sum to 1.0

3. **Reference wavelength**:
   
   * AER.Waref should match your simulation wavelength for single-wavelength studies

4. **Humidity**:
   
   * Shettle & Fenn models are very sensitive to RH
   * RH > 95% can cause numerical issues

Validation
----------

Compare with AERONET data::

    # Example AERONET site: midway island (maritime)
    # Typical values:
    # AOT(500nm) = 0.06 ± 0.03
    # Angstrom exponent = 0.3 ± 0.2
    # Single scattering albedo = 0.98 ± 0.01

Your simulations should produce similar atmospheric radiance patterns when using comparable parameters.

Next Steps
----------

* :doc:`hydrosol_models` - Ocean particle models
* :doc:`rough_surface` - Combined aerosol and surface effects
* :doc:`custom_profiles` - Vertical aerosol profiles
* :doc:`../reference/parameter_reference` - Complete parameter list

Further Reading
---------------

* Shettle, E.P., and Fenn, R.W. (1979) "Models for the aerosols of the lower atmosphere and the effects of humidity variations on their optical properties"
* WMO (1986) "A preliminary cloudless standard atmosphere for radiation computation"
* Dubovik et al. (2002) "Variability of absorption and optical properties of key aerosol types observed in worldwide locations"
