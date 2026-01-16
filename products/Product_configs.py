from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path
@dataclass
class VersionConfig:
    """Configuration for a specific product version."""
    name: str
    projects: List[str]
    sets: List[str]
    trends: bool
    climatology: bool
    input_folder: str
    output_folder: str
    experiments: Optional[List[str]] = None


# Version configurations
VERSION_CONFIGS = {
    "dry": VersionConfig(
        name="dry",
                projects=["ERA5"],
        sets=[],
        trends=False,
        climatology=True,
        input_folder="/lustre/gmeteo/WORK/PROYECTOS/2022_C3S_Atlas/workflow/datasets/CICAv2_refactored/CICAv2.5_refactored-extremes/raw/c3s-atlas-dataset",
        output_folder="/lustre/gmeteo/WORK/PROYECTOS/2022_C3S_Atlas/workflow/products/CICAv2/v20231017/dry_all/"
    ),
    "extremes": VersionConfig(
        name="extremes",
        projects=["CPC", "BERKELEY", "E-OBS", "CORDEX-EUR-11", 
                  "CORDEX-CORE", "CMIP5", "CERRA", "ERA5", 
                  "ERA5-Land", "CMIP6"],
        sets=[],
        trends=False,
        climatology=True,
        input_folder="/lustre/gmeteo/WORK/PROYECTOS/2022_C3S_Atlas/workflow/datasets/CICAv2.0_refactored/compressed_v2/c3s-atlas-dataset",
        output_folder="/lustre/gmeteo/WORK/PROYECTOS/2022_C3S_Atlas/workflow/products/CICAv2/v20231017/extremes_all/"
    ),
    "ssp119": VersionConfig(
        name="ssp119",
        projects=["CMIP6"],
        sets=["eucra", "european-countries", "AR6", "megacities"],
        trends=False,
        climatology=True,
        input_folder="None",
        output_folder="None",
        experiments=["ssp119"]
    ),
    "v23": VersionConfig(
        name="v23",
        projects=["CPC", "BERKELEY", "E-OBS", "CORDEX-EUR-11", 
                  "CORDEX-CORE", "CMIP5", "CERRA", "ERA5", 
                  "ERA5-Land", "CMIP6"],
        sets=["eucra", "european-countries", "AR6"],
        trends=False,
        climatology=True,
        input_folder="None",
        output_folder="None"
    ),
    "megacities": VersionConfig(
        name="megacities",
        projects=["CMIP6"],
        sets=["megacities"],
        trends=False,
        climatology=True,
        input_folder="None",
        output_folder="None"
    ),
    "rural": VersionConfig(
        name="rural",
        projects=["CORDEX-EUR-11-RUR"],
        sets=["eucra", "european-countries", "AR6"],
        trends=False,
        climatology=True,
        input_folder="None",
        output_folder="None"
    ),
    "urban": VersionConfig(
        name="urban",
        projects=["CORDEX-EUR-11-URB"],
        sets=["eucra", "european-countries", "AR6"],
        trends=False,
        climatology=True,
        input_folder="None",
        output_folder="None"
    ),
    "all": VersionConfig(
        name="all",
        projects=["CPC", "BERKELEY", "E-OBS", "CORDEX-EUR-11", 
                  "CORDEX-CORE", "CMIP5", "CERRA", "ERA5", 
                  "ERA5-Land", "CMIP6"],
        sets=["eucra", "european-countries", "AR6"],
        trends=False,
        climatology=True,
        input_folder="None",
        output_folder="None"
    ),
    "cmip6poland": VersionConfig(
        name="cmip6poland",
        projects=["CMIP6"],
        sets=["cities-urban", "cities-rural"],
        trends=False,
        climatology=True,
        input_folder="None",
        output_folder="None"
    ),
    "ERA5-Land_correction": VersionConfig(
        name="ERA5-Land_correction",
        projects=["ERA5-Land"],
        sets=[],
        trends=False,
        climatology=True,
        input_folder="/lustre/gmeteo/WORK/PROYECTOS/2022_C3S_Atlas/workflow/datasets/CICAv2.0_refactored/compressed_v2/ERA5-Land_correction/c3s-atlas-dataset",
        output_folder="/lustre/gmeteo/WORK/PROYECTOS/2022_C3S_Atlas/workflow/products/CICAv2/ERA5-Land_correction/"
    )
}


def get_version_config(version: str) -> VersionConfig:
    """
    Get configuration for a specific version.
    
    Parameters
    ----------
    version : str
        Version identifier
        
    Returns
    -------
    VersionConfig
        Configuration object for the version
        
    Raises
    ------
    ValueError
        If version is not found
    """
    if version not in VERSION_CONFIGS:
        raise ValueError(f"Unknown version: {version}. Available versions: {list(VERSION_CONFIGS.keys())}")
    return VERSION_CONFIGS[version]


def list_available_versions() -> List[str]:
    """Return list of available version names."""
    return list(VERSION_CONFIGS.keys())

def get_output_path(version: str, product_type: str, project: str, var: str) -> str:
    """
    Get the output path for a specific version, product type, project and variable.
    
    The path is constructed as: {output_folder}/{product_type}/{project}/{var}/
    
    Parameters
    ----------
    version : str
        Version identifier (e.g., "v23", "ssp119")
    product_type : str
        Type of product ("climatology", "trends", "temporal_series")
    project : str
        Project name
    var : str
        Variable name
        
    Returns
    -------
    str
        Output path, or "None" if version doesn't exist
    """
    if version not in VERSION_CONFIGS:
        return "None"
    
    config = VERSION_CONFIGS[version]
    
    # Handle special case where output_folder is "None"
    if config.output_folder == "None":
        return "None"
    
    # Construct path: {output_folder}/{product_type}/{project}/{var}/
    output_path = Path(config.output_folder) / product_type / project / var
    
    return str(output_path) + "/"

def check_existing_files(path_data: str, var: str, experiment: str, 
                        project: str, is_observation: bool, 
                        file_extension: str = "nc", set_name: str = None,
                        return_pattern: bool = False) -> bool:
    """
    Check if output files already exist.
    
    Parameters
    ----------
    path_data : str
        Base path to check for files
    var : str
        Variable name
    experiment : str
        Experiment name
    project : str
        Project name
    is_observation : bool
        Whether project is observational
    file_extension : str
        File extension to check (nc, csv)
    set_name : str, optional
        Set name for temporal series
    return_pattern : bool, optional
        If True, return the search pattern along with the result
        
    Returns
    -------
    bool or tuple
        If return_pattern is False: True if files exist, False otherwise
        If return_pattern is True: (bool, str) tuple with existence status and pattern
    """
    if path_data == "None":
        pattern = "N/A (path_data is 'None')"
        return (False, pattern) if return_pattern else False
    
    path = Path(path_data)
    if not path.exists():
        pattern = f"N/A (path does not exist: {path_data})"
        return (False, pattern) if return_pattern else False
    
    # Build search pattern
    if is_observation:
        if set_name:
            pattern = f'*{var}*{set_name}.{file_extension}'
        else:
            pattern = f'*{var}*.{file_extension}'
    else:
        if set_name:
            pattern = f'*{var}*{experiment}*{set_name}.{file_extension}'
        else:
            pattern = f'*{var}*{experiment}*.{file_extension}'
    
    file_list = list(path.rglob(pattern))
    
    exists = len(file_list) > 0
    
    if return_pattern:
        return (exists, str(path) + "/" + pattern)
    return exists

