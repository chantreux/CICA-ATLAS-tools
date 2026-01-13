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
import load_parameters


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
    "CORDEX-CORE": ["AFR", "AUS", "CAM", "EAS", "EUR", "NAM", "SAM", "SEA", "WAS"],
    "CORDEX-EUR-11": ["EUR"],
    "CORDEX-CORERUR": ["EUR"],
    "CORDEX-COREURB": ["EUR"],
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
}

# Reference grids per project
PROJECT_GRIDS = {
    "CMIP6": {"resolution": 1.0, "type": "regular"},
    "CMIP5": {"resolution": 1.0, "type": "regular"},
    "CORDEX-EUR-11": {"resolution": 0.12, "type": "rotated"},
    "CORDEX-CORE": {"resolution": 0.25, "type": "rotated"},
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

# Trend calculation enabled per project (used in config['products'][product_key]['magnitudes']['trends'])
# Only enabled for observation datasets when type='trends'
PROJECT_TRENDS = {
    "ERA5": True,
    "ERA5-Land": True,
    "E-OBS": True,
    "ORAS5": True,
    "CERRA": True,
    "CERRARUR": True,
    "CERRAURB": True,
    "CPC": True,
    "BERKELEY": True,
    "SSTSAT": True,
}

# Robustness calculation enabled per project (used in config['products'][product_key]['magnitudes']['anom_emergence'])
# Boolean values: True for projection projects, False for observation projects
PROJECT_ROBUSTNESS = {
    "CMIP6": True,
    "CMIP5": True,
    "CORDEX-EUR-11": True,
    "CORDEX-CORE": True,
    "CORDEX-CORERUR": True,
    "CORDEX-COREURB": True,
    "ERA5": False,
    "ERA5-Land": False,
    "E-OBS": False,
    "ORAS5": False,
    "CERRA": False,
    "CERRARUR": False,
    "CERRAURB": False,
    "CPC": False,
    "BERKELEY": False,
    "SSTSAT": False,
}

# Baseline periods per project (used in config['products'][product_key]['baselines'])
BASELINES = {
    "CMIP6": {
        "preIndustrial": "1850-1900",
        "AR5": "1986-2005",
        "AR6": "1995-2014",
        "WMO1": "1961-1990",
        "WMO2": "1981-2010",
        "WMO3": "1991-2020"
    },
    "CMIP5": {
        "preIndustrial": "1850-1900",
        "AR5": "1986-2005",
        "AR6": "1995-2014",
        "WMO1": "1961-1990",
        "WMO2": "1981-2010",
        "WMO3": "1991-2020"
    },
    "CORDEX-EUR-11": {
        "preIndustrial": "1850-1900",
        "AR5": "1986-2005",
        "AR6": "1995-2014",
        "WMO1": "1961-1990",
        "WMO2": "1981-2010",
        "WMO3": "1991-2020"
    },
    "CORDEX-CORE": {
        "preIndustrial": "1850-1900",
        "AR5": "1986-2005",
        "AR6": "1995-2014",
        "WMO1": "1961-1990",
        "WMO2": "1981-2010",
        "WMO3": "1991-2020"
    },
    "CORDEX-CORERUR": {
        "preIndustrial": "1850-1900",
        "AR5": "1986-2005",
        "AR6": "1995-2014",
        "WMO1": "1961-1990",
        "WMO2": "1981-2010",
        "WMO3": "1991-2020"
    },
    "CORDEX-COREURB": {
        "preIndustrial": "1850-1900",
        "AR5": "1986-2005",
        "AR6": "1995-2014",
        "WMO1": "1961-1990",
        "WMO2": "1981-2010",
        "WMO3": "1991-2020"
    },
    "ERA5": {
        "AR5": "1986-2005",
        "AR6": "1995-2014",
        "WMO1": "1961-1990",
        "WMO2": "1981-2010",
        "WMO3": "1991-2020"
    },
    "ERA5-Land": {
        "AR5": "1986-2005",
        "AR6": "1995-2014",
        "WMO1": "1961-1990",
        "WMO2": "1981-2010",
        "WMO3": "1991-2020"
    },
    "E-OBS": {
        "AR5": "1986-2005",
        "AR6": "1995-2014",
        "WMO1": "1961-1990",
        "WMO2": "1981-2010",
        "WMO3": "1991-2020"
    },
    "ORAS5": {
        "AR5": "1986-2005",
        "AR6": "1995-2014",
        "WMO2": "1981-2010",
        "WMO3": "1991-2020"
    },
    "CERRA": {
        "AR5": "1986-2005",
        "AR6": "1995-2014",
        "WMO2": "1981-2010",
        "WMO3": "1991-2020"
    },
    "CERRARUR": {
        "AR5": "1986-2005",
        "AR6": "1995-2014",
        "WMO2": "1981-2010",
        "WMO3": "1991-2020"
    },
    "CERRAURB": {
        "AR5": "1986-2005",
        "AR6": "1995-2014",
        "WMO2": "1981-2010",
        "WMO3": "1991-2020"
    },
    "CPC": {
        "AR5": "1986-2005",
        "AR6": "1995-2014",
        "WMO2": "1981-2010",
        "WMO3": "1991-2020"
    },
    "BERKELEY": {
        "AR5": "1986-2005",
        "AR6": "1995-2014",
        "WMO2": "1981-2010",
        "WMO3": "1991-2020"
    },
    "SSTSAT": {
        "AR5": "1986-2005",
        "AR6": "1995-2014",
        "WMO2": "1981-2010",
        "WMO3": "1991-2020"
    },
}

# Climatology periods for projection projects (used in config['products'][product_key]['periods'])
CLIMATOLOGY_PERIODS = {
    "near": "2021-2040",
    "medium": "2041-2060",
    "long": "2081-2100"
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


def get_scenario_lines(project: str, main_experiment: str = "None") -> dict:
    """
    Get scenario line configuration for a project.
    
    Used in config['products'][product_key]['scenarios'].
    
    Parameters
    ----------
    project : str
        Project name
    main_experiment : str
        Main experiment name
        
    Returns
    -------
    dict
        Dictionary with 'main', 'baseline', and 'fill_baseline' keys
    """
    canonical = PROJECT_ALIASES.get(project, project)
    
    if canonical in OBSERVATION_PROJECTS:
        return {
            "main": None,
            "baseline": None,
            "fill_baseline": None
        }
    
    if canonical in PROJECTION_PROJECTS:
        result = {
            "main": main_experiment,
            "baseline": "historical",
            "fill_baseline": []
        }
        
        # Adjust baseline for fullperiod variables
        # This will be handled in variable-specific logic
        
        # Set fill_baseline based on project
        if canonical == "CMIP6":
            if main_experiment == "ssp119":
                result["fill_baseline"] = ["ssp119", "ssp126", "ssp245", "ssp370", "ssp585"]
            else:
                result["fill_baseline"] = ["ssp126", "ssp245", "ssp370", "ssp585"]
        elif canonical in ["CORDEX-CORE", "CORDEX-CORERUR", "CORDEX-COREURB"]:
            result["fill_baseline"] = ["rcp26", "rcp85"]
        else:  # CMIP5, CORDEX-EUR-11
            result["fill_baseline"] = ["rcp26", "rcp45", "rcp85"]
        
        return result
    
    raise ValueError(f"Scenarios not defined for project {project}")


def get_warming_levels(project: str) -> tuple:
    """
    Get warming levels and file path for a project.
    
    Used in config['products'][product_key]['warming_levels'].
    
    Parameters
    ----------
    project : str
        Project name
        
    Returns
    -------
    tuple
        (warming_levels_list, warming_file_path)
    """
    canonical = PROJECT_ALIASES.get(project, project)
    
    if canonical not in PROJECTION_PROJECTS:
        return [], None
    
    warming_levels = [1.5, 2, 3, 4]
    
    if canonical == "CMIP6":
        warming_file = "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/resources/resources/warming_levels/CMIP6_WarmingLevels.csv"
    else:
        warming_file = "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/resources/resources/warming_levels/CMIP5_WarmingLevels.csv"
    
    return warming_levels, warming_file


def get_spatial_mask(project: str, variable: str) -> str:
    """
    Get spatial mask file path for a project and variable.
    
    Used in config['data'][0]['spatial_mask'].
    
    Parameters
    ----------
    project : str
        Project name
    variable : str
        Variable name
        
    Returns
    -------
    str or None
        Path to spatial mask file, or None if not applicable
    """
    canonical = PROJECT_ALIASES.get(project, project)
    
    if "CORDEX-EUR-11" in canonical:
        if "bals" in variable or "baisimip" in variable:
            return "/lustre/gmeteo/WORK/chantreuxa/cica/data/resources/reference-grids/CORDEX-EUR-11_EuropeOnly.nc"
        else:
            return "/lustre/gmeteo/WORK/chantreuxa/cica/data/resources/reference-grids/CORDEX-EUR-11_domain_simplified.nc"
    elif canonical == "E-OBS":
        return "/lustre/gmeteo/WORK/chantreuxa/cica/data/resources/reference-grids/EOBS_EuropeOnly.nc"
    else:
        return None


def get_baseline_dict(project: str) -> dict:
    """
    Get baseline periods dictionary for a project.
    
    Used in config['products'][product_key]['baselines'].
    
    Parameters
    ----------
    project : str
        Project name
        
    Returns
    -------
    dict
        Dictionary of baseline periods
        
    Raises
    ------
    ValueError
        If baselines not defined for project
    """
    canonical = PROJECT_ALIASES.get(project, project)
    
    if canonical not in BASELINES:
        raise ValueError(f"Baselines not defined for project {project}")
    
    return BASELINES[canonical]


def get_period_climatology_dict(project: str, product_type: str, 
                                 is_historical: bool, baselines: dict) -> dict:
    """
    Get period climatology dictionary based on product type and project.
    
    Used in config['products'][product_key]['periods'].
    
    Parameters
    ----------
    project : str
        Project name
    product_type : str
        Type of product ("climatology", "temporal_series", "trends")
    is_historical : bool
        Whether main experiment is historical
    baselines : dict
        Baseline periods dictionary
        
    Returns
    -------
    dict
        Dictionary of climatology periods
        
    Raises
    ------
    ValueError
        If product type is invalid
    """
    if product_type not in ["climatology", "temporal_series", "trends"]:
        raise ValueError(f"Invalid product type: {product_type}")
    
    if product_type == "trends":
        raise ValueError("Climatology periods not applicable for trends type")
    
    canonical = PROJECT_ALIASES.get(project, project)
    
    # For projection datasets (non-historical runs)
    if canonical in PROJECTION_PROJECTS and not is_historical:
        return CLIMATOLOGY_PERIODS.copy()
    else:
        # For observation datasets or historical runs, use baselines
        return baselines.copy()


def get_period_experiments_dict(project: str, variable: str, 
                                 main_experiment: str, dataset) -> dict:
    """
    Get period information for experiments.
    
    Used in config['data'][0]['period'].
    
    Parameters
    ----------
    project : str
        Project name
    variable : str
        Variable name
    main_experiment : str
        Main experiment name
    dataset : Dataset
        Dataset object from load_parameters
        
    Returns
    -------
    dict or str
        Dictionary mapping experiments to periods, or single period string
    """
    canonical = PROJECT_ALIASES.get(project, project)
    
    hist, fut = dataset.load_period(variable, version="v2")
    hist_period = f"{hist[0]}-{hist[-1]}"
    
    # For observation datasets
    if canonical in OBSERVATION_PROJECTS:
        if canonical == "BERKELEY":
            return "1960-2017"
        return hist_period
    
    # For projection datasets
    if canonical in PROJECTION_PROJECTS:
        if "fullperiod" in variable:
            fut_period = f"{hist[0]}-{fut[-1]}"
        else:
            fut_period = f"{fut[0]}-{fut[-1]}"
        
        period_dict = {}
        
        if canonical == "CMIP6":
            if main_experiment == "ssp119":
                period_dict = {
                    "historical": hist_period,
                    "ssp119": fut_period,
                    "ssp126": fut_period,
                    "ssp245": fut_period,
                    "ssp370": fut_period,
                    "ssp585": fut_period
                }
            else:
                period_dict = {
                    "historical": hist_period,
                    "ssp126": fut_period,
                    "ssp245": fut_period,
                    "ssp370": fut_period,
                    "ssp585": fut_period
                }
        elif "CORDEX-EUR-11" in canonical or "CORDEX-CORE" in canonical or canonical == "CMIP5":
            period_dict = {
                "historical": hist_period,
                "rcp26": fut_period,
                "rcp45": fut_period,
                "rcp85": fut_period
            }
        
        # Remove historical for fullperiod variables
        if "fullperiod" in variable and "historical" in period_dict:
            del period_dict["historical"]
        
        return period_dict
    
    raise ValueError(f"Period not defined for project {project}")


def get_scenario_lines_dict(project: str, main_experiment: str, variable: str) -> dict:
    """
    Get scenario lines dictionary with variable-specific adjustments.
    
    Used in config['products'][product_key]['scenarios'].
    
    Parameters
    ----------
    project : str
        Project name
    main_experiment : str
        Main experiment name
    variable : str
        Variable name
        
    Returns
    -------
    dict
        Dictionary with 'main', 'baseline', and 'fill_baseline' keys
    """
    result = get_scenario_lines(project, main_experiment)
    
    # Adjust baseline for fullperiod variables
    if "fullperiod" in variable and result["baseline"] == "historical":
        result["baseline"] = main_experiment
    
    return result


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
    return PROJECT_DATA_TYPE.get(canonical, "observation")


def get_trend_enabled(project: str, product_type: str) -> bool:
    """
    Check if trend calculation is enabled for a project and product type.
    
    Used in config['products'][product_key]['magnitudes']['trends'].
    
    Parameters
    ----------
    project : str
        Project name
    product_type : str
        Type of product ("climatology", "temporal_series", "trends")
        
    Returns
    -------
    bool
        True if trends should be calculated, False otherwise
    """
    canonical = PROJECT_ALIASES.get(project, project)
    
    # Trends only for observation datasets and trends type
    return (canonical in OBSERVATION_PROJECTS and 
            product_type == "trends" and 
            PROJECT_TRENDS.get(canonical, False))
