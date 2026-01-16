"""
Variable workflow configuration for CICA-ATLAS Products.

This module defines all variable lists used across different climate projects,
including base variable sets, project-specific combinations, and bias adjustment
variables.
"""

from .projects import PROJECTION_PROJECTS


# =============================================================================
# VARIABLE NAME ALIASES
# =============================================================================

VAR_NAME_ALIASES = {
    "r": "pr",
    "pet": "pethg",
    "r01": "r01mm",
    "r10": "r10mm",
    "r20": "r20mm"
}

# Variable base name to pipeline name mapping
VAR_TO_PIPELINE_INDEX= {
    "cdd": "cddcica",
    "hd": "hdcica",
    "cd": "cdcica",
    "spi6": "spi6cica",
    "spei6": "spei6cica",
    "psl": "pslcica",
    "pethg": "pethg85cicamean"
}

TEMPORAL_AGG_MAPPING = {
    "cdd": ["YS"],
    "hd": ["YS"],
    "cd": ["YS"],
    "t": ["MS"],
    "pr": ["MS"],
    "rsds": ["MS"],
    "sfcwind": ["MS"],
    "psl": ["MS"],
    "tx": ["MS"],
    "tn": ["MS"],
    "txx": ["MS"],
    "tx35": ["MS"],
    "tx40": ["MS"],
    "fd": ["MS"],
    "rx1day": ["MS"],
    "rx5day": ["MS"],
    "tnn": ["MS"],
    "r01mm": ["MS"],
    "sdii": ["MS"],
    "pethg": ["MS"],
    "tr": ["MS"],
    "dtr": ["MS"],
    "r10mm": ["MS"],
    "r20mm": ["MS"],
    "spi6": ["MS"],
    "spei6": ["MS"],
    "evspsbl": ["MS"],
}

MONTHLY_INPUT_INDEXES = [
    "spei6", "spi6", "spei6extremedry", "spei6severedry", 
    "spei6extremewet", "spei6severewet", "spi6extremedry", 
    "spi6severedry", "spi6extremewet", "spi6severewet"
]

# =============================================================================
# SPECIAL VARIABLE CATEGORIES
# =============================================================================

ANNUAL_ONLY_VARS = [
    "cd", "hd", "cdd", "cdbals", "hdbals",
    "cdbaisimip", "hdbaisimip", "cddbaisimip"
]

BIASADJUSTMENT_VARS = [
    "cddbaisimip", "fdbals", "cdbals", "hdbals", "txbals", "tnbals", "tbals",
    "tx35bals", "tx40bals", "tx35baisimip", "tx40baisimip", "fdbaisimip",
    "cdbaisimip", "hdbaisimip", "txbaisimip", "tnbaisimip", "tbaisimip",
    "r01mmbaisimip", "sdiibaisimip", "trbaisimip", "dtrbaisimip",
    "r10mmbaisimip", "r20mmbaisimip", "trbals", "dtrbals"
]

REFERENCE_VARS = ["spei6reference", "spi6reference"]


# =============================================================================
# BASE INDEXS SETS
# =============================================================================

# Temperature variables
_BASE_TEMP = [
    "t", "tn", "tx", "tnn", "txx", "tx35", "tx40",
    "tr", "dtr", "fd", "hd", "cd"
]

# Precipitation variables
_BASE_PRECIP = [
    "pr", "r01mm", "sdii", "r10mm", "r20mm",
    "rx1day", "rx5day", "cdd", "spi6"
]

# Ocean variables
_BASE_OCEAN = ["sst", "siconc"]

# Other atmospheric/surface variables
_BASE_OTHER = [
    "spei6", "pethg", "sfcwind", "psl", "huss", "prsn",
    "rsds", "rlds", "clt", "evspsbl", "mrro", "mrsos"
]

# =============================================================================
# BASE INPUT SETS
# =============================================================================

_INPUT_TEMP = ["tas", "tasmin", "tasmax"]
_INPUT_PRECIP = ["pr"]
_INPUT_OCEAN = ["sst", "siconc"]
_INPUT_OTHER = ["sfcwind", "psl", "huss", "prsn",
             "rsds", "rlds", "clt", "evspsbl", "mrro", "mrsos"]


# =============================================================================
# PROJECT-SPECIFIC BASE LISTS
# =============================================================================

_CORDEX_CORE_BASE = (
    _BASE_TEMP + _BASE_PRECIP +
    ["spei6", "pethg", "sfcwind", "huss", "rsds", "rlds", "clt", "evspsbl"]
)
_CORDEX_CORE_INPUT= _INPUT_TEMP+_INPUT_PRECIP+ ["sfcwind", "huss", "rsds", "rlds", "clt", "evspsbl"]

_CERRA_BASE = (
    _BASE_TEMP + _BASE_PRECIP +
    ["spei6", "pethg", "sfcwind", "psl", "prsn", "rsds", "rlds", "clt", "evspsbl"]
)
_CERRA_INPUT= _INPUT_TEMP+_INPUT_PRECIP+ ["sfcwind", "psl", "prsn", "rsds", "rlds", "clt", "evspsbl"]


# =============================================================================
# PROJECT VARIABLE DEFINITIONS
# =============================================================================

ALL_VAR_PROJECT = {
    # Global climate models
    "CMIP6": {
        "homogenization": _INPUT_TEMP+_INPUT_PRECIP+_INPUT_OTHER+_INPUT_OCEAN,
        "indices": (
            _BASE_TEMP + _BASE_PRECIP + _BASE_OCEAN +
            ["spei6", "pethg", "sfcwind", "psl", "huss", "prsn",
             "rsds", "rlds", "clt", "evspsbl", "mrro", "mrsos"]
        ),
    },
    
    "CMIP5": {
        "homogenization": _INPUT_TEMP+_INPUT_PRECIP+_INPUT_OTHER+_INPUT_OCEAN, 
        "indices": (
            _BASE_TEMP + _BASE_PRECIP + _BASE_OCEAN +
            ["spei6", "pethg", "sfcwind", "huss", "prsn",
             "rsds", "rlds", "clt", "evspsbl", "mrro", "mrsos", "psl"]
        ),
    },
    
    # Regional climate models
    "CORDEX-EUR-11": {
        "homogenization": _INPUT_TEMP+_INPUT_PRECIP+[ "sfcwind", "huss", "rsds", "rlds",
             "clt", "evspsbl", "mrro", "psl"],  
        "indices": (
            _BASE_TEMP + _BASE_PRECIP +
            ["spei6", "pethg", "sfcwind", "huss", "rsds", "rlds",
             "clt", "evspsbl", "mrro", "psl"]
        ),
    },
    
    "CORDEX-CORE": {
        "homogenization": _CORDEX_CORE_INPUT,
        "indices": _CORDEX_CORE_BASE,
    },
    
    "CORDEX-CORERUR": {
        "homogenization": _CORDEX_CORE_INPUT,
        "indices": _CORDEX_CORE_BASE,
    },
    
    "CORDEX-COREURB": {
        "homogenization": _CORDEX_CORE_INPUT, 
        "indices": _CORDEX_CORE_BASE,
    },
    
    # Reanalysis
    "ERA5": {
        "homogenization": _INPUT_TEMP+_INPUT_PRECIP+["sfcwind", "psl", "prsn",
             "rsds", "rlds", "clt", "evspsbl", "mrro", "mrsos"]+_INPUT_OCEAN,
        "indices": (
            _BASE_TEMP + _BASE_PRECIP + _BASE_OCEAN +
            ["spei6", "pethg", "sfcwind", "psl", "prsn",
             "rsds", "rlds", "clt", "evspsbl", "mrro", "mrsos"]
        ),
    },
    
    "ERA5-Land": {
        "homogenization": _INPUT_TEMP+_INPUT_PRECIP+["sfcwind", "prsn","rsds","rlds","evspsbl", "mrro", "mrsos"], 
        "indices": (
            _BASE_TEMP + _BASE_PRECIP +
            ["spei6", "pethg", "sfcwind", "prsn", "rsds", "rlds",
             "evspsbl", "mrro", "mrsos"]
        ),
    },
    
    "CERRA": {
        "homogenization": _CERRA_INPUT,
        "indices": _CERRA_BASE,
    },
    
    "CERRARUR": {
        "homogenization": _CERRA_INPUT,
        "indices": _CERRA_BASE,
    },
    
    "CERRAURB": {
        "homogenization": _CERRA_INPUT,
        "indices": _CERRA_BASE,
    },
    
    # Observations
    "E-OBS": {
        "homogenization": _INPUT_TEMP+_INPUT_PRECIP+ ["sfcwind", "psl", "rsds"],  
        "indices": (
            _BASE_TEMP + _BASE_PRECIP +
            ["spei6", "pethg", "sfcwind", "psl", "rsds"]
        ),
    },
    
    "ORAS5": {
        "homogenization": _INPUT_OCEAN,  
        "indices": _BASE_OCEAN,
    },
    
    "BERKELEY": {
        "homogenization":   _INPUT_TEMP,
        "indices": _BASE_TEMP,
    },
    
    "CPC": {
        "homogenization":   _INPUT_PRECIP,
        "indices": _BASE_PRECIP,
    },
    
    "SSTSAT": {
        "homogenization": ["sst"],
        "indices": ["sst"],
    }
}


# =============================================================================
# COMBINED VARIABLE LISTS
# =============================================================================

# All base variables combined
ALL_VAR = _BASE_TEMP + _BASE_PRECIP + _BASE_OCEAN + _BASE_OTHER

# Total number of variables
NUM_ALL_VAR = len(ALL_VAR)


# =============================================================================
# FUNCTIONS
# =============================================================================

def get_project_variables(project, include_bias_adjustment=True, use_pipeline_names=False, step="indices"):
    """
    Get the list of variables for a given project.
    
    Parameters
    ----------
    project : str
        Project name (e.g., "CMIP6", "ERA5", "CORDEX-CORE")
    include_bias_adjustment : bool, optional
        If True and project is a projection, add bias-adjusted variables
        that have their base variable in the project. Default is True.
    use_pipeline_names : bool, optional
        If True, transform base variable names to pipeline names using
        VAR_TO_PIPELINE_INDEX mapping. Default is False.
    step : str, optional
        Processing step: "indices" or "homogenization". Default is "indices".
    
    Returns
    -------
    list
        List of variable names for the project
    
    Raises
    ------
    ValueError
        If project is not found in ALL_VAR_PROJECT or step is invalid
    """
    if project not in ALL_VAR_PROJECT:
        raise ValueError(
            f"Project '{project}' not found in ALL_VAR_PROJECT. "
            f"Available projects: {list(ALL_VAR_PROJECT.keys())}"
        )
    
    if step not in ["indices", "homogenization"]:
        raise ValueError(f"Invalid step '{step}'. Must be 'indices' or 'homogenization'.")
    
    # Get variables for the specified step
    variables = list(ALL_VAR_PROJECT[project][step])
    
    # Add bias-adjusted variables if it's a projection project (only for indices)
    if step == "indices" and include_bias_adjustment and project in PROJECTION_PROJECTS:
        for ba_var in BIASADJUSTMENT_VARS:
            base_var = index_only(ba_var)
            if base_var in variables:
                variables.append(ba_var)
    
    # Transform to pipeline names if requested
    if use_pipeline_names:
        variables = [VAR_TO_PIPELINE_INDEX.get(var, var) for var in variables]
    
    return variables

def temporal_agg(var: str):
    """
    Return the temporal aggregation for a given variable.

    Parameters
    ----------
    var : str
        The variable name to get the temporal aggregation for.

    Returns
    -------
    list of str
        The temporal aggregation code(s) for the variable, e.g., ["MS"] or ["YS"].

    Raises
    ------
    ValueError
        If the variable is not defined in the mapping.
    """
    agg = TEMPORAL_AGG_MAPPING.get(var)
    if agg is None:
        raise ValueError(f"Variable '{var}' not found in temporal aggregation mapping.")
    return agg

def index_only(index):
    """Extract base variable name by removing bias adjustment suffix."""
    if "ba" in index:
        index = index.split("ba")[0]
    return index


def normalize_variable_name(var_name):
    """
    Normalize variable name to standard format.
    
    Parameters
    ----------
    var_name : str
        Variable name (may use alternative naming)
    
    Returns
    -------
    str
        Normalized variable name
    """
    return VAR_NAME_ALIASES.get(var_name, var_name)
