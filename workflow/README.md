# Workflow

This directory contains tools for generating and managing climate data processing workflows. It provides configuration file generation, cluster job templates, and pipeline execution tools.

## Overview

The workflow tools enable:

- Automated generation of configuration files for different climate projects
- Cluster job submission templates (GPFS, Lustre)
- Pipeline execution and orchestration
- Support for multiple processing steps (indices, homogenization, bias adjustment)

## Directory Structure

```
workflow/
├── generation_scripts/     # Scripts for generating configuration files
├── config_files_template/  # Template configuration files
└── runner/                 # Pipeline execution scripts
```

## Generation Scripts

### `cfile.py`

Main script for generating configuration files from templates. Supports various climate data projects and processing steps.

**Key Features:**
- Template-based configuration generation
- Project-specific customization (CORDEX-CORE, ERA5, CERRA-Land, E-OBS)
- Variable aggregation and temporal processing configuration
- Cluster-specific job file generation

**Usage:**
```bash
python cfile.py --project CORDEX-CORE --step indices --variables tas,pr
```

### Supporting Modules

- **`load_parameters.py`** - Parameter loading and dataset configuration utilities
- **`variables.py`** - Variable definitions, temporal aggregation settings, and processing steps
- **`cluster.py`** - Cluster configuration for different HPC systems
- **`projects.py`** - Project-specific settings and metadata
- **`aliases.py`** - Project aliases and step mappings
- **`cordex-core.py`** - CORDEX-CORE specific configurations

## Configuration Templates

The `config_files_template/` directory contains YAML templates for different projects and processing steps:

### Available Templates

- **CORDEX-CORE**:
  - `config_template_CORDEX-CORE_all.yml`
  - `config_template_CORDEX-CORE_indices.yml`
  - `config_template_CORDEX-CORE_homogenization.yml`
  - `config_template_CORDEX-CORE_biasadjustment.yml`
  - `config_template_CORDEX-CORE_indices_CICA.yml`

- **ERA5**:
  - `config_template_ERA5_all.yml`
  - `config_template_ERA5_indices.yml`
  - `config_template_ERA5_homogenization.yml`

- **CERRA-Land**:
  - `config_template_CERRA-Land_all.yml`

- **E-OBS**:
  - `config_template_E-OBS_all.yml`

### Job Templates

- `Job_template_gpfs.sh` - SLURM job template for GPFS filesystem
- `Job_template_lustre.sh` - SLURM job template for Lustre filesystem

## Pipeline Runner

### `run_climate_pipeline.py`

Executes the climate data processing pipeline using a configuration file.

**Usage:**
```bash
python runner/run_climate_pipeline.py --config-file path/to/config.yml
```

**Features:**
- Configuration file validation
- Pipeline initialization and execution
- Integration with ClimateDataPipeline framework

## Supported Projects

### CORDEX-CORE

Coordinated Regional Climate Downscaling Experiment Core simulations.

**Supported Steps:**
- `indices` - Climate indices calculation
- `homogenization` - Data homogenization
- `biasadjustment` - Bias correction
- `indices_CICA` - CICA-specific indices

### ERA5

ECMWF Reanalysis v5 dataset processing.

**Supported Steps:**
- `indices` - Climate indices from reanalysis
- `homogenization` - Temporal homogenization

### CERRA-Land

Copernicus European Regional ReAnalysis Land component.

### E-OBS

European gridded observational dataset.

## Supported Processing Steps

The `variables.py` module defines supported processing steps:

- `biasadjustment` - Statistical bias correction
- `homogenization` - Temporal homogenization
- `indices` - Climate indices calculation
- `indices_CICA` - CICA-specific indices
- `all` - Complete processing workflow

## Cluster Support

Supported cluster configurations (defined in `cluster.py`):

- GPFS-based systems
- Lustre-based systems
- Custom cluster configurations

Job templates include:
- Resource allocation (nodes, tasks, memory)
- Module loading
- Environment setup
- Output/error logging

## Configuration File Structure

Generated configuration files typically include:

```yaml
project: CORDEX-CORE
step: indices
variables:
  - tas
  - pr
  - tasmax
  - tasmin
domain: EUR-11
model: model_name
experiment: historical
temporal_aggregation: monthly
output_path: /path/to/output
```

## Tips

- Use project aliases for convenience (e.g., 'cc' for 'CORDEX-CORE')
- Check `SUPPORTED_STEPS` in `variables.py` for available processing steps
- Review template files before generation to understand structure
- Customize cluster templates for your HPC environment
- Use `--help` flag with scripts for detailed parameter information

## Requirements

- Python 3.x
- pyyaml
- fire (for CLI interface in runner)
- Access to HPC cluster (for job submission)
- climate_data_pipeline package (for pipeline execution)
