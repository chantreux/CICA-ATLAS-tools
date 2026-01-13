
import numpy as np
import glob
import os
import xarray as xr

def load_root_directories(dataset_list, domain, project_list):
    """
    Load root directories for each dataset.

    Parameters:
    - dataset_list: list of str, the list of datasets.
    - domain: str, the domain name.
    - project_list: list of str, the list of projects.

    Returns:
    - root_dict: dict, the root directories for each dataset.
    """
    root_dict = {}

    for dataset, project in zip(dataset_list, project_list):
        if dataset=="CERRA-land_Test_finals":
           root_dict[dataset] = "/gpfs/projects/meteo/DATA/CERRA-land/final_products-ruben-test/Global/CERRA/"
        elif dataset == "CERRA-land_CICAv2":
            # Mapping for user-provided CICAv2 CERRA-land interpolation products
            # Set root to the interpolation directory (parent of variable folders)
            root_dict[dataset] = "/gpfs/projects/meteo/WORK/PROYECTOS/2022_C3S_Atlas/workflow/datasets/CICAv2/CERRA-land/interpolation/Global/CERRA-land/"
        elif dataset=="CERRA_CICA_finals":
            root_dict[dataset] = f"/gpfs/projects/meteo/WORK/PROYECTOS/2022_C3S_Atlas/workflow/datasets/CICAv2/CERRA/final_products/climate_index/{project}/"
        elif dataset=="CERRA-land_Test_I":
            root_dict[dataset] = "/gpfs/projects/meteo/DATA/CERRA-land/interpolation-ruben-test/Global/CERRA/"
        elif dataset=="CERRA_CICA_I":
            root_dict[dataset] = f"/gpfs/projects/meteo/WORK/PROYECTOS/2022_C3S_Atlas/workflow/datasets/CICAv2/CERRA/intermediate_products/interpolator/{project}/"
        elif dataset=="CORDEX-CORE_FAO_int_ind":
            root_dict[dataset] = f"/gpfs/projects/meteo/DATA/FAO/intermediate_indices/indices/Global/CORDEX/{domain}/day/"
        elif dataset == "CORDEX-CORE_FAO_BA":
            root_dict[dataset] = f"/gpfs/projects/meteo/DATA/FAO/biasadjustment/Global/CORDEX/{domain}/day/"
        elif dataset == "CORDEX-CORE_CICA_BA":
            root_dict[dataset] = f"/gpfs/projects/meteo/WORK/PROYECTOS/2022_C3S_Atlas/workflow/datasets/CICAv2/CORDEX-CORE/biasadjustment/CORDEX/{domain}/"
        elif dataset == "CORDEX-CORE_FAO_INT":
            root_dict[dataset] = f"/gpfs/projects/meteo/DATA/FAO/interpolation/Global/CORDEX/{domain}/day/"
        elif dataset == "CORDEX-CORE_CICA_INT":
            root_dict[dataset] = f"/gpfs/projects/meteo/WORK/PROYECTOS/2022_C3S_Atlas/workflow/datasets/CICAv2/CORDEX-CORE/intermediate_products/interpolator_ba/CORDEX/{domain}/"
        elif dataset == "CORDEX-CORE_FAO_H":
            root_dict[dataset] = f"/gpfs/projects/meteo/DATA/FAO/homogenization/Global/CORDEX/{domain}/day/"
        elif dataset == "CORDEX-CORE_FAO_finals" or dataset == "CORDEX-CORE_FAO_finalsvscica":
            root_dict[dataset] = f"/gpfs/projects/meteo/DATA/FAO/final_products/indices/Global/CORDEX/{domain}/mon/"
        elif dataset == "CORDEX-CORE_CICA_H":
            root_dict[dataset] = f"/gpfs/projects/meteo/WORK/PROYECTOS/2022_C3S_Atlas/workflow/datasets/CICAv2/CORDEX-CORE/intermediate_products/provider/CORDEX/{domain}/"
        elif dataset == "CORDEX-CORE_CICA_finals" or dataset == "CORDEX-CORE_CICA_finalsvscica":
            root_dict[dataset] = f"/gpfs/projects/meteo/WORK/PROYECTOS/2022_C3S_Atlas/workflow/datasets/CICAv2/CORDEX-CORE/final_products/climate_index/CORDEX/{domain}/"
        elif dataset == "ERA5_FAO_H":
            root_dict[dataset] = f"/gpfs/projects/meteo/DATA/FAO/homogenization/Global/{project}/day/"
        elif dataset == "ERA5_CICA_H":
            root_dict[dataset] = f"/gpfs/projects/meteo/WORK/PROYECTOS/2022_C3S_Atlas/workflow/datasets/CICAv2/CERRA/intermediate_products/provider/{project}/"
        elif dataset == "ERA5_FAO_finals":
            root_dict[dataset] = f"/gpfs/projects/meteo/DATA/FAO/final_products/indices/Global/{project}/"
        elif dataset == "ERA5_CICA_I":
            root_dict[dataset] = f"/gpfs/projects/meteo/BACKUP/lustre/gmeteo/WORK/PROYECTOS/2022_C3S_Atlas/workflow/datasets/CICAv2/final_products/climate_index/{project}/"
        elif dataset == "ERA5-Land_gr25_CICA":
            root_dict[dataset] = f"/gpfs/projects/meteo/WORK/PROYECTOS/2022_C3S_Atlas/workflow/datasets/CICAv2/CORDEX-CORE/intermediate_products/interpolator/{project}/"
        elif dataset == "CERRA-land_CICAv2_Finals":
             root_dict[dataset] = "/gpfs/projects/meteo/WORK/PROYECTOS/2022_C3S_Atlas/workflow/datasets/CICAv2/CERRA-land/final_products/Global/CERRA-land/"

    return root_dict

def load_parameters(version):
    """
    Load parameters based on the version.

    Parameters:
    - version: str, the version to load parameters for.

    Returns:
    - params: dict, the loaded parameters.
    """
    params = {}
    print(version)
    if version == "interpolation":
        params["dataset_list"] = ["CORDEX-CORE_CICA_INT", "CORDEX-CORE_FAO_INT"]
        params["project_list"] = ["CORDEX-CORE", "CORDEX-CORE"]
        params["domain"] = "AFR-22"
        params["experiment"] = "historical"
        params["model"] = "MOHC-HadGEM2-ES_r1i1p1_GERICS_REMO2015_v1"
        params["var_list"] = ["tasbaisimip"]
    elif version == "bias_vs_pre":
        params["dataset_list"] = [ "CORDEX-CORE_FAO_INT", "CORDEX-CORE_FAO_BA"]
        params["project_list"] = ["CORDEX-CORE", "CORDEX-CORE"]
        params["domain"] = "AFR-22"
        params["experiment"] = "historical"
        params["model"] = "MOHC-HadGEM2-ES_r1i1p1_GERICS_REMO2015_v1"
        params["var_list"] = ["hurs","rsds","sfcwind"]
    elif version == "ERA5_vs_CORE_int":
        params["dataset_list"] = [ "CORDEX-CORE_FAO_INT", "ERA5_FAO_H"]
        params["project_list"] = ["CORDEX-CORE", "ERA5"]
        params["domain"] = "AFR-22"
        params["experiment"] = "historical"
        params["model"] = "MOHC-HadGEM2-ES_r1i1p1_GERICS_REMO2015_v1"
        params["var_list"] = ["hurs","rsds","sfcwind"]
    elif version == "biasadjustment":
        params["dataset_list"] = ["CORDEX-CORE_CICA_BA", "CORDEX-CORE_FAO_BA"]
        params["project_list"] = ["CORDEX-CORE", "CORDEX-CORE"]
        params["domain"] = "AFR-22"
        params["experiment"] = "historical"
        params["model"] = "MOHC-HadGEM2-ES_r1i1p1_GERICS_REMO2015_v1"
        params["var_list"] = ["tasmaxbaisimip","tasminbaisimip","tasbaisimip","rangebaisimip","skewnessbaisimip"]

    elif version == "CORE_homogenization":
        params["dataset_list"] = ["CORDEX-CORE_FAO", "CORDEX-CORE_CICA"]
        params["project_list"] = ["CORDEX-CORE", "CORDEX-CORE"]
        params["domain"] = "AFR-22"
        params["experiment"] = "historical"
        params["model"] = "MOHC-HadGEM2-ES_r1i1p1_GERICS_REMO2015_v1"
        params["var_list"] = ["tasmin", "tasmax", "tas", "pr"]

    elif version == "ERA5_homogenization":
        params["dataset_list"] = ["ERA5_FAO_H", "ERA5_CICA_H"]
        params["project_list"] = ["ERA5", "ERA5"]
        params["var_list"] = ["tasmin", "tasmax", "tas", "sfcwind", "pr", "rsds"]
        params["model"] = "NONE"
        params["domain"] = "Global"
        params["experiment"] = "None"

    elif version == "ERA5_indices":
        params["dataset_list"] = ["ERA5_FAO_finals", "ERA5_CICA_finals"]
        params["project_list"] = ["ERA5", "ERA5"]
        params["var_list"] = ["tx35"]
        params["model"] = "NONE"
        params["domain"] = "Global"
        params["experiment"] = "None"

    elif version == "ERA5land_interpolation":
        params["dataset_list"] = ["ERA5_CICA_H", "ERA5-Land_gr25_CICA"]
        params["project_list"] = ["ERA5", "ERA5-land"]
        params["var_list"] = ["pr"]
        params["model"] = "NONE"
        params["domain"] = "Global"
        params["experiment"] = "None"

    elif version == "CERRA_test_finals":
        params["dataset_list"] = ["CERRA-land_Test_finals", "CERRA_CICA_finals"]
        params["project_list"] = ["CERRA-land", "CERRA"]
        params["var_list"] = ["pr"]
        params["model"] = "NONE"
        params["domain"] = "Global"
        params["experiment"] = "None"
    elif  version == "CERRA_test_interpolation":
        params["dataset_list"] = ["CERRA-land_Test_I", "CERRA_CICA_I"]
        params["project_list"] = ["CERRA-land", "CERRA"]
        params["var_list"] = ["pr"]
        params["model"] = "NONE"
        params["domain"] = "Global"
        params["experiment"] = "None"

    return params





def load_files(root_dict, dataset_list, var_list, model, experiment, domain):
    """
    Load file paths for each dataset and variable.

    Parameters:
    - root_dict: dict, the root directories for each dataset.
    - dataset_list: list of str, the list of datasets.
    - var_list: list of str, the list of variables.
    - model: str, the model name.
    - experiment: str, the experiment name.
    - domain: str, the domain name.

    Returns:
    - file_dict: dict, the file paths for each dataset and variable.
    """
    file_dict = {}
    print(model)
    if model !="NONE":
        gcm, ensemble, rcm1, rcm2, version = model.split("_")
    
    for dataset in dataset_list:
        root = root_dict[dataset]
        file_dict[dataset] = {}
        for varin in var_list:
            varin = check_varin(dataset, varin)
            # Build the file search pattern based on dataset layout
            pattern = None
            if dataset in ["CORDEX-CORE_FAO_BA", "CORDEX-CORE_FAO_INT"]:
                if model != "NONE":
                    if version == "biasadjustment" and dataset == "CORDEX-CORE_FAO_BA":
                        varin = check_varin(dataset, varin)
                    pattern = f"{varin}/gr025/{gcm}/{experiment}/{ensemble}/{rcm1}/{rcm2}/{version}/day/{varin}*.nc"
            elif dataset == "CORDEX-CORE_CICA_BA":
                pattern = f"{varin}/gr025/{gcm}/{experiment}/{ensemble}/{rcm1}-{rcm2}/{version}/{varin}*.nc"
            elif dataset == "CORDEX-CORE_CICA_INT":
                pattern = f"{varin}/{gcm}/{experiment}/{ensemble}/{rcm1}-{rcm2}/{version}/{varin}*.nc"
            elif dataset == "CORDEX-CORE_CICA":
                pattern = f"{varin}/raw/{gcm}/{experiment}/{ensemble}/{rcm1}-{rcm2}/{version}/{varin}*.nc"
            elif dataset == "CORDEX-CORE_FAO":
                pattern = f"{varin}/gridded/{gcm}/{experiment}/{ensemble}/{rcm1}/{rcm2}/{version}/day/{varin}*.nc"
            elif dataset == "ERA5_FAO_H":
                pattern = f"{varin}/gridded/day/{varin}*.nc"
            elif dataset == "ERA5_CICA_H":
                pattern = f"{varin}/raw/{varin}*.nc"
            elif dataset == "ERA5_FAO_I":
                pattern = f"mon/{varin}/gr025/day/*.nc"
            elif dataset == "ERA5_CICA_I":
                pattern = f"{varin}/raw/{varin}*.nc"
            elif dataset == "ERA5-Land_gr25_CICA":
                pattern = f"{varin}/gr025/{varin}*.nc"
            elif dataset == "CERRA-land_Test_finals" :
                pattern = f"mon/{varin}/gr006/day/*.nc"
            elif dataset == "CERRA-land_Test_I" :
                pattern = f"day/{varin}/gr006/day/*.nc"
            elif dataset == "CERRA-land_CICAv2":
                # Files layout for CICAv2 CERRA-land interpolation products
                # (day/{var}/gr006/day/*.nc)
                pattern = f"day/{varin}/gr006/day/*.nc"
            elif dataset == "CERRA_CICA_finals" or dataset == "CERRA_CICA_I":
                pattern = f"{varin}/gr006/{varin}*.nc"
            elif dataset == "CERRA-land_CICAv2_Finals":
                if varin == "cdd":
                    pattern = f"year/{varin}/gr006/day/*.nc"
                else:
                    pattern = f"mon/{varin}/gr006/day/*.nc"

            if pattern is None:
                # If no pattern matched, set an empty list and continue
                file_list = []
                search_path = root
            else:
                search_path = os.path.join(root, pattern)
                file_list = np.sort(glob.glob(search_path))

            file_dict[dataset][varin] = file_list
            #print(dataset, file_dict[dataset][varin], search_path)

    return file_dict
def load_files_year(root_dict, dataset_list, var_list, model, experiment, domain, year):
    file_dict=load_files(root_dict, dataset_list, var_list, model, experiment, domain)
    for dataset in dataset_list:
        root = root_dict[dataset]
        for varin in var_list:
            selected_files = [f for f in  file_dict[dataset][varin]if f"_{year}" in f]
            file_dict[dataset][varin] = selected_files
    return file_dict
def load_datasets(file_dict, dataset_list, var_list):
    """
    Load datasets for each dataset and variable.

    Parameters:
    - file_dict: dict, the file paths for each dataset and variable.
    - dataset_list: list of str, the list of datasets.
    - var_list: list of str, the list of variables.

    Returns:
    - ds_dict: dict, the loaded datasets for each dataset.
    """
    ds_dict = {}
    ds_dict["ds"]={}
    for dataset in dataset_list:
        for i, varin in enumerate(var_list):
            varin = check_varin(dataset, varin)
            dict_varin = file_dict[dataset][varin]
            
            # Validar que hay archivos antes de intentar abrir
            if not dict_varin or len(dict_varin) == 0:
                print(f"WARNING: No files found for dataset={dataset}, var={varin}")
                print(f"         Skipping this dataset/variable combination")
                continue
            
            if i == 0:
                ds = xr.open_mfdataset(dict_varin, concat_dim='time', combine='nested')
            else:
                ds[varin] = xr.open_mfdataset(dict_varin, concat_dim='time', combine='nested')[varin]

            #if varin in ["rsds", "rlds", "sfcwind"]:
            #    ds[varin] = ds[varin].resample(time="MS").mean()

        # Solo añadir el dataset si se creó exitosamente
        if 'ds' in locals():
            ds_dict["ds"][dataset] = ds
        else:
            print(f"WARNING: Dataset {dataset} was not loaded (no valid files found)")

    return ds_dict

def check_varin(dataset,varin):
    if dataset in ["CORDEX-CORE_FAO_BA","CORDEX-CORE_CICA_INT","CORDEX-CORE_FAO_INT"]:
        if "ba" in varin:
            varba_dict = get_varba_dict()
            return varba_dict.get(varin)
    else:
        return varin
    
def get_varba_dict():
    varba_dict = {
        "tasminbaisimip": "tasmin",
        "tasmaxbaisimip": "tasmax",
        "tasbaisimip": "tas",
        "sfcwind": "sfcwind",
        "prbaisimip": "pr",
        "rsds": "rsds",
        "tx35": "tx35",
        "rangebaisimip": "tasrange",
        "skewnessbaisimip": "tasskew"}
    return varba_dict



