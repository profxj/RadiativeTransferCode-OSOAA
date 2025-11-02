.. _ocean_model:

Ocean Model
===========

This section describes the optical properties of the ocean component in OSOAA, including absorption and scattering by water molecules, phytoplankton, mineral particles, and dissolved organic matter.

.. contents:: Contents
   :local:
   :depth: 3

Introduction
------------

The ocean in OSOAA is characterized by its inherent optical properties (IOPs), which describe how seawater absorbs and scatters light. These properties are fundamental to ocean color remote sensing and underwater light field calculations.

OSOAA models the ocean as a vertically stratified medium with depth-dependent optical properties determined by:

* Pure seawater (molecular absorption and scattering)
* Phytoplankton (chlorophyll-bearing particles)
* Mineral-like particles (suspended sediments)
* Colored dissolved organic matter (CDOM, "yellow substance")
* Detritus (dead organic matter)

The model supports both bio-optical parameterizations based on chlorophyll concentration and user-defined profiles from in-situ measurements.

Inherent Optical Properties
---------------------------

Definition and Significance
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Inherent optical properties (IOPs) characterize the medium's interaction with light, independent of the ambient light field. The fundamental IOPs are:

**Absorption Coefficient** a(λ, z)
   Describes the fractional loss of radiant flux per unit path length due to absorption:

   .. math::

      a(\lambda, z) = \frac{d\Phi_{abs}}{d\Phi \, dz}

   Units: m⁻¹

**Scattering Coefficient** b(λ, z)
   Describes the fractional loss of radiant flux per unit path length due to scattering:

   .. math::

      b(\lambda, z) = \frac{d\Phi_{sca}}{d\Phi \, dz}

   Units: m⁻¹

**Extinction Coefficient** β(λ, z)
   Total attenuation combining absorption and scattering:

   .. math::

      \beta(\lambda, z) = a(\lambda, z) + b(\lambda, z)

   Units: m⁻¹

**Single Scattering Albedo** ω₀(λ, z)
   Ratio of scattering to total extinction:

   .. math::

      \omega_0(\lambda, z) = \frac{b(\lambda, z)}{\beta(\lambda, z)}

   Dimensionless, range: 0 ≤ ω₀ ≤ 1

**Optical Depth** τ(λ, z₁, z₂)
   Integrated extinction along a path:

   .. math::

      \tau(\lambda, z_1, z_2) = \int_{z_1}^{z_2} \beta(\lambda, z') \, dz'

   Dimensionless

Component Contributions
~~~~~~~~~~~~~~~~~~~~~~~

The total absorption and scattering coefficients are the sum of contributions from all constituents:

**Total Absorption:**

.. math::

   a_{total}(\lambda, z) = a_w(\lambda) + a_{ph}(\lambda, z) + a_{CDOM}(\lambda, z) + a_{det}(\lambda, z)

Where:

* :math:`a_w` = Pure water absorption
* :math:`a_{ph}` = Phytoplankton absorption
* :math:`a_{CDOM}` = Colored dissolved organic matter absorption
* :math:`a_{det}` = Detritus absorption

**Total Scattering:**

.. math::

   b_{total}(\lambda, z) = b_w(\lambda) + b_{ph}(\lambda, z) + b_{min}(\lambda, z)

Where:

* :math:`b_w` = Pure water (molecular) scattering
* :math:`b_{ph}` = Phytoplankton scattering
* :math:`b_{min}` = Mineral particle scattering

Pure Seawater Properties
------------------------

Absorption
~~~~~~~~~~

Pure water absorption is highly wavelength-dependent, with strong absorption in the red and infrared regions:

**Data Source:**

OSOAA uses absorption coefficients from Pope and Fry (1997) for 380-700 nm and Kou et al. (1993) for longer wavelengths, stored in:

``specific/info_OSOAA_SEA_MOL_COEFFS_JUNE_2013.txt``

**Spectral Characteristics:**

* **Blue (400-500 nm)**: Very low absorption (~0.005 m⁻¹)
* **Green (500-600 nm)**: Low absorption (~0.05 m⁻¹)
* **Red (600-700 nm)**: High absorption (0.2-0.5 m⁻¹)
* **Near-IR (>700 nm)**: Very high absorption (>1.0 m⁻¹)

This explains why underwater environments appear blue-green - red light is quickly absorbed.

Scattering
~~~~~~~~~~

Molecular (Rayleigh) scattering by water molecules follows a λ⁻⁴·³² power law:

.. math::

   b_w(\lambda) = b_w(550) \left(\frac{550}{\lambda}\right)^{4.32}

Where:

* :math:`b_w(550) \approx 0.0015` m⁻¹ at 550 nm
* Temperature and salinity have minor effects

**Phase Function:**

Molecular scattering in water is nearly isotropic with slight forward preference. The volume scattering function is:

.. math::

   \beta_w(\theta) = \frac{b_w}{4\pi} \left[1 + 0.835\cos^2\theta\right]

**Backscattering Ratio:**

.. math::

   \tilde{b}_w = \frac{b_{bw}}{b_w} \approx 0.5

Much higher than atmospheric Rayleigh scattering due to density fluctuations in liquid phase.

Phytoplankton Optical Properties
--------------------------------

Bio-Optical Model
~~~~~~~~~~~~~~~~~

OSOAA implements the bio-optical model of Morel (1988) and extensions, relating optical properties to chlorophyll-a concentration [Chl].

Absorption
~~~~~~~~~~

**Chlorophyll-Specific Absorption:**

Phytoplankton absorption depends on chlorophyll concentration and wavelength:

.. math::

   a_{ph}(\lambda) = A(\lambda) \cdot [Chl]^{B(\lambda)}

Where A(λ) and B(λ) are empirically determined coefficients based on Bricaud et al. (1995, 1998).

**Spectral Shape:**

* **Blue band (440 nm)**: Strong absorption peak (chlorophyll-a)
* **Green band (550 nm)**: Minimum absorption
* **Red band (675 nm)**: Moderate absorption peak (chlorophyll-a)

**Typical Values:**

For [Chl] = 1.0 mg/m³:

* a_ph(440) ≈ 0.035 m⁻¹
* a_ph(550) ≈ 0.008 m⁻¹
* a_ph(675) ≈ 0.024 m⁻¹

The package effect causes the exponent B(λ) < 1, meaning per-chlorophyll absorption decreases with increasing concentration.

Scattering
~~~~~~~~~~

**Particle Backscattering:**

.. math::

   b_{bp}(\lambda) = b_{bp}(550) \left(\frac{\lambda}{550}\right)^{-\eta}

Where:

* :math:`b_{bp}(550) \approx 0.3 \cdot [Chl]^{0.62} \cdot 0.002` m⁻¹
* :math:`\eta \approx 1.0` (spectral slope)

**Backscattering Ratio:**

.. math::

   \tilde{b}_{bp} = \frac{b_{bp}}{b_p} \approx 0.01 \text{ to } 0.02

Phytoplankton are strongly forward-scattering particles.

**Phase Function:**

The phytoplankton phase function is highly peaked in the forward direction, typically represented by Petzold's average particle phase function or Fournier-Forand models.

Vertical Profiles
~~~~~~~~~~~~~~~~~

OSOAA supports three types of chlorophyll vertical profiles:

**1. Homogeneous Profile (Type 0):**

.. math::

   [Chl](z) = [Chl]_0

Constant concentration throughout the water column.

**2. Gaussian Profile (Type 1):**

.. math::

   [Chl](z) = [Chl]_{bg} + [Chl]_{max} \exp\left[-\frac{(z-z_{max})^2}{2\sigma_z^2}\right]

Where:

* :math:`[Chl]_{bg}` = Background chlorophyll concentration
* :math:`[Chl]_{max}` = Maximum chlorophyll enhancement
* :math:`z_{max}` = Depth of chlorophyll maximum (typically 30-80 m)
* :math:`\sigma_z` = Width of the maximum (typically 10-30 m)

This represents the deep chlorophyll maximum (DCM) common in stratified waters.

**3. User-Defined Profile (Type 2):**

Users can specify arbitrary depth-dependent chlorophyll profiles from measurements.

Typical Chlorophyll Ranges
~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Ultra-oligotrophic**: < 0.03 mg/m³ (subtropical gyres)
* **Oligotrophic**: 0.03-0.1 mg/m³ (open ocean)
* **Mesotrophic**: 0.1-1.0 mg/m³ (coastal waters)
* **Eutrophic**: 1.0-10.0 mg/m³ (productive coastal regions)
* **Highly eutrophic**: > 10.0 mg/m³ (blooms, upwelling zones)

Mineral-Like Particles
----------------------

Suspended sediments and other non-algal particles contribute to ocean optical properties, especially in coastal and turbid waters.

Concentration Parameter
~~~~~~~~~~~~~~~~~~~~~~~

Mineral-like particles are characterized by concentration:

.. math::

   C_{sed} \text{ [g/m³]}

Typical ranges:

* Open ocean: < 0.1 g/m³
* Coastal waters: 0.1-10 g/m³
* Turbid estuaries: 10-100 g/m³
* Extreme resuspension: > 100 g/m³

Optical Properties
~~~~~~~~~~~~~~~~~~

**Absorption:**

Mineral particles have weak but spectrally flat absorption:

.. math::

   a_{min}(\lambda) = a_{min}^* \cdot C_{sed}

Where :math:`a_{min}^*` is the mass-specific absorption coefficient (~0.01-0.05 m²/g).

**Scattering:**

Much stronger than absorption:

.. math::

   b_{min}(\lambda) = b_{min}^* \cdot C_{sed} \left(\frac{\lambda}{550}\right)^{-\gamma}

Where:

* :math:`b_{min}^*` = Mass-specific scattering coefficient (~0.5-1.0 m²/g)
* :math:`\gamma \approx 0.5` to 1.5 (spectral slope)

**Backscattering Ratio:**

Minerals have higher backscattering ratios than phytoplankton:

.. math::

   \tilde{b}_{min} \approx 0.01 \text{ to } 0.03

**Phase Function:**

Similar to phytoplankton but less forward-peaked. Depends on particle size distribution and composition.

**Refractive Index:**

Typical values for minerals:

* Real part: n = 1.15-1.18
* Imaginary part: n_i = 0.001-0.01

Colored Dissolved Organic Matter (CDOM)
---------------------------------------

Also known as "yellow substance" or gelbstoff, CDOM consists of dissolved organic compounds that absorb light, particularly in the blue-UV region.

Absorption Model
~~~~~~~~~~~~~~~~

CDOM absorption follows an exponential spectral decay:

.. math::

   a_{CDOM}(\lambda) = a_{CDOM}(440) \exp[-S(\lambda - 440)]

Where:

* :math:`a_{CDOM}(440)` = Reference absorption at 440 nm [m⁻¹]
* :math:`S` = Spectral slope parameter [nm⁻¹]
* Typical :math:`S = 0.014` to 0.020 nm⁻¹

**Characteristics:**

* **Non-scattering**: CDOM only absorbs, does not scatter
* **Decreases with wavelength**: Strong in UV/blue, negligible in red
* **Highly variable**: Depends on terrestrial input, biology, photodegradation

Typical Concentration Ranges
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Values of a_CDOM(440):

* **Oligotrophic open ocean**: 0.001-0.01 m⁻¹
* **Mesotrophic ocean**: 0.01-0.05 m⁻¹
* **Coastal waters**: 0.05-0.5 m⁻¹
* **River-influenced**: 0.5-5.0 m⁻¹
* **High-CDOM rivers/wetlands**: > 5.0 m⁻¹

Spectral Slope Variations
~~~~~~~~~~~~~~~~~~~~~~~~~

The slope S varies by source:

* **Marine CDOM**: S ≈ 0.020 nm⁻¹ (steeper decay)
* **Mixed sources**: S ≈ 0.015 nm⁻¹
* **Terrestrial CDOM**: S ≈ 0.012 nm⁻¹ (slower decay)

**Impact on Ocean Color:**

High CDOM absorption in blue wavelengths can mask chlorophyll signals, making atmospheric correction and algorithm development challenging in coastal waters.

Detritus
--------

Dead organic matter (detritus) contributes to absorption with spectral characteristics similar to CDOM:

.. math::

   a_{det}(\lambda) = a_{det}(440) \exp[-S_{det}(\lambda - 440)]

Where:

* :math:`S_{det} \approx 0.011` nm⁻¹
* Typically coupled to phytoplankton concentration

OSOAA often combines detritus with CDOM in the "yellow substance" absorption term.

User-Defined Optical Properties
-------------------------------

Custom IOP Profiles
~~~~~~~~~~~~~~~~~~~

For specialized applications or validation studies, OSOAA allows users to input measured absorption and scattering profiles directly.

**Input Format (HYD.Model = 5):**

File structure for ``HYD.UserIOP.File``:

::

    # Depth(m)  a_total(m^-1)  b_total(m^-1)  bb_total(m^-1)
    0.0         0.050          0.300          0.010
    5.0         0.055          0.320          0.011
    10.0        0.060          0.340          0.012
    20.0        0.065          0.360          0.013
    ...

**Advantages:**

* Direct use of field measurements
* Bypass bio-optical models
* Validate model assumptions
* Study non-standard water types

**Requirements:**

* Absorption coefficient a(z)
* Scattering coefficient b(z)
* Backscattering coefficient b_b(z)
* Depth resolution adequate for vertical structure

Optical Water Types
-------------------

Case 1 Waters
~~~~~~~~~~~~~

**Definition:** Waters where optical properties are dominated by phytoplankton and their associated products (CDOM and detritus).

**Characteristics:**

* Open ocean environments
* Bio-optical models applicable
* Chlorophyll is primary driver
* Predictable relationships between IOPs

**OSOAA Application:**

Use bio-optical models (HYD.Model = 0 or 1) with chlorophyll concentration as primary input.

Case 2 Waters
~~~~~~~~~~~~~

**Definition:** Waters where optical properties are significantly influenced by constituents other than phytoplankton (minerals, land-derived CDOM).

**Characteristics:**

* Coastal and inland waters
* River influence
* Sediment resuspension
* Bio-optical models may not apply

**OSOAA Application:**

Use combined models (HYD.Model = 2 or 3) with explicit mineral and CDOM inputs, or custom IOP profiles (HYD.Model = 5).

Implementation in OSOAA
-----------------------

Hydrosol Models
~~~~~~~~~~~~~~~

OSOAA provides five hydrosol model options:

**Model 0: Mono-modal size distribution**
   Direct specification of particle size distribution parameters for Mie calculations.

**Model 1: Bio-optical (chlorophyll-based)**
   Morel-type bio-optical model relating optical properties to [Chl].

**Model 2: Mineral-like particles**
   Explicit mineral particle properties based on concentration.

**Model 3: Combined bio-optical + minerals**
   Both phytoplankton and mineral contributions.

**Model 4: External phase functions**
   User-provided phase functions and radiative properties.

**Model 5: User-defined IOPs**
   Direct input of measured absorption/scattering profiles.

Vertical Discretization
~~~~~~~~~~~~~~~~~~~~~~~

The ocean is divided into layers for radiative transfer calculations:

* **Typical resolution**: 20-50 layers
* **Depth range**: 0 to specified maximum depth (50-200 m typical)
* **Finer resolution near surface**: Captures steep gradients
* **Layer spacing**: Linear or logarithmic

Profile Construction
~~~~~~~~~~~~~~~~~~~~

The vertical profile construction involves:

1. **Read input parameters** (chlorophyll, minerals, CDOM)
2. **Compute vertical profiles** (Gaussian, homogeneous, or custom)
3. **Calculate component IOPs** at each depth and wavelength
4. **Sum total absorption and scattering**
5. **Compute optical depth** by integration

Key Algorithms
~~~~~~~~~~~~~~

Located in ``src/OSOAA_HYDROSOLS.F`` and ``src/OSOAA_PROFILE.F``:

.. code-block:: fortran

   SUBROUTINE HYDROSOLS_CHLOROPHYLL(CHL_CONCENTRATION, WAVELENGTH, ...)
   ! Computes phytoplankton optical properties from [Chl]

   SUBROUTINE HYDROSOLS_MINERAL(CSED, WAVELENGTH, ...)
   ! Computes mineral particle optical properties

   SUBROUTINE HYDROSOLS_YELLOW_SUBSTANCE(ACDOM440, S, WAVELENGTH, ...)
   ! Computes CDOM absorption

   SUBROUTINE PROFILE_OCEAN(Z_LEVELS, N_LEVELS, ...)
   ! Builds complete ocean vertical profile

Truncation of Forward Peak
~~~~~~~~~~~~~~~~~~~~~~~~~~

Strongly forward-scattering phase functions (phytoplankton, large particles) require special numerical treatment:

**Delta-Eddington Approximation:**

The extreme forward peak is separated and treated as unscattered:

.. math::

   p(\theta) = 2f\delta(\cos\theta - 1) + (1-f)p'(\theta)

Where:

* :math:`f` = Forward fraction (typically 0.8-0.9 for phytoplankton)
* :math:`p'(\theta)` = Truncated phase function

**Adjusted Optical Properties:**

.. math::

   \beta' = (1-f\omega_0)\beta

.. math::

   \omega_0' = \frac{(1-f)\omega_0}{1-f\omega_0}

**Truncation Constants:**

In ``OSOAA.h``:

.. code-block:: c

   #define CTE_HYD_MU1_TRONCA 0.85
   #define CTE_HYD_MU2_TRONCA 0.92

Output and Validation
---------------------

IOP Output Files
~~~~~~~~~~~~~~~~

OSOAA generates detailed logs of computed optical properties:

**SEA_LOG.txt**

Contains:

* Input parameters (chlorophyll, minerals, CDOM)
* Computed IOPs at each level
* Vertical profiles
* Total optical depths

Example output::

    ==========================================
    Ocean Optical Properties
    ==========================================
    
    Wavelength: 550.0 nm
    
    Phytoplankton:
      Chlorophyll concentration: 0.5 mg/m³
      Absorption coefficient: 0.0234 m⁻¹
      Scattering coefficient: 0.0456 m⁻¹
      Backscattering ratio: 0.015
    
    Minerals:
      Concentration: 1.0 g/m³
      Absorption coefficient: 0.0123 m⁻¹
      Scattering coefficient: 0.0789 m⁻¹
      Backscattering ratio: 0.020
    
    CDOM:
      a_CDOM(440): 0.05 m⁻¹
      Spectral slope: 0.014 nm⁻¹
      a_CDOM(550): 0.0187 m⁻¹
    
    Total:
      Total absorption: 0.0544 m⁻¹
      Total scattering: 0.1260 m⁻¹
      Total extinction: 0.1804 m⁻¹
      Single scattering albedo: 0.698
      Optical depth (100m): 18.04

Validation Strategies
~~~~~~~~~~~~~~~~~~~~~

**1. In-Situ Measurements:**

Compare OSOAA IOPs with:

* AC-9/AC-S absorption/attenuation meters
* BB-series backscattering sensors
* VSF (volume scattering function) measurements
* HPLC chlorophyll analysis

**2. Remote Sensing Validation:**

* Water-leaving radiance comparisons
* Remote sensing reflectance (Rrs)
* Satellite matchups (SeaWiFS, MODIS, OLCI)

**3. Bio-Optical Model Validation:**

* Test [Chl]-IOP relationships
* Regional tuning of coefficients
* Validate vertical profile shapes

Uncertainty Analysis
~~~~~~~~~~~~~~~~~~~~

**Sources of Uncertainty:**

1. **Chlorophyll Concentration:**
   
   * Measurement: ±5-30%
   * Spatial/temporal variability
   * HPLC vs. fluorescence

2. **Bio-Optical Models:**
   
   * [Chl]-absorption: ±20-40%
   * Backscattering: ±50%
   * Regional/seasonal variations

3. **CDOM Characterization:**
   
   * Spectral slope: ±20%
   * Spatial variability
   * Photodegradation

4. **Mineral Properties:**
   
   * Composition variability
   * Size distribution
   * Refractive index

Sensitivity Studies
~~~~~~~~~~~~~~~~~~~

Recommended parameter perturbations:

* Chlorophyll: ±50%
* CDOM: ±100%
* Mineral concentration: ±50%
* Vertical profile shape: Homogeneous vs. Gaussian

Best Practices
--------------

Model Selection
~~~~~~~~~~~~~~~

1. **Open Ocean (Case 1):**
   
   * Use bio-optical model (HYD.Model = 1)
   * Specify chlorophyll concentration
   * Use Gaussian profile for stratified waters

2. **Coastal Waters (Case 2):**
   
   * Use combined model (HYD.Model = 3)
   * Include mineral particles
   * Specify realistic CDOM values
   * Consider homogeneous or custom profiles

3. **Validation Studies:**
   
   * Use custom IOPs (HYD.Model = 5)
   * Input measured profiles directly

Parameter Selection
~~~~~~~~~~~~~~~~~~~

**Chlorophyll:**

* Match climatology or satellite data
* Use in-situ measurements when available
* Consider seasonal variations

**CDOM:**

* Open ocean: 0.01-0.05 m⁻¹
* Coastal: 0.05-0.5 m⁻¹
* Check local measurements

**Minerals:**

* Negligible in open ocean
* Significant in coastal/turbid waters
* Depends on sediment type and resuspension

Vertical Resolution
~~~~~~~~~~~~~~~~~~~

* **Euphotic zone**: At least 10-20 layers
* **Deep chlorophyll maximum**: Finer resolution around DCM
* **Surface layer**: 1-5 m resolution for accurate boundary conditions

Computational Considerations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Wavelength coverage**: Simulate full visible spectrum (400-700 nm)
* **Spectral resolution**: 10-50 nm steps adequate
* **Multiple scenarios**: Test sensitivity to parameter variations

See Also
--------

* :ref:`radiative_transfer` - Theoretical foundation
* :ref:`atmosphere_model` - Atmospheric optical properties
* :ref:`surface_interface` - Ocean-atmosphere boundary
* :ref:`successive_orders` - Numerical solution method
* :ref:`parameter_reference` - Complete parameter descriptions
* :ref:`bibliography` - References (Morel 1988, Bricaud et al. 1995, Pope & Fry 1997)

References
----------

**Primary References:**

* Morel, A. (1988). "Optical modeling of the upper ocean in relation to its biogenous matter content (Case I waters)." *Journal of Geophysical Research* 93(C9): 10749-10768.

* Bricaud, A., et al. (1995). "Variability in the chlorophyll-specific absorption coefficients of natural phytoplankton: Analysis and parameterization." *Journal of Geophysical Research* 100(C7): 13321-13332.

* Pope, R. M. and E. S. Fry (1997). "Absorption spectrum (380-700 nm) of pure water. II. Integrating cavity measurements." *Applied Optics* 36: 8710-8723.

* Mobley, C. D. (1994). *Light and Water: Radiative Transfer in Natural Waters*. Academic Press.

**Additional Reading:**

* Gordon, H. R. and A. Morel (1983). *Remote Assessment of Ocean Color for Interpretation of Satellite Visible Imagery*. Springer-Verlag.

* IOCCG (2006). *Remote Sensing of Inherent Optical Properties*. Report 5, International Ocean-Colour Coordinating Group.
