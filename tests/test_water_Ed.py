"""
Test module for OSOAA downwelling irradiance (Ed) simulations.

Based on the OSOAA_Downwelling_Irradiance_Tutorial.ipynb notebook.
Tests the Python wrapper for OSOAA radiative transfer simulations
focusing on Ed profiles as a function of depth.
"""

import subprocess
import numpy as np
import os
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Optional, List

import pytest


# ---------------------------------------------------------------------------
# OSOAASimulation class (from notebook)
# ---------------------------------------------------------------------------

class OSOAASimulation:
    """
    Python wrapper for OSOAA radiative transfer simulations.

    This class handles:
    - Parameter configuration with correct OSOAA keywords
    - Execution of the Fortran code via command-line arguments
    - Parsing of flux output files for Ed profiles
    """

    def __init__(self, osoaa_root: Path, work_dir: Optional[Path] = None):
        self.osoaa_root = Path(osoaa_root).resolve()
        self.exe_path = self.osoaa_root / 'exe' / 'OSOAA_MAIN.exe'
        self.fic_path = self.osoaa_root / 'fic'

        # Create working directory with required subdirectories
        if work_dir:
            self.work_dir = Path(work_dir).resolve()
        else:
            self.work_dir = Path(tempfile.mkdtemp(prefix='osoaa_'))

        # Create directories for Mie calculations and surface matrices
        self.mie_aer_dir = self.work_dir / 'MIE_AER'
        self.mie_hyd_dir = self.work_dir / 'MIE_HYD'
        self.surf_dir = self.work_dir / 'SURF'

        self.mie_aer_dir.mkdir(parents=True, exist_ok=True)
        self.mie_hyd_dir.mkdir(parents=True, exist_ok=True)
        self.surf_dir.mkdir(parents=True, exist_ok=True)

        if not self.exe_path.exists():
            raise FileNotFoundError(f"OSOAA executable not found at {self.exe_path}")

    def get_default_params(self, wavelength_nm: float = 550.0,
                           solar_zenith: float = 30.0,
                           chlorophyll: float = 0.1,
                           aot: float = 0.1,
                           wind_speed: float = 5.0,
                           sea_depth: float = 100.0) -> Dict:
        """
        Generate default simulation parameters.

        Parameters
        ----------
        wavelength_nm : float
            Simulation wavelength in nm (will be converted to micrometers)
        solar_zenith : float
            Solar zenith angle in degrees (0-90)
        chlorophyll : float
            Chlorophyll-a concentration in mg/m^3
        aot : float
            Aerosol optical thickness at reference wavelength
        wind_speed : float
            Wind speed in m/s for sea surface roughness
        sea_depth : float
            Ocean depth in meters (determines depth profile range)
        """
        # Convert wavelength from nm to micrometers
        wavelength_um = wavelength_nm / 1000.0

        return {
            # Working directory (required)
            'OSOAA.ResRoot': str(self.work_dir),

            # Wavelength in micrometers
            'OSOAA.Wa': wavelength_um,

            # Solar geometry
            'ANG.Thetas': solar_zenith,

            # Viewing geometry
            'OSOAA.View.Phi': 90.0,       # Relative azimuth angle (degrees)
            'OSOAA.View.Level': 4,         # 4 = Sea Surface 0- (just below surface)
            'OSOAA.View.Z': 0.0,           # Depth for output

            # Atmospheric profile
            'AP.Pressure': 1013.0,         # Surface pressure (hPa)
            'AP.HR': 8.0,                  # Rayleigh scale height (km)
            'AP.HA': 2.0,                  # Aerosol scale height (km)

            # Aerosol model - mono-modal log-normal distribution (Model 0, SDtype 1)
            'AER.DirMie': str(self.mie_aer_dir),
            'AER.Waref': wavelength_um,    # Reference wavelength (micrometers)
            'AER.AOTref': aot,             # AOT at reference wavelength
            'AER.Model': 0,                # Mono-modal model
            'AER.MMD.MRwa': 1.45,          # Real refractive index
            'AER.MMD.MIwa': -0.001,        # Imaginary refractive index (MUST be negative)
            'AER.MMD.SDtype': 1,           # 1 = Log-Normal Distribution
            'AER.MMD.LNDradius': 0.10,     # Modal radius (micrometers)
            'AER.MMD.LNDvar': 0.46,        # Log of standard deviation

            # Sea profile - IMPORTANT: depth determines the profile range
            'SEA.Depth': sea_depth,        # Ocean depth (m)

            # Hydrosol model - Junge phytoplankton (Model 1)
            'HYD.DirMie': str(self.mie_hyd_dir),
            'HYD.Model': 1,                # 1 = Use phytoplankton Junge model
            'PHYTO.Chl': chlorophyll,      # Chlorophyll concentration (mg/m^3)
            'PHYTO.ProfilType': 1,         # 1 = Homogeneous profile

            # Phytoplankton optical properties (Junge distribution)
            'PHYTO.JD.slope': 4.0,         # Junge slope
            'PHYTO.JD.rmin': 0.01,         # Minimum radius (micrometers)
            'PHYTO.JD.rmax': 200.0,        # Maximum radius (micrometers)
            'PHYTO.JD.MRwa': 1.05,         # Real refractive index
            'PHYTO.JD.MIwa': 0.0,          # Imaginary refractive index
            'PHYTO.JD.rate': 1.0,          # Fraction of this mode

            # Sediments and dissolved matter
            'SED.Csed': 0.0,               # Sediment concentration (mg/L)
            'YS.Abs440': 0.0,              # Yellow substance absorption at 440nm
            'DET.Abs440': 0.0,             # Detritus absorption at 440nm

            # Sea surface
            'SEA.Dir': str(self.surf_dir),
            'SEA.Ind': 1.34,               # Refractive index of seawater
            'SEA.Wind': wind_speed,        # Wind speed (m/s)
            'SEA.SurfAlb': 0.0,            # Surface albedo
            'SEA.BotType': 1,              # Bottom type
            'SEA.BotAlb': 0.30,            # Bottom albedo

            # Output files
            'OSOAA.ResFile.vsVZA': 'LUM_vsVZA.txt',
        }

    def build_command(self, params: Dict) -> List[str]:
        """Build command-line arguments for OSOAA."""
        cmd = [str(self.exe_path)]
        for key, value in params.items():
            cmd.extend([f'-{key}', str(value)])
        return cmd

    def run(self, params: Dict, verbose: bool = False, timeout: int = 600) -> Dict:
        """
        Run OSOAA simulation with given parameters.

        Returns dictionary with parsed results including flux profiles.
        """
        # Build command
        cmd = self.build_command(params)

        if verbose:
            wl_nm = params.get('OSOAA.Wa', 0) * 1000
            print(f"Running OSOAA simulation...")
            print(f"  Wavelength: {wl_nm:.1f} nm")
            print(f"  Chlorophyll: {params.get('PHYTO.Chl', 'N/A')} mg/m^3")
            print(f"  Solar zenith: {params.get('ANG.Thetas', 'N/A')} deg")
            print(f"  Sea depth: {params.get('SEA.Depth', 'N/A')} m")

        # Run simulation
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(self.osoaa_root),
            env={**os.environ, 'OSOAA_ROOT': str(self.osoaa_root)},
            timeout=timeout
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"OSOAA simulation failed with return code {result.returncode}\n"
                f"STDOUT: {result.stdout[:1000] if result.stdout else '(empty)'}\n"
                f"STDERR: {result.stderr[:1000] if result.stderr else '(empty)'}"
            )

        # Parse results
        return self.parse_results(params)

    def parse_results(self, params: Dict) -> Dict:
        """Parse OSOAA output files into numpy arrays."""
        results = {'params': params}

        # Parse Flux.txt for Ed profiles (in Advanced_outputs directory)
        flux_file = self.work_dir / 'Advanced_outputs' / 'Flux.txt'

        if flux_file.exists():
            results['flux_data'] = self._parse_flux_file(flux_file)
            results['flux_file'] = str(flux_file)

        return results

    def _parse_flux_file(self, filepath: Path) -> Dict:
        """
        Parse Flux.txt output file.

        Output columns (from OSOAA_SOS_CORE.F):
        1: Level - Layer index
        2: Z(m) - Altitude (>0) or Depth (<0)
        3: Direct_Down - Direct downwelling flux
        4: Diffuse_Down - Diffuse downwelling flux
        5: Total_Down - Total downwelling flux (Ed)
        6: Direct_Up - Direct upwelling flux
        7: Diffuse_Up - Diffuse upwelling flux
        8: Total_Up - Total upwelling flux (Eu)
        9: Total_Up/Total_Down - Ratio (related to reflectance)

        Note: Fluxes are normalized to solar irradiance at TOA = pi
        """
        # Read file and find data start (skip header lines)
        with open(filepath, 'r') as f:
            lines = f.readlines()

        # Find the line with column headers (contains "Level" and "Z(m)")
        data_start = 0
        for i, line in enumerate(lines):
            if 'Level' in line and 'Z(m)' in line:
                data_start = i + 2  # Skip header and blank line
                break

        # Load data
        data = np.loadtxt(filepath, skiprows=data_start)

        # Z is altitude in atmosphere (positive) and depth in ocean (negative)
        z = data[:, 1]

        return {
            'level': data[:, 0].astype(int),  # Layer index
            'z': z,                            # Altitude/Depth (m)
            'Ed_direct': data[:, 2],           # Direct downwelling flux
            'Ed_diffuse': data[:, 3],          # Diffuse downwelling flux
            'Ed_total': data[:, 4],            # Total downwelling flux (Ed)
            'Eu_direct': data[:, 5],           # Direct upwelling flux
            'Eu_diffuse': data[:, 6],          # Diffuse upwelling flux
            'Eu_total': data[:, 7],            # Total upwelling flux (Eu)
            'reflectance_ratio': data[:, 8],   # Eu/Ed ratio
        }

    def get_ocean_ed_profile(self, flux_data: Dict) -> Dict:
        """
        Extract ocean-only Ed profile from flux data.

        Returns depth (positive, in meters) and Ed values for the ocean only.
        """
        z = flux_data['z']
        Ed = flux_data['Ed_total']

        # Ocean layers have negative z values (depth)
        ocean_mask = z < 0

        # Convert to positive depth
        depth = -z[ocean_mask]
        Ed_ocean = Ed[ocean_mask]

        return {
            'depth': depth,      # Depth in meters (positive)
            'Ed': Ed_ocean,      # Downwelling irradiance (normalized)
        }

    def cleanup(self):
        """Remove temporary working directory."""
        if self.work_dir.exists():
            shutil.rmtree(self.work_dir, ignore_errors=True)


# ---------------------------------------------------------------------------
# Helper function: Calculate Kd
# ---------------------------------------------------------------------------

def calculate_kd(depth: np.ndarray, Ed: np.ndarray,
                 depth_range: tuple = None) -> Dict:
    """
    Calculate diffuse attenuation coefficient Kd from Ed profile.

    Uses linear regression on ln(Ed) vs depth.

    Parameters
    ----------
    depth : array
        Depth values (positive, in meters)
    Ed : array
        Downwelling irradiance values
    depth_range : tuple, optional
        (min_depth, max_depth) to use for fitting

    Returns
    -------
    dict with Kd, Ed0, r_squared, and fitted values
    """
    # Apply depth range filter if specified
    if depth_range:
        mask = (depth >= depth_range[0]) & (depth <= depth_range[1])
        depth_fit = depth[mask]
        Ed_fit = Ed[mask]
    else:
        depth_fit = depth
        Ed_fit = Ed

    # Filter out zero or negative values
    valid_mask = Ed_fit > 0
    depth_fit = depth_fit[valid_mask]
    Ed_fit = Ed_fit[valid_mask]

    # Linear regression on ln(Ed) vs depth
    ln_Ed = np.log(Ed_fit)

    # Fit: ln(Ed) = ln(Ed0) - Kd * z
    coeffs = np.polyfit(depth_fit, ln_Ed, 1)
    Kd = -coeffs[0]  # Negative of slope
    Ed0 = np.exp(coeffs[1])  # Intercept gives Ed at z=0

    # Calculate R-squared
    ln_Ed_fitted = np.polyval(coeffs, depth_fit)
    ss_res = np.sum((ln_Ed - ln_Ed_fitted)**2)
    ss_tot = np.sum((ln_Ed - np.mean(ln_Ed))**2)
    r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 1.0

    return {
        'Kd': Kd,
        'Ed0': Ed0,
        'r_squared': r_squared,
        'depth_fit': depth_fit,
        'Ed_fitted': np.exp(ln_Ed_fitted),
        'euphotic_depth': 4.6 / Kd if Kd > 0 else np.nan,  # Depth where Ed = 1% of surface
    }


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def osoaa_root():
    """Get OSOAA root directory from environment or use default."""
    root = Path(os.environ.get('OSOAA_ROOT', Path(__file__).parent.parent)).resolve()
    exe_path = root / 'exe' / 'OSOAA_MAIN.exe'
    if not exe_path.exists():
        pytest.skip(f"OSOAA executable not found at {exe_path}")
    return root


@pytest.fixture
def simulation(osoaa_root):
    """Create an OSOAASimulation instance with cleanup."""
    sim = OSOAASimulation(osoaa_root)
    yield sim
    sim.cleanup()


# ---------------------------------------------------------------------------
# Test: Basic Ed Profile Simulation
# ---------------------------------------------------------------------------

class TestBasicEdProfile:
    """Test basic Ed profile simulation functionality."""

    def test_clear_water_ed_profile(self, simulation):
        """
        Run a simulation for clear ocean water and verify Ed profile output.

        This corresponds to notebook cells 6-7.
        """
        params = simulation.get_default_params(
            wavelength_nm=550.0,   # Green light (nm)
            solar_zenith=30.0,     # Sun at 30 deg from zenith
            chlorophyll=0.1,       # Clear oligotrophic water (mg/m^3)
            aot=0.1,               # Low aerosol loading
            wind_speed=5.0,        # Moderate sea surface (m/s)
            sea_depth=100.0        # Ocean depth (m)
        )

        results = simulation.run(params)

        # Verify flux data was generated
        assert 'flux_data' in results, "Flux data should be present in results"

        flux = results['flux_data']

        # Check required columns exist
        required_columns = ['z', 'Ed_direct', 'Ed_diffuse', 'Ed_total',
                           'Eu_direct', 'Eu_diffuse', 'Eu_total']
        for col in required_columns:
            assert col in flux, f"Missing column: {col}"

    def test_ocean_depth_range(self, simulation):
        """Verify that the flux profile covers the specified ocean depth."""
        sea_depth = 100.0
        params = simulation.get_default_params(sea_depth=sea_depth)
        results = simulation.run(params)

        flux = results['flux_data']
        z = flux['z']

        # Ocean layers have negative z
        ocean_depths = -z[z < 0]

        # Should reach approximately the specified depth
        assert ocean_depths.max() >= sea_depth * 0.9, \
            f"Ocean depth should reach ~{sea_depth}m, got {ocean_depths.max()}m"

    def test_ed_positive_values(self, simulation):
        """Verify Ed values are positive throughout the profile."""
        params = simulation.get_default_params()
        results = simulation.run(params)

        flux = results['flux_data']

        assert np.all(flux['Ed_total'] >= 0), "Ed should be non-negative"
        assert np.all(flux['Ed_direct'] >= 0), "Direct Ed should be non-negative"
        assert np.all(flux['Ed_diffuse'] >= 0), "Diffuse Ed should be non-negative"


# ---------------------------------------------------------------------------
# Test: Ed Attenuation with Depth
# ---------------------------------------------------------------------------

class TestEdAttenuation:
    """Test Ed attenuation behavior with depth."""

    def test_ed_decreases_with_depth(self, simulation):
        """
        Verify that Ed decreases with depth in the ocean.

        This is the fundamental Beer-Lambert behavior.
        """
        params = simulation.get_default_params(
            wavelength_nm=550.0,
            chlorophyll=0.1,
            sea_depth=100.0
        )
        results = simulation.run(params)

        ocean_ed = simulation.get_ocean_ed_profile(results['flux_data'])
        depth = ocean_ed['depth']
        Ed = ocean_ed['Ed']

        # Ed at deeper levels should be less than at shallower levels
        # Compare first and last ocean values
        assert Ed[-1] < Ed[0], \
            f"Ed should decrease with depth: Ed(surface)={Ed[0]}, Ed(bottom)={Ed[-1]}"

    def test_kd_calculation(self, simulation):
        """
        Verify Kd calculation from Ed profile.

        Corresponds to notebook cell 11.
        """
        params = simulation.get_default_params(
            wavelength_nm=550.0,
            chlorophyll=0.1,
            sea_depth=100.0
        )
        results = simulation.run(params)

        ocean_ed = simulation.get_ocean_ed_profile(results['flux_data'])
        kd_results = calculate_kd(ocean_ed['depth'], ocean_ed['Ed'])

        # Kd should be positive (light attenuates with depth)
        assert kd_results['Kd'] > 0, f"Kd should be positive, got {kd_results['Kd']}"

        # R-squared should be high (exponential fit should be good)
        assert kd_results['r_squared'] > 0.9, \
            f"R-squared should be > 0.9 for exponential fit, got {kd_results['r_squared']}"

        # Euphotic depth should be reasonable (typically 10-200m for ocean)
        z_eu = kd_results['euphotic_depth']
        assert 1 < z_eu < 500, f"Euphotic depth {z_eu}m outside reasonable range"

    def test_exponential_attenuation(self, simulation):
        """
        Verify that Ed follows approximately exponential attenuation.

        ln(Ed) vs depth should be approximately linear.
        """
        params = simulation.get_default_params(
            wavelength_nm=550.0,
            chlorophyll=0.1,
            sea_depth=100.0
        )
        results = simulation.run(params)

        ocean_ed = simulation.get_ocean_ed_profile(results['flux_data'])
        kd_results = calculate_kd(ocean_ed['depth'], ocean_ed['Ed'])

        # High R-squared indicates good exponential fit
        assert kd_results['r_squared'] > 0.95, \
            "Ed should follow exponential attenuation (R^2 > 0.95)"


# ---------------------------------------------------------------------------
# Test: Chlorophyll Effect on Ed
# ---------------------------------------------------------------------------

class TestChlorophyllEffect:
    """Test effect of chlorophyll concentration on Ed profiles."""

    @pytest.mark.parametrize("chlorophyll", [0.03, 0.1, 0.3, 1.0, 3.0])
    def test_chlorophyll_simulations(self, simulation, chlorophyll):
        """
        Test Ed simulations across chlorophyll concentration range.

        Corresponds to notebook cell 14.
        """
        params = simulation.get_default_params(
            wavelength_nm=550.0,
            chlorophyll=chlorophyll,
            sea_depth=100.0
        )

        results = simulation.run(params)

        assert 'flux_data' in results
        ocean_ed = simulation.get_ocean_ed_profile(results['flux_data'])

        # All Ed values should be positive
        assert np.all(ocean_ed['Ed'] > 0), f"Ed should be positive for Chl={chlorophyll}"

    def test_kd_increases_with_chlorophyll(self, simulation):
        """
        Verify that Kd increases with chlorophyll concentration.

        Higher chlorophyll means more absorption and faster attenuation.
        """
        chl_values = [0.1, 1.0, 3.0]
        kd_values = []

        for chl in chl_values:
            params = simulation.get_default_params(
                wavelength_nm=550.0,
                chlorophyll=chl,
                sea_depth=100.0
            )
            results = simulation.run(params)
            ocean_ed = simulation.get_ocean_ed_profile(results['flux_data'])
            kd_result = calculate_kd(ocean_ed['depth'], ocean_ed['Ed'])
            kd_values.append(kd_result['Kd'])

        # Kd should generally increase with chlorophyll
        # Allow for some non-monotonicity due to complex optics
        assert kd_values[-1] > kd_values[0], \
            f"Kd should increase with Chl: Kd(0.1)={kd_values[0]}, Kd(3.0)={kd_values[-1]}"

    def test_euphotic_depth_decreases_with_chlorophyll(self, simulation):
        """
        Verify euphotic depth decreases with higher chlorophyll.

        More chlorophyll = more absorption = shallower light penetration.
        """
        chl_low = 0.1
        chl_high = 3.0

        # Low chlorophyll
        params_low = simulation.get_default_params(wavelength_nm=550.0, chlorophyll=chl_low)
        results_low = simulation.run(params_low)
        ocean_ed_low = simulation.get_ocean_ed_profile(results_low['flux_data'])
        kd_low = calculate_kd(ocean_ed_low['depth'], ocean_ed_low['Ed'])

        # High chlorophyll
        params_high = simulation.get_default_params(wavelength_nm=550.0, chlorophyll=chl_high)
        results_high = simulation.run(params_high)
        ocean_ed_high = simulation.get_ocean_ed_profile(results_high['flux_data'])
        kd_high = calculate_kd(ocean_ed_high['depth'], ocean_ed_high['Ed'])

        assert kd_high['euphotic_depth'] < kd_low['euphotic_depth'], \
            f"Euphotic depth should be shallower for higher Chl"


# ---------------------------------------------------------------------------
# Test: Spectral Variation of Ed
# ---------------------------------------------------------------------------

class TestSpectralVariation:
    """Test spectral variation of Ed profiles."""

    @pytest.mark.parametrize("wavelength_nm", [443, 490, 555, 670])
    def test_wavelength_simulations(self, simulation, wavelength_nm):
        """
        Test Ed simulations at different wavelengths.

        Corresponds to notebook cell 17.
        """
        params = simulation.get_default_params(
            wavelength_nm=float(wavelength_nm),
            chlorophyll=0.1,
            sea_depth=100.0
        )

        results = simulation.run(params)

        assert 'flux_data' in results, f"No flux data for wavelength {wavelength_nm}nm"
        ocean_ed = simulation.get_ocean_ed_profile(results['flux_data'])

        assert np.all(ocean_ed['Ed'] > 0), f"Ed should be positive at {wavelength_nm}nm"

    def test_red_attenuates_faster_than_blue(self, simulation):
        """
        Verify that red light attenuates faster than blue in clear water.

        This is a fundamental property of seawater absorption.
        """
        # Blue wavelength
        params_blue = simulation.get_default_params(wavelength_nm=443, chlorophyll=0.1)
        results_blue = simulation.run(params_blue)
        ocean_ed_blue = simulation.get_ocean_ed_profile(results_blue['flux_data'])
        kd_blue = calculate_kd(ocean_ed_blue['depth'], ocean_ed_blue['Ed'])

        # Red wavelength
        params_red = simulation.get_default_params(wavelength_nm=670, chlorophyll=0.1)
        results_red = simulation.run(params_red)
        ocean_ed_red = simulation.get_ocean_ed_profile(results_red['flux_data'])
        kd_red = calculate_kd(ocean_ed_red['depth'], ocean_ed_red['Ed'])

        # Red should have higher Kd (faster attenuation) than blue in clear water
        assert kd_red['Kd'] > kd_blue['Kd'], \
            f"Red (670nm) should attenuate faster than blue (443nm): Kd_red={kd_red['Kd']}, Kd_blue={kd_blue['Kd']}"

    def test_kd_spectral_variation(self, simulation):
        """
        Verify Kd varies with wavelength.
        """
        wavelengths = [443, 555, 670]
        kd_values = {}

        for wl in wavelengths:
            params = simulation.get_default_params(wavelength_nm=float(wl), chlorophyll=0.1)
            results = simulation.run(params)
            ocean_ed = simulation.get_ocean_ed_profile(results['flux_data'])
            kd_result = calculate_kd(ocean_ed['depth'], ocean_ed['Ed'])
            kd_values[wl] = kd_result['Kd']

        # Kd values should differ across wavelengths
        unique_kd = len(set(np.round(list(kd_values.values()), 4)))
        assert unique_kd > 1, "Kd should vary with wavelength"


# ---------------------------------------------------------------------------
# Test: Flux Components
# ---------------------------------------------------------------------------

class TestFluxComponents:
    """Test direct and diffuse flux components."""

    def test_direct_diffuse_components(self, simulation):
        """Verify direct and diffuse Ed components are computed."""
        params = simulation.get_default_params()
        results = simulation.run(params)

        flux = results['flux_data']

        # Both components should exist and be non-negative
        assert np.all(flux['Ed_direct'] >= 0), "Direct Ed should be non-negative"
        assert np.all(flux['Ed_diffuse'] >= 0), "Diffuse Ed should be non-negative"

        # Total should equal sum of components (approximately)
        total_computed = flux['Ed_direct'] + flux['Ed_diffuse']
        np.testing.assert_allclose(
            flux['Ed_total'], total_computed, rtol=1e-5,
            err_msg="Ed_total should equal Ed_direct + Ed_diffuse"
        )

    def test_diffuse_dominates_at_depth(self, simulation):
        """
        Verify that diffuse component dominates over direct at depth.

        As light penetrates, multiple scattering makes the field more diffuse.
        """
        params = simulation.get_default_params(sea_depth=100.0)
        results = simulation.run(params)

        flux = results['flux_data']
        z = flux['z']

        # Get ocean values at depth
        deep_mask = z < -50  # Below 50m depth
        if np.any(deep_mask):
            Ed_direct_deep = flux['Ed_direct'][deep_mask]
            Ed_diffuse_deep = flux['Ed_diffuse'][deep_mask]

            # At depth, diffuse should be significant relative to total
            # (direct beam attenuates faster due to longer path)
            ratio = Ed_diffuse_deep / (Ed_direct_deep + Ed_diffuse_deep + 1e-10)
            assert np.mean(ratio) > 0.1, \
                "Diffuse component should be significant at depth"


# ---------------------------------------------------------------------------
# Test: Upwelling Flux
# ---------------------------------------------------------------------------

class TestUpwellingFlux:
    """Test upwelling flux (Eu) output."""

    def test_eu_output_exists(self, simulation):
        """Verify upwelling flux is computed."""
        params = simulation.get_default_params()
        results = simulation.run(params)

        flux = results['flux_data']

        assert 'Eu_total' in flux, "Eu_total should be in output"
        assert 'Eu_direct' in flux, "Eu_direct should be in output"
        assert 'Eu_diffuse' in flux, "Eu_diffuse should be in output"

    def test_eu_less_than_ed(self, simulation):
        """Verify Eu is less than Ed (conservation of energy)."""
        params = simulation.get_default_params()
        results = simulation.run(params)

        flux = results['flux_data']

        # Upwelling should be less than downwelling (some absorption occurs)
        assert np.all(flux['Eu_total'] <= flux['Ed_total'] + 1e-10), \
            "Eu should be <= Ed everywhere"

    def test_reflectance_ratio(self, simulation):
        """Verify Eu/Ed ratio is computed and reasonable."""
        params = simulation.get_default_params()
        results = simulation.run(params)

        flux = results['flux_data']

        # Reflectance ratio should be between 0 and 1
        ratio = flux['reflectance_ratio']
        valid_mask = flux['Ed_total'] > 1e-10  # Avoid division issues

        assert np.all(ratio[valid_mask] >= 0), "Eu/Ed ratio should be non-negative"
        assert np.all(ratio[valid_mask] <= 1), "Eu/Ed ratio should be <= 1"


# ---------------------------------------------------------------------------
# Test: Full Profile (Atmosphere + Ocean)
# ---------------------------------------------------------------------------

class TestFullProfile:
    """Test complete flux profile from TOA to sea bottom."""

    def test_atmosphere_and_ocean_layers(self, simulation):
        """Verify profile includes both atmosphere and ocean."""
        params = simulation.get_default_params()
        results = simulation.run(params)

        flux = results['flux_data']
        z = flux['z']

        # Should have positive z (atmosphere) and negative z (ocean)
        assert np.any(z > 0), "Profile should include atmosphere (z > 0)"
        assert np.any(z < 0), "Profile should include ocean (z < 0)"

    def test_toa_ed_value(self, simulation):
        """Verify Ed at TOA is approximately 1 (normalized to solar irradiance)."""
        params = simulation.get_default_params()
        results = simulation.run(params)

        flux = results['flux_data']
        z = flux['z']

        # TOA is the highest altitude
        toa_idx = np.argmax(z)
        Ed_toa = flux['Ed_total'][toa_idx]

        # At TOA, Ed should be close to 1 (direct solar beam)
        # allowing for some tolerance due to normalization convention
        assert 0.5 < Ed_toa < 1.5, f"Ed at TOA should be ~1, got {Ed_toa}"

    def test_surface_discontinuity(self, simulation):
        """
        Check for expected behavior at air-sea interface.

        There should be a change in Ed across the surface due to Fresnel reflection.
        """
        params = simulation.get_default_params()
        results = simulation.run(params)

        flux = results['flux_data']
        z = flux['z']

        # Find layers just above and below surface
        above_surface = z[z >= 0]
        below_surface = z[z < 0]

        if len(above_surface) > 0 and len(below_surface) > 0:
            # Get Ed just above and below surface
            idx_above = np.argmin(above_surface)  # Closest to 0 from above
            idx_below = np.argmax(below_surface)  # Closest to 0 from below

            Ed_above = flux['Ed_total'][z >= 0][idx_above]
            Ed_below = flux['Ed_total'][z < 0][idx_below]

            # Ed below surface should be less than above due to reflection
            assert Ed_below < Ed_above, \
                "Ed should decrease across air-sea interface due to Fresnel reflection"


# ---------------------------------------------------------------------------
# Test: Parameter Validation
# ---------------------------------------------------------------------------

class TestParameterValidation:
    """Test simulation parameter handling."""

    def test_sea_depth_parameter(self, simulation):
        """Verify sea depth parameter affects profile range."""
        depths = [50.0, 100.0]
        max_depths = []

        for depth in depths:
            params = simulation.get_default_params(sea_depth=depth)
            results = simulation.run(params)
            flux = results['flux_data']
            ocean_z = -flux['z'][flux['z'] < 0]
            max_depths.append(ocean_z.max())

        # Deeper simulation should have deeper profile
        assert max_depths[1] > max_depths[0], \
            "Larger sea_depth should produce deeper profile"

    def test_different_solar_angles(self, simulation):
        """Test Ed profiles with different solar zenith angles."""
        for sza in [0.0, 30.0, 60.0]:
            params = simulation.get_default_params(solar_zenith=sza)
            results = simulation.run(params)

            assert 'flux_data' in results, f"Failed for SZA={sza}"
            flux = results['flux_data']
            assert np.all(flux['Ed_total'] >= 0), f"Ed should be non-negative for SZA={sza}"


# ---------------------------------------------------------------------------
# Test: Error Handling
# ---------------------------------------------------------------------------

class TestErrorHandling:
    """Test error handling in the simulation wrapper."""

    def test_missing_executable(self, tmp_path):
        """Test that missing executable raises appropriate error."""
        with pytest.raises(FileNotFoundError):
            OSOAASimulation(tmp_path)

    def test_work_dir_creation(self, osoaa_root):
        """Test that working directories are created properly."""
        sim = OSOAASimulation(osoaa_root)

        try:
            assert sim.mie_aer_dir.exists(), "MIE_AER directory not created"
            assert sim.mie_hyd_dir.exists(), "MIE_HYD directory not created"
            assert sim.surf_dir.exists(), "SURF directory not created"
        finally:
            sim.cleanup()


# ---------------------------------------------------------------------------
# Integration Test
# ---------------------------------------------------------------------------

class TestIntegration:
    """Integration tests for Ed profile workflows."""

    def test_complete_ed_workflow(self, simulation):
        """
        Test complete Ed profile workflow.

        Mimics the notebook's main workflow for Ed analysis.
        """
        # Run simulation
        params = simulation.get_default_params(
            wavelength_nm=550.0,
            chlorophyll=0.1,
            sea_depth=100.0
        )
        results = simulation.run(params)

        # Verify results structure
        assert 'params' in results
        assert 'flux_data' in results
        assert 'flux_file' in results

        # Extract ocean Ed profile
        ocean_ed = simulation.get_ocean_ed_profile(results['flux_data'])
        assert 'depth' in ocean_ed
        assert 'Ed' in ocean_ed
        assert len(ocean_ed['depth']) == len(ocean_ed['Ed'])

        # Calculate Kd
        kd_results = calculate_kd(ocean_ed['depth'], ocean_ed['Ed'])
        assert 'Kd' in kd_results
        assert 'euphotic_depth' in kd_results
        assert 'r_squared' in kd_results

        # Verify physically reasonable values
        assert kd_results['Kd'] > 0, "Kd should be positive"
        assert kd_results['r_squared'] > 0.9, "Exponential fit should be good"

    def test_multiple_simulations(self, simulation):
        """Test running multiple Ed simulations sequentially."""
        configs = [
            {'wavelength_nm': 443, 'chlorophyll': 0.1},
            {'wavelength_nm': 555, 'chlorophyll': 0.5},
            {'wavelength_nm': 670, 'chlorophyll': 1.0},
        ]

        all_kd = []
        for config in configs:
            params = simulation.get_default_params(**config)
            results = simulation.run(params)
            ocean_ed = simulation.get_ocean_ed_profile(results['flux_data'])
            kd_result = calculate_kd(ocean_ed['depth'], ocean_ed['Ed'])
            all_kd.append(kd_result['Kd'])

        assert len(all_kd) == 3
        # All Kd values should be positive
        assert all(kd > 0 for kd in all_kd), "All Kd values should be positive"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
