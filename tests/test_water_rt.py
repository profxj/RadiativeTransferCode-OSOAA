"""
Test module for OSOAA water-leaving radiance simulations.

Based on the OSOAA_Water_Leaving_Radiance_Tutorial.ipynb notebook.
Tests the Python wrapper for OSOAA radiative transfer simulations.
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
    - Parsing of output files
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
                           wind_speed: float = 5.0) -> Dict:
        """
        Generate default simulation parameters.

        Parameters
        ----------
        wavelength_nm : float
            Simulation wavelength in nm (will be converted to micrometers)
        solar_zenith : float
            Solar zenith angle in degrees (0-90)
        chlorophyll : float
            Chlorophyll-a concentration in mg/m³
        aot : float
            Aerosol optical thickness at reference wavelength
        wind_speed : float
            Wind speed in m/s for sea surface roughness
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

            # Sea profile
            'SEA.Depth': 100.0,            # Ocean depth (m)

            # Hydrosol model - Junge phytoplankton (Model 1)
            'HYD.DirMie': str(self.mie_hyd_dir),
            'HYD.Model': 1,                # 1 = Use phytoplankton Junge model
            'PHYTO.Chl': chlorophyll,      # Chlorophyll concentration (mg/m³)
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

        Returns dictionary with parsed results.
        """
        # Build command
        cmd = self.build_command(params)

        if verbose:
            wl_nm = params.get('OSOAA.Wa', 0) * 1000
            print(f"Running OSOAA simulation...")
            print(f"  Wavelength: {wl_nm:.1f} nm")
            print(f"  Chlorophyll: {params.get('PHYTO.Chl', 'N/A')} mg/m³")
            print(f"  Solar zenith: {params.get('ANG.Thetas', 'N/A')}°")
            print(f"  AOT: {params.get('AER.AOTref', 'N/A')}")

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

        # Output files are in Standard_outputs subdirectory
        output_dir = self.work_dir / 'Standard_outputs'

        # Parse LUM_vsVZA.txt (radiance vs viewing zenith angle)
        vza_filename = params.get('OSOAA.ResFile.vsVZA', 'LUM_vsVZA.txt')
        vza_file = output_dir / vza_filename

        if vza_file.exists():
            results['vza_data'] = self._parse_vza_file(vza_file)
            results['output_file'] = str(vza_file)

        return results

    def _parse_vza_file(self, filepath: Path) -> Dict:
        """
        Parse LUM_vsVZA.txt output file.

        Output columns:
        1: VZA - Viewing Zenith Angle (degrees)
        2: SCA_ANG - Scattering angle (degrees)
        3: I - Stokes I, normalized radiance (pi*L/Esun)
        4: REFL - Reflectance (pi*L/Ed)
        5: POL_RATE - Degree of polarization (%)
        6: LPOL - Polarized intensity
        7: REFL_POL - Polarized reflectance
        """
        # Read file and find data start (skip header lines)
        with open(filepath, 'r') as f:
            lines = f.readlines()

        # Find the line with column headers
        data_start = 0
        for i, line in enumerate(lines):
            if line.strip().startswith('VZA') and 'SCA_ANG' in line:
                data_start = i + 1
                break

        # Load data
        data = np.loadtxt(filepath, skiprows=data_start)

        return {
            'vza': data[:, 0],              # Viewing Zenith Angle (degrees)
            'scattering_angle': data[:, 1], # Scattering angle (degrees)
            'I': data[:, 2],                # Normalized radiance (pi*L/Esun)
            'reflectance': data[:, 3],      # Reflectance (pi*L/Ed)
            'DoLP': data[:, 4],             # Degree of polarization (%)
            'I_pol': data[:, 5],            # Polarized intensity
            'refl_pol': data[:, 6],         # Polarized reflectance
        }

    def cleanup(self):
        """Remove temporary working directory."""
        if self.work_dir.exists():
            shutil.rmtree(self.work_dir, ignore_errors=True)


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
# Test: Basic Simulation (Clear Water at 550 nm)
# ---------------------------------------------------------------------------

class TestBasicSimulation:
    """Test basic OSOAA simulation functionality."""

    def test_clear_water_550nm(self, simulation):
        """
        Run a simple simulation for clear ocean water (low chlorophyll) at 550 nm.

        This corresponds to notebook cell 6-7: first OSOAA simulation.
        """
        params = simulation.get_default_params(
            wavelength_nm=550.0,   # Green light (nm)
            solar_zenith=30.0,     # Sun at 30° from zenith
            chlorophyll=0.1,       # Clear oligotrophic water (mg/m³)
            aot=0.1,               # Low aerosol loading
            wind_speed=5.0         # Moderate sea surface (m/s)
        )

        results = simulation.run(params)

        # Verify output was generated
        assert 'vza_data' in results, "VZA data should be present in results"

        vza_data = results['vza_data']
        vza = vza_data['vza']
        I = vza_data['I']

        # Check VZA range (should span -90 to +90 degrees approximately)
        assert vza.min() < -80, f"VZA min should be < -80, got {vza.min()}"
        assert vza.max() > 80, f"VZA max should be > 80, got {vza.max()}"

        # Check radiance values are physically reasonable (positive, not too large)
        assert np.all(I > 0), "Radiance should be positive"
        assert np.all(I < 1.0), "Normalized radiance should be < 1.0"

        # Check nadir value (VZA closest to 0)
        nadir_idx = np.argmin(np.abs(vza))
        nadir_radiance = I[nadir_idx]

        # Expected nadir radiance for clear water at 550nm is around 0.006
        assert 0.001 < nadir_radiance < 0.05, \
            f"Nadir radiance {nadir_radiance} outside expected range for clear water"

    def test_output_file_columns(self, simulation):
        """Verify all expected output columns are present."""
        params = simulation.get_default_params(wavelength_nm=550.0)
        results = simulation.run(params)

        vza_data = results['vza_data']

        expected_columns = ['vza', 'scattering_angle', 'I', 'reflectance',
                           'DoLP', 'I_pol', 'refl_pol']

        for col in expected_columns:
            assert col in vza_data, f"Missing column: {col}"
            assert len(vza_data[col]) > 0, f"Column {col} is empty"


# ---------------------------------------------------------------------------
# Test: Chlorophyll Concentration Series
# ---------------------------------------------------------------------------

class TestChlorophyllSeries:
    """Test effect of chlorophyll concentration on water-leaving radiance."""

    @pytest.mark.parametrize("chlorophyll", [0.03, 0.1, 0.3, 1.0, 3.0])
    def test_chlorophyll_values(self, simulation, chlorophyll):
        """
        Test simulations across chlorophyll concentration range.

        This corresponds to notebook cell 11: chlorophyll series.
        Covers ultra-oligotrophic (0.03) to eutrophic (3.0) waters.
        """
        params = simulation.get_default_params(
            wavelength_nm=550.0,
            solar_zenith=30.0,
            chlorophyll=chlorophyll,
            aot=0.1,
            wind_speed=5.0
        )
        params['OSOAA.ResFile.vsVZA'] = f'LUM_vsVZA_chl{chlorophyll}.txt'

        results = simulation.run(params)

        assert 'vza_data' in results
        I = results['vza_data']['I']

        # All radiance values should be positive
        assert np.all(I > 0), f"Negative radiance found for Chl={chlorophyll}"

    def test_chlorophyll_trend(self, simulation):
        """
        Verify that increasing chlorophyll affects radiance at 550nm.

        At green wavelengths, higher chlorophyll generally increases
        backscattering and thus water-leaving radiance (up to a point).
        """
        chl_values = [0.1, 1.0, 3.0]
        nadir_radiances = []

        for chl in chl_values:
            params = simulation.get_default_params(
                wavelength_nm=550.0,
                chlorophyll=chl
            )
            params['OSOAA.ResFile.vsVZA'] = f'LUM_vsVZA_trend_chl{chl}.txt'

            results = simulation.run(params)
            vza = results['vza_data']['vza']
            I = results['vza_data']['I']

            nadir_idx = np.argmin(np.abs(vza))
            nadir_radiances.append(I[nadir_idx])

        # Higher chlorophyll should produce different radiance values
        # (the relationship is complex, but values should not be identical)
        assert len(set(np.round(nadir_radiances, 6))) > 1, \
            "Radiance should vary with chlorophyll concentration"


# ---------------------------------------------------------------------------
# Test: Spectral Simulations
# ---------------------------------------------------------------------------

class TestSpectralSimulations:
    """Test simulations across visible wavelength spectrum."""

    @pytest.mark.parametrize("wavelength_nm", [443, 490, 510, 555, 670])
    def test_wavelength_bands(self, simulation, wavelength_nm):
        """
        Test simulations at common ocean color wavelength bands.

        This corresponds to notebook cell 14: spectral simulations.
        """
        params = simulation.get_default_params(
            wavelength_nm=float(wavelength_nm),
            solar_zenith=30.0,
            chlorophyll=0.3,  # Moderate chlorophyll
            aot=0.1,
            wind_speed=5.0
        )
        params['OSOAA.ResFile.vsVZA'] = f'LUM_vsVZA_wl{wavelength_nm}.txt'

        results = simulation.run(params)

        assert 'vza_data' in results, f"No output for wavelength {wavelength_nm}nm"

        I = results['vza_data']['I']
        assert np.all(I > 0), f"Negative radiance at {wavelength_nm}nm"
        assert np.all(I < 1.0), f"Unrealistic radiance at {wavelength_nm}nm"

    def test_spectral_shape(self, simulation):
        """
        Verify spectral variation in water-leaving radiance.

        For moderate chlorophyll water, radiance should vary with wavelength
        (typically higher in green, lower in blue due to absorption).
        """
        wavelengths = [443, 555, 670]
        nadir_radiances = {}

        for wl in wavelengths:
            params = simulation.get_default_params(
                wavelength_nm=float(wl),
                chlorophyll=0.3
            )
            params['OSOAA.ResFile.vsVZA'] = f'LUM_vsVZA_spectral_{wl}.txt'

            results = simulation.run(params)
            vza = results['vza_data']['vza']
            I = results['vza_data']['I']

            nadir_idx = np.argmin(np.abs(vza))
            nadir_radiances[wl] = I[nadir_idx]

        # Verify spectral variation exists
        values = list(nadir_radiances.values())
        assert max(values) != min(values), \
            "Radiance should vary across wavelengths"


# ---------------------------------------------------------------------------
# Test: Polarization Output
# ---------------------------------------------------------------------------

class TestPolarization:
    """Test polarization output from OSOAA simulations."""

    def test_polarization_output(self, simulation):
        """
        Verify polarization quantities are computed.

        This corresponds to notebook cell 17: polarization analysis.
        """
        params = simulation.get_default_params(wavelength_nm=550.0)
        results = simulation.run(params)

        vza_data = results['vza_data']

        # Check polarization columns exist
        assert 'DoLP' in vza_data, "Degree of Linear Polarization missing"
        assert 'I_pol' in vza_data, "Polarized intensity missing"

        DoLP = vza_data['DoLP']
        I_pol = vza_data['I_pol']

        # DoLP should be between 0 and 100 (percentage)
        assert np.all(DoLP >= 0), "DoLP should be non-negative"
        assert np.all(DoLP <= 100), "DoLP should be <= 100%"

        # Polarized intensity should be non-negative
        assert np.all(I_pol >= 0), "Polarized intensity should be non-negative"

    def test_polarization_relation(self, simulation):
        """
        Verify relationship between total and polarized radiance.

        Polarized intensity should always be <= total intensity.
        """
        params = simulation.get_default_params(wavelength_nm=550.0)
        results = simulation.run(params)

        vza_data = results['vza_data']
        I = vza_data['I']
        I_pol = vza_data['I_pol']

        # Polarized component should not exceed total
        assert np.all(I_pol <= I + 1e-10), \
            "Polarized intensity should not exceed total intensity"


# ---------------------------------------------------------------------------
# Test: Parameter Validation
# ---------------------------------------------------------------------------

class TestParameterValidation:
    """Test simulation parameter handling."""

    def test_default_params_structure(self, simulation):
        """Verify default parameters contain all required keys."""
        params = simulation.get_default_params()

        required_keys = [
            'OSOAA.ResRoot', 'OSOAA.Wa', 'ANG.Thetas',
            'AER.AOTref', 'PHYTO.Chl', 'SEA.Wind'
        ]

        for key in required_keys:
            assert key in params, f"Missing required parameter: {key}"

    def test_wavelength_conversion(self, simulation):
        """Verify wavelength is correctly converted from nm to micrometers."""
        params = simulation.get_default_params(wavelength_nm=550.0)

        # Internal wavelength should be in micrometers
        assert params['OSOAA.Wa'] == 0.55, \
            f"Wavelength conversion error: expected 0.55, got {params['OSOAA.Wa']}"

    def test_different_solar_angles(self, simulation):
        """Test simulations with different solar zenith angles."""
        for sza in [0.0, 30.0, 60.0]:
            params = simulation.get_default_params(
                wavelength_nm=550.0,
                solar_zenith=sza
            )
            params['OSOAA.ResFile.vsVZA'] = f'LUM_vsVZA_sza{sza}.txt'

            results = simulation.run(params)
            assert 'vza_data' in results, f"Failed for SZA={sza}"

    def test_different_wind_speeds(self, simulation):
        """Test simulations with different wind speeds."""
        for wind in [1.0, 5.0, 10.0]:
            params = simulation.get_default_params(
                wavelength_nm=550.0,
                wind_speed=wind
            )
            params['OSOAA.ResFile.vsVZA'] = f'LUM_vsVZA_wind{wind}.txt'

            results = simulation.run(params)
            assert 'vza_data' in results, f"Failed for wind={wind}m/s"


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
# Integration Test: Full Workflow
# ---------------------------------------------------------------------------

class TestIntegration:
    """Integration tests for complete simulation workflows."""

    def test_full_simulation_workflow(self, simulation):
        """
        Test complete simulation workflow from setup to result parsing.

        This mimics the notebook's main workflow.
        """
        # Setup parameters
        params = simulation.get_default_params(
            wavelength_nm=550.0,
            solar_zenith=30.0,
            chlorophyll=0.1,
            aot=0.1,
            wind_speed=5.0
        )

        # Run simulation
        results = simulation.run(params)

        # Verify results structure
        assert 'params' in results
        assert 'vza_data' in results
        assert 'output_file' in results

        # Verify output file exists
        assert Path(results['output_file']).exists()

        # Verify data arrays have consistent lengths
        vza_data = results['vza_data']
        n_points = len(vza_data['vza'])

        for key, arr in vza_data.items():
            assert len(arr) == n_points, \
                f"Inconsistent array length for {key}: {len(arr)} vs {n_points}"

    def test_multiple_sequential_runs(self, simulation):
        """Test running multiple simulations sequentially."""
        configs = [
            {'wavelength_nm': 443, 'chlorophyll': 0.1},
            {'wavelength_nm': 555, 'chlorophyll': 0.5},
            {'wavelength_nm': 670, 'chlorophyll': 1.0},
        ]

        all_results = []
        for i, config in enumerate(configs):
            params = simulation.get_default_params(**config)
            params['OSOAA.ResFile.vsVZA'] = f'LUM_vsVZA_seq_{i}.txt'

            results = simulation.run(params)
            all_results.append(results)

        assert len(all_results) == 3
        for results in all_results:
            assert 'vza_data' in results


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
