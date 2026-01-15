.. _file_formats:

File Formats
============

This page documents the file formats used for input and output in PyBaMM.

.. contents:: Contents
   :local:
   :depth: 2

Parameter Files
---------------

CSV Format
~~~~~~~~~~

Parameters can be stored in CSV (Comma-Separated Values) format.

**Structure:**

.. code-block:: text

   Name,Value,Units
   "Negative particle radius",5.86e-6,m
   "Positive particle radius",5.22e-6,m
   "Negative electrode porosity",0.25,dimensionless
   "Separator thickness",25e-6,m

**Loading in PyBaMM:**

.. code-block:: python

   import pybamm
   
   params = pybamm.ParameterValues(csv_file="my_parameters.csv")

**Requirements:**

- First row must be header: ``Name,Value,Units``
- Parameter names must match PyBaMM conventions
- Values can be numeric or string expressions
- Units column is optional but recommended for documentation

**Example with expressions:**

.. code-block:: text

   Name,Value,Units
   "Electrode height",0.065,m
   "Electrode width",1.58,m
   "Electrode area","[Electrode height] * [Electrode width]",m2

JSON Format
~~~~~~~~~~~

Parameters can be stored in JSON (JavaScript Object Notation) format.

**Structure:**

.. code-block:: json

   {
     "Negative particle radius [m]": 5.86e-6,
     "Positive particle radius [m]": 5.22e-6,
     "Negative electrode porosity": 0.25,
     "Separator thickness [m]": 25e-6,
     "chemistry": {
       "name": "graphite-NMC",
       "description": "Graphite negative, NMC positive"
     }
   }

**Loading in PyBaMM:**

.. code-block:: python

   import pybamm
   import json
   
   with open("my_parameters.json") as f:
       param_dict = json.load(f)
   
   params = pybamm.ParameterValues(param_dict)

**Advantages:**

- Hierarchical structure
- Support for nested data
- Easy to parse and manipulate
- Human-readable

Python Format
~~~~~~~~~~~~~

Parameters can be defined directly in Python files.

**Example file** ``my_parameters.py``:

.. code-block:: python

   import numpy as np
   
   def graphite_ocp(sto):
       """Open-circuit potential for graphite"""
       return (
           0.194 + 1.5 * np.exp(-120.0 * sto)
           + 0.0351 * np.tanh((sto - 0.286) / 0.083)
           - 0.0045 * np.tanh((sto - 0.9) / 0.119)
           - 0.035 * np.tanh((sto - 0.99) / 0.05)
           - 0.0147 * np.tanh((sto - 0.5) / 0.034)
           - 0.102 * np.tanh((sto - 0.194) / 0.142)
           - 0.022 * np.tanh((sto - 0.9) / 0.0164)
           - 0.011 * np.tanh((sto - 0.124) / 0.0226)
           + 0.0155 * np.tanh((sto - 0.105) / 0.029)
       )
   
   parameters = {
       "Negative particle radius [m]": 5.86e-6,
       "Positive particle radius [m]": 5.22e-6,
       "Negative electrode OCP [V]": graphite_ocp,
   }

**Loading in PyBaMM:**

.. code-block:: python

   import pybamm
   from my_parameters import parameters
   
   params = pybamm.ParameterValues(parameters)

Data Files
----------

Drive Cycle Data
~~~~~~~~~~~~~~~~

Drive cycles define current or power as a function of time.

**CSV Format:**

.. code-block:: text

   Time [s],Current [A]
   0,0
   10,5.0
   20,10.0
   30,5.0
   40,0

**Loading and using:**

.. code-block:: python

   import pybamm
   import pandas as pd
   
   # Load drive cycle
   data = pd.read_csv("drive_cycle.csv")
   time = data["Time [s]"]
   current = data["Current [A]"]
   
   # Create interpolated function
   drive_cycle = pybamm.Interpolant(time, current, t)
   
   # Use in simulation
   experiment = pybamm.Experiment(
       [pybamm.step.Current(drive_cycle, duration=max(time))]
   )

**Common formats:**

- EPA drive cycles (UDDS, HWFET, US06)
- WLTP drive cycles
- Custom profiles

OCP Data
~~~~~~~~

Open-circuit potential data for electrode materials.

**Format:**

.. code-block:: text

   Stoichiometry,Voltage [V]
   0.0,0.1394
   0.05,0.1281
   0.1,0.1194
   0.15,0.1147
   ...
   0.95,0.0612
   1.0,0.0531

**Loading:**

.. code-block:: python

   import pybamm
   import pandas as pd
   
   # Load OCP data
   data = pd.read_csv("graphite_ocp.csv")
   sto = data["Stoichiometry"]
   voltage = data["Voltage [V]"]
   
   # Create interpolant
   graphite_ocp = pybamm.Interpolant(sto, voltage, "Stoichiometry")
   
   # Use in parameters
   params = pybamm.ParameterValues("Chen2020")
   params["Negative electrode OCP [V]"] = graphite_ocp

Experimental Data
~~~~~~~~~~~~~~~~~

Data from experiments for comparison and validation.

**Format:**

.. code-block:: text

   Time [s],Voltage [V],Current [A],Temperature [K]
   0,4.2,0,298.15
   1,4.19,5.0,298.2
   2,4.18,5.0,298.3
   3,4.17,5.0,298.4
   ...

**Loading for comparison:**

.. code-block:: python

   import pybamm
   import pandas as pd
   
   # Load experimental data
   exp_data = pd.read_csv("experimental_discharge.csv")
   
   # Run simulation
   model = pybamm.lithium_ion.DFN()
   sim = pybamm.Simulation(model)
   sim.solve([0, 3600])
   
   # Compare
   import matplotlib.pyplot as plt
   
   plt.plot(exp_data["Time [s]"], exp_data["Voltage [V]"], 
            'o', label="Experiment")
   plt.plot(sim.solution["Time [s]"].entries, 
            sim.solution["Voltage [V]"].entries,
            '-', label="Simulation")
   plt.legend()
   plt.show()

Output Files
------------

Solution Objects
~~~~~~~~~~~~~~~~

PyBaMM solution objects can be saved and loaded.

**Saving:**

.. code-block:: python

   import pybamm
   
   # Run simulation
   model = pybamm.lithium_ion.SPM()
   sim = pybamm.Simulation(model)
   solution = sim.solve([0, 3600])
   
   # Save solution
   solution.save("my_solution.pkl")

**Loading:**

.. code-block:: python

   import pybamm
   
   # Load solution
   solution = pybamm.load("my_solution.pkl")
   
   # Use loaded solution
   print(solution["Voltage [V]"].entries)

**File format:** Python pickle format (``.pkl``)

CSV Export
~~~~~~~~~~

Export solution data to CSV for use in other tools.

**Example:**

.. code-block:: python

   import pybamm
   import pandas as pd
   
   # Run simulation
   model = pybamm.lithium_ion.SPM()
   sim = pybamm.Simulation(model)
   solution = sim.solve([0, 3600])
   
   # Extract variables
   time = solution["Time [s]"].entries
   voltage = solution["Voltage [V]"].entries
   current = solution["Current [A]"].entries
   
   # Create DataFrame
   df = pd.DataFrame({
       "Time [s]": time,
       "Voltage [V]": voltage,
       "Current [A]": current
   })
   
   # Save to CSV
   df.to_csv("simulation_results.csv", index=False)

**Output format:**

.. code-block:: text

   Time [s],Voltage [V],Current [A]
   0.0,4.2,5.0
   1.0,4.19,5.0
   2.0,4.18,5.0
   ...

MATLAB Export
~~~~~~~~~~~~~

Export data for use in MATLAB.

**Example:**

.. code-block:: python

   import pybamm
   from scipy.io import savemat
   
   # Run simulation
   solution = sim.solve([0, 3600])
   
   # Prepare data
   data = {
       "time": solution["Time [s]"].entries,
       "voltage": solution["Voltage [V]"].entries,
       "current": solution["Current [A]"].entries
   }
   
   # Save to .mat file
   savemat("simulation_results.mat", data)

**Loading in MATLAB:**

.. code-block:: matlab

   % Load data
   load('simulation_results.mat');
   
   % Plot
   plot(time, voltage);
   xlabel('Time [s]');
   ylabel('Voltage [V]');

VTK Export
~~~~~~~~~~

Export spatial data for visualization in ParaView.

**Example:**

.. code-block:: python

   import pybamm
   
   # Run simulation with spatial model
   model = pybamm.lithium_ion.DFN()
   sim = pybamm.Simulation(model)
   solution = sim.solve([0, 3600])
   
   # Export to VTK
   solution.save_data("output.vtu", 
                     ["Electrolyte concentration [mol.m-3]"],
                     to_format="vtk")

**Usage:**

- Open ``.vtu`` files in ParaView
- Visualize 1D, 2D, or 3D spatial distributions
- Create animations over time

Model Files
-----------

Custom Models
~~~~~~~~~~~~~

Custom models can be saved as Python modules.

**Example structure:**

.. code-block:: python

   # my_model.py
   import pybamm
   
   class MyCustomModel(pybamm.lithium_ion.BaseModel):
       """Custom lithium-ion model"""
       
       def __init__(self, name="My Custom Model"):
           super().__init__({}, name)
           
           # Define variables
           # Define equations
           # Set boundary conditions
           # etc.

**Using custom model:**

.. code-block:: python

   from my_model import MyCustomModel
   
   model = MyCustomModel()
   sim = pybamm.Simulation(model)

Mesh Files
----------

Custom Mesh Definitions
~~~~~~~~~~~~~~~~~~~~~~~

Advanced users can define custom meshes.

**Example:**

.. code-block:: python

   import pybamm
   import numpy as np
   
   # Define custom mesh edges
   edges = {
       "negative electrode": np.linspace(0, 0.1, 20),
       "separator": np.linspace(0.1, 0.125, 10),
       "positive electrode": np.linspace(0.125, 0.225, 20),
   }
   
   # Create mesh
   mesh = pybamm.Mesh(geometry, submesh_types, var_pts, edges=edges)

Configuration Files
-------------------

Solver Settings
~~~~~~~~~~~~~~~

Solver configurations can be stored in JSON.

**Example:**

.. code-block:: json

   {
     "solver": "CasadiSolver",
     "mode": "safe",
     "rtol": 1e-6,
     "atol": 1e-8,
     "max_step": 100,
     "dt_max": 10
   }

**Loading:**

.. code-block:: python

   import pybamm
   import json
   
   with open("solver_config.json") as f:
       config = json.load(f)
   
   solver = getattr(pybamm, config["solver"])(
       mode=config["mode"],
       rtol=config["rtol"],
       atol=config["atol"]
   )

Experiment Definitions
~~~~~~~~~~~~~~~~~~~~~~

Experiments can be defined in JSON.

**Example:**

.. code-block:: json

   {
     "steps": [
       {
         "type": "Charge",
         "C_rate": 1,
         "termination": "4.2 V"
       },
       {
         "type": "Rest",
         "duration": "1 hour"
       },
       {
         "type": "Discharge",
         "C_rate": 1,
         "termination": "2.5 V"
       }
     ],
     "cycles": 100
   }

Image Files
-----------

Plot Export
~~~~~~~~~~~

PyBaMM plots can be exported in various formats.

**Example:**

.. code-block:: python

   import pybamm
   
   # Run simulation
   sim = pybamm.Simulation(pybamm.lithium_ion.SPM())
   sim.solve([0, 3600])
   
   # Create plot
   quick_plot = pybamm.QuickPlot(sim)
   
   # Save as PNG
   quick_plot.fig.savefig("simulation_plot.png", dpi=300)
   
   # Save as PDF (vector graphics)
   quick_plot.fig.savefig("simulation_plot.pdf")
   
   # Save as SVG
   quick_plot.fig.savefig("simulation_plot.svg")

**Supported formats:**

- PNG: Raster graphics, good for presentations
- PDF: Vector graphics, good for publications
- SVG: Vector graphics, good for web
- EPS: Vector graphics, required by some journals

Animation Files
~~~~~~~~~~~~~~~

Dynamic plots can be exported as animations.

**Example:**

.. code-block:: python

   import pybamm
   
   # Run simulation
   sim = pybamm.Simulation(pybamm.lithium_ion.SPM())
   sim.solve([0, 3600])
   
   # Create dynamic plot
   pybamm.dynamic_plot(sim, ["Voltage [V]"])
   
   # Save as GIF
   # (requires additional setup)

**Formats:**

- GIF: Simple animations
- MP4: Video format
- AVI: Video format

Best Practices
--------------

File Organization
~~~~~~~~~~~~~~~~~

Recommended directory structure:

.. code-block:: text

   project/
   ├── data/
   │   ├── parameters/
   │   │   ├── cell_parameters.csv
   │   │   └── material_properties.json
   │   ├── experiments/
   │   │   ├── discharge_data.csv
   │   │   └── drive_cycle.csv
   │   └── ocps/
   │       ├── graphite_ocp.csv
   │       └── nmc_ocp.csv
   ├── models/
   │   └── custom_model.py
   ├── results/
   │   ├── solutions/
   │   ├── plots/
   │   └── exports/
   └── scripts/
       └── run_simulation.py

Naming Conventions
~~~~~~~~~~~~~~~~~~

**Parameters:**

- Use descriptive names with units: ``negative_particle_radius_m.csv``
- Include chemistry: ``graphite_nmc_parameters.json``
- Version control: ``params_v1.0.csv``

**Results:**

- Include timestamp: ``results_20240115_143022.pkl``
- Describe conditions: ``discharge_1C_25degC.csv``
- Use consistent naming: ``sim_{chemistry}_{condition}.pkl``

Documentation
~~~~~~~~~~~~~

Include metadata in files:

**CSV:**

.. code-block:: text

   # Battery parameters for LG M50 cell
   # Chemistry: Graphite-NMC622
   # Source: Chen et al. (2020)
   # Date: 2024-01-15
   Name,Value,Units

**JSON:**

.. code-block:: json

   {
     "_metadata": {
       "cell": "LG M50",
       "chemistry": "Graphite-NMC622",
       "source": "Chen et al. (2020)",
       "date": "2024-01-15"
     },
     "parameters": {
       ...
     }
   }

Version Control
~~~~~~~~~~~~~~~

**Track parameter changes:**

- Use git for version control
- Include parameter files in repository
- Document changes in commit messages
- Tag releases with version numbers

**Example:**

.. code-block:: bash

   git add data/parameters/cell_v2.csv
   git commit -m "Update negative electrode thickness from 85 to 88 μm"
   git tag -a v2.0 -m "Parameter set version 2.0"

See Also
--------

- :ref:`parameter_reference` for parameter descriptions
- :ref:`tutorial_importing_data` for data import examples
- :ref:`api_io` for API documentation on I/O functions
