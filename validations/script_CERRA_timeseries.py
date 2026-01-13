import xarray as xr
#import xoak
import matplotlib.pyplot as plt
from load_files import load_root_directories, load_files, load_parameters, load_datasets,check_varin
from timeseries import select_data_point, plot_timeseries
import numpy as np

import os

version_list=["CERRA_test_finals", "CERRA_test_interpolation"]
for version in version_list:
    save_dir="/gpfs/users/garciar/work/Validations/results/CERRA-Land/"
    os.makedirs(save_dir, exist_ok=True) 
    params = load_parameters(version)
    root_dict = load_root_directories(params["dataset_list"], params["domain"], params["project_list"])
    file_dict = load_files(root_dict, params["dataset_list"], params["var_list"], params["model"], params["experiment"], params["domain"])
    ds_dict = load_datasets(file_dict, params["dataset_list"], params["var_list"])
    Dict=ds_dict
    dataset_list=params["dataset_list"]
    var_list=params["var_list"]
    model=params["model"]
    experiment=params["experiment"]


    lon_p=-3.8
    lat_p=40.4 #lonlat Madrid
    year=1990
    if "CORDEX-CORE" in dataset_list[0] and version=="pre" :
        lon="x"
        lat="y"
    elif "ERA5" in dataset_list[0]:
        lon="lon"
        lat="lat"
    else:
        lon="lon"
        lat="lat" 
    points = xr.Dataset(
        {
            lat: lat_p,
            lon: lon_p,
        }
    )


    Dict["ds_point"]={}
    print("calculating for point")
    for dataset in dataset_list:
        Dict["ds_point"][dataset] = select_data_point(Dict["ds"][dataset],dataset, lon_p, lat_p)
        print(Dict["ds_point"][dataset])

    #plot timeseries for point all

    for varin in var_list:
        data_list=[]
        for dataset in  dataset_list:
            varin=check_varin(dataset,varin)
            data_list.append(Dict["ds_point"][dataset][varin])
        print(f"plotting for point all {varin}")
        title=f"timeseries {varin} dataset comparison for model:{model},experiment:{experiment}, lon:{lon_p} and lat:{lat_p}"
        save_file=f"{save_dir}/timeseries_{varin}_dataset_comparison:lon{lon_p}_lat{lat_p}_{varin}_{version}.png"
        plot_timeseries(data_list, varin, dataset_list,  title,  save_file)


    for dataset in dataset_list:
        Dict["ds_point"][dataset]=Dict["ds_point"][dataset].sel(time=slice(f"{year}-01-01",f"{year}-12-31"))
        Dict["ds"][dataset]=Dict["ds"][dataset].sel(time=slice(f"{year}-01-01",f"{year}-12-31"))

    ## plot timeseries for point one year
    for varin in var_list:
        data_list=[]
        for dataset in  dataset_list:
            varin=check_varin(dataset,varin)
            data_list.append(Dict["ds_point"][dataset][varin])
        print(f"plotting for point one year {varin}")
        title=f"timeseries {varin} dataset comparison for model:{model},experiment:{experiment}, lon:{lon_p} and lat:{lat_p} year:{year}"
        save_file=f"{save_dir}/timeseries_{varin}_dataset_comparison:lon{lon_p}_lat{lat_p}_{varin}_{year}_{version}.png"
        plot_timeseries(data_list, varin, dataset_list,  title,  save_file)


    ## plot timeseries for lonlat mean
    for varin in var_list:
        data_list=[]
        for dataset in  dataset_list:
            varin=check_varin(dataset,varin)
            data_list.append(Dict["ds"][dataset][varin].mean(dim=(lat,lon)))
        print(f"plotting for mean lonlat {varin}")
        title=f"timeseries {varin} dataset daily comparison for lonlatmean, year:{year}"
        save_file=f"{save_dir}/timeseries_{varin}_dataset_comparison:lonlatmean_{year}_{version}.png"
        plot_timeseries(data_list, varin, dataset_list,  title,  save_file)



