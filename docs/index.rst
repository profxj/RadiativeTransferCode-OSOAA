.. OSOAA documentation master file

OSOAA: Ocean Successive Orders with Atmosphere - Advanced
=========================================================

Version 2.0 - April 2025

.. image:: https://img.shields.io/badge/License-GPLv3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0
   :alt: License: GPL v3

Welcome to the official documentation for **OSOAA** (Ocean Successive Orders with Atmosphere - Advanced), 
a vector radiative transfer model for coupled atmosphere-ocean systems.

Overview
--------

OSOAA enables accurate calculation of radiative transfer in the Ocean-Atmosphere system including:

* **Polarization**: Full vector radiative transfer with Stokes parameters
* **Coupling terms**: Proper treatment of atmosphere-ocean interactions
* **Rough surface**: Cox & Munk sea surface model for realistic interface
* **Successive orders method**: Accurate scattering calculations

Key Features
------------

The OSOAA model provides comprehensive capabilities for:

**Atmospheric and Ocean Profiles**
   Define molecular and aerosol optical thickness, chlorophyll concentration, 
   mineral-like particles, yellow substance absorption, and custom profiles.

**Aerosol Models**
   Log-normal (LND) or Junge mono-modal distributions, bimodal LND, 
   WMO models, Shettle & Fenn models, or custom phase functions.

**Hydrosol Models**
   Phytoplankton and mineral-like particles with custom scattering 
   and absorption properties.

**Sea Surface Interface**
   Flat or rough surface modeling using wind speed and wave parameters.

**Output Options**
   Radiance fields at any altitude/depth, directional radiance profiles, 
   complete radiance fields (upward/downward, intensity/polarization).

Reference
---------

When using OSOAA in your research, please cite:

   Chami M, Lafrance B, Fougnie B, Chowdhary J, Harmel T, Waquet F (2015), 
   "OSOAA: a vector radiative transfer model of coupled atmosphere-ocean system 
   for a rough sea surface application to the estimates of the directional 
   variations of the water leaving reflectance to better process multi-angular 
   satellite sensors data over the ocean", *Opt Express* 23: 27829-27852, 
   doi: `10.1364/OE.23.027829 <https://doi.org/10.1364/OE.23.027829>`_

Copyright and License
---------------------

© 2015–2025 **Université Pierre et Marie Curie - Paris 6** (Sorbonne Université) and 
**Centre National d'Études Spatiales (CNES)**

This program is free software, licensed under the **GNU General Public License v3.0 (GPLv3)**.

Development carried out by **CS GROUP**.  
Funded by **Centre National d'Études Spatiales (CNES)**.

Documentation Contents
----------------------

.. toctree::
   :maxdepth: 2
   :caption: User Guide
   
   user_guide/introduction
   user_guide/installation
   user_guide/quickstart
   user_guide/input_parameters
   user_guide/running_osoaa
   user_guide/output_files

.. toctree::
   :maxdepth: 2
   :caption: Scientific Background
   
   science/radiative_transfer
   science/atmosphere_model
   science/ocean_model
   science/surface_interface
   science/successive_orders

.. toctree::
   :maxdepth: 2
   :caption: Technical Documentation
   
   technical/code_structure
   technical/fortran_modules
   technical/algorithms
   technical/performance

.. toctree::
   :maxdepth: 2
   :caption: Examples and Tutorials
   
   examples/basic_simulation
   examples/aerosol_models
   examples/hydrosol_models
   examples/rough_surface
   examples/custom_profiles

.. toctree::
   :maxdepth: 2
   :caption: Reference
   
   reference/parameter_reference
   reference/constants
   reference/file_formats
   reference/faq
   reference/bibliography

.. toctree::
   :maxdepth: 1
   :caption: Additional Information
   
   changelog
   license


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
