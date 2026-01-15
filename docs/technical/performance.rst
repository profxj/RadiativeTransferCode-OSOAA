Performance
===========

This section provides guidance on optimizing OSOAA performance and understanding computational costs.

Performance Overview
--------------------

OSOAA is a computationally intensive radiative transfer model. Execution time depends on:

* Angular resolution (number of viewing angles)
* Vertical discretization (number of atmospheric/ocean layers)
* Surface type (flat vs. rough surface)
* Number of scattering orders required for convergence
* Optical properties (optical depth, single scattering albedo)

Typical Execution Times
-----------------------

On a modern workstation (Intel i7, 3.5 GHz):

.. list-table:: Execution Time Estimates
   :widths: 40 30 30
   :header-rows: 1

   * - Configuration
     - Time (flat surface)
     - Time (rough surface)
   * - Quick test (20 angles, 50 levels)
     - 30 seconds
     - 2 minutes
   * - Standard (40 angles, 100 levels)
     - 3 minutes
     - 15 minutes
   * - High resolution (60 angles, 150 levels)
     - 15 minutes
     - 1-2 hours
   * - Very high (80 angles, 200 levels)
     - 45 minutes
     - 4-6 hours

.. note::
   Rough surface calculations require significantly more time due to wave-facet integration 
   over 1024 azimuthal angles.

Performance Bottlenecks
-----------------------

The main computational bottlenecks are:

1. Surface Matrix Calculation (30-70% of total time)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For rough surfaces using Cox & Munk model:

* Integration over wave slope distribution
* 1024 azimuthal angles (``CTE_PH_NU = 1024``)
* Fresnel coefficient calculation for each facet
* Geometric configuration checks

**Computational cost**: :math:`O(N_{\theta}^2 \times N_{\phi})` where :math:`N_{\phi} = 1024`

**Optimization strategies**:

* Use flat surface (``SEA.Type = 0``) for testing
* Reduce angular resolution during development
* Pre-compute and cache surface matrices for standard wind speeds

2. Successive Orders Iteration (20-50% of total time)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each scattering order requires:

* Integration over all viewing angles: :math:`O(N_{\theta}^2)`
* Integration over all vertical levels: :math:`O(N_z^2)`
* Fourier decomposition in azimuth

**Computational cost per order**: :math:`O(N_{\theta}^2 \times N_z^2)`

**Optimization strategies**:

* Reduce ``IGMAX`` (maximum iterations) if acceptable accuracy
* Increase convergence threshold slightly (e.g., 0.001 → 0.005)
* Use geometric series acceleration

3. Mie Calculations (5-10% of total time)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For each particle size and wavelength:

* Recursive computation of Bessel functions
* Summation over :math:`n_{max} \approx x + 4x^{1/3} + 2` terms
* Phase function and phase matrix evaluation

**Computational cost**: :math:`O(N_r \times n_{max}^2 \times N_{\theta})` where :math:`N_r` 
is the number of size distribution points

**Optimization strategies**:

* Use pre-computed Mie tables
* Reduce size distribution quadrature points (if accuracy permits)
* Cache results for repeated wavelength calculations

Optimization Strategies
-----------------------

Compilation Optimization
~~~~~~~~~~~~~~~~~~~~~~~~

Use aggressive compiler optimization flags:

**gfortran** (recommended):

.. code-block:: makefile

   CCOPTS = -O3 -march=native -w

* ``-O3``: Maximum optimization level
* ``-march=native``: CPU-specific optimizations
* ``-w``: Suppress non-critical warnings (cleaner output)

**Intel Fortran** (ifort):

.. code-block:: makefile

   CCOPTS = -O3 -xHost -ipo -no-prec-div

* ``-xHost``: Optimize for current processor
* ``-ipo``: Interprocedural optimization
* ``-no-prec-div``: Faster floating-point division

**Performance gain**: 20-30% faster than default ``-O`` optimization

Parameter Optimization
~~~~~~~~~~~~~~~~~~~~~~

1. Angular Resolution
^^^^^^^^^^^^^^^^^^^^^

**Trade-off**: Accuracy vs. speed

* **Minimum**: 20 Gauss angles (``ANG.Rad.NbGauss 20``)
  
  * Fast, good for testing
  * Adequate for smooth phase functions

* **Standard**: 40-50 Gauss angles (``ANG.Rad.NbGauss 40``)
  
  * Good balance for most applications
  * Recommended for production runs

* **High**: 60-80 Gauss angles (``ANG.Rad.NbGauss 80``)
  
  * Required for strongly peaked phase functions
  * High optical depths

**Scaling**: Execution time scales approximately as :math:`N_{\theta}^2`

Example impact:

.. code-block:: text

   20 angles → baseline (1.0×)
   40 angles → 4× slower
   80 angles → 16× slower

2. Vertical Discretization
^^^^^^^^^^^^^^^^^^^^^^^^^^

**Trade-off**: Vertical resolution vs. speed

* **Coarse**: 30-50 levels
  
  * Fast, suitable for homogeneous media
  * May miss sharp gradients

* **Standard**: 50-100 levels
  
  * Good for most profiles
  * Captures main features

* **Fine**: 100-200 levels
  
  * Required for sharp chlorophyll peaks
  * Thin aerosol layers
  * Stratified atmosphere

**Scaling**: Execution time scales approximately as :math:`N_z^2`

3. Surface Type Selection
^^^^^^^^^^^^^^^^^^^^^^^^^

**Flat surface** (``SEA.Type = 0``):

* Fast: ~5-10× faster than rough surface
* Use for:
  
  * Initial testing
  * Low wind conditions (< 2 m/s)
  * Subsurface radiance calculations

**Rough surface** (``SEA.Type = 1``):

* Realistic for most applications
* Required for:
  
  * Remote sensing simulations
  * Sun glint modeling
  * Polarization studies

**Recommendation**: Use flat surface during development, switch to rough for final results.

4. Convergence Criteria
^^^^^^^^^^^^^^^^^^^^^^^

Adjust convergence thresholds in ``inc/OSOAA.h``:

.. code-block:: c

   // Standard (default)
   #define CTE_PH_SEUIL_CV_SG  0.005
   #define CTE_PH_SEUIL_SUMDIF  0.001
   
   // Faster (reduced accuracy)
   #define CTE_PH_SEUIL_CV_SG  0.01
   #define CTE_PH_SEUIL_SUMDIF  0.005
   
   // Higher accuracy (slower)
   #define CTE_PH_SEUIL_CV_SG  0.001
   #define CTE_PH_SEUIL_SUMDIF  0.0001

**Performance gain**: 20-40% speedup with looser criteria, typically < 1% accuracy loss

Algorithmic Optimization
~~~~~~~~~~~~~~~~~~~~~~~~

1. Fourier Series Truncation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The radiance is expanded in Fourier series:

.. math::

   I(\theta, \phi) = \sum_{m=0}^{M} I_m(\theta) \cos[m(\phi - \phi_0)]

**Optimization**: Truncate at :math:`M_{max}` when higher terms are negligible.

From ``OSOAA.h``:

.. code-block:: c

   #define CTE_PH_SEUIL_SF  0.0002      // Fourier convergence threshold

**Performance gain**: Reduces azimuthal integration points by factor of 2-3 for smooth phase functions.

2. Phase Function Truncation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For strongly forward-scattering phase functions, truncate the forward peak:

.. code-block:: c

   #define CTE_AER_MU1_TRONCA 0.8       // First truncation threshold
   #define CTE_AER_MU2_TRONCA 0.94      // Second truncation threshold

**Method**: Delta-Eddington approximation for :math:`\cos\theta > 0.94`

**Performance gain**: 10-20% speedup for aerosol-dominated cases

3. Geometric Series Acceleration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For optically thick media, approximate tail of scattering series:

.. math::

   \sum_{n=N}^{\infty} I^{(n)} \approx \frac{I^{(N)}}{1 - r}

Where :math:`r` is estimated from last few orders.

**Threshold**:

.. code-block:: c

   #define CTE_PH_SEUIL_CV_SG  0.005

**Performance gain**: Can reduce required orders from 100+ to 20-30 for turbid water.

Memory Optimization
-------------------

Memory Usage
~~~~~~~~~~~~

OSOAA's memory footprint is determined by:

.. math::

   \text{Memory} \approx 8 \times N_{\theta} \times N_z \times 4 \times N_{fields}

Where:

* 8 bytes per double-precision number
* :math:`N_{\theta}` = number of angles
* :math:`N_z` = number of vertical levels
* 4 = Stokes vector components (I, Q, U, V)
* :math:`N_{fields}` ≈ 10-20 (various intermediate fields)

Example calculation:

.. code-block:: text

   40 angles × 100 levels × 4 components × 15 fields × 8 bytes
   = 40 × 100 × 4 × 15 × 8 = 19.2 MB (core arrays)
   
   Total with overhead: ~100-200 MB

Reducing Memory Usage
~~~~~~~~~~~~~~~~~~~~~

If memory is limited:

1. **Reduce angular resolution**: Most effective
2. **Reduce vertical levels**: For homogeneous media
3. **Use single precision**: Edit Fortran code (``REAL*8 → REAL*4``)
   
   * Cuts memory in half
   * May reduce accuracy by ~0.1%

Memory-Constrained Systems
~~~~~~~~~~~~~~~~~~~~~~~~~~

For systems with < 4 GB RAM:

* Limit to 40 angles, 80 levels
* Use flat surface only
* Run single wavelength at a time

Parallelization
---------------

Current Status
~~~~~~~~~~~~~~

OSOAA v2.0 is a **serial code** with no built-in parallelization.

Opportunities for Parallelization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Multiple Wavelengths** (Embarrassingly Parallel)
   
   Run separate OSOAA instances for each wavelength:
   
   .. code-block:: bash
   
      # GNU Parallel
      parallel -j 4 ./OSOAA_MAIN.exe ::: param_440nm.txt param_550nm.txt \
                                          param_670nm.txt param_870nm.txt
   
   **Speedup**: Linear with number of cores

2. **Multiple Viewing Angles** (Embarrassingly Parallel)
   
   Run separate instances for different viewing geometries:
   
   .. code-block:: bash
   
      parallel -j 8 ./OSOAA_MAIN.exe ::: geom_*.txt
   
   **Speedup**: Linear with number of cores

3. **Within-Order Parallelization** (Moderate)
   
   Add OpenMP pragmas to angular loops:
   
   .. code-block:: fortran
   
      !$OMP PARALLEL DO PRIVATE(I, J, ...)
      DO I = 1, N_ANGLES
         DO J = 1, N_LEVELS
            ! Compute radiance contribution
         END DO
      END DO
      !$OMP END PARALLEL DO
   
   **Expected speedup**: 2-4× on 8-core system (not perfectly parallel due to data dependencies)

4. **Surface Matrix Calculation** (Easy to Parallelize)
   
   Each angle pair is independent:
   
   .. code-block:: fortran
   
      !$OMP PARALLEL DO COLLAPSE(2)
      DO I_INC = 1, N_ANGLES
         DO I_VIEW = 1, N_ANGLES
            CALL COMPUTE_SURFACE_MATRIX(I_INC, I_VIEW, ...)
         END DO
      END DO
      !$OMP END PARALLEL DO
   
   **Expected speedup**: Near-linear (7-8× on 8 cores)

MPI Parallelization
~~~~~~~~~~~~~~~~~~~

For large-scale studies across compute clusters:

.. code-block:: fortran

   ! Master process distributes wavelengths to workers
   IF (rank == 0) THEN
      DO i = 1, n_wavelengths
         worker = MOD(i, n_procs - 1) + 1
         CALL MPI_SEND(wavelength(i), worker, tag, ...)
      END DO
   ELSE
      CALL MPI_RECV(my_wavelength, 0, tag, ...)
      CALL RUN_OSOAA(my_wavelength)
   END IF

**Scalability**: Excellent for wavelength/geometry sweeps

Benchmarking
------------

Standard Benchmark Cases
~~~~~~~~~~~~~~~~~~~~~~~~

For performance comparison, use these standard configurations:

**Test 1: Quick Check**

.. code-block:: text

   Wavelength: 550 nm
   Solar zenith: 30°
   Viewing zenith: 0° (nadir)
   Angles: 20
   Levels: 50
   Surface: Flat
   Aerosol: Maritime, τ=0.1
   Ocean: Chl=0.1 mg/m³
   Expected time: ~30 seconds (baseline)

**Test 2: Standard Case**

.. code-block:: text

   Wavelength: 550 nm
   Solar zenith: 30°
   Viewing zenith: 0° to 60° (10° steps)
   Angles: 40
   Levels: 100
   Surface: Rough, wind=5 m/s
   Aerosol: Maritime, τ=0.1
   Ocean: Chl=0.3 mg/m³, depth=100m
   Expected time: ~15 minutes

**Test 3: High Resolution**

.. code-block:: text

   Wavelength: 550 nm
   Solar zenith: 60°
   Viewing zenith: 0° to 70° (5° steps)
   Angles: 80
   Levels: 150
   Surface: Rough, wind=7 m/s
   Aerosol: Urban, τ=0.5
   Ocean: Chl=1.0 mg/m³, depth=50m
   Expected time: ~2 hours

Performance Monitoring
----------------------

Profiling Tools
~~~~~~~~~~~~~~~

**Linux**: Use ``gprof`` for profiling:

.. code-block:: bash

   # Compile with profiling
   gfortran -pg -O3 -o OSOAA_MAIN.exe ...
   
   # Run
   ./OSOAA_MAIN.exe < input.txt
   
   # Analyze
   gprof OSOAA_MAIN.exe gmon.out > profile.txt

**Output shows**:

* Time spent in each subroutine
* Number of calls
* Cumulative time

Log File Analysis
~~~~~~~~~~~~~~~~~

OSOAA generates detailed log files:

**SOS_LOG.txt** shows iteration progress:

.. code-block:: text

   Order  1: CPU time = 2.34 seconds
   Order  2: CPU time = 2.56 seconds
   Order  3: CPU time = 2.61 seconds
   ...
   Total CPU time: 15.25 seconds

**SEA_LOG.txt** shows surface calculation time:

.. code-block:: text

   Reflection matrices: 15.3 minutes
   Transmission matrices: 12.7 minutes
   Total: 28.0 minutes

Performance Tips
----------------

For Interactive Work
~~~~~~~~~~~~~~~~~~~~

1. Start with minimal resolution:
   
   * 20 angles
   * Flat surface
   * Homogeneous profiles

2. Gradually increase complexity

3. Use rough surface only for final runs

For Production Runs
~~~~~~~~~~~~~~~~~~~

1. Pre-compute Mie tables for common aerosols

2. Batch similar cases:
   
   * Group by wavelength
   * Group by geometry

3. Use shell scripts for parameter sweeps:
   
   .. code-block:: bash
   
      for chl in 0.03 0.1 0.3 1.0 3.0; do
         sed "s/CHL_VALUE/$chl/" template.txt > param_chl${chl}.txt
         ./OSOAA_MAIN.exe < param_chl${chl}.txt
      done

For Large-Scale Studies
~~~~~~~~~~~~~~~~~~~~~~~

1. Use parallel execution (wavelengths, geometries)

2. Consider cluster/cloud computing

3. Optimize I/O:
   
   * Write only necessary output
   * Use binary formats when possible

4. Archive results efficiently

Hardware Recommendations
------------------------

For Different Use Cases
~~~~~~~~~~~~~~~~~~~~~~~

**Student/Learning**:

* CPU: Intel i5 or equivalent
* RAM: 8 GB
* Storage: 100 GB SSD
* Expected: 1-2 test cases per hour

**Research/Development**:

* CPU: Intel i7/i9 or AMD Ryzen 7/9 (8+ cores)
* RAM: 16-32 GB
* Storage: 500 GB SSD
* Expected: 10-20 cases per day

**Production/Operational**:

* CPU: Dual Xeon or AMD EPYC (32+ cores)
* RAM: 64-128 GB
* Storage: 2+ TB SSD (RAID)
* Network: Fast interconnect for clusters
* Expected: 100+ cases per day with parallelization

Future Improvements
-------------------

Planned optimizations for future versions:

1. **GPU Acceleration**
   
   * Target: Surface matrix calculations
   * Expected speedup: 10-50×

2. **OpenMP Threading**
   
   * Multi-threaded scattering orders
   * Expected speedup: 3-6× on multi-core systems

3. **Adaptive Grid Refinement**
   
   * Automatic angular/vertical grid adjustment
   * Optimize accuracy vs. speed trade-off

4. **Improved Convergence**
   
   * Better acceleration schemes
   * Reduce typical orders from 10-20 to 5-10

5. **Pre-computed Tables**
   
   * Standard aerosol models
   * Common ocean IOPs
   * Surface matrices for standard winds

Troubleshooting Performance Issues
----------------------------------

Simulation Hangs or Very Slow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptoms**:

* No output for > 1 hour
* CPU usage at 100% but no progress

**Possible causes**:

1. **Surface matrix stuck**: Reduce wind speed or use flat surface temporarily
2. **Non-convergent iteration**: Check optical properties for validity
3. **Excessive scattering orders**: Reduce ``IGMAX`` or increase thresholds

**Solutions**:

.. code-block:: text

   # Check current parameters
   SEA.Type 0              # Use flat surface for testing
   IGMAX 50                # Limit iterations
   ANG.Rad.NbGauss 20      # Reduce angles

High Memory Usage
~~~~~~~~~~~~~~~~~

**Symptoms**:

* System swapping
* Out of memory errors

**Solutions**:

1. Reduce angular resolution
2. Reduce vertical levels
3. Run one wavelength at a time
4. Close other applications

Poor Accuracy Despite Long Runtime
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptoms**:

* Results don't match expectations
* High residuals

**Possible causes**:

1. Insufficient angular resolution for sharp features
2. Too coarse vertical grid for gradients
3. Convergence not achieved

**Solutions**:

* Increase ``ANG.Rad.NbGauss``
* Refine vertical grid near features
* Check convergence in ``SOS_LOG.txt``

Next Steps
----------

* :doc:`code_structure` - Understanding code organization
* :doc:`algorithms` - Algorithm details
* :doc:`../user_guide/running_osoaa` - Execution guide

See Also
--------

* :doc:`../examples/basic_simulation` - Example workflows
* :doc:`../reference/parameter_reference` - Parameter optimization
