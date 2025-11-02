Changelog
=========

This document tracks changes, improvements, and bug fixes across OSOAA versions.

Version 2.0 (April 2025)
------------------------

Major Features
~~~~~~~~~~~~~~

* **Custom IOP Profiles**: Users can now provide their own absorption and scattering coefficient profiles from in-situ measurements
* **Enhanced Output Options**: New advanced output file format with detailed component breakdown
* **Improved Convergence**: Optimized successive orders algorithm for faster convergence
* **Extended Wavelength Range**: Support for wavelengths down to 299 nm

Improvements
~~~~~~~~~~~~

* Better handling of high solar zenith angles (up to 85°)
* Optimized surface matrix calculations (30% faster)
* Improved memory management for large angular grids
* Enhanced error messages and validation
* Updated GUI with better usability

Bug Fixes
~~~~~~~~~

* Fixed edge case in Cox & Munk surface calculations at very high wind speeds
* Corrected polarization rotation angles in specific geometries
* Fixed memory leak in Mie calculations for bi-modal distributions
* Resolved numerical instability in Fourier series truncation

Technical Changes
~~~~~~~~~~~~~~~~~

* Migrated to Fortran 90 standard (backward compatible with F77)
* Improved code documentation and comments
* Refactored module dependencies
* Added unit tests for core functions

Version 1.5 (December 2020)
----------------------------

Features
~~~~~~~~

* Added Shettle & Fenn aerosol models
* Implemented custom aerosol phase function input
* Enhanced hydrosol models with mineral particles
* Added bottom reflectance options for shallow water

Improvements
~~~~~~~~~~~~

* 20% performance improvement in radiative transfer core
* Better default parameters
* Expanded user manual
* Added example input files

Bug Fixes
~~~~~~~~~

* Fixed Gaussian profile normalization
* Corrected wavelength-dependent refractive index
* Fixed output file formatting issues

Version 1.0 (March 2016)
-------------------------

Initial Features
~~~~~~~~~~~~~~~~

* Successive orders of scattering method
* Cox & Munk rough surface model
* Vector radiative transfer (full polarization)
* Multiple aerosol size distribution models
* Chlorophyll-based bio-optical model
* Java GUI for parameter configuration
* Multi-wavelength simulations
* Comprehensive output options

Supported Capabilities
~~~~~~~~~~~~~~~~~~~~~~

* Atmosphere-ocean coupled system
* Rayleigh scattering in air and water
* Aerosol scattering and absorption
* Phytoplankton and mineral particles
* Yellow substance absorption
* Flat and rough sea surfaces
* Fresnel reflection/refraction
* Wave-slope statistics

Legacy OSOA Version
-------------------

Original OSOA (pre-2015)
~~~~~~~~~~~~~~~~~~~~~~~~

* Flat surface only
* Basic aerosol models
* Simple bio-optical model
* Limited polarization handling
* Fortran 77 codebase

Upgrade Path
------------

From Version 1.x to 2.0
~~~~~~~~~~~~~~~~~~~~~~~

**Input File Changes**:

* No breaking changes - v1.x input files work with v2.0
* New optional parameters for custom profiles
* Enhanced output file specifications available

**Compilation**:

* Same Makefiles work
* Recommend recompiling from source
* No changes to dependencies

**Output Format**:

* Backward compatible
* New columns added to advanced output (optional)
* Binary format unchanged

From OSOA to OSOAA 1.0
~~~~~~~~~~~~~~~~~~~~~~~

**Major Changes**:

* Input parameter file format redesigned
* Must specify surface type (flat/rough)
* New aerosol model options
* Enhanced hydrosol parameterization

**Migration Guide**:

1. Review new parameter structure
2. Add surface type specification
3. Update aerosol model selection
4. Verify chlorophyll parameterization
5. Test with example files

Deprecation Notices
-------------------

Version 2.0
~~~~~~~~~~~

* **Legacy binary format**: The old v1.0 binary format is deprecated. Use new format for future compatibility.
* **Fortran 77 syntax**: While still supported, F77-specific constructs will be removed in v3.0.

Planned for Version 3.0
~~~~~~~~~~~~~~~~~~~~~~~

* Complete migration to Fortran 90/95
* Removal of deprecated binary format
* Modernized build system (CMake)
* Python API bindings

Known Issues
------------

Version 2.0
~~~~~~~~~~~

* **Performance**: Surface matrix calculation can be slow for wind speeds > 15 m/s
* **Memory**: Very high angular resolution (>100 angles) may exceed RAM on systems with <16GB
* **Convergence**: Extreme geometries (SZA > 85°) may require manual convergence threshold adjustment

Workarounds
~~~~~~~~~~~

* For high wind speeds: Consider reducing angular resolution initially
* For memory issues: Run on high-memory node or reduce grid resolution
* For convergence: Increase maximum iterations or relax threshold slightly

Future Development
------------------

Version 3.0 (Planned)
~~~~~~~~~~~~~~~~~~~~~

* Python API for programmatic control
* Parallel execution support (OpenMP/MPI)
* GPU acceleration for Mie calculations
* NetCDF output format option
* Integration with remote sensing processing chains
* Real-time visualization during execution

Long-term Goals
~~~~~~~~~~~~~~~

* Non-spherical particle support
* Time-dependent simulations
* Fluorescence modeling
* Raman scattering
* 3D geometry (beyond plane-parallel)

Contributing
------------

We welcome contributions! See :doc:`contributing` for guidelines.

To report bugs or request features:

* Open an issue on GitHub
* Email the development team
* Provide detailed description and reproducible example

Acknowledgments
---------------

We thank all users who have provided feedback, reported bugs, and suggested improvements over the years. Special thanks to:

* Beta testers of version 2.0
* Contributors to the bio-optical models
* International user community for validation data

References
----------

For scientific background on changes:

* Version 2.0: See updated documentation at https://osoaa.readthedocs.io
* Version 1.0: Chami et al. (2015), Opt. Express 23:27829-27852
* Original OSOA: Chami et al. (2001), Appl. Opt. 40:2398-2416

Support
-------

For version-specific support:

* **v2.0**: Full support, active development
* **v1.5**: Maintenance mode, critical bugs only
* **v1.0**: Limited support, recommend upgrade
* **OSOA**: No longer supported, migrate to OSOAA
