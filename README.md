# CICA-ATLAS-tools

This repository contains tools for climate data processing, validation, and product generation for the CICA-ATLAS project. The toolkit supports various climate datasets including CORDEX-CORE, CERRA-Land, E-OBS, and ERA5.

## Repository Structure

The repository is organized into three main components:

- **[validations/](validations/)** - Tools for generating validation plots and analyses
- **[workflow/](workflow/)** - Configuration templates and pipeline generation scripts
- **[products/](products/)** - Tools for generating climate data products

## Overview

CICA-ATLAS-tools provides a comprehensive suite for:

- Processing climate model outputs and observational datasets
- Calculating climatological indices and extremes
- Generating validation visualizations (maps, time series, stripes)
- Automating climate data processing workflows
- Creating standardized climate data products

## Supported Projects

- **CORDEX-CORE**: Coordinated Regional Climate Downscaling Experiment Core simulations
- **CERRA-Land**: Copernicus European Regional ReAnalysis Land component
- **E-OBS**: European gridded observational dataset
- **ERA5**: ECMWF Reanalysis v5

## Quick Start

### Validations

Generate validation plots and analyses:

```bash
cd validations
python generate_plots.py ymls/your_config.yml
```

See [validations/README.md](validations/README.md) for details.

### Workflow

Generate configuration files for climate data processing pipelines:

```bash
cd workflow/generation_scripts
python cfile.py --project CORDEX-CORE --step indices --variables tas,pr
```

See [workflow/README.md](workflow/README.md) for details.

### Products

Generate climate data products with specific configurations:

```python
from products.Product_cfile import Product_Config

config = Product_Config(
    project="CORDEX-CORE",
    variable="tas",
    type="climatology"
)
```

See [products/README.md](products/README.md) for details.

## Requirements

- Python 3.x
- xarray
- numpy
- matplotlib
- pyyaml/ruamel.yaml
- Additional dependencies specific to each component (see individual README files)

## Contributing

Please refer to the individual README files in each directory for specific contribution guidelines and detailed usage instructions.

## License

[Add license information here]
