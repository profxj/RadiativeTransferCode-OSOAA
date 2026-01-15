Installation Guide
==================

This guide walks you through installing and setting up OSOAA on your system.

System Requirements
-------------------

Minimum Requirements
~~~~~~~~~~~~~~~~~~~~

* **Operating System**: Linux (recommended), Unix, macOS, or Windows with MinGW/Cygwin
* **Fortran Compiler**: gfortran, f77, g77, or compatible Fortran 77/90 compiler
* **Memory**: 2 GB RAM (minimum), 8 GB RAM (recommended)
* **Disk Space**: 500 MB for installation, additional space for results

Recommended Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

* Multi-core processor (for running multiple simulations)
* 16 GB RAM or more for large-scale calculations
* Fast SSD for improved I/O performance

Supported Compilers
-------------------

OSOAA has been tested with:

* **gfortran** (GNU Fortran) - Recommended, version 4.8 or later
* **f77** - Standard Fortran 77 compiler
* **g77** - GNU Fortran 77 (legacy systems)
* **Intel Fortran** - Commercial compiler (ifort)

Download OSOAA
--------------

From GitHub
~~~~~~~~~~~

Clone the repository::

    git clone https://github.com/your-organization/RadiativeTransfer-OSOAA.git
    cd RadiativeTransfer-OSOAA

Or download a specific release::

    wget https://github.com/your-organization/RadiativeTransfer-OSOAA/archive/refs/tags/v2.0.tar.gz
    tar -xzf v2.0.tar.gz
    cd RadiativeTransfer-OSOAA-2.0

Repository Structure
--------------------

After downloading, you should see the following structure::

    RadiativeTransfer-OSOAA/
    ├── gen/                    # Makefiles for different compilers
    │   ├── Makefile_OSOAA.gfortran
    │   ├── Makefile_OSOAA.f77
    │   └── Makefile_OSOAA.g77
    ├── inc/                    # Include files and constants
    │   └── OSOAA.h
    ├── src/                    # Fortran source code
    │   ├── OSOAA_MAIN.F
    │   ├── OSOAA_ANGLES.F
    │   ├── OSOAA_AEROSOLS.F
    │   ├── OSOAA_HYDROSOLS.F
    │   ├── OSOAA_MIE.F
    │   ├── OSOAA_PARTICLES_RAD.F
    │   ├── OSOAA_PROFILE.F
    │   ├── OSOAA_SURFACE.F
    │   ├── OSOAA_SURF_MATRICES.F
    │   ├── OSOAA_SOS.F
    │   ├── OSOAA_SOS_CORE.F
    │   └── OSOAA_TRPHI.F
    ├── ihm/                    # Java GUI (optional)
    ├── fic/                    # Data files
    ├── exe/                    # Compiled executables (after build)
    ├── obj/                    # Object files (after build)
    └── README.md

Compilation
-----------

Step 1: Environmental Variable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Set an environment variable for the OSOAA root directory. 
Add to your shell profile (e.g., ``~/.bashrc``)::

    export OSOAA_ROOT=/path/to/RadiativeTransfer-OSOAA

Step 2: Select Makefile
~~~~~~~~~~~~~~~~~~~~~~~

Choose the appropriate Makefile for your compiler:

For **gfortran** (recommended)::

    gen/Makefile_OSOAA.gfortran

For **f77**::

    gen/Makefile_OSOAA.f77

For **g77**::

    gen/Makefile_OSOAA.g77

Now execute::

    cd gen/
    make -f Makefile_OSOAA.XXX 

This will:

1. Create the object file directory (``obj/``)
2. Compile all Fortran source files
3. Link the executable
4. Create ``exe/OSOAA_MAIN.exe``
5. Generate ``exe/config.txt`` with compilation information

Successful compilation output::

    ------------> Compilation of obj/OSOAA_MAIN.o
    ------------> Compilation of obj/OSOAA_ANGLES.o
    ------------> Compilation of obj/OSOAA_AEROSOLS.o
    ...
    ------------> Link of exe/OSOAA_MAIN.exe
    ------------>ok

Compilation Troubleshooting
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem**: Compiler not found

.. code-block:: bash

    make: gfortran: Command not found

**Solution**: Install gfortran::

    # Debian/Ubuntu
    sudo apt-get install gfortran
    
    # RedHat/CentOS
    sudo yum install gcc-gfortran
    
    # macOS with Homebrew
    brew install gcc

**Problem**: Include file not found

**Solution**: Verify the ``NCL`` variable in Makefile points to ``./inc``

Verifying Installation
----------------------

Test Basic Functionality
~~~~~~~~~~~~~~~~~~~~~~~~

1. Navigate to the executable directory::

    cd exe

2. Check that the executable exists::

    ls -lh OSOAA_MAIN.exe

3. Run a quick help check (the program will prompt for input)::

    ./OSOAA_MAIN.exe < /dev/null

The program should exit with:

   OSOAA_MAIN : ERROR_1990 on parameters
   --> Required (-Keyword Value) definition :      -OSOAA.ResRoot Value 
   ==>  Working folder of OSOAA computations


Setting Up Data Files
----------------------

Required Data Directories
~~~~~~~~~~~~~~~~~~~~~~~~~

OSOAA requires several data file directories:

1. **Mie calculation files** (for aerosols and hydrosols)
2. **Surface property files** (for sea surface modeling)
3. **Spectral data files** (for optical properties)

These should be organized as::

    OSOAA-data/
    ├── aerosols/
    │   └── mie/
    ├── hydrosols/
    │   └── mie/
    └── surface/

The paths to these directories are specified in the OSOAA input parameter file.

Optional: GUI Installation
--------------------------

OSOAA includes an optional Java-based graphical user interface (GUI).

Requirements
~~~~~~~~~~~~

* Java Runtime Environment (JRE) 8 or later
* Java Development Kit (JDK) if building from source

Running the GUI
~~~~~~~~~~~~~~~

.. code-block:: bash

    cd ihm/bin
    ./runOSOAAUI.bash

The GUI provides:

* Easy parameter configuration
* Form validation
* Batch simulation setup
* Result visualization

Environment Variables (Optional)
---------------------------------

For convenient access, add OSOAA to your PATH::

    # Add to ~/.bashrc or ~/.bash_profile
    export OSOAA_HOME=/path/to/RadiativeTransfer-OSOAA
    export PATH=$PATH:$OSOAA_HOME/exe

After reloading your shell, you can run OSOAA from any directory::

    OSOAA_MAIN.exe < input_parameters.txt

Clean Installation
------------------

To remove compiled files and start fresh::

    make clean

This removes:

* All object files (``obj/*.o``)
* Executable (``exe/OSOAA_MAIN.exe``)
* Configuration file (``exe/config.txt``)

Source files and data remain untouched.

Next Steps
----------

* :doc:`quickstart` - Run your first OSOAA simulation
* :doc:`input_parameters` - Learn about input parameter configuration
* :doc:`running_osoaa` - Detailed guide on running simulations
