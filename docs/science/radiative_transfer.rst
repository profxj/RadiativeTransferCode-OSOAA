.. _radiative_transfer:

Radiative Transfer Theory
=========================

This section provides the theoretical foundation for radiative transfer in coupled atmosphere-ocean systems.

.. contents:: Contents
   :local:
   :depth: 2

Introduction
------------

Radiative transfer describes how electromagnetic radiation propagates through a medium that absorbs, emits, and scatters light. OSOAA solves the vector radiative transfer equation for coupled atmosphere-ocean systems, accounting for:

- Multiple scattering
- Polarization (Stokes vector formalism)
- Absorption and emission
- Atmosphere-ocean boundary conditions
- Rough surface effects

Fundamental Concepts
--------------------

Radiance and Intensity
~~~~~~~~~~~~~~~~~~~~~~

**Radiance** L(r, Ω, t, λ) is the fundamental radiometric quantity describing the flow of radiant energy:

.. math::

   L = \frac{d^2\Phi}{dA\cos\theta \, d\Omega}

Where:

- dΦ: Radiant flux (power) [W]
- dA: Area element [m²]
- θ: Angle between surface normal and direction
- dΩ: Solid angle element [sr]

**Units:** W·m⁻²·sr⁻¹·nm⁻¹ (spectral radiance)

**Properties:**

- Radiance is conserved along a ray in a non-absorbing medium
- Direction-dependent: L = L(r, Ω, λ, t)
- Wavelength-dependent (spectral radiance)

Inherent Optical Properties (IOPs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

IOPs characterize the medium's interaction with light, independent of the light field:

**Absorption Coefficient** a(λ)

.. math::

   a(\lambda) = \frac{d\Phi_{abs}}{d\Phi \, dz}

- Units: m⁻¹
- Fraction of beam absorbed per unit path length
- Components: water, phytoplankton, CDOM, detritus

**Scattering Coefficient** b(λ)

.. math::

   b(\lambda) = \frac{d\Phi_{sca}}{d\Phi \, dz}

- Units: m⁻¹
- Fraction of beam scattered per unit path length
- Components: water molecules, particles

**Extinction Coefficient** β(λ)

.. math::

   \beta(\lambda) = a(\lambda) + b(\lambda)

Total attenuation (absorption + scattering).

**Single Scattering Albedo** ω₀

.. math::

   \omega_0 = \frac{b}{\beta} = \frac{b}{a+b}

Ratio of scattering to extinction (0 ≤ ω₀ ≤ 1).

**Optical Depth** τ

.. math::

   \tau = \int_0^z \beta(z') dz'

Dimensionless measure of attenuation along path.

Volume Scattering Function
~~~~~~~~~~~~~~~~~~~~~~~~~~

The **Volume Scattering Function** (VSF) β(ψ) describes angular distribution of scattered light:

.. math::

   \beta(\psi) = \frac{dI_s(\psi)}{I_0 \, dz}

Where:

- ψ: Scattering angle
- I₀: Incident intensity
- Iₛ(ψ): Scattered intensity in direction ψ
- Units: m⁻¹·sr⁻¹

**Relationship to scattering coefficient:**

.. math::

   b = \int_{4\pi} \beta(\psi) d\Omega = 2\pi \int_0^\pi \beta(\psi) \sin\psi \, d\psi

**Phase Function** p(ψ)

Normalized VSF:

.. math::

   p(\psi) = \frac{\beta(\psi)}{b/(4\pi)} = \frac{4\pi\beta(\psi)}{b}

Normalization:

.. math::

   \frac{1}{4\pi}\int_{4\pi} p(\psi) d\Omega = 1

**Asymmetry Parameter** g

.. math::

   g = \langle\cos\psi\rangle = \frac{1}{2}\int_{-1}^1 p(\cos\psi) \cos\psi \, d(\cos\psi)

- g = 0: Isotropic scattering
- g > 0: Forward scattering dominant
- g < 0: Backward scattering dominant
- Typical values: 0.6-0.95 for oceanic particles

Scalar Radiative Transfer Equation
----------------------------------

Basic Form
~~~~~~~~~~

The scalar (unpolarized) radiative transfer equation in a plane-parallel medium:

.. math::

   \mu\frac{dI(z,\mu,\phi)}{dz} = -\beta(z)I(z,\mu,\phi) + S(z,\mu,\phi)

Where:

- z: Vertical coordinate (positive upward)
- μ = cos θ: Cosine of zenith angle
- φ: Azimuthal angle
- I(z, μ, φ): Radiance
- β(z): Extinction coefficient
- S(z, μ, φ): Source function

Source Function
~~~~~~~~~~~~~~~

The source function includes scattering from all directions:

.. math::

   S(z,\mu,\phi) = \frac{\omega_0(z)\beta(z)}{4\pi}\int_0^{2\pi}\int_{-1}^1 p(\mu,\phi;\mu',\phi') I(z,\mu',\phi') d\mu' d\phi'

For azimuthally symmetric problems, Fourier decomposition:

.. math::

   I(z,\mu,\phi) = \sum_{m=0}^\infty I^m(z,\mu)\cos[m(\phi-\phi_0)]

Simplifies the angular integration.

Boundary Conditions
~~~~~~~~~~~~~~~~~~~

**Top of Atmosphere (TOA):**

Downward radiance = 0 (no incoming radiation from space, except direct solar):

.. math::

   I(z_{TOA}, \mu<0, \phi) = 0 \quad \text{for } \mu < 0

Plus direct solar beam:

.. math::

   I_{sun} = F_0 \delta(\mu - \mu_0)\delta(\phi - \phi_0)

Where:

- F₀: Solar irradiance
- μ₀ = cos θₛ: Solar zenith angle
- φ₀: Solar azimuth angle
- δ: Dirac delta function

**Sea Surface:**

Coupled boundary condition with Fresnel reflection/transmission (see :ref:`surface_interface`).

**Ocean Bottom:**

For finite-depth ocean:

.. math::

   I(z_{bottom}, \mu>0, \phi) = \rho_{bottom}(\mu,\phi) E_d(z_{bottom})

Where ρ_bottom is the bottom reflectance.

Vector Radiative Transfer Equation
----------------------------------

Stokes Vector Formalism
~~~~~~~~~~~~~~~~~~~~~~~

Light polarization is described by the **Stokes vector**:

.. math::

   \vec{I} = \begin{pmatrix} I \\ Q \\ U \\ V \end{pmatrix}

**Components:**

- **I**: Total intensity (unpolarized + polarized)
- **Q**: Horizontal-vertical linear polarization difference
- **U**: +45°/-45° linear polarization difference  
- **V**: Right-left circular polarization difference

**Interpretation:**

.. math::

   I &= I_h + I_v \\
   Q &= I_h - I_v \\
   U &= I_{+45°} - I_{-45°} \\
   V &= I_{RCP} - I_{LCP}

**Degree of Linear Polarization (DoLP):**

.. math::

   DoLP = \frac{\sqrt{Q^2 + U^2}}{I}

**Angle of Linear Polarization (AoLP):**

.. math::

   AoLP = \frac{1}{2}\arctan\left(\frac{U}{Q}\right)

Mueller Matrix
~~~~~~~~~~~~~~

Scattering transforms the Stokes vector via the **Mueller matrix** (or phase matrix):

.. math::

   \vec{I}_{sca} = \mathbf{M}(\Theta) \vec{I}_{inc}

The 4×4 Mueller matrix for spherical particles (Mie theory):

.. math::

   \mathbf{M}(\Theta) = \begin{pmatrix}
   M_{11} & M_{12} & 0 & 0 \\
   M_{12} & M_{22} & 0 & 0 \\
   0 & 0 & M_{33} & M_{34} \\
   0 & 0 & -M_{34} & M_{44}
   \end{pmatrix}

For randomly oriented spheres, the matrix has this block-diagonal form with zero elements due to symmetry.

**Normalization:**

.. math::

   \frac{1}{4\pi}\int_{4\pi} M_{11}(\Theta) d\Omega = 1

Vector RTE
~~~~~~~~~~

The vector radiative transfer equation:

.. math::

   \mu\frac{d\vec{I}(z,\mu,\phi)}{dz} = -\beta(z)\vec{I}(z,\mu,\phi) + \vec{S}(z,\mu,\phi)

With vector source function:

.. math::

   \vec{S}(z,\mu,\phi) = \frac{\omega_0(z)\beta(z)}{4\pi}\int_0^{2\pi}\int_{-1}^1 \mathbf{P}(\mu,\phi;\mu',\phi') \vec{I}(z,\mu',\phi') d\mu' d\phi'

Where **P** is the 4×4 phase matrix.

Rotation of Reference Frame
~~~~~~~~~~~~~~~~~~~~~~~~~~~

When changing the scattering plane, apply rotation matrix:

.. math::

   \mathbf{L}(\alpha) = \begin{pmatrix}
   1 & 0 & 0 & 0 \\
   0 & \cos 2\alpha & \sin 2\alpha & 0 \\
   0 & -\sin 2\alpha & \cos 2\alpha & 0 \\
   0 & 0 & 0 & 1
   \end{pmatrix}

Transformed Stokes vector:

.. math::

   \vec{I}' = \mathbf{L}(\alpha) \vec{I}

Molecular (Rayleigh) Scattering
-------------------------------

Rayleigh Scattering Cross Section
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For air molecules:

.. math::

   \sigma_{Ray}(\lambda) = \frac{24\pi^3(n^2-1)^2}{N^2\lambda^4(n^2+2)^2}F_K

Where:

- n: Refractive index of air
- N: Molecular number density
- λ: Wavelength
- F_K: King correction factor (accounts for anisotropy)

**Wavelength dependence:** σ ∝ λ⁻⁴

**King Factor:**

.. math::

   F_K = \frac{6+3\delta}{6-7\delta}

Where δ is the depolarization factor:

- δ_air = 0.0279 (OSOAA: CTE_MDF_AIR)
- δ_water = 0.0906 (OSOAA: CTE_MDF_SEA)

Rayleigh Phase Matrix
~~~~~~~~~~~~~~~~~~~~~

For molecular scattering including depolarization:

.. math::

   \mathbf{M}_{Ray}(\Theta) = \frac{3}{4(1+2\gamma)}
   \begin{pmatrix}
   1+\cos^2\Theta & -\sin^2\Theta & 0 & 0 \\
   -\sin^2\Theta & 1+\cos^2\Theta & 0 & 0 \\
   0 & 0 & 2\cos\Theta & 0 \\
   0 & 0 & 0 & 2\cos\Theta - (1-\gamma)(1+\cos^2\Theta)
   \end{pmatrix}

Where:

.. math::

   \gamma = \frac{\delta}{2-\delta}

**Limiting cases:**

- δ = 0 (no depolarization): Pure Rayleigh scattering
- δ > 0: Reduced polarization

Mie Scattering Theory
---------------------

For spherical particles with radius r and refractive index m = n + ik.

Size Parameter
~~~~~~~~~~~~~~

.. math::

   x = \frac{2\pi r}{\lambda}

Scattering regimes:

- x ≪ 1: Rayleigh scattering (λ⁻⁴)
- x ~ 1: Mie scattering (resonances)
- x ≫ 1: Geometric optics

Scattering Amplitudes
~~~~~~~~~~~~~~~~~~~~~

.. math::

   S_1(\theta) = \sum_{n=1}^\infty \frac{2n+1}{n(n+1)}(a_n\pi_n + b_n\tau_n)

.. math::

   S_2(\theta) = \sum_{n=1}^\infty \frac{2n+1}{n(n+1)}(a_n\tau_n + b_n\pi_n)

Where aₙ, bₙ are Mie coefficients (see :ref:`bibliography` Bohren & Huffman 1983).

Mueller Matrix Elements
~~~~~~~~~~~~~~~~~~~~~~~

.. math::

   M_{11} = \frac{1}{2}(|S_1|^2 + |S_2|^2)

.. math::

   M_{12} = \frac{1}{2}(|S_2|^2 - |S_1|^2)

.. math::

   M_{33} = \frac{1}{2}(S_1^*S_2 + S_1S_2^*)

.. math::

   M_{34} = \frac{i}{2}(S_1S_2^* - S_1^*S_2)

Successive Orders Method
------------------------

Decomposition
~~~~~~~~~~~~~

The total radiance is expanded as a sum over scattering orders:

.. math::

   \vec{I}_{total}(z,\mu,\phi) = \sum_{n=0}^\infty \vec{I}^{(n)}(z,\mu,\phi)

Where n is the number of scattering events.

Order 0: Direct Transmission
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Zero-order term (unscattered light):

.. math::

   I^{(0)}(z,\mu,\phi) = F_0 e^{-\tau/\mu_0} \delta(\mu-\mu_0)\delta(\phi-\phi_0)

Where:

- F₀: Extraterrestrial solar irradiance
- τ: Optical depth
- μ₀: Cosine of solar zenith angle

Order n ≥ 1: Multiple Scattering
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Recursive relationship:

.. math::

   \vec{I}^{(n)} = \mathcal{S}[\vec{I}^{(n-1)}]

Where 𝒮 is the single scattering operator:

.. math::

   \mathcal{S}[\vec{I}](z,\mu,\phi) = \frac{\omega_0\beta}{4\pi}\int_0^{2\pi}\int_{-1}^1 \mathbf{P}(\mu,\phi;\mu',\phi') \vec{I}(z',\mu',\phi') e^{-\tau(z,z')} d\mu' d\phi'

Convergence
~~~~~~~~~~~

The series converges when successive terms become negligible:

.. math::

   \frac{|\vec{I}^{(n)}|}{|\vec{I}_{total}|} < \epsilon

Typical threshold: ε = 0.001

**Convergence depends on:**

- Optical thickness (τ)
- Single scattering albedo (ω₀)
- Phase function (forward/backward scattering)

Fourier Decomposition
---------------------

Azimuthal Expansion
~~~~~~~~~~~~~~~~~~~

Due to azimuthal symmetry in the source (sun), radiance can be expanded:

.. math::

   \vec{I}(z,\mu,\phi) = \sum_{m=0}^M \vec{I}^m(z,\mu)\cos[m(\phi-\phi_0)]

This reduces the 3D problem to a series of 2D problems, one for each Fourier mode m.

**Benefits:**

- Computational efficiency
- Decoupling of azimuthal dependence
- Faster convergence with fewer terms

Phase Matrix Expansion
~~~~~~~~~~~~~~~~~~~~~~

The phase matrix is similarly expanded:

.. math::

   \mathbf{P}(\Theta,\phi-\phi') = \sum_{m=0}^M \mathbf{P}^m(\Theta)\cos[m(\phi-\phi')]

Where Θ is the scattering angle determined by:

.. math::

   \cos\Theta = \mu\mu' + \sqrt{1-\mu^2}\sqrt{1-\mu'^2}\cos(\phi-\phi')

Truncation
~~~~~~~~~~

The Fourier series is truncated when:

.. math::

   \frac{|\vec{I}^m|}{|\vec{I}^0|} < \epsilon_F

Typical: ε_F = 0.0002 (CTE_PH_SEUIL_SF in OSOAA)

Radiometric Quantities
----------------------

Irradiance
~~~~~~~~~~

**Downward irradiance:**

.. math::

   E_d(z) = \int_0^{2\pi}\int_0^1 I(z,\mu,\phi)\mu \, d\mu d\phi

**Upward irradiance:**

.. math::

   E_u(z) = \int_0^{2\pi}\int_0^1 I(z,-\mu,\phi)\mu \, d\mu d\phi

**Scalar irradiance:**

.. math::

   E_0(z) = \int_0^{2\pi}\int_{-1}^1 I(z,\mu,\phi) d\mu d\phi = E_u + E_d

Remote Sensing Reflectance
~~~~~~~~~~~~~~~~~~~~~~~~~~

Water-leaving radiance normalized by downward irradiance:

.. math::

   R_{rs}(\lambda,\theta,\phi) = \frac{L_w(\lambda,\theta,\phi)}{E_d(\lambda,0^+)}

Units: sr⁻¹

**Related to reflectance:**

.. math::

   \rho_w = \pi R_{rs}

Diffuse Attenuation Coefficient
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. math::

   K_d(z) = -\frac{1}{E_d}\frac{dE_d}{dz}

Describes exponential attenuation of downward irradiance with depth.

Energy Conservation
-------------------

The radiative transfer equation conserves energy:

.. math::

   \nabla \cdot \vec{F} + \beta I = \beta\omega_0 \int_{4\pi} p(\Omega,\Omega')I(\Omega') d\Omega'

Where F is the radiant flux vector.

Numerical Considerations
------------------------

Angular Discretization
~~~~~~~~~~~~~~~~~~~~~~

- **Gauss-Legendre quadrature**: Optimal for smooth integrands
- **User-defined angles**: Additional directions for output
- **Typical resolution**: 16-48 angles per hemisphere

Vertical Discretization
~~~~~~~~~~~~~~~~~~~~~~~

- **Atmosphere**: 30-100 layers
- **Ocean**: 20-50 layers
- **Finer near interfaces** for accurate boundary conditions

Truncation of Forward Peak
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Strong forward scattering (g ≈ 1) causes numerical difficulties:

- **Delta-Eddington approximation**: Separate forward peak
- **Truncation**: Remove extreme forward angles
- **Similarity relations**: Adjust optical properties

See Also
--------

- :ref:`atmosphere_model` for atmospheric optical properties
- :ref:`ocean_model` for oceanic optical properties
- :ref:`surface_interface` for boundary conditions
- :ref:`successive_orders` for numerical implementation
- :ref:`bibliography` for detailed references
