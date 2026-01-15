Code Structure
==============

This section describes the organization and structure of the OSOAA source code.

Directory Organization
----------------------

The OSOAA code is organized into the following directory structure:

.. code-block:: text

    RadiativeTransfer-OSOAA/
    ├── gen/                    # Build system (Makefiles)
    ├── inc/                    # Include files and constants
    ├── src/                    # Fortran source code
    ├── ihm/                    # Java GUI (optional)
    ├── fic/                    # Data files and examples
    ├── exe/                    # Compiled executables
    ├── obj/                    # Object files (build artifacts)
    └── docs/                   # Documentation

gen/ - Build System
~~~~~~~~~~~~~~~~~~~

Contains Makefiles for different Fortran compilers:

* ``Makefile_OSOAA.gfortran`` - GNU gfortran compiler (recommended)
* ``Makefile_OSOAA.f77`` - Standard Fortran 77 compiler
* ``Makefile_OSOAA.g77`` - GNU g77 compiler (legacy)

**Key features**:

* Automatic dependency tracking
* Optimization flags (``-O3 -march=native`` for gfortran)
* Debug mode support
* Configurable compilation options

inc/ - Include Files
~~~~~~~~~~~~~~~~~~~~

Contains the main header file ``OSOAA.h`` which defines:

* Physical constants
* Default parameter values
* Array dimensions
* Convergence thresholds
* File naming conventions

**Critical constants** (examples):

.. code-block:: c

   #define CTE_DEFAULT_IGMAX 100          // Max scattering orders
   #define CTE_WAMIN 0.299                // Min wavelength (nm)
   #define CTE_MDF_AIR 0.0279            // Air depolarization factor
   #define CTE_MDF_SEA 0.0906            // Seawater depolarization
   #define CTE_PH_NU 1024                 // Azimuthal angles
   #define CTE_PH_SEUIL_CV_SG 0.005      // Convergence threshold

src/ - Source Code
~~~~~~~~~~~~~~~~~~

Contains 12 main Fortran modules (F77/F90):

.. list-table:: Source File Organization
   :widths: 30 70
   :header-rows: 1

   * - File
     - Purpose
   * - OSOAA_MAIN.F
     - Main program and control flow
   * - OSOAA_ANGLES.F
     - Angular discretization
   * - OSOAA_AEROSOLS.F
     - Aerosol optical properties
   * - OSOAA_HYDROSOLS.F
     - Ocean particle properties
   * - OSOAA_MIE.F
     - Mie scattering calculations
   * - OSOAA_PARTICLES_RAD.F
     - Particle radiative properties
   * - OSOAA_PROFILE.F
     - Vertical profile construction
   * - OSOAA_SURFACE.F
     - Surface boundary conditions
   * - OSOAA_SURF_MATRICES.F
     - Surface reflection/transmission matrices
   * - OSOAA_SOS.F
     - Successive orders method
   * - OSOAA_SOS_CORE.F
     - Core radiative transfer solver
   * - OSOAA_TRPHI.F
     - Coordinate transformations

Module Hierarchy
----------------

The modules follow a hierarchical dependency structure:

.. code-block:: text

    OSOAA_MAIN (main entry point)
    │
    ├─→ OSOAA_ANGLES
    │   └─→ Gauss-Legendre quadrature
    │       User-defined angles
    │
    ├─→ OSOAA_PROFILE
    │   ├─→ Atmospheric layers
    │   └─→ Ocean layers
    │
    ├─→ OSOAA_AEROSOLS
    │   ├─→ OSOAA_MIE
    │   │   └─→ Mie coefficients computation
    │   └─→ OSOAA_PARTICLES_RAD
    │       └─→ Size distribution integration
    │
    ├─→ OSOAA_HYDROSOLS
    │   ├─→ OSOAA_MIE
    │   └─→ OSOAA_PARTICLES_RAD
    │
    ├─→ OSOAA_SURFACE
    │   └─→ OSOAA_SURF_MATRICES
    │       ├─→ Fresnel coefficients
    │       ├─→ Cox & Munk statistics
    │       └─→ OSOAA_TRPHI (rotation angles)
    │
    └─→ OSOAA_SOS (successive orders method)
        ├─→ OSOAA_SOS_CORE (RT equation solver)
        │   ├─→ Source function computation
        │   ├─→ Integration over angles/layers
        │   └─→ Stokes vector propagation
        └─→ OSOAA_TRPHI (coordinate transformations)

Data Flow
---------

The typical execution flow through the code:

1. Initialization Phase
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    Read input parameters
         ↓
    Validate configuration
         ↓
    Allocate memory structures
         ↓
    Initialize constants

2. Setup Phase
~~~~~~~~~~~~~~

.. code-block:: text

    OSOAA_ANGLES
    └─→ Compute Gauss quadrature nodes/weights
        Merge with user-defined angles
        Sort combined angular grid
         ↓
    OSOAA_PROFILE
    └─→ Build atmospheric vertical grid
        Build ocean vertical grid
        Compute coupling at interface
         ↓
    OSOAA_AEROSOLS
    └─→ OSOAA_MIE: Compute Mie coefficients
        OSOAA_PARTICLES_RAD: Integrate over size distribution
        Output: βₑₓₜ, βₛcₐ, ω₀, P(Θ), Phase matrix
         ↓
    OSOAA_HYDROSOLS
    └─→ Bio-optical model or custom IOPs
        OSOAA_MIE: Compute particle scattering
        Output: absorption, scattering, phase functions
         ↓
    OSOAA_SURFACE / OSOAA_SURF_MATRICES
    └─→ Compute Fresnel coefficients
        Integrate over wave slope distribution (Cox & Munk)
        Build reflection/transmission Mueller matrices

3. Radiative Transfer Phase
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    OSOAA_SOS (successive orders)
    │
    ├─→ Order 0: Direct transmission
    │            I⁽⁰⁾ = I₀ exp(-τ)
    │
    └─→ Loop over orders n = 1, 2, 3, ...
        │
        ├─→ OSOAA_SOS_CORE
        │   ├─→ Compute source function J⁽ⁿ⁾
        │   ├─→ Integrate over all directions (4π sr)
        │   ├─→ Integrate over all layers
        │   ├─→ Apply surface boundary conditions
        │   └─→ Compute I⁽ⁿ⁾ at output level
        │
        ├─→ Check convergence: |I⁽ⁿ⁾ - I⁽ⁿ⁻¹⁾| < ε
        │
        └─→ If converged: exit loop
            If not: continue to next order

4. Output Phase
~~~~~~~~~~~~~~~

.. code-block:: text

    Accumulate all scattering orders
         ↓
    Perform Fourier decomposition in azimuth
         ↓
    Write radiance fields (I, Q, U, V)
         ↓
    Compute derived quantities (DoLP, AoLP)
         ↓
    Write log files and diagnostics

Compilation Process
-------------------

The build system follows these steps:

1. **Environment Setup**

   .. code-block:: bash

      export OSOAA_ROOT=/path/to/OSOAA
      cd $OSOAA_ROOT

2. **Select Makefile**

   .. code-block:: bash

      cp gen/Makefile_OSOAA.gfortran Makefile

3. **Compilation Stages**

   .. code-block:: text

      make all
      │
      ├─→ Create obj/ directory
      │
      ├─→ Compile each module: .F → .o
      │   ├─→ OSOAA_MAIN.o
      │   ├─→ OSOAA_ANGLES.o
      │   ├─→ OSOAA_AEROSOLS.o
      │   ├─→ ... (all modules)
      │   └─→ OSOAA_TRPHI.o
      │
      ├─→ Link all object files
      │   └─→ Creates exe/OSOAA_MAIN.exe
      │
      └─→ Copy configuration
          └─→ Creates exe/config.txt

4. **Optimization Flags**

   * ``-O3``: Aggressive optimization
   * ``-march=native``: CPU-specific optimization
   * ``-w``: Suppress non-critical warnings

5. **Debug Mode** (optional)

   .. code-block:: bash

      # Uncomment DEBUG line in Makefile
      DEBUG = -g -D_DEBUG
      
      # Remove optimization
      # CCOPTS = -O3 -march=native

Code Organization Principles
----------------------------

Modularity
~~~~~~~~~~

* Each module handles a specific physical process
* Clear interfaces between modules
* Minimal inter-module dependencies
* Subroutines follow single-responsibility principle

Data Structures
~~~~~~~~~~~~~~~

* Arrays for angular grids (Gauss points, user angles)
* Vertical level arrays (atmosphere and ocean)
* Phase function and phase matrix storage
* Stokes vector fields (4 components: I, Q, U, V)

Naming Conventions
~~~~~~~~~~~~~~~~~~

**Subroutine names**:

* Descriptive names indicating functionality
* Example: ``ANGLES_GAUSS_LEGENDRE``, ``AEROSOLS_MONO_MODAL``

**Variable names**:

* Physical quantities use standard notation
* ``THETA``, ``PHI`` for angles
* ``WAVELENGTH`` for wavelength
* ``BETA_EXT``, ``BETA_SCA`` for optical coefficients

**Constants**:

* Prefix ``CTE_`` for constants in OSOAA.h
* Example: ``CTE_DEFAULT_IGMAX``, ``CTE_MDF_AIR``

File I/O Organization
---------------------

Input Files
~~~~~~~~~~~

* ASCII text format
* Keyword-value pairs
* Comment lines start with ``#``
* Organized by parameter categories

Output Files
~~~~~~~~~~~~

* Binary files for efficiency (optional)
* ASCII files for portability
* Separate files for different quantities:
  
  * Radiance fields
  * Polarization components
  * IOPs (inherent optical properties)
  * Log files

Memory Management
-----------------

Static Allocation
~~~~~~~~~~~~~~~~~

* Array dimensions defined in ``OSOAA.h``
* Fixed-size arrays at compile time
* Predictable memory usage

Dynamic Considerations
~~~~~~~~~~~~~~~~~~~~~~

* Angular grid size: user-configurable
* Vertical levels: adjustable
* Scattering orders: runtime-determined

Typical memory usage:

* Small simulation (20 angles, 50 levels): ~100 MB
* Medium simulation (50 angles, 100 levels): ~500 MB
* Large simulation (100 angles, 200 levels): ~2 GB

Error Handling
--------------

The code includes error checks for:

* Invalid input parameters
* File I/O errors
* Numerical overflow/underflow
* Non-convergence conditions
* Memory allocation failures

Error messages are written to:

* Standard output
* Log files (``LOG_OSOAA.txt``)
* Component-specific logs (``AER_LOG.txt``, ``SEA_LOG.txt``, etc.)

Extensibility
-------------

The code is designed for extension:

Adding New Aerosol Models
~~~~~~~~~~~~~~~~~~~~~~~~~

1. Add model in ``OSOAA_AEROSOLS.F``
2. Define parameters in ``OSOAA.h``
3. Update input parameter reading
4. Document in user guide

Adding New Output Options
~~~~~~~~~~~~~~~~~~~~~~~~~

1. Add output subroutine in ``OSOAA_SOS.F``
2. Define file format
3. Update output file documentation

Modifying Physical Constants
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Edit values in ``inc/OSOAA.h``
2. Recompile entire code
3. Document changes in ``exe/config.txt``

Version Control
---------------

Recommended practices:

* Use git for source code management
* Tag releases (v2.0, v2.1, etc.)
* Maintain separate branches for development
* Document code changes in commit messages
* Keep Makefiles under version control
* Track parameter file changes

Next Steps
----------

* :doc:`fortran_modules` - Detailed module documentation
* :doc:`algorithms` - Algorithm implementations
* :doc:`performance` - Performance optimization

See Also
--------

* :doc:`../user_guide/installation` - Compilation instructions
* :doc:`../reference/constants` - Complete constant definitions
