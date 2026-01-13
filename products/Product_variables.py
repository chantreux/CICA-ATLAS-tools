import load_parameters
# Variables not to be calculated
VAR_NOT_CALCULATED = [
    "spei6reference", "spi6reference", "tbaisimip", "txbaisimip", 
    "tnbaisimip", "prbaisimip", "tbals", "tnbals", "txbals"
]

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
        "default": ["txx","tnn","rx1day","rx5day","cdd"]
    }
}


def get_variables_for_version(project: str, version: str = "v2"):
    """
    Get the list of variables for a given project and version.
    
    Parameters
    ----------
    project : str
        Project name
    version : str
        Version identifier
    dataset : Dataset object, optional
        Dataset object to get project variables from
        
    Returns
    -------
    list of str
        List of variable names, excluding VAR_NOT_CALCULATED
    """
    dataset=load_parameters.Dataset(project,"")
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
        if dataset is None:
            raise ValueError("Dataset object required when using 'all' variables")
        var_list = dataset.check_vars_proj()
    else:
        var_list = var_config.copy()
    
    # Remove variables not to be calculated
    var_list = [v for v in var_list if v not in VAR_NOT_CALCULATED]
    
    return var_list