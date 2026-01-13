# Products

This directory contains tools for generating standardized climate data products with versioning and configuration management. It provides a framework for creating climate products with consistent structure and metadata.

## Overview

The products module enables:

- Automated climate product generation with versioning
- Variable-specific product configurations
- Output path management and file organization
- Support for climatology and extreme indices products
- Integration with multiple climate projects (CORDEX-CORE, ERA5, CERRA-Land)

## Main Modules

### `Product_cfile.py`

Main class for product configuration and file generation.

**Key Class: `Product_Config`**

Manages product configuration including:
- Project identification and setup
- Variable selection and validation
- Version management
- Input/output path configuration
- Configuration file generation (cfile and jobfile)

**Usage Example:**
```python
from Product_cfile import Product_Config

# Create a climatology product configuration
config = Product_Config(
    project="CORDEX-CORE",
    variable="tas",
    type="climatology",
    extreme=False
)

# Generate configuration files
config.generate_config_files()
```

**Parameters:**
- `project` - Climate project name (e.g., "CORDEX-CORE", "ERA5")
- `variable` - Climate variable (e.g., "tas", "pr", "tasmax")
- `cfile_in` - Optional input configuration file path
- `jobfile_in` - Optional input job file path
- `main_proj_experiment` - Experiment type (e.g., "historical")
- `type` - Product type ("climatology", "timeseries", etc.)
- `set` - Dataset set identifier
- `input_folder` - Custom input directory
- `output_folder` - Custom output directory
- `extreme` - Boolean flag for extreme indices

### `Product_configs.py`

Utility functions for product configuration management.

**Key Functions:**

- `get_version_config(project, variable, version)` - Retrieve version-specific configuration
- `get_output_path(project, variable, version, type)` - Generate output paths
- `check_existing_files(output_path)` - Validate output directory and check for existing files

**Features:**
- Version-based product organization
- Automatic path generation
- File existence validation
- Configuration validation and error handling

### `Product_variables.py`

Variable definitions and version mappings for different projects.

**Key Components:**

- `VERSION_VARIABLES` - Dictionary mapping projects to version-variable associations
- `get_variables_for_version(project, version)` - Get available variables for a specific version

**Supported Variable Categories:**
- Temperature variables (tas, tasmax, tasmin, tn, tx)
- Precipitation variables (pr, pr_sum)
- Extreme indices (r01mm, r10mm, r20mm, rx1day, cdd)
- Other climate variables (hurs, sfcWind, rsds)

### `load_parameters.py`

Parameter loading and dataset configuration utilities.

**Key Features:**
- Urban variable definitions
- Model list management (CMIP5, CMIP6)
- Variable name transformations
- Core model list loading
- Dataset class for project-specific parameters

**Example Functions:**
- `urban_vars()` - Returns list of urban-relevant climate variables
- `CMIP5_model_list()` - Returns supported CMIP5 models
- `new_name_var(var)` - Transform variable names between conventions

## Product Types

### Climatology Products

Calculate climatological means over reference periods.

**Configuration:**
```python
config = Product_Config(
    project="CORDEX-CORE",
    variable="tas",
    type="climatology",
    main_proj_experiment="historical"
)
```

### Extreme Indices Products

Generate products for climate extremes.

**Configuration:**
```python
config = Product_Config(
    project="CORDEX-CORE",
    variable="r01mm",
    type="climatology",
    extreme=True
)
```

## Version Management

Products are organized by versions, allowing for:
- Multiple data versions for the same variable
- Version-specific variable availability
- Tracked product evolution
- Reproducible product generation

## Output Structure

Products are typically organized as:

```
output_folder/
├── project_name/
│   ├── version_1/
│   │   ├── variable_1/
│   │   │   └── product_files.nc
│   │   └── variable_2/
│   │       └── product_files.nc
│   └── version_2/
│       └── ...
```

## Configuration File Generation

The module generates two types of configuration files:

1. **cfile** - Processing configuration (variables, domains, temporal settings)
2. **jobfile** - Job submission configuration (cluster, resources, paths)

These files are used by the workflow system to execute product generation.

## Supported Projects

- **CORDEX-CORE**: Regional climate model ensemble
- **ERA5**: Reanalysis dataset products
- **CERRA-Land**: European reanalysis land component
- **E-OBS**: Observational gridded dataset

## Variable Support

Common variables include:
- **Temperature**: tas, tasmax, tasmin, tn, tx, tnn, txx
- **Precipitation**: pr, pr_sum, evspsbl
- **Extremes**: r01mm, r10mm, r20mm, rx1day, rx5day, cdd, sdii
- **Other**: hurs, sfcWind, rsds, rlds, huss

## Best Practices

1. **Version Control**: Always specify versions explicitly for reproducibility
2. **Path Management**: Use the automatic path generation to maintain consistent structure
3. **Validation**: Check for existing files before regenerating products
4. **Configuration**: Review generated cfile and jobfile before submission
5. **Extreme Flags**: Set `extreme=True` for extreme indices to ensure proper handling

## Integration with Workflow

The products module integrates with the workflow system:

1. Generate product configuration using `Product_Config`
2. Create cfile and jobfile
3. Submit to workflow system for processing
4. Output products stored in versioned structure

## Requirements

- Python 3.x
- ruamel.yaml (YAML processing with comment preservation)
- logging (included in standard library)
- pathlib (included in standard library)

## Tips

- Use `check_existing_files()` before regenerating products to avoid duplication
- Review `VERSION_VARIABLES` to understand available variables per project
- For historical experiments, set `main_proj_experiment="historical"`
- Custom input/output folders can override default paths
- Logging is configured automatically for debugging and tracking
