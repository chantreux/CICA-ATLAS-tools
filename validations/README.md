# Validations

This directory contains tools for validating climate data through various visualization and analysis methods. The validation suite supports multiple plot types and statistical analyses for climate model outputs and observational datasets.

## Overview

The validation tools enable:

- Generation of validation maps (single, triple, multi-model comparisons)
- Time series analysis and visualization
- Climatology calculations for reference periods
- Warming stripes visualizations
- Comparison between model outputs and observations

## Main Scripts

### `generate_plots.py`

Main script for generating validation visualizations. Reads configuration from YAML files and produces various plot types.

**Usage:**
```bash
python generate_plots.py ymls/your_config.yml
```

**Supported Plot Types:**
- `triple_map` - Three-panel comparison maps
- `single_map` - Individual map visualization
- `timeseries` - Time series plots with optional climatology
- `stripes` - Warming stripes visualization

### Core Modules

- **`climatology.py`** - Calculate climatological means for specified periods
- **`maps.py`** - Generate spatial map visualizations
- **`new_maps.py`** - Enhanced map generation with additional features
- **`timeseries.py`** - Time series plotting and analysis
- **`stripes.py`** - Warming stripes visualization
- **`load_files.py`** - Utilities for loading and preprocessing climate data files

### Specialized Scripts

- **`script_maps_CERRA.py`** - Generate validation maps for CERRA datasets
- **`script_maps_multimodel.py`** - Multi-model ensemble map generation
- **`script_CERRA_timeseries.py`** - Time series analysis for CERRA data

## Configuration Files

Configuration files are stored in the `ymls/` directory. Each YAML file specifies:

### Global Settings

```yaml
globals:
  step: 'I'                    # Processing step identifier
  unit: 'mm/day'              # Variable units
  project: 'PROJECT_NAME'      # Project identifier
  start_year: 1990            # Analysis start year
  end_year: 2020              # Analysis end year
  domain_list:                # Geographic domains
    - 'Global'
  experiment: 'historical'    # Experiment name
  model: 'MODEL_NAME'         # Model identifier
  type_of_plot:               # Plot type(s) to generate
    - 'triple_map'
    - 'timeseries'
```

### Climatology Configuration

```yaml
  climatology:
    enabled: true
    reference_period_start: 1989
    reference_period_end: 2019
```

### Dataset Configuration

```yaml
datasets:
  - name: 'CERRA-land_CICAv2_Finals'
    v1_list:                  # Variables for first version
      - 'pr'
      - 'tas'
      - 'r01mm'
    v2_list:                  # Variables for comparison version
      - 'pr'
      - 'tas'
      - 'r01mm'
```

## Example Configurations

The `ymls/` directory contains several example configurations:

- `cerra_climatology_1989_2019.yml` - CERRA climatology validation
- `prueba_CERRA-L_climatology.yml` - CERRA-Land climatology test
- `prueba_CERRA-L_singlemaps.yml` - Single map generation example

## Output

Generated plots are typically saved in output directories specified in the configuration or determined by the project structure. Common output formats include PNG and PDF.

## Requirements

- xarray
- numpy
- matplotlib
- pyyaml
- netCDF4
- cartopy (for map projections)

## Tips

- Use climatology configuration for comparing against reference periods
- Adjust `lon_point` and `lat_point` for time series at specific locations
- Multiple plot types can be generated in a single run by listing them in `type_of_plot`
- For large datasets, consider memory management settings in the scripts