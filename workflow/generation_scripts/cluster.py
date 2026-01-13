from dataclasses import dataclass
from pathlib import Path


SUPPORTED_CLUSTERS = ["lustre", "gpfs", "local"]

@dataclass
class ClusterConfig:
    name: str
    job_template: Path
    partition: str

def get_cluster_config(cluster: str) -> ClusterConfig:
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

