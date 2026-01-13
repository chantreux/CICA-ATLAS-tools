"""
Project-product parameters for CICA-ATLAS Products module.

This module contains product-specific project parameters including:
- Baselines and climatology periods
- Scenario configurations
- Warming levels
- Spatial masks
- Region masks

Depends on projects.py for core project definitions.
Compatible with workflow/generation_scripts/ structure for future unification.
"""

from typing import Dict, List, Tuple, Optional, Union

# Import from projects.py (using relative import since they're in the same package)
from .projects import (
    CANONICAL_PROJECTS,
    OBSERVATION_PROJECTS,
    PROJECTION_PROJECTS,
    PROJECT_ALIASES,
    PROJECT_PERIODS,
    is_observation_project,
    is_projection_project,
)


# =============================================================================
# CONSTANTS
# =============================================================================

# Climatology periods for projection projects (used in config['products'][product_key]['periods'])
CLIMATOLOGY_FUTURE_PERIODS = {
    "near": "2021-2040",
    "medium": "2041-2060",
    "long": "2081-2100"
}

# Region mask files per set
REGION_MASKS = {
    "AR6": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/resources/resources/reference-regions/IPCC-WGI-reference-regions-v4_areas.geojson",
    "eucra": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/resources/resources/reference-regions/EUCRA_areas.geojson",
    "european-countries": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/resources/resources/reference-regions/european-countries_areas.geojson",
    "megacities": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/resources/resources/reference-regions/megacities.geojson",
    "cities-rural": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/resources/resources/reference-regions/cities_contour.geojson",
    "cities-urban": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/resources/resources/reference-regions/cities_contour.geojson"
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


def generate_baselines_project(project: str) -> Dict[str, str]:
    """
    Generate baseline periods dictionary for a project.
    
    Parameters
    ----------
    project : str
        Project name (canonical or alias)
        
    Returns
    -------
    Dict[str, str]
        Dictionary of baseline periods
    """
    canonical = PROJECT_ALIASES.get(project, project)
    
    # Common baselines for all projects
    baselines = {
        "AR5": "1986-2005",
        "AR6": "1995-2014",
        "WMO2": "1981-2010",
        "WMO3": "1991-2020"
    }
    
    # Add preIndustrial for projection projects
    if canonical in PROJECTION_PROJECTS:
        baselines["preIndustrial"] = "1850-1900"
    
    # Add WMO1 for most projects (exclude ORAS5, CERRA*, CPC, BERKELEY, SSTSAT)
    excluded_from_wmo1 = ["ORAS5", "CERRA", "CERRARUR", "CERRAURB", "CPC", "BERKELEY", "SSTSAT"]
    if canonical not in excluded_from_wmo1:
        baselines["WMO1"] = "1961-1990"
    
    return baselines

def get_baseline_project(project: str) -> Dict[str, str]:
    """
    Get baseline periods dictionary for a project.
    
    Parameters
    ----------
    project : str
        Project name
        
    Returns
    -------
    Dict[str, str]
        Dictionary of baseline periods
        
    Raises
    ------
    ValueError
        If baselines not defined for project
    """
    canonical = PROJECT_ALIASES.get(project, project)
    
    if canonical not in PROJECT_BASELINES:
        raise ValueError(f"Baselines not defined for project {project}")
    
    return PROJECT_BASELINES[canonical]





def get_scenario_lines(project: str, main_experiment: str = "None") -> dict:
    """
    Get scenario line configuration for a project.
    
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

def get_scenario_lines_project_var(project: str, main_experiment: str, variable: str) -> dict:
    """
    Get scenario lines dictionary with variable-specific adjustments.
        
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

def get_warming_levels(project: str) -> tuple:
    """
    Get warming levels and file path for a project.
    
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




def get_period_climatology(project: str, product_type: str, 
                                 is_historical: bool, baselines: Dict[str, str]) -> Dict[str, str]:
    """
    Get period climatology dictionary based on product type and project.
    
   
    Parameters
    ----------
    project : str
        Project name
    product_type : str
        Type of product ("climatology", "temporal_series", "trends")
    is_historical : bool
        Whether main experiment is historical
    baselines : Dict[str, str]
        Baseline periods dictionary
        
    Returns
    -------
    Dict[str, str]
        Dictionary of climatology periods, or empty dict for trends
        
    Raises
    ------
    ValueError
        If product type is invalid
    """
    if product_type not in ["climatology", "temporal_series", "trends"]:
        raise ValueError(f"Invalid product type: {product_type}")
    
    # Trends type doesn't use climatology periods
    if product_type == "trends":
        return {}
    
    canonical = PROJECT_ALIASES.get(project, project)
    
    # For projection datasets (non-historical runs)
    if canonical in PROJECTION_PROJECTS and not is_historical:
        return CLIMATOLOGY_FUTURE_PERIODS.copy()
    else:
        # For observation datasets or historical runs, use baselines
        return baselines.copy()


def get_period_experiments(project: str, variable: str, 
                                 main_experiment: str) -> Union[Dict[str, str], str]:
    """
    Get period information for experiments.
       
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
    Union[Dict[str, str], str]
        Dictionary mapping experiments to periods, or single period string
    """
    canonical = PROJECT_ALIASES.get(project, project)
    
    periods = PROJECT_PERIODS.get(canonical, {"hist": (None, None), "fut": (None, None)})
    hist = periods.get("hist", (None, None))
    fut = periods.get("fut", (None, None))
    hist_period = f"{hist[0]}-{hist[1]}"
    
    # For observation datasets
    if canonical in OBSERVATION_PROJECTS:
        if canonical == "BERKELEY":
            return "1960-2017"
        return hist_period
    
    # For projection datasets
    if canonical in PROJECTION_PROJECTS:
        if "fullperiod" in variable:
            fut_period = f"{hist[0]}-{fut[1]}"
        else:
            fut_period = f"{fut[0]}-{fut[1]}"
        
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




def get_region_mask(set_name: str) -> str:
    """
    Get region mask file path for a set.
    
    Parameters
    ----------
    set_name : str
        Set name (e.g., "AR6", "eucra", "european-countries")
        
    Returns
    -------
    str or None
        Path to region mask file, or None if not found
    """
    return REGION_MASKS.get(set_name)


# =============================================================================
# GENERATED DICTIONARIES
# =============================================================================

# Generate PROJECT_TRENDS dictionary for backward compatibility
PROJECT_TRENDS = {project: is_observation_project(project) for project in CANONICAL_PROJECTS}
PROJECT_BASELINES = {project: generate_baselines_project(project) for project in CANONICAL_PROJECTS}
PROJECT_ROBUSTNESS = {project: is_projection_project(project) for project in CANONICAL_PROJECTS}

