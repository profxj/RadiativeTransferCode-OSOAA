Introduction to OSOAA
======================

What is OSOAA?
--------------

OSOAA (Ocean Successive Orders with Atmosphere - Advanced) is a state-of-the-art 
vector radiative transfer model designed for coupled atmosphere-ocean systems. 
It provides accurate simulations of light propagation, scattering, and absorption 
in both atmospheric and oceanic media, with full treatment of polarization.

Historical Development
----------------------

The OSOAA model evolved from the original OSOA (Ocean Successive Orders with Atmosphere) 
code, which was the first radiative transfer model capable of computing radiance and 
polarization in an ocean-atmosphere system with a flat surface interface.

The OSOA-Advanced code (OSOAA) introduced significant enhancements:

* **Rough sea surface modeling**: Implementation of the Cox & Munk surface model
* **Enhanced realism**: Better representation of the air-sea interface
* **Improved accuracy**: More realistic wave-slope distributions
* **Polarization**: Complete vector radiative transfer treatment

Scientific Applications
-----------------------

OSOAA is particularly valuable for:

Remote Sensing
~~~~~~~~~~~~~~

* Satellite ocean color retrieval
* Atmospheric correction of ocean observations
* Multi-angular remote sensing studies
* Polarimetric remote sensing applications

Ocean Optics Research
~~~~~~~~~~~~~~~~~~~~~

* Water-leaving radiance calculations
* Underwater light field studies
* Bio-optical modeling
* In-water radiometry validation

Atmospheric Studies
~~~~~~~~~~~~~~~~~~~

* Aerosol optical property retrievals
* Atmosphere-ocean coupling effects
* Sky radiance and polarization
* Sun glint analysis

Model Capabilities
------------------

Physical Processes
~~~~~~~~~~~~~~~~~~

OSOAA simulates the following physical processes:

1. **Atmospheric scattering and absorption**
   
   * Rayleigh (molecular) scattering
   * Aerosol scattering and absorption
   * Gas absorption

2. **Ocean scattering and absorption**
   
   * Molecular scattering in water
   * Phytoplankton scattering and absorption
   * Mineral-like particle scattering
   * Yellow substance (CDOM) absorption
   * Detritus absorption

3. **Surface interactions**
   
   * Fresnel reflection and refraction
   * Wave-facet statistics (Cox & Munk)
   * Wind-speed dependence
   * Foam effects (optional)

4. **Polarization**
   
   * Full Stokes vector representation
   * Mueller matrix calculations
   * Depolarization effects

Computational Method
~~~~~~~~~~~~~~~~~~~~

The **successive orders of scattering** method provides:

* Rigorous treatment of multiple scattering
* Separate calculation of each scattering order
* Controlled accuracy through order truncation
* Fourier decomposition in azimuth

Typical Use Cases
-----------------

Standard Scenarios
~~~~~~~~~~~~~~~~~~

1. **Clear water radiance calculations**
   
   Simulate water-leaving radiance for various chlorophyll concentrations 
   and viewing geometries.

2. **Turbid water studies**
   
   Investigate the effects of high mineral particle concentrations on 
   ocean color signals.

3. **Atmospheric correction validation**
   
   Generate reference data for evaluating atmospheric correction algorithms.

4. **Polarimetric simulations**
   
   Study the degree and angle of linear polarization in the ocean-atmosphere system.

Advanced Applications
~~~~~~~~~~~~~~~~~~~~~

1. **Custom optical properties**
   
   Use measured phase functions and inherent optical properties (IOPs).

2. **Vertical profile effects**
   
   Examine how chlorophyll vertical distributions affect remote sensing signals.

3. **Multi-angle observations**
   
   Simulate directional variations for multi-angular sensors (POLDER, MISR, etc.).

4. **Sun glint analysis**
   
   Study specular reflection from rough sea surfaces.

Model Limitations
-----------------

Users should be aware of the following limitations:

* **Plane-parallel geometry**: Assumes horizontally homogeneous layers
* **Steady-state**: No time-dependent effects
* **Spectral resolution**: Monochromatic calculations (run multiple wavelengths separately)
* **Computational cost**: High accuracy requires significant computation time
* **Wind-wave model**: Cox & Munk model may not capture all surface conditions

Getting Help
------------

If you encounter issues or have questions:

1. Check the :doc:`../reference/faq` section
2. Review the :doc:`../examples/basic_simulation` tutorials
3. Consult the scientific reference paper (Chami et al., 2015)
4. Contact the development team through the project repository

Next Steps
----------

* :doc:`installation` - Install OSOAA on your system
* :doc:`quickstart` - Run your first simulation
* :doc:`input_parameters` - Understand the input parameter file
