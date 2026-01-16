
# In variables.py or a similar config file
TEMPORAL_AGG_MAPPING = {
    "cddcica": ["YS"],
    "hdcica": ["YS"],
    "cdcica": ["YS"],
    "t": ["MS"],
    "pr": ["MS"],
    "rsds": ["MS"],
    "sfcwind": ["MS"],
    "pslcica": ["MS"],
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
    "pethg85cicamean": ["MS"],
    "tr": ["MS"],
    "dtr": ["MS"],
    "r10mm": ["MS"],
    "r20mm": ["MS"],
    "spi6cica": ["MS"],
    "spei6cica": ["MS"],
    "evspsbl": ["MS"],
}


MONTHLY_INPUT_INDEXES = ["spei6cica","spi6cica"]

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


# Step definitions per project
PROJECT_STEPS = {
    "ERA5": ["homogenization", "indices"],
    "CERRA-Land": ["homogenization", "interpolation", "indices"],
    "E-OBS": ["homogenization", "interpolation", "indices"],
}


# Base variables per project (for homogenization and indices)
BASE_PROJECT_VARIABLES = {
    "E-OBS": {
        "homogenization": ["pr","tasmax","tasmin","tas","sfcwind","rsds","psl"],
        "indices": [
            "cdcica","hdcica","t","pr","cddcica","rsds","pslcica",
            "sfcwind","rx1day","tn","tx","txx","tx35","tx40","fd",
            "rx5day","tnn","r01mm","sdii","pethg85cicamean","tr",
            "dtr","r10mm","r20mm","spi6cica","spei6cica",
        ],
    },
    "CERRA-Land": {
        "homogenization": ["pr","tasmax","tasmin","tas","evspsbl","rsds","rlds"],
        "indices": [
            "pr","evspsbl","rx1day","rx5day","r01mm","r10mm",
            "r20mm","cddcica","sdii","spi6cica"
        ],
    },
    "ERA5": {
        "homogenization": ["pr","tasmax","tasmin","tas"],
        "indices": ["pr","tasmax","tasmin","tas"],
    },
}



