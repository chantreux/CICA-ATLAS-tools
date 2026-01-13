"""
Variable-level parameters for CICA-ATLAS Products module.

This module contains all variable-specific configuration:
- Anomaly types (relative vs absolute)
- Time aggregation functions
- Period aggregation functions
- Time filters (seasonal/monthly selections)
- Variable categorizations (urban, land-only, ocean-only, etc.)
"""

from ruamel.yaml import YAML
import load_parameters

yaml = YAML()
yaml.preserve_quotes = True
yaml.default_flow_style = False

# ============================================================================
# Anomaly Configuration
# ============================================================================

# Variables that use relative anomaly (percentages) instead of absolute differences
# Used in config['products'][product_key]['magnitudes']['relanom']
RELATIVE_ANOMALY_VARS = [
    "pr", "rx1day", "rx5day", "huss", "sfcwind", "evspsbl",
    "mrsos", "mrro", "rsds", "rlds", "tr", "r01mm", "r10mm",
    "r20mm", "sdii", "pethg"
]


def get_anomaly_dict(variable, project):
    """
    Get anomaly configuration dictionary for a variable.
    
    Used in config['products'][product_key]['magnitudes']
    
    Args:
        variable: Variable name
        project: Project name (to determine if consensus should be enabled)
        
    Returns:
        dict: Anomaly configuration with keys:
            - anomaly: "relative" or "absolute"
            - anom: bool (always True)
            - anom_consensus: bool (True for projections, False for observations)
            - relanom: bool (True if relative anomaly variable)
            - relanom_consensus: bool (True for projections + relative vars)
    """
    Dict = {}
    
    # Remove bals/baisimip suffixes for checking
    var = load_parameters.index_only(variable)
    
    # Determine anomaly type
    if var in RELATIVE_ANOMALY_VARS:
        Dict["anomaly"] = "relative"
    else:
        Dict["anomaly"] = "absolute"

    # Always calculate absolute anomaly
    Dict["anom"] = True
    Dict["anom_consensus"] = True

    # Activate relative anomaly if needed
    if Dict["anomaly"] == "relative":
        Dict["relanom"] = True
        Dict["relanom_consensus"] = True
    else:
        Dict["relanom"] = False
        Dict["relanom_consensus"] = False

    # Deactivate consensus when not a projection dataset
    if project not in load_parameters.proj_datasets():
        Dict["anom_consensus"] = False
        Dict["relanom_consensus"] = False

    return Dict


# ============================================================================
# Time Aggregation
# ============================================================================

# Path to aggregation functions YAML file
AGG_FUNCTIONS_FILE = "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/resources/resources/metadata/agg-functions.yaml"


def get_time_aggregation(variable):
    """
    Get time aggregation function for a variable.
    
    Used in config['products'][product_key]['time_aggregation_stat']
    
    Args:
        variable: Variable name
        
    Returns:
        str: Aggregation function ("mean", "min", "max", "sum")
    """
    with open(AGG_FUNCTIONS_FILE) as f:
        agg_dict = yaml.load(f)
    
    if variable in agg_dict["mean"]:
        return "mean"
    elif variable in agg_dict["min"]:
        return "min"
    elif variable in agg_dict["max"]:
        return "max"
    elif variable in agg_dict["sum"]:
        return "sum"
    else:
        raise ValueError(f"Variable {variable} not found in aggregation file {AGG_FUNCTIONS_FILE}")


# ============================================================================
# Period Aggregation
# ============================================================================

# Period aggregation for extreme variables
# Used in config['products'][product_key]['period_aggregation_stat']
EXTREME_PERIOD_AGGREGATION = {
    "tnn": "one_in_20_year_event_min",
    # All other extreme variables use max
    "default": "one_in_20_year_event_max"
}


def get_period_aggregation(variable, extreme):
    """
    Get period aggregation function for a variable.
    
    Used in config['products'][product_key]['period_aggregation_stat']
    
    Args:
        variable: Variable name
        extreme: Boolean indicating if this is an extreme calculation
        
    Returns:
        str: Aggregation function ("mean", "one_in_20_year_event_min", "one_in_20_year_event_max")
    """
    if not extreme:
        return "mean"
    else:
        if variable == "tnn":
            return EXTREME_PERIOD_AGGREGATION["tnn"]
        else:
            return EXTREME_PERIOD_AGGREGATION["default"]


# ============================================================================
# Time Filters
# ============================================================================

# Variables that only support annual time filters (no seasonal/monthly)
# Used in get_time_filters_dict()
ANNUAL_ONLY_VARS = [
    "cd", "hd", "cdd", "cdbals", "hdbals",
    "cdbaisimip", "hdbaisimip", "cddbaisimip"
]


def get_time_filters_dict(variable):
    """
    Get time filters dictionary for a variable.
    
    Used in config['products'][product_key]['time_filters']
    
    Args:
        variable: Variable name
        
    Returns:
        dict: Dictionary mapping filter names to month ranges
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


# ============================================================================
# Variable Categories
# ============================================================================

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

# Land-only variables (cannot be calculated over ocean)
LAND_ONLY_VARS = [
    "mrro", "mrsos", "tx35", "tx40", "tx35bals", "tx40bals",
    "tx35baisimip", "tx40baisimip"
]

# Ocean-only variables (cannot be calculated over land)
OCEAN_ONLY_VARS = [
    "sst", "siconc"
]

# Version-specific variable configurations
# From Product_variables.py
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


def get_variables_for_version(project, version="v2"):
    """
    Get the list of variables for a given project and version.
    
    Args:
        project: Project name
        version: Version identifier
        
    Returns:
        list: List of variable names, excluding VAR_NOT_CALCULATED
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
