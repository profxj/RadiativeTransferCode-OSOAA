.. _faq:

Frequently Asked Questions (FAQ)
================================

This page addresses common questions about using OSOAA.

.. contents:: Contents
   :local:
   :depth: 2

General Questions
-----------------

What is OSOAA?
~~~~~~~~~~~~~~

OSOAA (Ocean Successive Orders with Atmosphere - Advanced) is a vector radiative transfer model for coupled atmosphere-ocean systems. It computes polarized radiance fields accounting for:

- Molecular and aerosol scattering in atmosphere
- Absorption and scattering by ocean constituents
- Rough sea surface (Cox & Munk model)
- Full polarization (Stokes vector)

**Key features:**

- Successive orders of scattering method
- Vector radiative transfer (polarization)
- Atmosphere-ocean coupling
- Realistic rough surface
- Multiple aerosol/hydrosol models

Who should use OSOAA?
~~~~~~~~~~~~~~~~~~~~~

OSOAA is designed for:

- **Researchers** studying ocean color remote sensing
- **Algorithm developers** for satellite missions (MODIS, OLCI, PACE, etc.)
- **Students** learning radiative transfer
- **Scientists** validating bio-optical models

**Prerequisites:**

- Basic understanding of radiative transfer
- Familiarity with ocean optics
- Command-line experience (Fortran execution)
- Knowledge of atmospheric optics helpful

Is OSOAA free?
~~~~~~~~~~~~~~

Yes! OSOAA is free and open-source under the GNU General Public License v3.0 (GPLv3).

- Free for academic and commercial use
- Source code available
- No license fees
- Community-driven development

What makes OSOAA different?
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Unique capabilities:**

- **Full polarization:** Complete Stokes vector treatment
- **Rough surface:** Cox & Munk wind-wave model
- **Atmosphere-ocean coupling:** Proper treatment of interface
- **Successive orders:** Accurate multiple scattering
- **Heritage:** Based on validated OSOA code

**Compared to other models:**

- More detailed than simple two-stream models
- Faster than Monte Carlo for most cases
- Full polarization vs. scalar-only codes
- Specialized for ocean-atmosphere system

Installation and Setup
----------------------

How do I install OSOAA?
~~~~~~~~~~~~~~~~~~~~~~~

**Basic installation:**

1. Download/clone the repository
2. Navigate to ``gen/`` directory
3. Run: ``make -f Makefile_OSOAA.gfortran``
4. Executable created in ``exe/`` directory

See :ref:`installation` for detailed instructions.

What compilers are supported?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Recommended:**

- GNU gfortran (version 4.8+)

**Also supported:**

- Intel ifort
- Standard Fortran 77/90 compilers

**Not supported:**

- Very old compilers (<F77 standard)
- Non-standard Fortran dialects

Do I need special libraries?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

No external libraries required! OSOAA is self-contained Fortran code.

**Optional tools:**

- Python/MATLAB for analysis
- Plotting software for visualization
- Text editor for parameter files

Why does compilation fail?
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Common issues:**

1. **Compiler not found**
   
   - Install gfortran: ``sudo apt-get install gfortran``
   - Check PATH includes compiler

2. **Optimization errors**
   
   - Remove ``-march=native`` from Makefile
   - Use ``-O2`` instead of ``-O3``

3. **Fortran version mismatch**
   
   - Ensure F90-compatible compiler
   - Try different Makefile variant

Running Simulations
-------------------

How do I run a basic simulation?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Steps:**

1. Create parameter file ``simulation.txt``
2. Run: ``exe/OSOAA_MAIN.exe < simulation.txt``
3. Check output: ``LUM_vsVZA.txt``

**Quick example:**

::

    # Minimal simulation
    OSOAA.Wa 550.0
    ANG.Thetas 30.0
    OSOAA.View.Phi 0.0
    OSOAA.View.Level -1
    OSOAA.View.Z -0.0
    ANG.Rad.NbGauss 24
    PROFILE.Atm.MOT 0.1
    AER.AOTref 0.1
    PROFILE.Sea.Depth 100.0
    HYD.Model 1
    HYD.BioOpt.Chl 0.5
    SOS.Surface.Model 1
    SOS.Surface.Wind 5.0

Save and run: ``exe/OSOAA_MAIN.exe < simulation.txt``

Why is my simulation slow?
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Common causes:**

1. **High angular resolution**
   
   - Reduce ``ANG.Rad.NbGauss`` (try 16-24)
   - Remove unnecessary user angles

2. **Too many scattering orders**
   
   - Check convergence in log
   - Reduce ``SOS.IGMAX`` if appropriate

3. **Fine vertical grid**
   
   - Reduce ``PROFILE.Atm.Tlay``
   - Reduce ``PROFILE.Sea.Tlay``

4. **Rough surface**
   
   - High wind speeds slow surface calculation
   - Reduce ``SOS.Surface.WaveNum``

**Optimization tips:**

- Start with coarse grids, refine as needed
- Check if simulation converges early
- Use flat surface (Model=0) for testing

How long should a simulation take?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Typical times (modern laptop):**

- Simple case (24 angles, flat surface): 30 seconds
- Standard case (24 angles, rough surface): 2-5 minutes
- High resolution (48 angles): 10-20 minutes
- Very detailed (100+ angles): 1+ hour

**Factors affecting speed:**

- Number of angles (quadratic impact)
- Surface type (rough vs. flat)
- Vertical resolution
- Scattering orders needed

Parameters and Configuration
-----------------------------

How do I choose parameters?
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Start simple:**

1. Use default values
2. Adjust one parameter at a time
3. Check sensitivity to changes
4. Validate against known cases

**Key parameters:**

- **Wavelength:** Match your application (e.g., 550 nm)
- **Solar angle:** Typical conditions (30-45°)
- **AOT:** 0.05-0.15 for clear, 0.3+ for hazy
- **Chlorophyll:** 0.1-1.0 mg/m³ typical range
- **Wind speed:** 3-8 m/s common values

What aerosol model should I use?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Recommendations:**

- **Remote ocean:** Mono-modal, maritime properties
  ::

      AER.Model 0
      AER.MMD.SDtype 2
      AER.MMD.SDradius 0.2
      AER.MMD.MRwa 1.38
      AER.MMD.MIwa 0.001

- **Coastal/polluted:** Bi-modal (fine + coarse)
  ::

      AER.Model 3
      # Fine mode: pollution
      # Coarse mode: sea salt

- **Dust events:** WMO continental or dust-like
  ::

      AER.Model 1
      AER.WMO.Model 2

- **Known conditions:** External phase function (Model=4)

What chlorophyll concentration?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Typical values:**

- 0.01-0.1 mg/m³: Oligotrophic (open ocean, gyres)
- 0.1-1.0 mg/m³: Mesotrophic (most ocean)
- 1.0-10.0 mg/m³: Eutrophic (coastal, upwelling)
- 10.0-50.0 mg/m³: Highly eutrophic (blooms)

**Sources for data:**

- Satellite ocean color (MODIS, VIIRS)
- In-situ measurements
- Climatologies (WOA, ESA-CCI)
- Bio-optical models

Should I use flat or rough surface?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Flat surface (Model=0):**

- Faster computation
- Good for nadir viewing
- Testing/debugging
- Low wind conditions

**Rough surface (Model=1):**

- More realistic
- Required for off-nadir angles
- Sun glint studies
- Moderate to high wind

**Decision:**

- Start flat for testing
- Use rough for final results
- Always rough for viewing angles > 30°

How do I set convergence parameters?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Default is usually fine:**

::

    SOS.IGMAX 100  # Maximum orders

**Adjust if:**

- **Non-convergence:** Increase IGMAX (try 150-200)
- **Over-iteration:** Check log, may need fewer orders
- **Turbid conditions:** May need more orders

**Check convergence in log file:**

::

    Order 15: Max relative change = 0.0003

When change < 0.001, convergence is good.

Results and Interpretation
--------------------------

My radiance values seem wrong
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Check list:**

1. **Units:** W·m⁻²·sr⁻¹·nm⁻¹ for radiance
2. **Magnitude:** Typical range 0.01-0.1
3. **Spectral behavior:** Blue > green > red (clear water)
4. **Geometry:** Reasonable angular variation
5. **Comparison:** Similar conditions in literature

**Common errors:**

- Wrong wavelength units (nm not µm)
- Incorrect viewing level (above vs. below surface)
- Unrealistic input parameters

I get negative radiances
~~~~~~~~~~~~~~~~~~~~~~~~

**Causes:**

1. **Non-convergence:** Increase maximum orders
2. **Numerical issues:** Extreme geometries (SZA > 80°)
3. **Bad parameters:** Unphysical optical properties
4. **Surface issues:** Very high wind speed

**Solutions:**

- Check convergence in log file
- Review input parameters
- Try simpler case first
- Avoid extreme solar angles

How do I validate my results?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Validation approaches:**

1. **Physical checks:**
   
   - Positive radiances
   - Energy conservation
   - Spectral consistency
   - Angular smoothness

2. **Comparison:**
   
   - Published benchmark cases
   - Other RT models (6S, VLIDORT)
   - Satellite data
   - Field measurements

3. **Sensitivity:**
   
   - Parameter variations
   - Internal consistency
   - Limiting cases

What is degree of polarization (DoLP)?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Definition:**

.. math::

   DoLP = \\frac{\\sqrt{Q^2 + U^2}}{I}

**Interpretation:**

- 0: Unpolarized light
- 0-0.3: Weakly polarized
- 0.3-0.7: Moderately polarized
- 0.7-1.0: Strongly polarized
- 1: Fully polarized

**Typical values:**

- Sky radiance: 0.1-0.6
- Water-leaving: 0.01-0.1
- Sun glint: 0.3-0.9

Errors and Troubleshooting
--------------------------

"Cannot open file" error
~~~~~~~~~~~~~~~~~~~~~~~~

**Solutions:**

1. Check file path (absolute vs. relative)
2. Verify filename spelling
3. Ensure file exists
4. Check file permissions
5. Run from correct directory

"Invalid parameter" error
~~~~~~~~~~~~~~~~~~~~~~~~~

**Solutions:**

1. Check parameter spelling
2. Verify numeric format (use decimal point)
3. Remove extra spaces
4. Check valid parameter ranges
5. Review parameter reference

Simulation crashes or hangs
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Debugging steps:**

1. Enable debug mode in Makefile
2. Review log files
3. Try simpler configuration
4. Check for NaN or infinity
5. Reduce problem size

**Common causes:**

- Extreme optical properties
- Very large grids
- Numerical overflow
- Non-converging iterations

How do I report a bug?
~~~~~~~~~~~~~~~~~~~~~~

**Information to include:**

1. OSOAA version
2. Compiler and version
3. Operating system
4. Complete parameter file
5. Error messages
6. Log files
7. Steps to reproduce

**Where to report:**

- GitHub Issues (if available)
- Email to developers
- User forum/mailing list

Advanced Topics
---------------

Can I use custom phase functions?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Yes! Use Model=4 for aerosols or hydrosols:

::

    AER.Model 4
    AER.ExtData MY_PHASE.txt

Format must include:

- Scattering angles (0-180°)
- Phase function P(θ)
- Single scattering albedo
- Phase matrix elements

See :ref:`file_formats` for details.

How do I simulate multiple wavelengths?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run separate simulations for each wavelength:

.. code-block:: bash

    # Script for multiple wavelengths
    for WL in 412 443 490 550 670 865; do
        sed "s/OSOAA.Wa.*/OSOAA.Wa $WL/" base_params.txt > params_${WL}.txt
        exe/OSOAA_MAIN.exe < params_${WL}.txt
        mv LUM_vsVZA.txt results_${WL}nm.txt
    done

Can I model subsurface profiles?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Yes! Use custom profile files:

::

    HYD.BioOpt.ProfileType 2
    HYD.BioOpt.ProfileFile MY_CHLOROPHYLL.txt

Or user-defined IOPs:

::

    HYD.Model 5
    HYD.UserIOP.File MY_IOPS.txt

How do I couple with ocean models?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Workflow:**

1. Export model IOPs (a, b, bb)
2. Create OSOAA profile file
3. Run OSOAA simulation
4. Compare radiance with satellite
5. Iterate parameter estimation

**Applications:**

- Data assimilation
- Model validation
- Inverse problems
- Algorithm development

Can I parallelize OSOAA?
~~~~~~~~~~~~~~~~~~~~~~~~

OSOAA is currently serial code. For multiple simulations:

**Embarrassingly parallel:**

- Different wavelengths
- Different geometries
- Parameter sweeps
- Ensemble runs

**Example (GNU parallel):**

.. code-block:: bash

    parallel -j 4 'exe/OSOAA_MAIN.exe < {}' ::: param_*.txt

Performance and Optimization
----------------------------

How much memory does OSOAA use?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Typical usage:**

- Small simulation: ~100 MB
- Standard simulation: ~500 MB
- Large simulation: ~2 GB

**Memory scales with:**

- Number of angles (N²)
- Number of vertical levels (N)
- Number of Fourier terms (N)

Can I run on HPC systems?
~~~~~~~~~~~~~~~~~~~~~~~~~

Yes! OSOAA works well on HPC:

**Recommendations:**

- Submit multiple jobs (different configs)
- Use job arrays for parameter sweeps
- Request modest resources per job
- Batch process wavelengths

**Example SLURM script:**

.. code-block:: bash

    #!/bin/bash
    #SBATCH --job-name=osoaa
    #SBATCH --nodes=1
    #SBATCH --ntasks=1
    #SBATCH --mem=2GB
    #SBATCH --time=00:30:00
    
    module load gcc/9.3.0
    
    cd $SLURM_SUBMIT_DIR
    exe/OSOAA_MAIN.exe < params.txt

How do I optimize for speed?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Quick wins:**

1. Reduce angular resolution (16-24 angles)
2. Use flat surface for testing
3. Reduce vertical layers
4. Enable compiler optimization
5. Reduce convergence threshold carefully

**Compilation flags:**

::

    CCOPTS = -O3 -march=native -funroll-loops

**Parameter tuning:**

- Balance accuracy vs. speed
- Test convergence requirements
- Use coarse grids for exploration

Community and Support
---------------------

Where can I get help?
~~~~~~~~~~~~~~~~~~~~~

**Resources:**

- Documentation (this site!)
- Example files in ``fic/`` directory
- Published papers (see Bibliography)
- User community (if available)
- Developer contact

How do I cite OSOAA?
~~~~~~~~~~~~~~~~~~~~

**Primary reference:**

Chami M, Lafrance B, Fougnie B, Chowdhary J, Harmel T, Waquet F (2015), 
"OSOAA: a vector radiative transfer model of coupled atmosphere-ocean system 
for a rough sea surface application to the estimates of the directional 
variations of the water leaving reflectance to better process multi-angular 
satellite sensors data over the ocean", *Opt Express* 23: 27829-27852, 
doi: 10.1364/OE.23.027829

See :ref:`bibliography` for additional references.

Is there a user community?
~~~~~~~~~~~~~~~~~~~~~~~~~~

The OSOAA user community includes:

- Ocean color researchers
- Satellite algorithm developers
- Radiative transfer scientists
- Students and educators

**Contributions welcome:**

- Bug reports
- Feature requests
- Example cases
- Documentation improvements

How can I contribute?
~~~~~~~~~~~~~~~~~~~~~

**Ways to contribute:**

1. Report bugs and issues
2. Share parameter sets
3. Add example cases
4. Improve documentation
5. Develop new features
6. Validate with field data

See :doc:`../contributing` for guidelines.

Where is OSOAA development headed?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Planned improvements:**

- Python API
- Parallel execution
- NetCDF output
- Enhanced GUI
- Additional aerosol models
- Non-spherical particles

**Long-term goals:**

- Real-time processing
- Operational implementation
- Integration with retrieval algorithms
- Extended spectral range

See Also
--------

- :ref:`parameter_reference` for complete parameter documentation
- :ref:`constants` for physical constants
- :ref:`file_formats` for file specifications
- User Guide for tutorials and examples
- :ref:`bibliography` for scientific references
