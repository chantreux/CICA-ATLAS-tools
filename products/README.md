# Products

This directory contains tools for generating standardized climate data products with versioning and configuration management.

## Overview

The products module provides utilities for:

- Automated climate product generation with version control
- Variable-specific product configurations  
- Output path management and file organization
- Support for climatology and extreme indices products
- Integration with multiple climate projects (CORDEX-CORE, ERA5, CERRA-Land, E-OBS)

## Main Components

- **`Product_cfile.py`** - Main configuration class for product generation
- **`Product_configs.py`** - Configuration management utilities
- **`Product_variables.py`** - Variable definitions and version mappings
- **`load_parameters.py`** - Parameter loading and dataset configuration

## Template Files

The products module uses 3 universal template files that work dynamically for all projects:

- **`refconfiguration-remote_TEMPLATE_climatology.yml`** - For climatology products
- **`refconfiguration-remote_TEMPLATE_trends.yml`** - For trend analysis products  
- **`refconfiguration-remote_TEMPLATE_temporal_series.yml`** - For temporal series products

All project-specific configurations (chunking, members, masks, etc.) are handled dynamically through the parameters system in `products/parameters/`.

### Adding Support for New Projects

To add a new project:
1. Add project configuration to `products/parameters/projects.py`
2. Add chunk configuration to `products/parameters/cluster_resources.py`
3. Add any project-specific logic to `products/parameters/projects_products.py`

No need to create new template files!

*Note: This module is under active development and subject to change.*
