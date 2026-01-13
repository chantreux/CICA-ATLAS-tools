import xarray as xr
#import xoak
import matplotlib.pyplot as plt
from load_files import check_varin

def select_data_point(data,dataset, lon_p, lat_p):
    """
    Select data for a specific point.

    Parameters:
    - dataset: xarray.Dataset, the dataset to select data from.
    - lon_p: float, the longitude of the point.
    - lat_p: float, the latitude of the point.

    Returns:
    - xarray.Dataset, the dataset with data selected for the point.
    """
    if dataset == "CORDEX-CORE_CICA":
        return data.sel(x=lon_p, y=lat_p, method="nearest")
    else:
        return data.sel(lat=lat_p, lon=lon_p, method="nearest")

def plot_timeseries(dataset_list, var, datasetname_list,  title,  save_file):
    marker_list=["*","o","^","+"]
    fig = plt.figure(figsize = (20, 10))
    ax = fig.add_subplot(1, 1, 1)
    for i, (marker, dataset, datasetname) in enumerate(zip(marker_list,dataset_list, datasetname_list)):
        varin=check_varin(datasetname,var)
        if i == 0:
            dataset.plot(label = f'{datasetname}_{varin}', ax = ax, linestyle='--', marker = marker, markersize=10, linewidth=2)
        else:
            dataset.plot(label = f'{datasetname}_{varin}', ax = ax, linestyle='--', marker = marker)
    plt.legend()
    plt.grid()
    plt.title(title)
    plt.savefig(save_file)
    plt.close(fig)


