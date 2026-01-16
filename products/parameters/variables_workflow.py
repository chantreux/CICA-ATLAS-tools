"""
Variable workflow configuration for CICA-ATLAS Products.

This module defines all variable lists used across different climate projects,
including base variable sets, project-specific combinations, and bias adjustment
variables.
"""

from .projects import PROJECTION_PROJECTS


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

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
# BASE VARIABLE SETS
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
# PROJECT-SPECIFIC BASE LISTS
# =============================================================================

_CORDEX_CORE_BASE = (
    _BASE_TEMP + _BASE_PRECIP +
    ["spei6", "pethg", "sfcwind", "huss", "rsds", "rlds", "clt", "evspsbl"]
)

_CERRA_BASE = (
    _BASE_TEMP + _BASE_PRECIP +
    ["spei6", "pethg", "sfcwind", "psl", "prsn", "rsds", "rlds", "clt", "evspsbl"]
)


# =============================================================================
# PROJECT VARIABLE DEFINITIONS
# =============================================================================

ALL_VAR_PROJECT = {
    # Global climate models
    "CMIP6": (
        _BASE_TEMP + _BASE_PRECIP + _BASE_OCEAN +
        ["spei6", "pethg", "sfcwind", "psl", "huss", "prsn",
         "rsds", "rlds", "clt", "evspsbl", "mrro", "mrsos"]
    ),
    
    "CMIP5": (
        _BASE_TEMP + _BASE_PRECIP + _BASE_OCEAN +
        ["spei6", "pethg", "sfcwind", "huss", "prsn",
         "rsds", "rlds", "clt", "evspsbl", "mrro", "mrsos", "psl"]
    ),
    
    # Regional climate models
    "CORDEX-EUR-11": (
        _BASE_TEMP + _BASE_PRECIP +
        ["spei6", "pethg", "sfcwind", "huss", "rsds", "rlds",
         "clt", "evspsbl", "mrro", "psl"]
    ),
    
    "CORDEX-CORE": _CORDEX_CORE_BASE,
    "CORDEX-CORERUR": _CORDEX_CORE_BASE,
    "CORDEX-COREURB": _CORDEX_CORE_BASE,
    
    # Reanalysis
    "ERA5": (
        _BASE_TEMP + _BASE_PRECIP + _BASE_OCEAN +
        ["spei6", "pethg", "sfcwind", "psl", "prsn",
         "rsds", "rlds", "clt", "evspsbl", "mrro", "mrsos"]
    ),
    
    "ERA5-Land": (
        _BASE_TEMP + _BASE_PRECIP +
        ["spei6", "pethg", "sfcwind", "prsn", "rsds", "rlds",
         "evspsbl", "mrro", "mrsos"]
    ),
    
    "CERRA": _CERRA_BASE,
    "CERRARUR": _CERRA_BASE,
    "CERRAURB": _CERRA_BASE,
    
    # Observations
    "E-OBS": (
        _BASE_TEMP + _BASE_PRECIP +
        ["spei6", "pethg", "sfcwind", "psl", "rsds"]
    ),
    
    "ORAS5": _BASE_OCEAN,
    "BERKELEY": _BASE_TEMP,
    "CPC": _BASE_PRECIP,
    "SSTSAT": ["sst"]
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

def get_project_variables(project, include_bias_adjustment=True):
    """
    Get the list of variables for a given project.
    
    Parameters
    ----------
    project : str
        Project name (e.g., "CMIP6", "ERA5", "CORDEX-CORE")
    include_bias_adjustment : bool, optional
        If True and project is a projection, add bias-adjusted variables
        that have their base variable in the project. Default is True.
    
    Returns
    -------
    list
        List of variable names for the project
    
    Raises
    ------
    ValueError
        If project is not found in ALL_VAR_PROJECT
    """
    if project not in ALL_VAR_PROJECT:
        raise ValueError(
            f"Project '{project}' not found in ALL_VAR_PROJECT. "
            f"Available projects: {list(ALL_VAR_PROJECT.keys())}"
        )
    
    # Get base variables for the project
    variables = list(ALL_VAR_PROJECT[project])
    
    # Add bias-adjusted variables if it's a projection project
    if include_bias_adjustment and project in PROJECTION_PROJECTS:
        for ba_var in BIASADJUSTMENT_VARS:
            base_var = index_only(ba_var)
            if base_var in variables:
                variables.append(ba_var)
    
    return variables
