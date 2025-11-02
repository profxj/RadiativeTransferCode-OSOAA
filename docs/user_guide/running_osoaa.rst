Running OSOAA
=============

This guide covers various methods for executing OSOAA simulations, from simple runs to advanced batch processing.

Basic Execution
---------------

Command Line Execution
~~~~~~~~~~~~~~~~~~~~~~

The simplest way to run OSOAA::

    cd exe
    ./OSOAA_MAIN.exe < ../input_file.txt

Or from any directory with full path::

    /path/to/OSOAA/exe/OSOAA_MAIN.exe < input_parameters.txt

With Output Redirection
~~~~~~~~~~~~~~~~~~~~~~~~

Capture console output to a log file::

    ./OSOAA_MAIN.exe < input.txt > simulation.log 2>&1

Separate standard output and errors::

    ./OSOAA_MAIN.exe < input.txt > output.log 2> error.log

Interactive Mode
~~~~~~~~~~~~~~~~

Run without input file (not recommended for production)::

    ./OSOAA_MAIN.exe

The program will prompt for each parameter. Use Ctrl+C to exit.

Execution Environments
----------------------

Linux/Unix
~~~~~~~~~~

Standard execution::

    #!/bin/bash
    cd /path/to/OSOAA/exe
    ./OSOAA_MAIN.exe < ../inputs/my_simulation.txt

With environment variables::

    export OSOAA_HOME=/path/to/OSOAA
    $OSOAA_HOME/exe/OSOAA_MAIN.exe < input.txt

macOS
~~~~~

Same as Linux. If using Homebrew gfortran::

    # May need to set library paths
    export DYLD_LIBRARY_PATH=/usr/local/opt/gcc/lib:$DYLD_LIBRARY_PATH
    ./OSOAA_MAIN.exe < input.txt

Windows
~~~~~~~

Using MinGW or Cygwin::

    cd C:\OSOAA\exe
    OSOAA_MAIN.exe < ..\inputs\input.txt

Using Command Prompt::

    C:\OSOAA\exe\OSOAA_MAIN.exe < C:\OSOAA\inputs\input.txt

Performance Considerations
--------------------------

Computational Cost Factors
~~~~~~~~~~~~~~~~~~~~~~~~~~

Simulation time depends on:

1. **Angular resolution**
   
   * More Gauss angles → longer runtime
   * ``ANG.Rad.NbGauss``: 40 (fast), 80 (accurate)

2. **Vertical resolution**
   
   * More atmospheric/ocean levels → longer runtime
   * Typically 50-100 levels per medium

3. **Scattering orders**
   
   * More orders → longer runtime but better accuracy
   * Typically converges in 5-15 orders

4. **Surface roughness**
   
   * Rough surface (Cox & Munk) much slower than flat
   * Requires integration over wave slopes

5. **Particle complexity**
   
   * Bi-modal distributions slower than mono-modal
   * External phase functions faster than Mie calculation

Typical Runtime
~~~~~~~~~~~~~~~

On a modern workstation (Intel i7, 16GB RAM):

.. list-table:: Approximate Runtime
   :widths: 40 60
   :header-rows: 1

   * - Configuration
     - Time
   * - Simple (flat surface, 40 angles)
     - 1-5 minutes
   * - Standard (rough surface, 50 angles)
     - 10-30 minutes
   * - High accuracy (rough surface, 80 angles)
     - 30-90 minutes
   * - Very high accuracy (100 angles, many levels)
     - 1-4 hours

Optimization Strategies
~~~~~~~~~~~~~~~~~~~~~~~

1. **For testing**: Use flat surface and fewer angles
2. **For production**: Use rough surface with optimal angle count
3. **Parallel approach**: Run multiple wavelengths in parallel
4. **Pre-compute**: Save Mie calculations for reuse

Memory Requirements
~~~~~~~~~~~~~~~~~~~

Typical memory usage:

* Simple simulation: 100-500 MB
* Standard simulation: 500 MB - 2 GB
* High-resolution: 2-8 GB

If encountering memory errors:

* Reduce angular resolution
* Decrease vertical levels
* Run on machine with more RAM

Monitoring Progress
-------------------

Console Output
~~~~~~~~~~~~~~

OSOAA prints progress information::

    ========================================
    OSOAA V2.0 - Radiative Transfer Model
    ========================================
    
    Reading input parameters... OK
    Validating parameters... OK
    
    Initializing angular grid...
    - Radiance angles: 40 Gauss + 10 user = 50 total
    - Mie angles: 83 Gauss angles
    
    Computing atmospheric profile...
    - Levels: 50
    - AOT at 550nm: 0.100
    
    Computing aerosol properties...
    - Model: Mono-modal log-normal
    - Calling Mie calculations... OK
    
    Computing ocean profile...
    - Depth: 100.0 m
    - Levels: 60
    
    Computing hydrosol properties...
    - Chlorophyll: 0.100 mg/m³
    - Profile: Homogeneous
    
    Computing surface matrices...
    - Type: Rough (Cox & Munk)
    - Wind speed: 5.0 m/s
    - Computing reflection matrices... [===>      ] 45%

Convergence Messages
~~~~~~~~~~~~~~~~~~~~

For each scattering order::

    Starting successive orders iteration...
    
    Order   1: Relative change = 1.000000  [Initial]
    Order   2: Relative change = 0.234567  
    Order   3: Relative change = 0.056789  
    Order   4: Relative change = 0.012345  
    Order   5: Relative change = 0.002345  
    Order   6: Relative change = 0.000456  CONVERGED
    
    Total scattering orders computed: 6
    Convergence achieved with threshold: 0.001000

Log Files
~~~~~~~~~

Several log files are created:

* ``AER_LOG.txt`` - Aerosol calculations
* ``HYD_LOG.txt`` - Hydrosol calculations  
* ``SEA_LOG.txt`` - Surface calculations
* ``SOS_LOG.txt`` - Radiative transfer core

Check these for detailed diagnostic information.

Error Handling
--------------

Common Errors
~~~~~~~~~~~~~

**Error 1: Input file not found**

::

    ERROR: Cannot open input file: input.txt

**Solution**: Check file path and name.

**Error 2: Invalid parameter value**

::

    ERROR: Parameter OSOAA.Wa = 1500.0 exceeds maximum 1000.0

**Solution**: Correct parameter to valid range.

**Error 3: Missing required parameter**

::

    ERROR: Required parameter ANG.Thetas not specified

**Solution**: Add missing parameter to input file.

**Error 4: File permission error**

::

    ERROR: Cannot write output file: LUM_vsVZA.txt

**Solution**: Check write permissions in output directory.

**Error 5: Memory allocation failed**

::

    ERROR: Memory allocation failed for array RADIANCE

**Solution**: 

* Reduce angular resolution
* Decrease vertical levels
* Run on machine with more RAM

Warning Messages
~~~~~~~~~~~~~~~~

Warnings don't stop execution but indicate potential issues:

::

    WARNING: Convergence not fully achieved at order 100
    WARNING: Large solar zenith angle (85°) may affect accuracy
    WARNING: Very high wind speed (20 m/s) - Cox & Munk may not be valid

Review warnings and consider if adjustments are needed.

Batch Processing
----------------

Shell Script (Linux/macOS)
~~~~~~~~~~~~~~~~~~~~~~~~~~

Create ``batch_run.sh``::

    #!/bin/bash
    
    # Configuration
    OSOAA_EXE="./exe/OSOAA_MAIN.exe"
    INPUT_DIR="./inputs"
    OUTPUT_DIR="./outputs"
    
    # Create output directory
    mkdir -p $OUTPUT_DIR
    
    # Process all input files
    for input_file in $INPUT_DIR/*.txt; do
        # Extract filename without path
        filename=$(basename "$input_file" .txt)
        
        echo "========================================="
        echo "Processing: $filename"
        echo "========================================="
        
        # Run simulation
        $OSOAA_EXE < $input_file > $OUTPUT_DIR/${filename}.log 2>&1
        
        # Check if successful
        if [ $? -eq 0 ]; then
            echo "SUCCESS: $filename"
            
            # Move output files
            mv exe/LUM_*.txt $OUTPUT_DIR/${filename}_
            mv exe/LUM_*.bin $OUTPUT_DIR/
        else
            echo "FAILED: $filename"
        fi
        
        echo ""
    done
    
    echo "All simulations complete!"

Run it::

    chmod +x batch_run.sh
    ./batch_run.sh

Parameter Sweep
~~~~~~~~~~~~~~~

Sweep over parameter values::

    #!/bin/bash
    
    # Sweep chlorophyll concentration
    for chl in 0.01 0.03 0.1 0.3 1.0 3.0 10.0; do
        echo "Running Chl = $chl mg/m³"
        
        # Create modified input file
        sed "s/HYD.Chl .*/HYD.Chl $chl/" template.txt > temp_input.txt
        
        # Run OSOAA
        ./exe/OSOAA_MAIN.exe < temp_input.txt > logs/chl_${chl}.log
        
        # Save results
        cp exe/LUM_vsVZA.txt results/LUM_chl_${chl}.txt
    done
    
    rm temp_input.txt

Multi-Wavelength Processing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Process multiple wavelengths::

    #!/bin/bash
    
    wavelengths=(412 443 490 510 550 670 765 865)
    
    for wl in "${wavelengths[@]}"; do
        echo "Processing wavelength: $wl nm"
        
        # Modify wavelength in input
        sed "s/OSOAA.Wa .*/OSOAA.Wa $wl/" base_input.txt > input_${wl}.txt
        
        # Run simulation
        ./exe/OSOAA_MAIN.exe < input_${wl}.txt > logs/wl_${wl}.log
        
        # Rename outputs
        mv exe/LUM_vsVZA.txt results/LUM_${wl}nm.txt
    done

Parallel Execution
~~~~~~~~~~~~~~~~~~

Run multiple simulations in parallel using GNU Parallel::

    # Install GNU Parallel if needed
    # sudo apt-get install parallel
    
    # Create list of input files
    ls inputs/*.txt > input_list.txt
    
    # Run in parallel (4 simultaneous jobs)
    parallel -j 4 './exe/OSOAA_MAIN.exe < {}' :::: input_list.txt

Or using xargs::

    ls inputs/*.txt | xargs -P 4 -I {} ./exe/OSOAA_MAIN.exe < {}

Python Wrapper
~~~~~~~~~~~~~~

For more complex workflows, use Python::

    import subprocess
    import os
    
    def run_osoaa(input_file, output_dir):
        """Run OSOAA simulation"""
        
        # Run OSOAA
        with open(input_file, 'r') as f_in:
            result = subprocess.run(
                ['./exe/OSOAA_MAIN.exe'],
                stdin=f_in,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        
        # Check success
        if result.returncode == 0:
            print(f"Success: {input_file}")
            
            # Move output files
            # ... (implement file management)
            
            return True
        else:
            print(f"Failed: {input_file}")
            print(result.stderr)
            return False
    
    # Run simulations
    input_files = ['input1.txt', 'input2.txt', 'input3.txt']
    for input_file in input_files:
        run_osoaa(input_file, './outputs')

Using the GUI
-------------

Starting the GUI
~~~~~~~~~~~~~~~~

Launch the Java interface::

    cd ihm
    java -jar OSOAA-GUI.jar

Or with more memory::

    java -Xmx2G -jar OSOAA-GUI.jar

GUI Features
~~~~~~~~~~~~

1. **Parameter Forms**
   
   * Organized by categories
   * Form validation
   * Tooltips for each parameter
   * Default value suggestions

2. **File Management**
   
   * Browse for input/output files
   * Load saved configurations
   * Export parameter files

3. **Batch Setup**
   
   * Create parameter sweeps
   * Define multiple scenarios
   * Queue simulations

4. **Visualization**
   
   * Plot results directly
   * Compare multiple runs
   * Export figures

Advantages of GUI:

* User-friendly parameter entry
* Validation prevents errors
* Easier for beginners
* Good for exploratory work

Disadvantages:

* Less scriptable than command line
* Harder to automate
* May not support all advanced features

Best Practices
--------------

1. **Test First**
   
   Run a quick test with low resolution before full simulation.

2. **Version Control**
   
   Keep input files in version control (git).

3. **Descriptive Names**
   
   Use meaningful filenames: ``chl01_wind5_sza30.txt``

4. **Document Parameters**
   
   Add comments in input files explaining choices.

5. **Backup Results**
   
   Save output files with descriptive names before re-running.

6. **Monitor Resources**
   
   Check CPU and memory usage during execution.

7. **Validate Results**
   
   Always check output for physical reasonableness.

Troubleshooting Performance
---------------------------

Simulation Too Slow
~~~~~~~~~~~~~~~~~~~

**Symptom**: Simulation takes hours

**Solutions**:

1. Reduce angular resolution (``ANG.Rad.NbGauss``)
2. Use flat surface for testing (``SEA.Type = 0``)
3. Reduce vertical levels
4. Check if stuck in surface matrix calculation

Memory Issues
~~~~~~~~~~~~~

**Symptom**: Program crashes or system swaps

**Solutions**:

1. Monitor memory with ``top`` or ``htop``
2. Reduce angular grid
3. Close other applications
4. Run on more powerful machine

Non-Convergence
~~~~~~~~~~~~~~~

**Symptom**: Maximum iterations reached without convergence

**Solutions**:

1. Check input parameters for physical validity
2. Increase maximum iterations (if reasonable)
3. Adjust convergence thresholds
4. Review scattering properties

Next Steps
----------

* :doc:`output_files` - Understanding result files
* :doc:`../examples/basic_simulation` - Example workflows
* :doc:`../technical/performance` - Performance optimization
