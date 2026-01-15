# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OSOAA (Ocean Successive Orders with Atmosphere - Advanced) is a vector radiative transfer model for coupled atmosphere-ocean systems. It computes radiance and polarization using the successive orders of scattering method, supporting rough sea surface modeling via Cox & Munk.

## Build Commands

### Fortran Core (computational engine)

```bash
# Set required environment variable
export OSOAA_ROOT=/path/to/OSOAA

# Copy appropriate makefile and build
cp gen/Makefile_OSOAA.gfortran Makefile
make all
# Produces: exe/OSOAA_MAIN.exe
```

For debug builds, edit the Makefile and uncomment `DEBUG = -g`.

### Java GUI

```bash
cd ihm/gen
ant all              # Full build with distribution
ant compile          # Compilation only
ant clean            # Clean build artifacts
ant unit-tests       # Run unit tests (Linux only, requires tests/conf)
```

### Documentation (Sphinx)

```bash
cd docs
make html            # Build HTML docs to _build/html/
make pdf             # Build PDF
```

## Architecture

### Three-Layer Design

1. **Fortran Core** (`src/`): 12 modules implementing the radiative transfer solver
2. **Java GUI** (`ihm/`): Swing-based interface for parameter configuration
3. **Documentation** (`docs/`): Sphinx-based user and scientific documentation

### Fortran Module Hierarchy

```
OSOAA_MAIN.F           Entry point, orchestrates simulation
├── OSOAA_ANGLES.F     Angular grid (Gauss-Legendre discretization)
├── OSOAA_PROFILE.F    Vertical structure of atmosphere/ocean
│   ├── OSOAA_AEROSOLS.F    Aerosol optical properties
│   │   ├── OSOAA_MIE.F          Mie scattering calculations
│   │   └── OSOAA_PARTICLES_RAD.F Size distributions
│   └── OSOAA_HYDROSOLS.F   Ocean particle properties
├── OSOAA_SURFACE.F    Sea surface boundary conditions
│   └── OSOAA_SURF_MATRICES.F Mueller matrices for surface
└── OSOAA_SOS.F        Successive orders method driver
    ├── OSOAA_SOS_CORE.F     Core RT equation solver
    └── OSOAA_TRPHI.F        Stokes vector transformations
```

### Key Algorithm: Successive Orders of Scattering

The solver decomposes total radiance as I_total = Σ I^(n):
- Order 0: Direct transmission (Beer-Lambert)
- Order n≥1: Multiple scattering contributions
- Fourier decomposition in azimuth angle
- Iterates until convergence (|I^(n) - I^(n-1)| < ε)

### Java GUI Architecture (`ihm/src/osoaa/`)

- **DAL** (Data Access Layer): File I/O and preferences
- **BLL** (Business Logic Layer): Parameter management and validation
- **USL** (User Interface Layer): Swing forms and panels
- Entry point: `osoaa.Launcher` → `MainJFrame`

### Constants and Configuration

All physical constants and array limits are defined in `inc/OSOAA.h`:
- `CTE_DEFAULT_IGMAX`: Maximum scattering orders (100)
- `CTE_WAMIN`: Minimum wavelength (0.299 nm)
- `CTE_MDF_AIR/SEA`: Depolarization factors

## Code Conventions

- **Fortran variables**: UPPERCASE (THETA, PHI, WAVELENGTH)
- **Constants**: `CTE_` prefix
- **Subroutines**: Descriptive names (e.g., `ANGLES_GAUSS_LEGENDRE`, `AEROSOLS_MONO_MODAL`)

## Output Files

Logs are written to working directory:
- `LOG_OSOAA.txt`: Main simulation log
- `AER_LOG.txt`: Aerosol calculations
- `SEA_LOG.txt`: Sea surface calculations

## Reference

Chami M, Lafrance B, Fougnie B, Chowdhary J, Harmel T, Waquet F (2015), "OSOAA: a vector radiative transfer model of coupled atmosphere-ocean system for a rough sea surface application to the estimates of the directional variations of the water leaving reflectance to better process multi-angular satellite sensors data over the ocean", Opt Express 23: 27829-27852, doi: 10.1364/OE.23.027829
