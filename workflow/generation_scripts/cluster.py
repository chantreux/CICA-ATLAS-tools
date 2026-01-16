from dataclasses import dataclass
from pathlib import Path


# =============================================================================
# SUPPORTED CLUSTERS
# =============================================================================

SUPPORTED_CLUSTERS = ["lustre", "gpfs", "local"]


# =============================================================================
# JOB PARAMETERS BY STEP
# =============================================================================

# Default job parameters for each processing step
JOB_PARAMETERS = {
    "homogenization": {
        "procs": "1",
        "time_limit": "72:00:00",
        "ram": "20G"
    },
    "biasadjustment": {
        "historical": {
            "procs": "4",
            "time_limit": "72:00:00",
            "ram": "5G"
        },
        "rcp": {
            "procs": "4",
            "time_limit": "72:00:00",
            "ram": "10G"
        }
    },
    "indices": {
        "procs": "1",
        "time_limit": "72:00:00",
        "ram": "30G"
    },
    "range-skewness": {
        "historical": {
            "procs": "1",
            "time_limit": "72:00:00",
            "ram": "30G"
        },
        "rcp": {
            "procs": "1",
            "time_limit": "72:00:00",
            "ram": "50G"
        }
    },
    "tasmaxba-tasminba": {
        "historical": {
            "procs": "1",
            "time_limit": "72:00:00",
            "ram": "30G"
        },
        "rcp": {
            "procs": "1",
            "time_limit": "72:00:00",
            "ram": "50G"
        }
    }
}


# =============================================================================
# CLUSTER CONFIGURATION
# =============================================================================

@dataclass
class ClusterConfig:
    name: str
    job_template: Path
    partition: str


def get_cluster_config(cluster: str) -> ClusterConfig:
    """
    Get cluster configuration for a given cluster name.
    
    Parameters
    ----------
    cluster : str
        Cluster name (must be in SUPPORTED_CLUSTERS)
    
    Returns
    -------
    ClusterConfig
        Cluster configuration object
    
    Raises
    ------
    ValueError
        If cluster is not supported
    """
    if cluster == "lustre":
        return ClusterConfig(
            name="lustre",
            job_template="Job_template_lustre.sh",
            partition="meteo_long"
        )
    if cluster == "gpfs":
        return ClusterConfig(
            name="gpfs",
            job_template="Job_template_gpfs.sh",
            partition="wncompute_ifca"
        )
    raise ValueError(f"Unsupported cluster: {cluster}")


def get_job_parameters(step: str, experiment: str = None) -> dict:
    """
    Get job parameters for a given processing step and experiment.
    
    Parameters
    ----------
    step : str
        Processing step name
    experiment : str, optional
        Experiment name (used for some steps to determine parameters)
    
    Returns
    -------
    dict
        Dictionary with keys: procs, time_limit, ram
    """
    if step not in JOB_PARAMETERS:
        return {}
    
    params = JOB_PARAMETERS[step]
    
    # Handle steps with experiment-specific parameters
    if isinstance(params, dict) and "procs" not in params:
        # This step has nested experiment configs
        if experiment and "historical" in experiment:
            return params.get("historical", {})
        elif experiment and "rcp" in experiment:
            return params.get("rcp", {})
        # Default to first available if no match
        return params.get("historical", params.get("rcp", {}))
    
    return params

