"""
Project-level parameters for CICA-ATLAS Products module.

This module contains all project-specific parameters including:
- Project definitions and aliases
- Experiments, periods, domains, and grids
- Data types and trends configuration
- Robustness and baseline definitions
- Helper functions for project-related queries

Compatible with workflow/generation_scripts/ structure for future unification.
"""

import sys
import os

# Add parent directory to path to import load_parameters
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# =============================================================================
# CORE PROJECT DEFINITIONS
# =============================================================================

# Canonical project names
CANONICAL_PROJECTS = [
    "CMIP6",
    "CMIP5",
    "CORDEX-EUR-11",
    "CORDEX-CORE",
    "CORDEX-CORERUR",
    "CORDEX-COREURB",
    "ERA5",
    "ERA5-Land",
    "E-OBS",
    "ORAS5",
    "CERRA",
    "CERRARUR",
    "CERRAURB",
    "CPC",
    "BERKELEY",
    "SSTSAT",
]

# Project aliases (alias -> canonical)
PROJECT_ALIASES = {
    "EOBS": "E-OBS",
    "ORAS-5": "ORAS5",
    "ERA5-land": "ERA5-Land",
    "CORDEX-EUR": "CORDEX-EUR-11",
    "CORDEX-EUR-11URB": "CORDEX-COREURB",
    "CORDEX-EUR-11RUR": "CORDEX-CORERUR",
}

# All supported projects (canonical + aliases)
SUPPORTED_PROJECTS = CANONICAL_PROJECTS + list(PROJECT_ALIASES.keys())

# Observation projects
OBSERVATION_PROJECTS = [
    "ERA5",
    "ERA5-Land",
    "E-OBS",
    "ORAS5",
    "CERRA",
    "CERRARUR",
    "CERRAURB",
    "CPC",
    "BERKELEY",
    "SSTSAT",
]

# Projection projects
PROJECTION_PROJECTS = [
    "CMIP6",
    "CMIP5",
    "CORDEX-EUR-11",
    "CORDEX-CORE",
    "CORDEX-CORERUR",
    "CORDEX-COREURB",
]


# =============================================================================
# PROJECT CONFIGURATION DICTIONARIES
# =============================================================================

# Project roots (used in config['directories'])
PROJECT_ROOTS = {
    "CMIP6": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/CMIP6/",
    "CMIP5": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/CMIP5/",
    "CORDEX-EUR-11": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/CORDEX-EUR-11/",
    "CORDEX-CORE": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/CORDEX-CORE/",
    "CORDEX-CORERUR": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/CORDEX-CORERUR/",
    "CORDEX-COREURB": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/CORDEX-COREURB/",
    "ERA5": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/ERA5/",
    "ERA5-Land": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/ERA5-Land/",
    "E-OBS": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/E-OBS/",
    "ORAS5": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/ORAS5/",
    "CERRA": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/CERRA/",
    "CERRARUR": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/CERRARUR/",
    "CERRAURB": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/CERRAURB/",
    "CPC": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/CPC/",
    "BERKELEY": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/BERKELEY/",
    "SSTSAT": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/SSTSAT/",
}

# Experiments per project (used in config['data'][0]['scenario'])
PROJECT_EXPERIMENTS = {
    "CMIP6": ["historical", "ssp119", "ssp126", "ssp245", "ssp370", "ssp585"],
    "CMIP5": ["historical", "rcp26", "rcp45", "rcp85"],
    "CORDEX-EUR-11": ["historical", "rcp26", "rcp45", "rcp85"],
    "CORDEX-CORE": ["historical", "rcp26", "rcp85"],
    "CORDEX-CORERUR": ["historical", "rcp26", "rcp85"],
    "CORDEX-COREURB": ["historical", "rcp26", "rcp85"],
    "ERA5": ["None"],
    "ERA5-Land": ["None"],
    "E-OBS": ["None"],
    "ORAS5": ["None"],
    "CERRA": ["None"],
    "CERRARUR": ["None"],
    "CERRAURB": ["None"],
    "CPC": ["None"],
    "BERKELEY": ["None"],
    "SSTSAT": ["None"],
}

# Periods per project (used in config['data'][0]['period'])
PROJECT_PERIODS = {
    "CMIP6": {"hist": (1850, 2014), "fut": (2015, 2100)},
    "CMIP5": {"hist": (1850, 2005), "fut": (2006, 2100)},
    "CORDEX-EUR-11": {"hist": (1970, 2005), "fut": (2006, 2100)},
    "CORDEX-CORE": {"hist": (1970, 2005), "fut": (2006, 2100)},
    "CORDEX-CORERUR": {"hist": (1970, 2005), "fut": (2006, 2100)},
    "CORDEX-COREURB": {"hist": (1970, 2005), "fut": (2006, 2100)},
    "ERA5": {"hist": (1940, 2024), "fut": None},
    "ERA5-Land": {"hist": (1950, 2024), "fut": None},
    "E-OBS": {"hist": (1950, 2024), "fut": None},
    "ORAS5": {"hist": (1958, 2014), "fut": None},
    "CERRA": {"hist": (1985, 2021), "fut": None},
    "CERRARUR": {"hist": (1985, 2021), "fut": None},
    "CERRAURB": {"hist": (1985, 2021), "fut": None},
    "CPC": {"hist": (1979, 2020), "fut": None},
    "BERKELEY": {"hist": (1881, 2017), "fut": None},
    "SSTSAT": {"hist": (1982, 2022), "fut": None},
}

# Domains per project
PROJECT_DOMAINS = {
    "CMIP6": ["None"],
    "CMIP5": ["None"],
    "CORDEX-EUR-11": ["EUR"],
    "CORDEX-CORE": ["AFR", "AUS", "CAM", "EAS", "EUR", "NAM", "SAM", "SEA", "WAS"],
    "CORDEX-CORERUR": ["EUR"],
    "CORDEX-COREURB": ["EUR"],
    "ERA5": ["None"],
    "ERA5-Land": ["None"],
    "E-OBS": ["None"],
    "ORAS5": ["None"],
    "CERRA": ["None"],
    "CERRARUR": ["None"],
    "CERRAURB": ["None"],
    "CPC": ["None"],
    "BERKELEY": ["None"],
    "SSTSAT": ["None"]
}

# Project IDs for CDS/API (used in config['data'][0]['project_id'])
PROJECT_IDS = {
    "CMIP6": "projections-cmip6",
    "CMIP5": "projections-cmip5-monthly-single-levels",
    "CORDEX-EUR-11": "projections-cordex-domains-single-levels",
    "CORDEX-CORE": "projections-cordex-domains-single-levels",
    "CORDEX-CORERUR": "projections-cordex-domains-single-levels",
    "CORDEX-COREURB": "projections-cordex-domains-single-levels",
    "ERA5": "reanalysis-era5-single-levels",
    "ERA5-Land": "reanalysis-era5-land",
    "E-OBS": "insitu-gridded-observations-europe",
    "ORAS5": "reanalysis-oras5",
    "CERRA": "reanalysis-cerra-single-levels",
    "CERRARUR": "reanalysis-cerra-single-levels",
    "CERRAURB": "reanalysis-cerra-single-levels",
    "CPC": "insitu-gridded-observations-global-and-regional",
    "BERKELEY": "insitu-gridded-observations-global-and-regional",
    "SSTSAT": "satellite-sea-surface-temperature",
}

# Reference grids per project
PROJECT_GRIDS = {
    "CMIP6": {"resolution": 1.0, "reference_grid": "land_sea_mask_grd100.nc"},
    "CMIP5": {"resolution": 2.0, "reference_grid": "land_sea_mask_grd200.nc"},
    "CORDEX-EUR-11": {"resolution": 0.125, "reference_grid": "land_sea_mask_grd012p5_EUR11-CORDEX.nc"},
    "CORDEX-CORE": {"resolution": 0.25, "reference_grid": "land_sea_mask_grd025.nc"},
    "CORDEX-CORERUR": {"resolution": 0.25, "reference_grid": "land_sea_mask_grd025.nc"},
    "CORDEX-COREURB": {"resolution": 0.25, "reference_grid": "land_sea_mask_grd025.nc"},
    "ERA5": {"resolution": 0.25, "reference_grid": "RAW"},
    "ERA5-Land": {"resolution": 0.1, "reference_grid": "RAW"},
    "E-OBS": {"resolution": 0.125, "reference_grid": "land_sea_mask_grd012_EOBS_EUR11-CORDEX.nc"},
    "ORAS5": {"resolution": 0.25, "reference_grid": "land_sea_mask_grd025.nc"},
    "CERRA": {"resolution": 0.065, "reference_grid": "land_sea_mask_grd011.nc"},
    "CERRARUR": {"resolution": 0.065, "reference_grid": "land_sea_mask_grd011.nc"},
    "CERRAURB": {"resolution": 0.065, "reference_grid": "land_sea_mask_grd011.nc"},
    "CPC": {"resolution": 1, "reference_grid": "RAW"},
    "BERKELEY": {"resolution": 1, "reference_grid": "RAW"},
    "SSTSAT": {"resolution": 0.05, "reference_grid": "RAW"},
}


# =============================================================================
# PRODUCTS-SPECIFIC PARAMETERS
# =============================================================================

# Data type per project (used in config['data'][0]['type'])
PROJECT_DATA_TYPE = {
    "CMIP6": "projection",
    "CMIP5": "projection",
    "CORDEX-EUR-11": "projection",
    "CORDEX-CORE": "projection",
    "CORDEX-CORERUR": "projection",
    "CORDEX-COREURB": "projection",
    "ERA5": "observation",
    "ERA5-Land": "observation",
    "E-OBS": "observation",
    "ORAS5": "observation",
    "CERRA": "observation",
    "CERRARUR": "observation",
    "CERRAURB": "observation",
    "CPC": "observation",
    "BERKELEY": "observation",
    "SSTSAT": "observation",
}






# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_project_root(project: str) -> str:
    """
    Get the root directory for a project.
    
    Parameters
    ----------
    project : str
        Project name (canonical or alias)
        
    Returns
    -------
    str
        Root directory path
    """
    # Resolve alias if needed
    canonical = PROJECT_ALIASES.get(project, project)
    return PROJECT_ROOTS.get(canonical, "None")


def is_observation_project(project: str) -> bool:
    """
    Check if a project is an observation dataset.
    
    Parameters
    ----------
    project : str
        Project name
        
    Returns
    -------
    bool
        True if observation project, False otherwise
    """
    canonical = PROJECT_ALIASES.get(project, project)
    return canonical in OBSERVATION_PROJECTS


def is_projection_project(project: str) -> bool:
    """
    Check if a project is a projection dataset.
    
    Parameters
    ----------
    project : str
        Project name
        
    Returns
    -------
    bool
        True if projection project, False otherwise
    """
    canonical = PROJECT_ALIASES.get(project, project)
    return canonical in PROJECTION_PROJECTS


def get_project_experiments(project: str) -> list:
    """
    Get list of experiments for a project.
    
    Parameters
    ----------
    project : str
        Project name
        
    Returns
    -------
    list
        List of experiment names
    """
    canonical = PROJECT_ALIASES.get(project, project)
    return PROJECT_EXPERIMENTS.get(canonical, ["None"])


def get_project_periods(project: str) -> dict:
    """
    Get historical and future periods for a project.
    
    Parameters
    ----------
    project : str
        Project name
        
    Returns
    -------
    dict
        Dictionary with 'hist' and 'fut' keys
    """
    canonical = PROJECT_ALIASES.get(project, project)
    return PROJECT_PERIODS.get(canonical, {"hist": None, "fut": None})


def get_project_domains(project: str) -> list:
    """
    Get list of domains for a project.
    
    Parameters
    ----------
    project : str
        Project name
        
    Returns
    -------
    list
        List of domain names, or ["None"] if not applicable
    """
    canonical = PROJECT_ALIASES.get(project, project)
    return PROJECT_DOMAINS.get(canonical, ["None"])


def get_data_type(project: str) -> str:
    """
    Get data type for a project.
    
    Used in config['data'][0]['type'].
    
    Parameters
    ----------
    project : str
        Project name
        
    Returns
    -------
    str
        "observation" or "projection"
    """
    canonical = PROJECT_ALIASES.get(project, project)
    return PROJECT_DATA_TYPE.get(canonical, "NOT DEFINED")




