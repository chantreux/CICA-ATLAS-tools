#!/usr/bin/env python
"""
Script to generate stripe-plots for the ATLAS.
Usage:
  stripeplots_ATLAS.py --project PROJECT --var VAR --experiment EXPERIMENT --domain DOMAIN --dest DEST --log_dest LOGDEST
  stripeplots_ATLAS.py (-h | --help)
  stripeplots_ATLAS.py --version
Arguments:
  PROJECT project (CORDEX, CMIP5 or CMIP6 are implemented)
  VAR     var or index (e.g., tas) - "all" will load all variables for the project
  EXPERIMENT experiment (e.g., "historical", "ssp126", "ssp245", "ssp370", "ssp585", "all")
  DOMAIN  domain (e.g., "AFR-22", "all")  
  DEST    Path where the results files and plots are generated
  LOGDEST Path where the log file is saved
Options:
  -h --help  Show this help
  --version  Show version
  --project PROJECT
  --var VAR
  --experiment EXPERIMENT
  --domain DOMAIN 
  --dest DEST
  --log_dest LOGDEST
"""
__version__ = '0.0.2'
__authors__ = "JavierDiezSierra - Chantreux"
__date__ = "2024-01-29"

import glob
from collections import defaultdict
import logging
import os
from docopt import docopt
from datetime import date
import numpy as np
import xarray as xr
import pandas as pd
from functools import partial
import matplotlib.pyplot as plt
import copy

def setup_logging(log_dest):
    logging.basicConfig(filename=log_dest, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

def area_lat_weight(ds):
    """Function to apply lat area weight to dataset."""
    weights = np.cos(np.deg2rad(ds.lat))
    weights.name = "weights"
    return weights

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

def preprocess(ds, var="t", weighted=True):
    """Function to aggregate files to yearly resolution and calculate the weighted mean over the domain."""
    if var in ["cdd","avg_lds_wt1","max_lds_wt1","nd_thre_cold_tn0","nd_thre_cold_tn20","nd_thre_hot_tx30","nd_thre_rain50","nd_thre_rain100","nhw_tx40_dur6","nhw_tx40_dur3"]:
        ds[var].values = ds[var].values.astype('timedelta64[D]')
        ds[var].values = ds[var].values / np.timedelta64(1, 'D')

    if weighted:
        weights = area_lat_weight(ds)
        ds_weighted = ds[[var]].weighted(weights)
        var_mean = ds_weighted.mean(dim=("lat", "lon"), skipna=True)
    else:
        var_mean = ds[[var]].mean(dim=("lat", "lon"), skipna=True)

    res = var_mean.groupby("time.year").mean(dim="time")
    res = res.rename(year="time")
    return res

def check_models_consistency(files_dict):
    """Check if all experiments have the same number of models and the same model names."""
    reference_models = None
    for var, var_dict in files_dict.items():
        for domain, domain_dict in var_dict.items():
            for experiment, models in domain_dict.items():
                current_models = set(models.keys())
                if reference_models is None:
                    reference_models = current_models
                else:
                    if current_models != reference_models:
                        print(f"Inconsistency found in Variable: {var}, Domain: {domain}, Experiment: {experiment}")
                        print("Reference Models:", reference_models)
                        print("Current Models:", current_models)
                        return False
                    else:
                        print(f"Consistency checked for Variable: {var}, Domain: {domain}, Experiment: {experiment}")
                        print("Models:", current_models)
    print("All experiments have the same number of models and the same model names.")
    return True

def load_period(project):
    """Load historical and future periods based on the project."""
    if "CORDEX" in project:
        return np.arange(1970, 2006), np.arange(2006, 2101)
    elif project in ["ERA5"]:
        return np.arange(1940, 2025), None
    else:
        raise ValueError("Invalid project specified.")

def check_period(hist_period, fut_period, expe):
    """Function to associate historical period to historical and future period to other experiments."""
    return hist_period if expe == 'historical' else fut_period

def calculate_annual_mean_1model(files_list, period, var, weighted=True):
    """Calculate the annual mean for a single model."""
    partial_func = partial(preprocess, var=var, weighted=weighted)
    dataframe_model = pd.DataFrame(index=period, columns=[var])
    for file in files_list:
        with xr.open_mfdataset(file, preprocess=partial_func, concat_dim='time', combine='nested') as ds:
            year = ds.time.data[0]
            dataframe_model.loc[year] = ds[var][:].values[0]
    return dataframe_model

def calculate_annual_mean(files_dict, hist_period, fut_period, var, expe, weighted=True):
    """Calculate the annual mean for all models in an experiment."""
    print(f"Calculating yearly mean for {var} {expe}")
    period = check_period(hist_period, fut_period, expe)
    members = files_dict.keys()
    dataframe_exp = pd.DataFrame(index=period, columns=members)
    print(members)
    for mem in members:
        print(mem)
        dataframe_exp[mem] = calculate_annual_mean_1model(files_dict[mem], period, var, weighted=weighted)
    return dataframe_exp

def plot_and_save_results(hist_sce, args, filename, units):
    """Plot and save the results."""
    print(f"Plotting {filename}")
    hist_sce = hist_sce[hist_sce.columns[::-1]]
    mat = hist_sce.copy()
    mat_values = np.array(hist_sce.values.transpose(), dtype='float64')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cmap = copy.copy(plt.cm.get_cmap("Reds"))
    cmap.set_bad(color='grey', alpha=1.)
    pl = ax.pcolormesh(mat_values, cmap=cmap, edgecolors='w', linewidths=0.025)
    plt.title(filename.replace("_", " "))
    name_file = args['--dest'] + filename

    year_line = 2006
    index_year = np.where(hist_sce.index.values == year_line)

    if any(index_year):
        index_year = index_year[0][0]
        ax.axvline(x=index_year, color='k', linewidth=0.5)
        plt.xticks([0, index_year, len(mat.index)], (str(np.min(mat.index)), str(year_line), str(np.max(mat.index))))
    else:
        plt.xticks([0, len(mat.index)], (str(np.min(mat.index)), str(np.max(mat.index))))

    ax.set_yticks(np.arange(0.5, len(mat.columns) + 0.5))
    ax.set_yticklabels(['_'.join(col.split('_')[0:]) for col in mat.columns], fontsize=5)
    cbar = fig.colorbar(pl, pad=0.02)
    cbar.ax.tick_params(labelsize=5)
    cbar.set_label(f'in {units}', labelpad=10, rotation=270)
    plt.savefig(name_file + '.pdf', bbox_inches='tight')
    mat.to_csv(name_file + '.csv')
    plt.close()

def create_files_dict(file_list,var):
    """Create a nested dictionary of files based on their attributes."""
    files_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))
    for file in file_list:
        filename = file.split('/')[-1]
        name=filename.split(var)[-1]
        parts = name.split('_')
        #var = parts[0]
        domain = parts[4]
        experiment = parts[6]
        gcm = parts[5]
        rcmgroup = parts[8]
        rcm = parts[9]
        rcmversion = parts[10]
        model = f"{gcm}_{rcmgroup}_{rcm}_{rcmversion}"
        files_dict[var][domain][experiment][model].append(file)

    files_dict = {var: {domain: {experiment: {model: file_list for model, file_list in models.items()}
                                          for experiment, models in domain_dict.items()}
                                for domain, domain_dict in var_dict.items()}
                      for var, var_dict in files_dict.items()}
    return files_dict

def print_model_info(files_dict):
    """Print information about the number of models and their names for each experiment."""
    for var, var_dict in files_dict.items():
        for domain, domain_dict in var_dict.items():
            for experiment, models in domain_dict.items():
                num_models = len(models)
                print(f"Variable: {var}, Domain: {domain}, Experiment: {experiment}, Number of Models: {num_models} {models.keys()}")

def main():
    args = docopt(__doc__, version=__version__)
    print(args['--dest'])
    os.makedirs(args['--dest'], exist_ok=True)
    setup_logging(args['--log_dest'])
    project = args['--project']
    var = args['--var']
    experiments = [args['--experiment']]
    domain = args['--domain']
    base_dir = f'/gpfs/projects/meteo/DATA/FAO/final_products/indices/Global/CORDEX/{domain}/mon/{var}/'
    file_pattern = base_dir + '**/*.nc'
    file_list = np.sort(glob.glob(file_pattern, recursive=True))

    files_dict = create_files_dict(file_list,var)
    print_model_info(files_dict)

    check_models_consistency(files_dict)
    hist_period, fut_period = load_period(project)
    members = list(files_dict[var][domain]["historical"].keys())
    print(members)
    print(files_dict.keys())
    print(files_dict[var].keys())
    print(files_dict[var][domain].keys())
    units = load_units(files_dict[var][domain]["historical"][members[0]][0], var)

    for experiment in experiments:
        filename = f"{project}_{domain}_{var}_{experiment}"
        name_file = args['--dest'] + filename
        if os.path.isfile(name_file + '.pdf'):
            logging.info(f"File {name_file}.pdf already exists, skipping")
            continue
        dic_res = {}
        if 'CORDEX' in project:
            dic_res[experiment] = calculate_annual_mean(files_dict[var][domain][experiment], hist_period, fut_period, var, experiment, weighted=True)
            if experiment != 'historical':
                if "historical" not in dic_res:
                    dic_res["historical"] = calculate_annual_mean(files_dict[var][domain]["historical"], hist_period, fut_period, var, "historical", weighted=True)
                hist_sce = pd.concat([dic_res['historical'], dic_res[experiment]])
            else:
                hist_sce = pd.concat([dic_res['historical']])

            plot_and_save_results(hist_sce, args, filename, units)

if __name__ == "__main__":
    main()
