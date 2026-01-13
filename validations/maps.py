
import os
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import xarray as xr
import warnings
import numpy as np



import zipfile, os
warnings.filterwarnings('ignore')

def load_scale(data):
    """
    Function to get a value scale for plots from max values
    """    
    max_abs = abs_max(data)
    if np.nanmin(data)<0:
        vmin = -max_abs * 0.9
    else:
        vmin=0
    vmax = max_abs * 0.9
    vscale = [vmin, vmax]
    return vscale

def abs_max(data):
    """
    Function to get max abs value from data
    """
    #Gives abs max from data
    #print(data)
    if abs(np.nanmax(data))> abs(np.nanmin(data)):
        max_abs = abs(np.nanmax(data))
    else:
        max_abs = abs(np.nanmin(data))
    print(f"max abs is {max_abs}")
    return max_abs
def load_units(file, var):
    """Load units for a given variable."""
    print(f"Loading units for {var} from {file}")
    if var == "cdd":
        return "days"
    else:
        with xr.open_dataset(file) as ds:
            if var in ["avg_lds_wt1","max_lds_wt1","nd_thre_cold_tn0","nd_thre_cold_tn20","nd_thre_hot_tx30","nd_thre_rain50","nd_thre_rain100","nhw_tx40_dur6","nhw_tx40_dur3"]:
                units="days"
            else:
                units=ds[var].attrs["units"]
            return units
def load_cds(var, year, path,new=False,month=None):
    """
    Function to load cds datasets for var,experiment and year
    """    
    # C3S DATA
    if new is True:
        var=var.split("_")[1]
    print("path:",path)
    ds = xr.open_dataset(path)
    if var in ["cdd","avg_lds_wt1","max_lds_wt1","nd_thre_cold_tn0","nd_thre_cold_tn20","nd_thre_hot_tx30","nd_thre_rain50","nd_thre_rain100","nhw_tx40_dur6","nhw_tx40_dur3"]:
        ds[var].values = ds[var].values.astype('timedelta64[D]')
        ds[var].values = ds[var].values / np.timedelta64(1, 'D')
    units=load_units(path, var)
    
    if month==None:
        ds = ds.sel(time=slice(f'{year}-01', f'{year}-12'))
    else:
        ds = ds.sel(time=slice(f'{year}-{month}', f'{year}-{month}'))
    #print(ds)    
    #print(ds[var].shape)
    ds_mean = ds[var].sel().mean("time")

    #print(ds_mean.shape)
    # noinspection PyArgumentList
    print("CDS min :", ds_mean.values.min(), "max:", ds_mean.values.max())
    ds.close()
    del ds
    return ds_mean,units
def unzipall(dir_name,extension=".zip"):
    os.chdir(dir_name) # change directory from working dir to dir with files

    for item in os.listdir(dir_name): # loop through items in dir
        if item.endswith(extension): # check for ".zip" extension
            file_name = os.path.abspath(item) # get full path of files
            zip_ref = zipfile.ZipFile(file_name) # create zipfile object
            zip_ref.extractall(dir_name) # extract file to dir
            zip_ref.close() # close file


def load_area(ds):
    min_lon=60
    max_lon=120
    min_lat=0
    max_lat=60
    ds = ds.sel({"lon":slice(min_lon, max_lon),
                "lat":slice(min_lat, max_lat)})
    return ds

def check_lonlat(ds):
    if "lon" in list(ds.coords.keys()):
        lon="lon"
    elif "longitude" in list(ds.coords.keys()):        
        lon="longitude"
    if "latitude" in list(ds.coords.keys()):
        lat="latitude"
    elif "lat" in list(ds.coords.keys()):
        lat="lat"
    return lon,lat


def plot_avg(data, ax, vscale=None, units="unit", shrink_cb=1,cmap="RdBu_r",grid=True):
    """
    Function to get plot map from 2d data
    """
    
    
    if vscale is None:
        vscale=load_scale(data)

    vmin = vscale[0]
    vmax = vscale[1]
    #print(data)
    lon,lat=check_lonlat(data)
    #print(lon,lat)
    #print(lon)
    p = data.plot(ax=ax, x=lon, y=lat,
                  vmin=vmin, vmax=vmax,
                  cmap=cmap,
                  #cmap="viridis",
                  cbar_kwargs={'label': units,"shrink":shrink_cb},
                  transform=ccrs.PlateCarree(),
                  extend="both")
    p.axes.coastlines(linewidth=1.5, color='k', alpha=0.5, linestyle='-')
    gl = p.axes.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                            linewidth=0.9, color='gray', alpha=0.5, linestyle='--')
    gl.xlabels_top = False
    gl.ylabels_right = False
    return vscale

def scale_abs(var):
    """
    Return the absolute vscale for a variable based on the given variable name.
    """
    vscale_dict = {
        "sfcwind": [0, 10],
        "psl": [980, 1030],
        "mrso": [-60, 60],
        "fdba": [-25, 25],
        "cdba": [-4000, 4000],
        "skewness_ba": [-1, 1],
        "spi6": [-3, 3],
        "tas_obs": [-40, 40],
        "pr_era5_land": [0, 15],
        "tx35ba": [-25, 25],
        "tas-nnvscn":[-40, 40],
        "detrending-2015-2040":[-4, 4],
        "detrending-2070-2100":[-14, 14],
        "tr": [-40, 40],
        "sfcwind": [-10, 10],
        "pr": [0, 15],
        "pr_CERRA": [0, 15],
        "prbaisimip": [0, 15],
        "rsds": [-500, 500],
        "multimodel_number": [0, 17],

        #"siconc": [0, 1]
    }
    if var in vscale_dict:
        return vscale_dict[var]
    else:
        print ("No vscale for variable", var)
        return None
def scale_dif(var):
    """ Absolute vscale for variable diferences  """
    vscale_dict = {
            "cdd": [-40, 40],
            "tx35ba": [-2, 2],
            "tx40ba": [-2, 2],
            "tas_ba": [-0.5, 0.5],
            "tasmin_ba": [-1, 1],
            "tasmax_ba": [-1, 1],
            "range_ba": [-0.1, 0.1],
            "skewness_ba": [-0.02, 0.02],
            "tas_obs": [-0.4, 0.4],
            "spi6": [-0.5, 0.5],
            "t": [-2, 2],
            "tas-nnvscn":[-2, 2],
            "detrending":[-1, 1],
            "prbaisimip":[-4,4 ],
            "pr":[-1,1 ],
            "pr_CERRA":[-2.5,2.5 ],
            "sfcwind":[-3,3 ],
            "rsds":[-60,60 ],

        }
    if var in vscale_dict:
        return vscale_dict[var]
    else:
        print ("No vscale for variable", var)
        return None

    
def single_map(data1, model_name='model', experiment='experiment', year='year',month=None, var1_name='var1_name',
               units="units",dataset1="CICA",vscale_name=None):
    """
    Function to plot in a figure a map for a var: cds data, atlas data and cds - atlas
    """  
    print(f"var1 {var1_name}  mean('CICA) {experiment} [ model:{model_name};year{year}")
    if vscale_name==None:
        vscale_name=var1_name
    vscale=scale_abs(vscale_name)
    #print(data1,data2)
    if vscale==None:
            vscale=load_scale(data1)

    print(var1_name)
    if month == None:
        period = year
    else:
        period= f"{year}-month:{month}"

    fontsize = 20
    plt.rcParams.update({'font.size': fontsize})
    fig = plt.figure(figsize=[20, 30])
    
    ax = plt.subplot(projection=ccrs.PlateCarree())
    ax.set_extent([data1.lon.min(), data1.lon.max(), data1.lat.min(), data1.lat.max()], crs=ccrs.PlateCarree())
    plot_avg(data1, ax,vscale=vscale, units=units,shrink_cb=0.3,grid=False,cmap="viridis")
    check_title(var1_name, var1_name,dataset1,"",model_name,experiment,period,step=1)

    return fig





def triple_map(data1, data2, model_name='model', experiment='experiment', year='year',month=None, var1_name='var1_name',
               var2_name='var2_name',units="units",dataset1="CICA",dataset2="v1_dataset",vscale_name=None,diff=False):
    """
    Function to plot in a figure 3 maps for a var: cds data, atlas data and cds - atlas
    """  
    print(f"var1 {var1_name} var2 {var2_name} mean('CICA) {experiment} [ model:{model_name};year{year}")
    if vscale_name==None:
        vscale_name=var1_name
    vscale=scale_abs(vscale_name)
    #print(data1,data2)
    if vscale==None:
        if abs_max(data1) >= abs_max(data2):
            vscale=load_scale(data1)
        else:
            vscale=load_scale(data2)
    print(var1_name,var2_name)
    if month == None:
        period = year
    else:
        period= f"{year}-month:{month}"

    fontsize = 20
    plt.rcParams.update({'font.size': fontsize})
    fig = plt.figure(figsize=[20, 30])
    
    ax1 = fig.add_subplot(311, projection=ccrs.PlateCarree())
    ax1.set_extent([data1.lon.min(), data1.lon.max(), data1.lat.min(), data1.lat.max()], crs=ccrs.PlateCarree())
    plot_avg(data1, ax1,vscale=vscale, units=units)
    check_title(var1_name, var2_name,dataset1,dataset2,model_name,experiment,period,step=1)

    ax2 = fig.add_subplot(312, projection=ccrs.PlateCarree())
    ax2.set_extent([data1.lon.min(), data1.lon.max(), data1.lat.min(), data1.lat.max()], crs=ccrs.PlateCarree())
    plot_avg(data2, ax2, vscale=vscale, units=units)
    check_title(var1_name, var2_name,dataset1,dataset2,model_name,experiment,period,step=2)

    if diff==True:
        ds_diff = data1- data2
        print("DIFF min :", ds_diff.values.min(), "dif max:", ds_diff.values.max())
        ax3 = fig.add_subplot(313, projection=ccrs.PlateCarree())
        ax3.set_extent([data1.lon.min(), data1.lon.max(), data1.lat.min(), data1.lat.max()], crs=ccrs.PlateCarree())
                                           
        vscale=scale_dif(vscale_name)
        plot_avg(ds_diff, ax3, units=units,vscale=vscale)

        check_title(var1_name, var2_name,dataset1,dataset2,model_name,experiment,period,step=3)

    return fig

def check_title(var1_name, var2_name,dataset1,dataset2,model_name,experiment,period,step=1):
    if dataset1=="original:no BA":
        if step==1:
            title=(f"{var1_name} mean('{dataset1}') difference for periods: {period} [ model:{model_name};experiment:{experiment}]")
        if step==2:
            title=(f"{var1_name} mean('{dataset2}') difference for periods: {period} [ model:{model_name};experiment:{experiment}]")
        if step==3:
            title=f"Diff delta({dataset1}) - delta({dataset2})"
    else:
        if step==1:
            title=(f"{var2_name} mean('{dataset1}') [ model:{model_name};period:{period};experiment:{experiment}]")
        if step==2:
            title=(f"{var2_name} mean('{dataset2}') [ model:{model_name};period:{period};experiment:{experiment}]")
        if step==3:
            title=(f"Diff ({dataset1}) - ({dataset2})') [ model:{model_name};period:{period};experiment:{experiment}]")

        
    plt.title(title)

