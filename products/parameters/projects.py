"""
Project-level parameters for CICA-ATLAS Products module.

This module contains all project-specific configuration:
- Project definitions and aliases
- Experiments, periods, domains for each project
- Baseline and climatology period configurations
- Warming levels and robustness settings
- Helper functions for accessing project parameters
"""

import load_parameters

# ============================================================================
# Core Project Definitions
# ============================================================================

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
    "CERRAURB",
    "CERRARUR",
    "CARRA",
    "CPC",
    "BERKELEY",
    "SSTSAT",
]

# Project aliases (maps alternative names to canonical names)
PROJECT_ALIASES = {
    "EOBS": "E-OBS",
    "ORAS-5": "ORAS5",
    "ERA5-land": "ERA5-Land",
    "CORDEX-EUR-11URB": "CORDEX-COREURB",
    "CORDEX-EUR-11RUR": "CORDEX-CORERUR",
}

# All supported projects (canonical + aliases)
SUPPORTED_PROJECTS = CANONICAL_PROJECTS + list(PROJECT_ALIASES.keys())

# Observation projects (used in config['data'][0]['type'])
OBSERVATION_PROJECTS = [
    "ERA5",
    "ERA5-Land",
    "E-OBS",
    "ORAS5",
    "CERRA",
    "CERRAURB",
    "CERRARUR",
    "CARRA",
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

# ============================================================================
# Project Properties
# ============================================================================

# Root directories for each project
PROJECT_ROOTS = {
    "CMIP6": "None",
    "CMIP5": "None",
    "CORDEX-EUR-11": "None",
    "CORDEX-CORE": "None",
    "CORDEX-CORERUR": "None",
    "CORDEX-COREURB": "None",
    "ERA5": "None",
    "ERA5-Land": "None",
    "E-OBS": "None",
    "ORAS5": "None",
    "CERRA": "None",
    "CERRAURB": "None",
    "CERRARUR": "None",
    "CARRA": "None",
    "CPC": "None",
    "BERKELEY": "None",
    "SSTSAT": "None",
}

# Available experiments per project (used in config['data'][0]['scenario'])
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
    "CERRAURB": ["None"],
    "CERRARUR": ["None"],
    "CARRA": ["None"],
    "CPC": ["None"],
    "BERKELEY": ["None"],
    "SSTSAT": ["None"],
}

# Historical and future periods per project (used indirectly via Dataset.load_period)
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
    "CERRAURB": {"hist": (1985, 2021), "fut": None},
    "CERRARUR": {"hist": (1985, 2021), "fut": None},
    "CARRA": {"hist": (1991, 2020), "fut": None},
    "CPC": {"hist": (1979, 2020), "fut": None},
    "BERKELEY": {"hist": (1881, 2017), "fut": None},
    "SSTSAT": {"hist": (1982, 2022), "fut": None},
}

# Domains per project
PROJECT_DOMAINS = {
    "CORDEX-EUR-11": ["EUR"],
    "CORDEX-CORE": ["AFR", "AUS", "CAM", "EAS", "EUR", "NAM", "SAM", "SEA", "WAS"],
    "CORDEX-CORERUR": ["AFR", "AUS", "CAM", "EAS", "EUR", "NAM", "SAM", "SEA", "WAS"],
    "CORDEX-COREURB": ["AFR", "AUS", "CAM", "EAS", "EUR", "NAM", "SAM", "SEA", "WAS"],
    # All other projects use None
}

# Project IDs for CDS/API
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
}

# Reference grids per project
PROJECT_GRIDS = {
    "CORDEX-EUR-11": 0.12,
    "CORDEX-CORE": 0.25,
    "CORDEX-CORERUR": 0.25,
    "CORDEX-COREURB": 0.25,
    "CMIP6": 1.0,
    "CMIP5": 1.0,
    "ERA5": "raw",
    "ERA5-Land": "raw",
    "E-OBS": "raw",
    "ORAS5": "raw",
}

# ============================================================================
# Products-Specific Parameters
# ============================================================================

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
    "CERRAURB": "observation",
    "CERRARUR": "observation",
    "CARRA": "observation",
    "CPC": "observation",
    "BERKELEY": "observation",
    "SSTSAT": "observation",
}

# Trend calculation enabled per project (used in config['products'][product_key]['magnitudes']['trends'])
# Only enabled for observation projects with type="trends"
PROJECT_TRENDS = {
    "ERA5": True,
    "ERA5-Land": True,
    "E-OBS": True,
    "ORAS5": True,
    "CERRA": True,
    "CERRAURB": True,
    "CERRARUR": True,
    "CARRA": True,
    "CPC": True,
    "BERKELEY": True,
    "SSTSAT": True,
    # All projection projects: False (default)
}

# Robustness calculation per project (used in config['products'][product_key]['magnitudes']['anom_emergence'])
# Simple boolean - True for projections, False for observations
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
    "CERRAURB": False,
    "CERRARUR": False,
    "CARRA": False,
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
        "WMO1": "1961-1990",
        "WMO2": "1981-2010",
        "WMO3": "1991-2020"
    },
    "CERRA": {
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
    "CERRARUR": {
        "AR5": "1986-2005",
        "AR6": "1995-2014",
        "WMO2": "1981-2010",
        "WMO3": "1991-2020"
    },
    "CPC": {
        "AR5": "1986-2005",
        "AR6": "1995-2014",
        "WMO1": "1961-1990",
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

# Climatology periods for projections (used in config['products'][product_key]['periods'])
CLIMATOLOGY_PERIODS = {
    "near": "2021-2040",
    "medium": "2041-2060",
    "long": "2081-2100"
}

# ============================================================================
# Helper Functions
# ============================================================================

def get_project_root(project):
    """Get root directory for a project."""
    return PROJECT_ROOTS.get(project, "None")


def is_observation_project(project):
    """Check if project is an observation dataset."""
    return project in OBSERVATION_PROJECTS


def is_projection_project(project):
    """Check if project is a projection dataset."""
    return project in PROJECTION_PROJECTS


def get_project_experiments(project):
    """Get list of experiments for a project."""
    return PROJECT_EXPERIMENTS.get(project, ["None"])


def get_project_periods(project):
    """Get historical and future periods for a project."""
    return PROJECT_PERIODS.get(project, {"hist": None, "fut": None})


def get_project_domains(project):
    """Get list of domains for a project."""
    return PROJECT_DOMAINS.get(project, ["None"])


def get_scenario_lines(project, main_experiment="None"):
    """
    Get scenario line configuration for a project.
    
    Used in config['products'][product_key]['scenarios']
    
    Returns dictionary with:
    - main: main experiment scenario
    - baseline: baseline scenario (historical or fullperiod)
    - fill_baseline: list of scenarios to fill baseline
    """
    Dict = {}
    
    if is_observation_project(project):
        Dict["main"] = None
        Dict["baseline"] = None
        Dict["fill_baseline"] = None
        
    elif is_projection_project(project):
        Dict["main"] = main_experiment
        
        # Note: fullperiod variables are handled in get_scenario_lines_dict
        Dict["baseline"] = "historical"
        
        if project == "CMIP6":
            if main_experiment == "ssp119":
                Dict["fill_baseline"] = ["ssp119", "ssp126", "ssp245", "ssp370", "ssp585"]
            else:
                Dict["fill_baseline"] = ["ssp126", "ssp245", "ssp370", "ssp585"]
        elif project in ["CORDEX-CORE", "CORDEX-CORERUR", "CORDEX-COREURB"]:
            Dict["fill_baseline"] = ["rcp26", "rcp85"]
        else:
            Dict["fill_baseline"] = ["rcp26", "rcp45", "rcp85"]
    else:
        raise ValueError(f"Scenarios not defined for project {project}")
            
    return Dict


def get_warming_levels(project):
    """
    Get warming levels configuration for a project.
    
    Used in config['products'][product_key]['warming_levels']
    
    Returns:
        tuple: (levels_list, warming_file_path) or ([], None) for observations
    """
    if is_projection_project(project):
        warming_levels = [1.5, 2, 3, 4]
        if project == "CMIP6":
            warming_file = "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/resources/resources/warming_levels/CMIP6_WarmingLevels.csv"
        else:
            warming_file = "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/resources/resources/warming_levels/CMIP5_WarmingLevels.csv"
        return warming_levels, warming_file
    else:
        return [], None


def get_spatial_mask(project, variable):
    """
    Get spatial mask file path for a project/variable combination.
    
    Used in config['data'][0]['spatial_mask']
    
    Returns:
        str or None: Path to spatial mask file
    """
    if "CORDEX-EUR-11" in project:
        if "bals" in variable or "baisimip" in variable:
            return "/lustre/gmeteo/WORK/chantreuxa/cica/data/resources/reference-grids/CORDEX-EUR-11_EuropeOnly.nc"
        else:
            return "/lustre/gmeteo/WORK/chantreuxa/cica/data/resources/reference-grids/CORDEX-EUR-11_domain_simplified.nc"
    elif project == "E-OBS":
        return "/lustre/gmeteo/WORK/chantreuxa/cica/data/resources/reference-grids/EOBS_EuropeOnly.nc"
    else:
        return None


def get_baseline_dict(project):
    """
    Get baseline periods dictionary for a project.
    
    Used in config['products'][product_key]['baselines']
    
    Returns:
        dict: Dictionary of baseline name -> period string
    """
    if project not in BASELINES:
        raise ValueError(f"Baselines not defined for project {project}")
    return BASELINES[project]


def get_period_climatology_dict(project, type, historical, baselines):
    """
    Get period climatology dictionary based on project type.
    
    Used in config['products'][product_key]['periods']
    
    Args:
        project: Project name
        type: Product type (climatology, temporal_series, trends)
        historical: Whether main experiment is historical
        baselines: Baseline periods dictionary
        
    Returns:
        dict: Dictionary of period names -> period strings
    """
    # For trends type, return baselines (trends are only for observations)
    if type == "trends":
        return baselines
    
    if is_projection_project(project) and not historical:
        return CLIMATOLOGY_PERIODS.copy()
    else:
        return baselines


def get_period_experiments_dict(project, variable, main_proj_experiment, dataset):
    """
    Get period experiments dictionary for a project.
    
    Used in config['data'][0]['period']
    
    Args:
        project: Project name
        variable: Variable name
        main_proj_experiment: Main project experiment
        dataset: Dataset object with load_period method
        
    Returns:
        dict or str: Dictionary of experiment -> period string, or single period string for observations
    """
    hist, fut = dataset.load_period(variable, version="v2")
    
    hist_period = f"{hist[0]}-{hist[-1]}"
    
    if is_observation_project(project):
        if project == "BERKELEY":
            return "1960-2017"
        return hist_period
    
    if is_projection_project(project):
        if "fullperiod" in variable:
            fut_period = f"{hist[0]}-{fut[-1]}"
        else:
            fut_period = f"{fut[0]}-{fut[-1]}"
        
        period_dict = {}
        
        if project == "CMIP6":
            if main_proj_experiment == "ssp119":
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
        elif "CORDEX-EUR-11" in project or "CORDEX-CORE" in project or project == "CMIP5":
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
    
    else:
        raise ValueError(f"Period not defined for project {project}")


def get_scenario_lines_dict(project, main_proj_experiment, variable):
    """
    Get scenario lines dictionary with variable-specific adjustments.
    
    This wraps get_scenario_lines and handles fullperiod variable logic.
    
    Args:
        project: Project name
        main_proj_experiment: Main project experiment
        variable: Variable name
        
    Returns:
        dict: Scenario lines dictionary
    """
    scenario_dict = get_scenario_lines(project, main_proj_experiment)
    
    # Adjust baseline for fullperiod variables
    if is_projection_project(project) and "fullperiod" in variable:
        scenario_dict["baseline"] = main_proj_experiment
    
    return scenario_dict


def get_data_type(project):
    """
    Get data type for a project.
    
    Used in config['data'][0]['type']
    
    Returns:
        str: "observation" or "projection"
    """
    return PROJECT_DATA_TYPE.get(project, "observation" if is_observation_project(project) else "projection")


def get_trend_enabled(project, type):
    """
    Check if trend calculation is enabled for a project.
    
    Used in config['products'][product_key]['magnitudes']['trends']
    
    Args:
        project: Project name
        type: Product type (trends, climatology, temporal_series)
        
    Returns:
        bool: True if trends should be calculated
    """
    return PROJECT_TRENDS.get(project, False) and type == "trends"
