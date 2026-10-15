# P-WAVES control software

This repository contains the Python control software used with the **Portable Water-vapor Analyzer Verification and Evaluation System (P-WAVES)** described in the associated manuscript:

**Portable system for characterizing greenhouse gas analyzers for sensitivity to water vapor**

The repository is intended to document the software used to operate the P-WAVES hardware during the experiments described in the manuscript and reviewer-response testing.

## Included source code

### Aeris

`aeris/Aeris_humidity_step_V2a_nobufferlag(20261015-184321).py`

This is the P-WAVES controller used with the Aeris MIRA Ultra analyzers. The script:

- controls the wet- and dry-stream mass-flow-controller setpoints through a Pi-Plates DAQC2;
- controls the calibration-gas and wet-stream shunt valves;
- calculates the commanded wet/dry mixing ratio from bath temperature and the requested H2O target;
- reads the Aeris serial data stream and records the most recent available observation to minimize serial-buffer lag;
- writes run metadata and analyzer observations to `humidity_step_aeris_YYYYMMDD_HHMMSS.csv`.

### Picarro

`picarro/Picarro_CFKADS2025_humidity_step_V2b (1)(1).py`

This is the representative P-WAVES controller used with Picarro CFKADS2025. The script uses the same P-WAVES wet/dry flow-control approach and queries the Picarro analyzer through its serial interface, writing results to `humidity_step_picarro_YYYYMMDD_HHMMSS.csv`.

Separate Picarro programs were used for individual Picarro instruments because their instrument communication/configuration details were not identical. The CFKADS2025 implementation is provided here as the representative Picarro P-WAVES control program.

## Source-code preservation

The two Python source files in this repository are archived **exactly as used**. They were not refactored, reformatted, cleaned up, or otherwise modified for public release.

SHA-256 checksums are provided in `SOURCE_CODE_SHA256.txt` so the archived source can be verified byte-for-byte.

## Hardware/software context

The scripts were developed for the P-WAVES hardware configuration described in the manuscript. They require:

- Python 3
- Raspberry Pi
- Pi-Plates DAQC2 hardware and Python library
- `pyserial`
- wet-stream MFC: 200 sccm full scale
- dry-stream MFC: 500 sccm full scale
- analyzer serial connection at `/dev/ttyUSB0` in the tested configuration

The Pi-Plates Python package can be installed as `Pi-Plates`; serial communication uses `pyserial`.

These scripts directly control valves and analog MFC commands. Anyone adapting them to another system should verify DAQC2 channel assignments, MFC scaling, valve logic, serial configuration, and flow limits before operating hardware.

## Important interpretation of logged values

`Wet_sccm`, `Dry_sccm`, and `Target_ppm` are **commanded/calculated values**, not independent MFC readbacks or reference-hygrometer measurements.

The target H2O value is calculated from the entered water-bath temperature, an assumed atmospheric pressure of 101.325 kPa, and the commanded wet/dry flow ratio. The measured H2O field written to each output file comes from the analyzer itself and was used in the scientific analysis.

Accordingly, the control code and logged target values should not be interpreted as an independent determination of absolute water-vapor accuracy.

## Typical operation

At program start, the user is prompted for parameters including:

- run mode;
- instrument serial number;
- pre-dry duration;
- total flow;
- number and duration of humidity steps;
- water-bath temperature;
- starting and ending H2O targets.

The program then performs the requested stepped-humidity sequence and logs approximately 1-Hz analyzer data together with the commanded flow settings and run metadata.

The scripts represent the tested research configuration rather than a generalized software package.

## Dependencies

See `requirements.txt`.

## Citation

Please cite the associated P-WAVES manuscript when using or referring to this software. The repository citation can be updated with the final journal citation/DOI after publication.
