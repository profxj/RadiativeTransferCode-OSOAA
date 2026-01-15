.. _surface_interface:

Surface Interface
=================

This section describes the treatment of the atmosphere-ocean interface in OSOAA, including Fresnel reflection and refraction, the Cox & Munk rough surface model, and wave-slope statistics.

.. contents:: Contents
   :local:
   :depth: 3

Introduction
------------

The air-sea interface is a critical boundary in coupled atmosphere-ocean radiative transfer. Light crossing this interface experiences:

* **Reflection**: Upward reflection of downwelling atmospheric radiance
* **Transmission**: Downward transmission of atmospheric light into ocean
* **Refraction**: Bending of light rays due to refractive index change
* **Roughness effects**: Wind-driven waves create a statistically distributed surface

OSOAA provides two surface models:

**Model 0: Flat Surface**
   Simple Fresnel reflection/transmission at a planar interface. Useful for calm conditions or theoretical studies.

**Model 1: Rough Surface (Cox & Munk)**
   Realistic wind-roughened surface with statistical wave-slope distribution. Essential for accurate ocean color remote sensing.

The surface interface affects:

* Water-leaving radiance magnitude and angular distribution
* Sun glint patterns
* Skylight reflection
* Polarization state of transmitted/reflected light
* Atmospheric correction algorithms

Physical Principles
-------------------

Refractive Index
~~~~~~~~~~~~~~~~

The refractive index of seawater relative to air determines reflection and refraction behavior:

.. math::

   n_{water} = \frac{c_{air}}{c_{water}}

**Typical Values:**

At 20°C, 35 PSU (practical salinity units):

* 400 nm: n ≈ 1.345
* 550 nm: n ≈ 1.340
* 700 nm: n ≈ 1.335

**Wavelength Dependence:**

.. math::

   n(\lambda) \approx n_0 + \frac{A}{\lambda^2} + \frac{B}{\lambda^4}

For most ocean color applications, n ≈ 1.34 is adequate (typical OSOAA default: 1.334).

**Temperature and Salinity Effects:**

* ∂n/∂T ≈ -0.0001/°C
* ∂n/∂S ≈ +0.0002/PSU

Generally small corrections for ocean color work.

Snell's Law
~~~~~~~~~~~

Light crossing the interface obeys Snell's law:

.. math::

   n_{air} \sin\theta_i = n_{water} \sin\theta_t

Where:

* θ_i = Incident angle (from normal)
* θ_t = Transmitted/refracted angle

**Key Consequences:**

1. **Transmitted cone compression**: Light from a 180° hemisphere in air maps to approximately 97° cone underwater (θ_t ≈ 48.6° for normal incidence)

2. **Critical angle**: Total internal reflection occurs for underwater light at:

   .. math::

      \theta_c = \arcsin(n_{air}/n_{water}) \approx 48.6°

3. **Snell's window**: Upwelling underwater light can only escape through a cone of half-angle ≈ 48.6°

Fresnel Equations
~~~~~~~~~~~~~~~~~

The Fresnel equations quantify reflection and transmission for unpolarized and polarized light.

**Reflectance for Perpendicular Polarization (⊥, s-polarized):**

.. math::

   R_\perp = \left|\frac{n_1\cos\theta_i - n_2\cos\theta_t}{n_1\cos\theta_i + n_2\cos\theta_t}\right|^2

**Reflectance for Parallel Polarization (∥, p-polarized):**

.. math::

   R_\parallel = \left|\frac{n_2\cos\theta_i - n_1\cos\theta_t}{n_2\cos\theta_i + n_1\cos\theta_t}\right|^2

**Unpolarized Reflectance:**

.. math::

   R = \frac{1}{2}(R_\parallel + R_\perp)

**Transmittance:**

.. math::

   T_\perp = 1 - R_\perp, \quad T_\parallel = 1 - R_\parallel

**Brewster's Angle:**

At Brewster's angle θ_B, parallel-polarized light has zero reflection:

.. math::

   \theta_B = \arctan(n_2/n_1) \approx 53.1°

This creates strong polarization in skylight reflected from the ocean surface.

Angular Dependence
~~~~~~~~~~~~~~~~~~

**Nadir Reflectance (θ = 0°):**

At normal incidence:

.. math::

   R(0°) = \left(\frac{n_{water} - n_{air}}{n_{water} + n_{air}}\right)^2 \approx 0.02

Only ~2% of light is reflected at nadir.

**Grazing Incidence (θ → 90°):**

At grazing angles:

.. math::

   R(90°) \rightarrow 1.0

Nearly 100% reflection occurs.

**Minimum Reflectance:**

For water-to-air transmission, minimum reflectance occurs at Brewster's angle (~53°) for parallel polarization.

Flat Surface Model
------------------

Description
~~~~~~~~~~~

The flat surface model (SEA.Type = 0) treats the air-sea interface as a smooth, horizontal plane.

**Assumptions:**

* No waves or roughness
* Specular (mirror-like) reflection
* Direct application of Fresnel equations

**When to Use:**

* Theoretical studies
* Calm conditions (wind < 1 m/s)
* Sensitivity analyses
* Computational efficiency

Implementation
~~~~~~~~~~~~~~

**Reflection Matrix:**

For incident direction Ω_i and reflected direction Ω_r:

.. math::

   \mathbf{R}(\Omega_i, \Omega_r) = R_{Fresnel}(\theta_i) \delta(\theta_r - \theta_i) \delta(\phi_r - \phi_i \pm \pi)

The delta functions enforce the law of reflection:

* Angle of incidence = angle of reflection
* Reflection occurs in the plane of incidence

**Transmission Matrix:**

For incident direction Ω_i and transmitted direction Ω_t:

.. math::

   \mathbf{T}(\Omega_i, \Omega_t) = T_{Fresnel}(\theta_i) \delta(\theta_t - \theta_t^{Snell})

Where θ_t^{Snell} satisfies Snell's law.

**Computational Efficiency:**

Flat surface calculations are extremely fast - only single Fresnel coefficient evaluations required.

Limitations
~~~~~~~~~~~

* **Unrealistic for most conditions**: Even light winds (>2 m/s) create significant roughness
* **No sun glint**: Cannot model specular reflection patterns
* **Incorrect polarization**: Overestimates polarization effects
* **Angular distribution**: Radiance angular patterns unrealistic

Rough Surface Model (Cox & Munk)
--------------------------------

Historical Development
~~~~~~~~~~~~~~~~~~~~~~

The Cox & Munk surface model, developed in the 1950s from sun glint photographs, remains the standard for ocean color applications.

**Original Papers:**

* Cox, C. and W. Munk (1954). "Measurement of the roughness of the sea surface from photographs of the sun's glitter." *JOSA* 44(11): 838-850.

* Cox, C. and W. Munk (1956). "Slopes of the sea surface deduced from photographs of sun glitter." *Bulletin of SIO* 6: 401-488.

**Key Insight:**

Sun glint patterns reveal the statistical distribution of wave slopes on the ocean surface.

Wave Slope Statistics
~~~~~~~~~~~~~~~~~~~~~

The Cox & Munk model describes the probability distribution of wave slopes as a bivariate Gaussian.

**Slope Components:**

Consider a wave facet with normal vector **n**. The slopes in cross-wind (x) and up-wind (y) directions are:

.. math::

   Z_x = \tan\theta_x, \quad Z_y = \tan\theta_y

For small angles (typical case): Z_x ≈ θ_x, Z_y ≈ θ_y

**Probability Density Function:**

.. math::

   P(Z_x, Z_y) = \frac{1}{2\pi\sigma_c\sigma_u} \exp\left[-\frac{1}{2}\left(\frac{Z_x^2}{\sigma_c^2} + \frac{Z_y^2}{\sigma_u^2}\right)\right]

Where:

* σ_c = Cross-wind standard deviation
* σ_u = Up-wind standard deviation
* Assumed uncorrelated (Gaussian approximation)

**Wind Speed Relationships:**

Cox and Munk derived empirical relationships from measurements:

.. math::

   \sigma_c^2 = 0.003 + 0.00512 \cdot U

.. math::

   \sigma_u^2 = 0.00316 \cdot U

Where U is the wind speed at 10 m height [m/s].

**Mean Square Slope:**

.. math::

   \sigma_{total}^2 = \sigma_c^2 + \sigma_u^2 = 0.003 + 0.00828 \cdot U

**Physical Interpretation:**

* **σ_c > σ_u**: Waves are elongated perpendicular to wind direction
* **Typical ratio**: σ_c/σ_u ≈ √(1.6) ≈ 1.26
* **Wind dependence**: Wave roughness increases linearly with wind speed

Typical Values
~~~~~~~~~~~~~~

Wind Speed vs. Wave Slope Statistics:

.. list-table:: Wind Speed Effects
   :widths: 20 20 20 20 20
   :header-rows: 1

   * - Wind (m/s)
     - σ_c²
     - σ_u²
     - σ_total²
     - RMS slope (°)
   * - 0
     - 0.003
     - 0.000
     - 0.003
     - 3.1°
   * - 3
     - 0.018
     - 0.009
     - 0.028
     - 9.5°
   * - 5
     - 0.029
     - 0.016
     - 0.044
     - 12.1°
   * - 10
     - 0.054
     - 0.032
     - 0.086
     - 16.8°
   * - 15
     - 0.080
     - 0.047
     - 0.127
     - 20.4°

**Beaufort Scale Correspondence:**

* 0-1 m/s: Calm (glassy surface)
* 1-3 m/s: Light air
* 3-5 m/s: Light breeze (small wavelets)
* 5-8 m/s: Gentle breeze (large wavelets)
* 8-11 m/s: Moderate breeze (small waves)
* 11-15 m/s: Fresh breeze (moderate waves)

Reflection from Rough Surface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Concept:**

Instead of single specular reflection, the rough surface consists of many randomly oriented facets. Each facet reflects according to Fresnel equations, then contributions are integrated over the slope distribution.

**Reflection Process:**

1. **Identify contributing facets**: For incident direction Ω_i and reflected direction Ω_r, only facets with normal **n** satisfying the law of reflection contribute

2. **Compute facet normal**: The required normal is the bisector of incident and reflected directions:

   .. math::

      \vec{n} = \frac{\vec{\Omega}_i + \vec{\Omega}_r}{|\vec{\Omega}_i + \vec{\Omega}_r|}

3. **Calculate Fresnel reflectance**: For this facet orientation

4. **Weight by probability**: Multiply by P(Z_x, Z_y) for this facet slope

5. **Apply geometric factors**: Account for shadowing, masking, and foreshortening

**Integrated Reflectance:**

.. math::

   R(\Omega_i, \Omega_r) = \int_{-\infty}^{\infty} \int_{-\infty}^{\infty} R_{Fresnel}(\vec{n}) \, P(Z_x, Z_y) \, \frac{|\vec{n} \cdot \vec{\Omega}_i|}{|\vec{k} \cdot \vec{\Omega}_i|} \, S(\Omega_i, \Omega_r, \vec{n}) \, dZ_x \, dZ_y

Where:

* R_Fresnel(n) = Fresnel reflectance for facet with normal n
* P(Z_x, Z_y) = Slope probability distribution
* Geometric factor accounts for projected area
* S = Shadowing/masking function

Transmission Through Rough Surface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Transmission from air into water (or vice versa) involves refraction by tilted wave facets.

**Process:**

1. **Find facet normal**: For incident Ω_i and transmitted Ω_t, solve for normal satisfying Snell's law:

   .. math::

      n_1 \sin\theta_i = n_2 \sin\theta_t

2. **Compute Fresnel transmission**: For this facet

3. **Weight by probability**: P(Z_x, Z_y) for facet slope

4. **Integrate** over all contributing facets

**Result:**

Light transmitted through the rough interface has a broader angular distribution than flat surface transmission.

Shadowing and Masking
~~~~~~~~~~~~~~~~~~~~~

At grazing angles, wave facets can shadow or mask each other, reducing the effective reflectance.

**Shadowing Function:**

Smith (1967) derived a shadowing correction:

.. math::

   S(\theta) = \frac{1}{1 + \Lambda(\theta)}

Where Λ(θ) increases with angle from normal, reducing reflectance at grazing angles more than simple Fresnel theory predicts.

**Physical Effect:**

* Small at near-nadir viewing (θ < 30°)
* Significant at large viewing angles (θ > 60°)
* Depends on wave slope variance

Sun Glint
~~~~~~~~~

**Definition:**

Sun glint is the bright, specular reflection of direct sunlight from wave facets oriented to satisfy the law of reflection.

**Glint Geometry:**

The specular direction Ω_spec is related to solar direction Ω_sun by:

.. math::

   \vec{\Omega}_{spec} = \vec{\Omega}_{sun} - 2(\vec{\Omega}_{sun} \cdot \vec{k})\vec{k}

Where **k** is the upward normal (for flat surface).

**Glint Angle:**

The angle θ_glint between viewing direction and specular direction:

.. math::

   \cos\theta_{glint} = \cos\theta_{sun}\cos\theta_{view} - \sin\theta_{sun}\sin\theta_{view}\cos\Delta\phi

Where Δφ is the relative azimuth.

**Glint Intensity:**

Peak radiance in glint can be 100-1000× higher than water-leaving radiance, completely dominating the signal.

**Avoidance Strategy:**

Ocean color algorithms avoid glint-contaminated pixels:

* Typically require θ_glint > 20-30°
* Use multi-angle viewing to find glint-free geometries
* Apply glint correction algorithms

Implementation in OSOAA
-----------------------

Surface Matrix Calculation
~~~~~~~~~~~~~~~~~~~~~~~~~~

OSOAA pre-computes surface reflection and transmission matrices for all geometric configurations.

**Computational Steps:**

1. **Discretize angles**: Set up incident and transmitted angle grids

2. **Azimuthal decomposition**: Use Fourier series in azimuth angle:

   .. math::

      R(\theta_i, \theta_r, \Delta\phi) = \sum_{m=0}^{M} R^m(\theta_i, \theta_r) \cos(m\Delta\phi)

3. **For each geometry**:
   
   a. Determine required wave normal
   b. Calculate slopes (Z_x, Z_y)
   c. Evaluate probability P(Z_x, Z_y)
   d. Compute Fresnel coefficients
   e. Apply geometric factors
   f. Accumulate Mueller matrix elements

4. **Store matrices**: Save for use in radiative transfer calculations

**Key Parameters:**

* Number of azimuthal angles: CTE_PH_NU = 1024
* Integration accuracy: CTE_THRESHOLD_GEO_CONFIG = 10⁻¹⁵
* Dichotomy threshold: CTE_THRESHOLD_DICHO = 10⁻¹⁰

**Computational Cost:**

Surface matrix calculations typically take 15-30 minutes, but only need to be computed once per wind speed and refractive index combination.

Fortran Implementation
~~~~~~~~~~~~~~~~~~~~~~

Located in ``src/OSOAA_SURFACE.F`` and ``src/OSOAA_SURF_MATRICES.F``:

.. code-block:: fortran

   SUBROUTINE SURFACE_ROUGH_COX_MUNK(WIND_SPEED, THETA_I, THETA_T,
  &                                   PHI_REL, REFLECTANCE, TRANSMITTANCE, ...)
   ! Computes rough surface reflectance and transmittance
   ! INPUT:
   !   WIND_SPEED - Wind speed at 10m (m/s)
   !   THETA_I - Incident zenith angle (degrees)
   !   THETA_T - Transmitted/reflected zenith angle (degrees)
   !   PHI_REL - Relative azimuth angle (degrees)
   ! OUTPUT:
   !   REFLECTANCE - Directional reflectance (Mueller matrix)
   !   TRANSMITTANCE - Directional transmittance (Mueller matrix)

   SUBROUTINE INTEGRATE_WAVE_FACETS(THETA_I, THETA_T, PHI,
  &                                  SIGMA_C, SIGMA_U,
  &                                  REFL_MATRIX, TRANS_MATRIX)
   ! Integrates over wave facet orientations

**Key Algorithms:**

* **Gaussian quadrature**: For slope integration
* **Dichotomy method**: To find wave normal satisfying Snell's law
* **Fourier decomposition**: Azimuthal angular dependence
* **Mueller matrix formalism**: Full polarization treatment

Output Files
~~~~~~~~~~~~

**SEA_LOG.txt:**

Contains detailed surface calculation information:

::

    ==========================================
    OSOAA Surface Calculations
    ==========================================
    
    Surface Type: Rough (Cox & Munk)
    
    Parameters:
      Wind speed: 5.0 m/s
      Refractive index: 1.334
      
    Wave Slope Statistics:
      Sigma_crosswind²: 0.0286
      Sigma_upwind²: 0.0158
      Mean square slope: 0.0444
      RMS slope: 12.1°
    
    Reflection/Transmission Matrices:
      Angular resolution: 1024 azimuth angles
      Geometric configurations computed: 2456
      Wave facet integration: Complete
      
    Fresnel Coefficients:
      Computed for 50 incident angles
      Computed for 50 viewing angles
      
    Computation Time:
      Reflection matrices: 15.3 minutes
      Transmission matrices: 12.7 minutes
      Total: 28.0 minutes

Polarization Effects
--------------------

Mueller Matrix Formalism
~~~~~~~~~~~~~~~~~~~~~~~~

The surface matrices in OSOAA are 4×4 Mueller matrices operating on Stokes vectors:

.. math::

   \begin{pmatrix} I_r \\ Q_r \\ U_r \\ V_r \end{pmatrix} = \mathbf{M}_R \begin{pmatrix} I_i \\ Q_i \\ U_i \\ V_i \end{pmatrix}

Where:

* I = Total intensity
* Q, U = Linear polarization
* V = Circular polarization

**Fresnel Mueller Matrix:**

For parallel and perpendicular reflectances:

.. math::

   \mathbf{M}_R = \frac{1}{2} \begin{pmatrix}
   R_\parallel + R_\perp & R_\parallel - R_\perp & 0 & 0 \\
   R_\parallel - R_\perp & R_\parallel + R_\perp & 0 & 0 \\
   0 & 0 & 2\sqrt{R_\parallel R_\perp} & 0 \\
   0 & 0 & 0 & 2\sqrt{R_\parallel R_\perp}
   \end{pmatrix}

Polarization by Reflection
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Brewster's Angle Effect:**

At θ_B ≈ 53°, parallel-polarized light has zero reflection (R_∥ = 0), resulting in completely perpendicularly polarized reflected light.

**Degree of Linear Polarization:**

.. math::

   DoLP = \frac{\sqrt{Q^2 + U^2}}{I} = \frac{R_\perp - R_\parallel}{R_\perp + R_\parallel}

**Maximum Polarization:**

* Occurs near Brewster's angle
* Can reach DoLP > 90% for reflected skylight
* Important for polarimetric remote sensing

Rotation Matrices
~~~~~~~~~~~~~~~~~

When light reflects or transmits through tilted wave facets, the polarization reference plane must be rotated.

**Rotation Mueller Matrix:**

.. math::

   \mathbf{M}_{rot}(\alpha) = \begin{pmatrix}
   1 & 0 & 0 & 0 \\
   0 & \cos 2\alpha & \sin 2\alpha & 0 \\
   0 & -\sin 2\alpha & \cos 2\alpha & 0 \\
   0 & 0 & 0 & 1
   \end{pmatrix}

Where α is the rotation angle.

**Application:**

Located in ``src/OSOAA_TRPHI.F``:

.. code-block:: fortran

   SUBROUTINE ROTATION_ANGLE(THETA_I, PHI_I, THETA_T, PHI_T, ALPHA)
   ! Computes rotation angle for polarization plane transformation

Applications and Effects
------------------------

Water-Leaving Radiance
~~~~~~~~~~~~~~~~~~~~~~

The rough surface affects water-leaving radiance in several ways:

**1. Transmission Enhancement:**

Compared to flat surface, rough surface increases transmission by distributing light over a wider angular range.

**Effect:** ~5-15% increase in water-leaving radiance at moderate wind speeds (5-10 m/s).

**2. Angular Distribution:**

Water-leaving radiance becomes less peaked and more distributed:

* Flat surface: Sharp angular features
* Rough surface: Smoothed angular distribution

**3. Viewing Geometry Dependence:**

Roughness reduces the strong viewing angle dependence predicted by flat surface models.

Skylight Reflection
~~~~~~~~~~~~~~~~~~~

Downwelling sky radiance reflected from the surface contributes significantly to top-of-atmosphere radiance.

**Reflection Coefficient:**

For diffuse skylight:

.. math::

   R_{sky} = \frac{L_{sky,reflected}}{L_{sky,incident}}

**Values:**

* Nadir viewing, calm: ~2%
* Nadir viewing, rough (U=5 m/s): ~2-3%
* Large viewing angles: 5-20%
* Glint conditions: Can approach 100%

**Atmospheric Correction:**

Accurate skylight reflection modeling is essential for atmospheric correction algorithms.

Sun Glint Contamination
~~~~~~~~~~~~~~~~~~~~~~~

**Problem:**

Sun glint can completely overwhelm the weak water-leaving radiance signal.

**Magnitudes:**

* Water-leaving radiance: ~0.01-0.1 W/m²/sr/nm
* Glint radiance (peak): 1-100 W/m²/sr/nm
* Enhancement factor: 10-1000×

**Mitigation Strategies:**

1. **Geometric avoidance**: Plan observations to avoid glint geometry
2. **Glint flagging**: Identify and exclude contaminated pixels
3. **Glint correction**: Model and subtract glint contribution
4. **Multi-angle viewing**: Use glint-free view angles

**OSOAA Application:**

Use glint angle calculations to:

* Predict glint contamination
* Design optimal viewing geometries
* Validate glint correction algorithms

Wind Speed Retrieval
~~~~~~~~~~~~~~~~~~~~

The Cox & Munk model enables wind speed retrieval from:

**1. Glint Pattern Analysis:**

Shape and intensity of sun glint relate to wave slope variance → wind speed.

**2. Polarization Measurements:**

Degree of polarization in reflected skylight depends on surface roughness → wind speed.

**3. Multi-angle Observations:**

Angular distribution of radiance contains wind speed information.

OSOAA can simulate these observables for algorithm development and validation.

Validation and Uncertainties
----------------------------

Model Validation
~~~~~~~~~~~~~~~~

**Sun Glint Observations:**

Compare OSOAA predictions with:

* Cox & Munk original data
* Satellite sun glint patterns (MODIS, MISR)
* Aircraft measurements

**Agreement:** Generally within 10-20% for moderate wind speeds.

**Radiance Measurements:**

Compare with field measurements:

* Above-water radiometry
* Underwater upwelling radiance
* Satellite matchups

**Agreement:** Within 5-15% for non-glint conditions.

Limitations of Cox & Munk Model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**1. Breaking Waves:**

At high wind speeds (>15 m/s), wave breaking and whitecaps occur. Cox & Munk does not model these effects.

**Solution:** Limit application to U < 15 m/s, or add foam/whitecap parameterizations.

**2. Long-Term Wave Development:**

Model assumes fully developed sea state. Fetch-limited or duration-limited conditions may differ.

**3. Swell Contributions:**

Cox & Munk describes wind waves. Swell from distant storms adds long-wavelength components.

**4. Shallow Water:**

Wave statistics differ in shallow water due to bottom effects.

**5. Wind Direction Uncertainty:**

While the model includes up-wind/cross-wind anisotropy, wind direction is often poorly known.

**Practical Solution:** Use isotropic average (σ_c ≈ σ_u) when wind direction unavailable.

Uncertainty Estimates
~~~~~~~~~~~~~~~~~~~~~

**Sources of Uncertainty:**

1. **Wind Speed:**
   
   * Measurement: ±0.5-1.0 m/s
   * Spatial/temporal variability
   * Height correction (10 m reference)

2. **Wave Slope Statistics:**
   
   * Cox & Munk fit: ±10-20%
   * Environmental conditions (fetch, duration)
   * Breaking waves at high wind

3. **Refractive Index:**
   
   * Wavelength dependence: ±0.001
   * Temperature/salinity: ±0.002
   * Impact on reflection: ~1-2%

4. **Computational:**
   
   * Angular discretization
   * Integration accuracy
   * Fourier series truncation

**Total Uncertainty:**

Water-leaving radiance uncertainty due to surface effects:

* Calm to moderate winds (0-10 m/s): 5-10%
* Higher winds (10-15 m/s): 10-20%
* Glint-contaminated geometries: 20-50% or worse

Best Practices
--------------

Model Selection
~~~~~~~~~~~~~~~

**Use Flat Surface When:**

* Wind speed < 1 m/s (calm conditions)
* Theoretical studies requiring simplicity
* Computational efficiency critical (testing)
* Sensitivity studies (baseline comparison)

**Use Rough Surface When:**

* Realistic simulations (wind > 2 m/s)
* Ocean color remote sensing applications
* Sun glint studies
* Polarimetric applications
* Validation against satellite/field data

Parameter Selection
~~~~~~~~~~~~~~~~~~~

**Wind Speed:**

* Use concurrent measurements when available
* Satellite winds (QuikSCAT, ASCAT, SMAP)
* Reanalysis products (NCEP, ECMWF)
* Climatological averages (5-8 m/s typical for open ocean)

**Refractive Index:**

* Default 1.334 adequate for most applications
* Wavelength-dependent if high accuracy needed
* Temperature/salinity corrections for specialized studies

**Wind Direction:**

* Include if known for detailed studies
* Use isotropic approximation if unknown
* Most important for polarimetry

Computational Considerations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Surface Matrix Computation:**

* Time-consuming (15-30 minutes)
* Compute once, store for reuse
* Pre-compute libraries for common wind speeds

**Angular Resolution:**

* Higher resolution for rough surface than flat
* Azimuthal resolution: CTE_PH_NU = 1024 typically adequate
* Zenith angle resolution: Match radiative transfer grid

**Convergence:**

* Check integration accuracy
* Verify energy conservation (reflectance + transmittance ≈ 1)

Viewing Geometry Optimization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Ocean Color Observations:**

1. **Calculate glint angle**:

   .. math::

      \theta_{glint} = \arccos(\cos\theta_s\cos\theta_v - \sin\theta_s\sin\theta_v\cos\Delta\phi)

2. **Avoid glint**: Require θ_glint > 25-30°

3. **Optimize polarization**: View near 90° from principal plane

4. **Multi-angle strategy**: Combine multiple view angles for robustness

**MODIS-like Configuration:**

* View zenith angles: ±55°
* Relative azimuth: ~90° from principal plane
* Typically glint-free except near sun glitter regions

See Also
--------

* :ref:`radiative_transfer` - Theoretical foundation
* :ref:`atmosphere_model` - Atmospheric optical properties
* :ref:`ocean_model` - Ocean optical properties
* :ref:`successive_orders` - Numerical solution method
* :ref:`parameter_reference` - Parameter descriptions (SEA.Type, SEA.Wind, SEA.Ind)
* :ref:`bibliography` - References (Cox & Munk 1954, Mobley 1999)

References
----------

**Primary References:**

* Cox, C. and W. Munk (1954). "Measurement of the roughness of the sea surface from photographs of the sun's glitter." *Journal of the Optical Society of America* 44(11): 838-850.

* Mobley, C. D. (1999). "Estimation of the remote-sensing reflectance from above-surface measurements." *Applied Optics* 38(36): 7442-7455.

**Additional Reading:**

* Born, M. and E. Wolf (1999). *Principles of Optics* (7th edition). Cambridge University Press. (Fresnel equations)

* Chami, M. et al. (2015). "OSOAA: a vector radiative transfer model of coupled atmosphere-ocean system for a rough sea surface." *Optics Express* 23(21): 27829-27852.

* Zhang, H. and M. Wang (2010). "Evaluation of sun glint models using MODIS measurements." *Journal of Quantitative Spectroscopy and Radiative Transfer* 111: 492-506.

* Kay, S. et al. (2009). "Sun glint correction of high and low spatial resolution images of aquatic scenes: a review of methods for visible and near-infrared wavelengths." *Remote Sensing* 1: 697-730.
