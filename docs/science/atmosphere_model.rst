.. _atmosphere_model:

Atmosphere Model
================

This section describes the atmospheric component of OSOAA, including molecular scattering, aerosol properties, and vertical structure.

.. contents:: Contents
   :local:
   :depth: 2

Overview
--------

The atmosphere in OSOAA is modeled as a plane-parallel medium consisting of:

- **Molecular atmosphere**: Rayleigh scattering by air molecules
- **Aerosols**: Particulate matter (scattering and absorption)
- **Vertical stratification**: Varying density and composition with altitude

The model accounts for:

- Wavelength-dependent molecular scattering (∝ λ⁻⁴)
- Multiple aerosol size distributions and compositions
- Exponential decay of density with altitude
- Polarization effects in scattering

Molecular Atmosphere
--------------------

Rayleigh Scattering Theory
~~~~~~~~~~~~~~~~~~~~~~~~~~

Air molecules scatter light through **Rayleigh scattering**, characterized by strong wavelength dependence.

**Scattering cross section:**

.. math::

   \sigma_{Ray}(\lambda) = \frac{24\pi^3(n_s^2-1)^2}{N_s^2\lambda^4(n_s^2+2)^2}F_K

Where:

- n_s: Refractive index of standard air (n_s ≈ 1.000293 at 15°C, 1013 mb)
- N_s: Molecular number density at standard conditions
- λ: Wavelength
- F_K: King correction factor (accounts for anisotropy)

**King Factor:**

.. math::

   F_K = \frac{6+3\delta}{6-7\delta}

Where δ is the **depolarization factor**:

- **Air**: δ = 0.0279 (CTE_MDF_AIR in OSOAA)
- Physical meaning: Fraction of scattered light depolarized

**Cabannes line factor:**

.. math::

   \rho_c = \frac{6(1-\delta)}{3+7\delta}

Values:

- Air: ρ_c ≈ 1.8134
- Used in rotational Raman scattering corrections

Molecular Optical Depth
~~~~~~~~~~~~~~~~~~~~~~~

The **molecular optical thickness** (MOT) is the total Rayleigh scattering optical depth:

.. math::

   \tau_{mol}(\lambda) = \int_0^{z_{TOA}} \beta_{Ray}(z,\lambda) dz

**Wavelength scaling:**

.. math::

   \tau_{mol}(\lambda) = \tau_{mol}(\lambda_0)\left(\frac{\lambda_0}{\lambda}\right)^4

**Typical values at sea level (λ = 550 nm):**

- τ_mol ≈ 0.10

**Spectral values:**

- 400 nm: τ_mol ≈ 0.28
- 550 nm: τ_mol ≈ 0.10  
- 700 nm: τ_mol ≈ 0.04
- 865 nm: τ_mol ≈ 0.017

Rayleigh Phase Matrix
~~~~~~~~~~~~~~~~~~~~~

The phase matrix for molecular scattering includes depolarization:

.. math::

   \mathbf{M}_{Ray}(\Theta) = \frac{3}{4(1+2\gamma)}
   \begin{pmatrix}
   1+\cos^2\Theta & -\sin^2\Theta & 0 & 0 \\
   -\sin^2\Theta & 1+\cos^2\Theta & 0 & 0 \\
   0 & 0 & 2\cos\Theta & 0 \\
   0 & 0 & 0 & (1+\cos^2\Theta)\gamma
   \end{pmatrix}

Where:

.. math::

   \gamma = \frac{\delta}{2-\delta}

**Properties:**

- Symmetric forward/backward scattering
- High polarization at 90° scattering angle
- DoLP(90°) ≈ 0.96 for pure Rayleigh scattering

Vertical Profile
~~~~~~~~~~~~~~~~

Molecular density decreases exponentially with altitude:

.. math::

   \rho(z) = \rho_0 \exp\left(-\frac{z}{H_R}\right)

Where:

- ρ₀: Sea-level density
- H_R: Scale height ≈ 8 km (typical value)
- z: Altitude above sea level

**Corresponding optical depth:**

.. math::

   \tau_{mol}(z) = \tau_{mol}(0) \exp\left(-\frac{z}{H_R}\right)

Aerosol Models
--------------

Overview
~~~~~~~~

Aerosols are suspended particles in the atmosphere originating from:

- **Natural sources**: Sea salt, dust, volcanic ash, biogenic particles
- **Anthropogenic sources**: Combustion products, industrial emissions

OSOAA includes multiple aerosol parameterizations:

1. Mono-modal size distributions (Junge or log-normal)
2. Bi-modal log-normal distributions
3. WMO multi-component models
4. Shettle & Fenn humidity-dependent models
5. External phase functions (user-defined)

Aerosol Optical Properties
~~~~~~~~~~~~~~~~~~~~~~~~~~

Key parameters characterizing aerosols:

**Aerosol Optical Thickness (AOT):**

.. math::

   \tau_{aer}(\lambda) = \int_0^{z_{TOA}} \beta_{ext,aer}(z,\lambda) dz

**Wavelength dependence (Angström law):**

.. math::

   \tau_{aer}(\lambda) = \tau_{aer}(\lambda_0)\left(\frac{\lambda}{\lambda_0}\right)^{-\alpha}

Where α is the **Angström exponent**:

- α = 0.0-0.5: Large particles (maritime, dust)
- α = 0.5-1.0: Mixed aerosols
- α = 1.0-2.0: Small particles (urban pollution, smoke)

**Single scattering albedo:**

.. math::

   \omega_0 = \frac{\beta_{sca}}{\beta_{ext}} = \frac{\beta_{sca}}{\beta_{sca} + \beta_{abs}}

Typical values:

- ω₀ = 0.95-1.00: Non-absorbing (sea salt, sulfates)
- ω₀ = 0.85-0.95: Weakly absorbing (dust)
- ω₀ = 0.70-0.85: Moderately absorbing (mixed pollution)
- ω₀ = 0.20-0.70: Strongly absorbing (soot, black carbon)

**Asymmetry parameter:**

.. math::

   g = \langle\cos\Theta\rangle = \frac{1}{2}\int_{-1}^1 p(\cos\Theta)\cos\Theta \, d(\cos\Theta)

Typical range: 0.5-0.8 (strong forward scattering)

Size Distribution Models
------------------------

Junge Power Law
~~~~~~~~~~~~~~~

Simple power-law distribution:

.. math::

   n(r) = C r^{-\nu}

Parameters:

- ν: Slope parameter (typically 3-4)
- C: Normalization constant
- Range: r_min to r_max

**Properties:**

- Analytical simplicity
- Good approximation for stratospheric aerosols
- No characteristic size

Log-Normal Distribution
~~~~~~~~~~~~~~~~~~~~~~~

Commonly used for tropospheric aerosols:

.. math::

   n(r) = \frac{N}{\sqrt{2\pi}\sigma r} \exp\left[-\frac{(\ln r - \ln r_0)^2}{2\sigma^2}\right]

Parameters:

- N: Total number concentration
- r₀: Median radius (geometric mean)
- σ: Standard deviation of ln(r) (typically 0.4-0.7)

**Volume mean radius:**

.. math::

   r_v = r_0 \exp(1.5\sigma^2)

**Effective radius:**

.. math::

   r_{eff} = r_0 \exp(2.5\sigma^2)

Bi-Modal Log-Normal
~~~~~~~~~~~~~~~~~~~

Represents fine and coarse particle modes:

.. math::

   n(r) = \sum_{i=1}^2 \frac{N_i}{\sqrt{2\pi}\sigma_i r} \exp\left[-\frac{(\ln r - \ln r_{0,i})^2}{2\sigma_i^2}\right]

**Fine mode** (i=1):

- r₀ ~ 0.05-0.2 μm
- Sources: Combustion, urban pollution, biomass burning

**Coarse mode** (i=2):

- r₀ ~ 0.5-2.0 μm
- Sources: Sea salt, dust, resuspended soil

**Volume concentration ratio:**

Defines relative contribution of each mode:

.. math::

   V_f = \frac{V_1}{V_1 + V_2}

WMO Models
----------

Multi-Component Approach
~~~~~~~~~~~~~~~~~~~~~~~~

The World Meteorological Organization defined standard aerosol models with multiple components:

.. math::

   n_{total}(r) = \sum_i f_i n_i(r)

Components:

1. **Water-soluble (WS)**: Sulfates, nitrates, ammonium
2. **Oceanic (OC)**: Sea salt from ocean spray
3. **Dust-like (DL)**: Mineral particles from soil
4. **Soot (SO)**: Black carbon from combustion

Standard Models
~~~~~~~~~~~~~~~

**Maritime:**

- High oceanic component (80-95%)
- Low soot (0-5%)
- Typical: f_OC=0.95, f_WS=0.05, f_DL=0.0, f_SO=0.0

**Continental:**

- Dominant water-soluble (50-70%)
- Moderate dust (20-30%)
- Some soot (10-20%)
- Typical: f_WS=0.5, f_DL=0.3, f_SO=0.2, f_OC=0.0

**Urban:**

- Mixed composition
- High soot content (30-50%)
- Water-soluble (30-50%)
- Some dust (10-20%)
- Typical: f_WS=0.4, f_DL=0.2, f_SO=0.4, f_OC=0.0

**Tropospheric:**

- Background stratospheric aerosols
- Very low concentrations
- Mostly sulfates

Properties by Component
~~~~~~~~~~~~~~~~~~~~~~~

**Water-soluble:**

- r₀ ~ 0.005-0.5 μm (accumulation mode)
- Weakly absorbing: m_i < 0.01
- Hygroscopic: grows with humidity

**Oceanic:**

- r₀ ~ 1.0-10.0 μm (coarse mode)
- Non-absorbing: m_i ≈ 0.0
- High hygroscopicity
- m_r ≈ 1.38-1.50 (increases with RH)

**Dust-like:**

- r₀ ~ 0.5-10.0 μm
- Weakly absorbing: m_i = 0.005-0.01
- m_r ≈ 1.53

**Soot:**

- r₀ ~ 0.01-0.1 μm (nucleation/accumulation)
- Strongly absorbing: m_i = 0.4-0.5
- m_r ≈ 1.75-1.95

Shettle & Fenn Models
---------------------

Humidity Dependence
~~~~~~~~~~~~~~~~~~~

Aerosol properties vary with relative humidity (RH) due to water uptake (hygroscopic growth).

**Dry to wet transition:**

- Particles absorb water at RH > 40%
- Significant growth at RH > 80%
- Deliquescence (phase transition) at RH ~ 75-95%

**Effects of increasing RH:**

1. **Size increase**: r(RH) = r_dry × f(RH)
2. **Refractive index change**: m(RH) decreases (more water)
3. **Scattering increase**: Larger particles scatter more
4. **Absorption change**: Often decreases (dilution effect)

Growth Factor
~~~~~~~~~~~~~

Empirical parameterization:

.. math::

   r(RH) = r_0 \left[1 + a\left(\frac{RH}{100-RH}\right)\right]^b

Where a and b are component-specific parameters.

**Typical growth:**

- RH = 50%: r/r₀ ≈ 1.1-1.2
- RH = 80%: r/r₀ ≈ 1.4-1.8
- RH = 95%: r/r₀ ≈ 2.0-3.0

Available Models
~~~~~~~~~~~~~~~~

1. **Maritime** (SR/LR): Rural/Large maritime
   
   - SR: Rural maritime (RH-dependent)
   - LR: Large maritime particles

2. **Urban** (SU/LU): Small/Large urban
   
   - SU: Small urban particles
   - LU: Large urban particles

3. **Tropospheric** (OM): Stratospheric background

**Humidity classes:**

- 0%, 50%, 70%, 80%, 90%, 95%, 98%, 99%

Refractive Index Variation
~~~~~~~~~~~~~~~~~~~~~~~~~~

As particles absorb water:

.. math::

   m(RH) = \frac{V_{dry}m_{dry} + V_{water}m_{water}}{V_{dry} + V_{water}}

Where:

- m_water = 1.33 + i×0.0 (pure water)
- V_water/V_dry increases with RH

**Result:**

- Real part decreases (approaches 1.33)
- Imaginary part decreases (dilution of absorbers)

Vertical Distribution
---------------------

Scale Height
~~~~~~~~~~~~

Aerosol concentration decreases exponentially:

.. math::

   N(z) = N_0 \exp\left(-\frac{z}{H_a}\right)

Where H_a is the aerosol scale height:

- **Boundary layer aerosols**: H_a ~ 1-2 km
- **Free troposphere**: H_a ~ 2-3 km
- **Elevated layers** (dust, smoke): H_a ~ 3-5 km

**Corresponding AOT profile:**

.. math::

   \tau_{aer}(z) = \tau_{aer}(0) \exp\left(-\frac{z}{H_a}\right)

Typical Values
~~~~~~~~~~~~~~

**Aerosol scale height by type:**

- Maritime: 1.5-2.5 km (confined near surface)
- Continental: 1.0-2.0 km (boundary layer)
- Urban: 0.5-1.5 km (shallow mixed layer)
- Dust layers: 2.0-5.0 km (elevated transport)
- Biomass burning: 2.0-4.0 km (convective lofting)

Layered Structure
~~~~~~~~~~~~~~~~~

Real atmosphere often has multiple layers:

.. math::

   \tau_{aer}(z) = \sum_i \tau_i \exp\left(-\frac{|z-z_i|}{H_i}\right)

Where:

- τ_i: Optical depth of layer i
- z_i: Center altitude of layer i
- H_i: Scale height of layer i

Gaseous Absorption
------------------

Ozone
~~~~~

Significant absorption in UV and visible:

- Hartley band: 200-310 nm (strong)
- Huggins band: 310-400 nm (moderate)
- Chappuis band: 400-700 nm (weak)

**Typical column amount:** 300 Dobson Units = 0.3 atm·cm

Water Vapor
~~~~~~~~~~~

Absorption bands in visible-NIR:

- 590-600 nm (weak)
- 690-730 nm (moderate)
- 810-840 nm (strong)
- 930-980 nm (very strong)

**Highly variable:** 0.5-5.0 cm precipitable water

Oxygen
~~~~~~

- O₂ A-band: 760 nm
- O₂ B-band: 687 nm

**Use:** Atmospheric correction, cloud detection

Note on Implementation
~~~~~~~~~~~~~~~~~~~~~~

OSOAA V2.0 does not include explicit gaseous absorption. Users can:

1. Pre-compute effective transmission
2. Adjust aerosol absorption to approximate gas effects
3. Apply corrections in post-processing

Total Atmospheric Optical Depth
-------------------------------

Combined Effects
~~~~~~~~~~~~~~~~

Total atmospheric optical depth:

.. math::

   \tau_{atm}(\lambda,z) = \tau_{mol}(\lambda,z) + \tau_{aer}(\lambda,z) + \tau_{gas}(\lambda,z)

**Typical partitioning at λ = 550 nm:**

- Clean maritime: τ_mol = 0.10, τ_aer = 0.05, τ_total = 0.15
- Average conditions: τ_mol = 0.10, τ_aer = 0.15, τ_total = 0.25
- Polluted: τ_mol = 0.10, τ_aer = 0.40, τ_total = 0.50

Atmospheric Transmission
~~~~~~~~~~~~~~~~~~~~~~~~

Direct beam transmission:

.. math::

   T_{dir}(\lambda,\theta_s) = \exp\left(-\frac{\tau_{atm}(\lambda)}{\mu_s}\right)

Where μ_s = cos(θ_s) is the cosine of solar zenith angle.

**Path length factor:**

.. math::

   m(\theta_s) = \frac{1}{\mu_s}

For θ_s = 60°, path length is doubled (m = 2.0).

Atmospheric Path Radiance
~~~~~~~~~~~~~~~~~~~~~~~~~

Radiance reaching the sensor from atmospheric scattering:

.. math::

   L_{atm} = L_{mol} + L_{aer} + L_{coup}

Where:

- L_mol: Rayleigh scattering
- L_aer: Aerosol scattering
- L_coup: Molecular-aerosol coupling

**Dominance:**

- Blue wavelengths: Molecular dominant
- Red/NIR wavelengths: Aerosol dominant

Polarization Properties
-----------------------

Degree of Polarization
~~~~~~~~~~~~~~~~~~~~~~

**Rayleigh scattering** produces high polarization:

- DoLP(90°) ≈ 0.96 (maximum)
- Neutral points: 0° and 180° (along sun direction)

**Aerosol scattering** reduces polarization:

- DoLP typically 0.1-0.4
- Depends on size, shape, composition
- Non-spherical particles further reduce polarization

**Combined atmosphere:**

.. math::

   DoLP_{atm} = \frac{\tau_{mol}DoLP_{mol} + \tau_{aer}DoLP_{aer}}{\tau_{mol} + \tau_{aer}}

Multiple Scattering Effects
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Multiple scattering tends to:

- Reduce degree of polarization
- Smooth angular patterns
- Mix polarization states

**Order dependence:**

- Single scattering: High polarization
- Double scattering: Moderate polarization
- Higher orders: Increasingly depolarized

Practical Considerations
------------------------

Parameter Selection
~~~~~~~~~~~~~~~~~~~

**For ocean color applications:**

- Use WMO maritime for open ocean
- Use Shettle & Fenn maritime for coastal with RH
- Measure/estimate local AOT when possible
- Match Angström exponent to conditions

**Typical configurations:**

**Clean ocean:**

::

   AER.Model 1
   AER.WMO.Model 1
   AER.AOTref 0.05
   AER.Angexp 0.5

**Coastal:**

::

   AER.Model 3
   AER.SF.Model 1
   AER.SF.RH 80.0
   AER.AOTref 0.15

Validation Data Sources
~~~~~~~~~~~~~~~~~~~~~~~

- **AERONET**: Ground-based sun photometer network
- **MODIS**: Satellite aerosol products
- **MISR**: Multi-angle aerosol retrievals
- **CALIOP**: Lidar vertical profiles

Uncertainties
~~~~~~~~~~~~~

**Major sources:**

1. AOT: ±0.02-0.05 (satellite), ±0.01 (AERONET)
2. Angström exponent: ±0.2
3. Single scattering albedo: ±0.03
4. Aerosol type/composition
5. Vertical distribution

See Also
--------

- :ref:`radiative_transfer` for theoretical foundation
- :ref:`ocean_model` for ocean optical properties
- :ref:`surface_interface` for atmosphere-ocean boundary
- :ref:`parameter_reference` for parameter details
- :ref:`bibliography` for references (Shettle & Fenn 1979, d'Almeida et al. 1991)
