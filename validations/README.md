# Validations

This directory contains tools for validating climate data through various visualization and analysis methods.

## Overview

The validation tools provide:

- Generation of validation maps (single, triple, multi-model comparisons)
- Time series analysis and visualization
- Climatology calculations for reference periods
- Warming stripes visualizations
- Comparison between model outputs and observations

## Main Components

- **`generate_plots.py`** - Main script for generating validation visualizations from YAML configuration files
- **`climatology.py`** - Calculate climatological means
- **`maps.py`** / **`new_maps.py`** - Spatial map visualizations
- **`timeseries.py`** - Time series plotting and analysis
- **`stripes.py`** - Warming stripes visualization
- **`load_files.py`** - Data loading utilities

## Usage

```bash
python generate_plots.py ymls/your_config.yml
```

Configuration files are stored in the `ymls/` directory.

*Note: This module is under active development and subject to change.*