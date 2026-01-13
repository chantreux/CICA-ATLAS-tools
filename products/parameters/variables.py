"""
Variable-level parameters for CICA-ATLAS Products module.

This module contains all variable-specific parameters including:
- Anomaly configuration (relative vs absolute)
- Time aggregation functions (mean, min, max, sum)
- Period aggregation for extremes
- Time filters (seasonal, monthly)
- Variable lists and classifications

Compatible with workflow/generation_scripts/ structure for future unification.
"""

import sys
import os
from ruamel.yaml import YAML

# Add parent directory to path to import load_parameters
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import load_parameters

# Variables that use relative anomaly instead of absolute
# (used in config['products'][product_key]['magnitudes'])
RELATIVE_ANOMALY_VARS = [
    "pr", "rx1day", "rx5day", "huss", "sfcwind", "evspsbl",
    "mrsos", "mrro", "rsds", "rlds", "tr", "r01mm", "r10mm",
    "r20mm", "sdii", "pethg"
]


def get_anomaly_dict(variable: str, project: str) -> dict:
    """
    Get anomaly configuration for a variable and project.
    
    Used in config['products'][product_key]['magnitudes'].
    
    Parameters
    ----------
    variable : str
        Variable name
    project : str
        Project name
        
    Returns
    -------
    dict
        Dictionary with anomaly configuration:
        - anomaly: "relative" or "absolute"
        - anom: True (always calculate absolute anomaly)
        - anom_consensus: True/False (consensus for projections only)
        - relanom: True/False (calculate relative anomaly)
        - relanom_consensus: True/False (consensus for projections only)
    """
    # Remove suffixes like 'bals' or 'baisimip'
    var_base = load_parameters.index_only(variable)
    
    result = {}
    
    # Determine anomaly type
    if var_base in RELATIVE_ANOMALY_VARS:
        result["anomaly"] = "relative"
    else:
        result["anomaly"] = "absolute"
    
    # Always calculate absolute anomaly
    result["anom"] = True
    result["anom_consensus"] = True
    
    # Activate relative anomaly if needed
    if result["anomaly"] == "relative":
        result["relanom"] = True
        result["relanom_consensus"] = True
    else:
        result["relanom"] = False
        result["relanom_consensus"] = False
    
    # Deactivate consensus for observation datasets
    if project not in load_parameters.proj_datasets():
        result["anom_consensus"] = False
        result["relanom_consensus"] = False
    
    return result


# =============================================================================
# TIME AGGREGATION
# =============================================================================

# Path to aggregation functions YAML file
AGG_FUNCTIONS_FILE = "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/resources/resources/metadata/agg-functions.yaml"


def get_time_aggregation(variable: str) -> str:
    """
    Get time aggregation function for a variable.
    
    Used in config['products'][product_key]['time_aggregation_stat'].
    
    Parameters
    ----------
    variable : str
        Variable name
        
    Returns
    -------
    str
        Aggregation function: "mean", "min", "max", or "sum"
        
    Raises
    ------
    ValueError
        If variable not found in aggregation file
    """
    yaml = YAML()
    
    # Remove suffixes like 'bals', 'baisimip', 'fullperiod' to get base variable
    var_base = load_parameters.index_only(variable)
    
    # Also remove 'fullperiod' suffix
    if "fullperiod" in var_base:
        var_base = var_base.replace("fullperiod", "")
    
    # Also remove 'reference' suffix
    if "reference" in var_base:
        var_base = var_base.replace("reference", "")
    
    # Try to load from file, fall back to hardcoded mapping if file doesn't exist

    with open(AGG_FUNCTIONS_FILE) as f:
        agg_dict = yaml.load(f)
    # Check both full variable name and base variable name
    if var_base in agg_dict.get("mean", []) or variable in agg_dict.get("mean", []):
        return "mean"
    elif var_base in agg_dict.get("min", []) or variable in agg_dict.get("min", []):
        return "min"
    elif var_base in agg_dict.get("max", []) or variable in agg_dict.get("max", []):
        return "max"
    elif var_base in agg_dict.get("sum", []) or variable in agg_dict.get("sum", []):
        return "sum"
    else:
        raise ValueError(f"Variable {variable} (base: {var_base}) not found in aggregation file {AGG_FUNCTIONS_FILE}")


# =============================================================================
# PERIOD AGGREGATION
# =============================================================================

# Period aggregation for extreme variables
# (used in config['products'][product_key]['period_aggregation_stat'])
EXTREME_PERIOD_AGGREGATION = {
    "tnn": "one_in_20_year_event_min",
    # All other extreme variables use max
    "default": "one_in_20_year_event_max"
}


def get_period_aggregation(variable: str, extreme: bool) -> str:
    """
    Get period aggregation statistic for a variable.
    
    Used in config['products'][product_key]['period_aggregation_stat'].
    
    Parameters
    ----------
    variable : str
        Variable name
    extreme : bool
        Whether this is an extreme product
        
    Returns
    -------
    str
        Period aggregation statistic
    """
    if not extreme:
        return "mean"
    else:
        if variable == "tnn":
            return EXTREME_PERIOD_AGGREGATION["tnn"]
        else:
            return EXTREME_PERIOD_AGGREGATION["default"]


# =============================================================================
# TIME FILTERS
# =============================================================================

# Variables that only support annual time filter
# (used in config['products'][product_key]['time_filters'])
ANNUAL_ONLY_VARS = [
    "cd", "hd", "cdd", "cdbals", "hdbals",
    "cdbaisimip", "hdbaisimip", "cddbaisimip"
]


def get_time_filters_variable(variable: str) -> dict:
    """
    Get time filters dictionary for a variable.
    
    Used in config['products'][product_key]['time_filters'].
    
    Parameters
    ----------
    variable : str
        Variable name
        
    Returns
    -------
    dict
        Dictionary mapping time filter names to month ranges
    """
    if variable in ANNUAL_ONLY_VARS:
        return {"Annual": "01-12"}
    else:
        return {
            "Annual": "01-12",
            "DecFeb": "12-02",
            "MarMay": "03-05",
            "JunAug": "06-08",
            "SepNov": "09-11",
            "Jan": "01-01",
            "Feb": "02-02",
            "Mar": "03-03",
            "Apr": "04-04",
            "May": "05-05",
            "Jun": "06-06",
            "Jul": "07-07",
            "Aug": "08-08",
            "Sep": "09-09",
            "Oct": "10-10",
            "Nov": "11-11",
            "Dec": "12-12"
        }


# =============================================================================
# VARIABLE LISTS AND CLASSIFICATIONS
# =============================================================================

# Variables not to be calculated
VAR_NOT_CALCULATED = [
    "spei6reference", "spi6reference", "tbaisimip", "txbaisimip",
    "tnbaisimip", "prbaisimip", "tbals", "tnbals", "txbals"
]

# Urban-specific variables
URBAN_VARS = [
    "t", "tx", "tn", "tnn", "txx", "tx35", "tx40", "tr", "dtr",
    "fd", "cd", "hd", "huss", "sfcwind", "rsds", "rlds"
]

# Land-only variables
LAND_ONLY_VARS = [
    "mrro", "mrsos", "tx35", "tx40", "tx35bals", "tx40bals",
    "tx35baisimip", "tx40baisimip"
]

# Ocean-only variables
OCEAN_ONLY_VARS = [
    "sst", "siconc"
]


# =============================================================================
# VERSION-SPECIFIC VARIABLE CONFIGURATIONS
# =============================================================================

# Version-specific variable configurations
VERSION_VARIABLES = {
    "v2": {
        # Default: use all project variables
        "default": "all"
    },
    "v1": {
        "default": "specific_v1_list"  # Define specific list if needed
    },
    "rural": {
        "CORDEX-EUR-11-RUR": ["t", "pr", "tx", "tn", "txx", "tnn", "fd", "tr",
                              "dtr", "rx1day", "rx5day", "r01mm", "r10mm",
                              "r20mm", "sdii", "cdd", "cd", "hd", "tx35",
                              "tx40", "rsds", "rlds", "sfcwind"]
    },
    "urban": {
        "CORDEX-EUR-11-URB": ["t", "pr", "tx", "tn", "txx", "tnn", "fd", "tr",
                              "dtr", "rx1day", "rx5day", "r01mm", "r10mm",
                              "r20mm", "sdii", "cdd", "cd", "hd", "tx35",
                              "tx40", "rsds", "rlds", "sfcwind"]
    },
    "all": {
        "default": "all"
    },
    "megacities": {
        "default": "all"
    },
    "v23": {
        "BERKELEY": "all",
        "CERRA": ["cdd", "evspsbl", "pethg", "pr", "prsn", "r01mm",
                  "r10mm", "r20mm", "rx1day", "rx5day", "rlds", "rsds",
                  "sdii", "spei6", "spi6"],
        "CMIP5": ["pethg"],
        "CMIP6": ["pethg"],
        "E-OBS": ["pethg"],
        "CORDEX-CORE": ["hd", "pethg"],
        "CORDEX-EUR-11": ["cddbaisimip", "fdbals", "cdbals", "hdbals",
                          "txbals", "tnbals", "tbals", "tx35bals", "tx40bals",
                          "cdbaisimip", "hdbaisimip", "pethg", "spei6", "spi6",
                          "clt", "evspsbl", "sfcwind"],
        "ERA5": "all",
        "ERA5-Land": "all"
    },
    "ERA5-Land_correction": {
        "ERA5-Land": ["t", "tx35", "tx40", "tx", "tn", "tnn", "txx",
                      "tr", "dtr", "fd", "hd", "cd", "pethg", "spei6"]
    },
    "cmip6poland": {
        "CMIP6": ["t", "pr", "tx", "tn", "txx", "tnn", "fd", "tr", "dtr",
                  "rx1day", "rx5day", "r01mm", "r10mm", "r20mm", "sdii",
                  "cdd", "cd", "hd", "tx35", "tx40", "rsds", "rlds",
                  "sfcwind", "pethg", "spei6", "spi6"]
    },
    "extremes": {
        "default": ["txx", "tnn", "rx1day", "rx5day", "cdd"]
    }
}


def get_variables_for_version(project: str, version: str = "v2") -> list:
    """
    Get the list of variables for a given project and version.
    
    Parameters
    ----------
    project : str
        Project name
    version : str
        Version identifier
        
    Returns
    -------
    list of str
        List of variable names, excluding VAR_NOT_CALCULATED
        
    Raises
    ------
    ValueError
        If version is unknown or dataset object required but not available
    """
    dataset = load_parameters.Dataset(project, "")
    
    if version not in VERSION_VARIABLES:
        raise ValueError(f"Unknown version: {version}")
    
    version_config = VERSION_VARIABLES[version]
    
    # Check if project-specific config exists
    if project in version_config:
        var_config = version_config[project]
    else:
        var_config = version_config.get("default", "all")
    
    # Get variable list
    if var_config == "all":
        var_list = dataset.check_vars_proj()
    else:
        var_list = var_config.copy()
    
    # Remove variables not to be calculated
    var_list = [v for v in var_list if v not in VAR_NOT_CALCULATED]
    
    return var_list
