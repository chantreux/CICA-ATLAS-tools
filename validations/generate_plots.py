import maps
import matplotlib.pyplot as plt
import os
import gc  # Para gestión explícita de memoria
from load_files import load_root_directories,load_files_year,load_files, load_parameters, load_datasets, check_varin
from timeseries import plot_timeseries, select_data_point
from climatology import calculate_climatology_for_period
import yaml
import sys

print(sys.argv)

if len(sys.argv) < 2:
    raise ValueError("Please add a yml file")

file = sys.argv[1]

with open(file,'r') as f:
    config=yaml.safe_load(f)

globals_cfg=config['globals']
datasets_cfg=config['datasets']

step = globals_cfg['step']
unit = globals_cfg['unit']
project = globals_cfg['project']

# Support for year ranges
if 'start_year' in globals_cfg and 'end_year' in globals_cfg:
    start_year = globals_cfg['start_year']
    end_year = globals_cfg['end_year']
    year_list = list(range(start_year, end_year + 1))
else:
    # Backward compatibility with single year
    year = globals_cfg['year']
    year_list = [year]

domain_list = globals_cfg['domain_list']
experiment = globals_cfg['experiment']
model = globals_cfg['model']

# Support for multiple plot types
type_of_plot = globals_cfg.get('type_of_plot', 'triple_map')
if isinstance(type_of_plot, str):
    plot_types = [type_of_plot]
else:
    plot_types = type_of_plot

# Climatology configuration
climatology_cfg = globals_cfg.get('climatology', None)
clim_ref_start = None
clim_ref_end = None
climatology_cache = {}  # Cache para almacenar climatologías por dataset/variable

# Check if 'climatology' is in plot_types
if 'climatology' in plot_types:
    if climatology_cfg:
        clim_ref_start = climatology_cfg.get('reference_period_start', None)
        clim_ref_end = climatology_cfg.get('reference_period_end', None)
    
    if clim_ref_start is None or clim_ref_end is None:
        raise ValueError("'climatology' in type_of_plot but reference period not specified in YML under 'climatology'")


# ============================================================
# CLIMATOLOGY PROCESSING (Runs once, independent of years)
# ============================================================
# Process climatology ONLY if requested, before year loop
if 'climatology' in plot_types:
    print("Starting Climatology Generation...")
    
    start_date = f"{clim_ref_start}-01-01"
    end_date = f"{clim_ref_end}-12-31"

    for domain in domain_list:
        #index of domain in domain_list
        domain_index = domain_list.index(domain)

        print(domain_index, domain_list)
        dataset_list = [ds['name'] for ds in datasets_cfg]
        root_dict = load_root_directories(dataset_list, domain, ["CERRA-land", "CERRA"])
        
        # We only need to iterate unique variable combinations to avoid redundancy
        # Assuming first dataset config drives the variables
        ds_cfg_ref = datasets_cfg[0] 
        v1_list = ds_cfg_ref['v1_list']
        v2_list = ds_cfg_ref.get('v2_list', v1_list)

        for v1, v2 in zip(v1_list, v2_list):

            path_dict_all = load_files(root_dict, dataset_list, [v1], model, experiment, domain)
            
            save_dir = f"/gpfs/users/garciar/work/Validations/results/{project}/"
            os.makedirs(save_dir, exist_ok=True)
            
            # --- Load/Calc Dataset 1 ---
            print(f"    Computing climatology for {dataset_list[0]} - {v1}")
            clim1, unit = calculate_climatology_for_period(
                path_dict_all[dataset_list[0]][v1],
                v1,
                start_date,
                end_date
            )
            
            # --- TRIPLE MAP (if 2 datasets) ---
            '''
            if len(dataset_list) > 1:
                path_dict_all_2 = load_files(root_dict, dataset_list, [v2], model, experiment, domain) # Ensure v2 files loaded
                print(f"    Computing climatology for {dataset_list[1]} - {v2}")
                clim2, unit2 = calculate_climatology_for_period(
                    path_dict_all_2[dataset_list[1]][v2],
                    v2,
                    start_date,
                    end_date
                )
                
                # Interpolate
                clim2_interp = clim2.interp(lat=clim1.lat, lon=clim1.lon, method="linear")
                
                save_file = f'{save_dir}/{step}_{domain}_{v1}_{model}_{experiment}_climatology_{clim_ref_start}-{clim_ref_end}_triple.png'
                
                print(f"    Generating map: {save_file}")
                fig = maps.triple_map(
                    data1=clim1,
                    data2=clim2_interp,
                    model_name=model,
                    experiment=experiment,
                    year=f"Climatology {clim_ref_start}-{clim_ref_end}",
                    var1_name=v1,
                    var2_name=v2,
                    units=unit,
                    dataset1=f"FAO-{step}",
                    dataset2=f"CICA-{step}",
                    diff=True,
                    vscale_name=f"{v1}_{project}"
                )
                plt.savefig(save_file, bbox_inches='tight')
                plt.close(fig)
                
                # CLEANUP MEMORY IMMEDIATELY
                del clim2, clim2_interp, fig
                gc.collect()'''

            # --- SINGLE MAP ---
            # Generate single map for Dataset 1
            # We will just do Dataset 1 for now to match main flow logic, or iterate if needed.
            save_file_s1 = f'{save_dir}/{step}_{domain}_{dataset_list[0]}_{v1}_{model}_{experiment}_climatology_{clim_ref_start}-{clim_ref_end}_single.png'
            fig = maps.single_map(
                data1=clim1,
                model_name=model,
                experiment=experiment,
                year=f"Climatology {clim_ref_start}-{clim_ref_end}",
                var1_name=v1,
                units=unit,
                dataset1=dataset_list[0],
                vscale_name=f'{v1}_{project}'
            )
            plt.savefig(save_file_s1, bbox_inches='tight')
            plt.close(fig)
            del fig, clim1, unit
            gc.collect()

            
            # If dataset 2 exists, generate its single map too
            '''
            if len(dataset_list) > 1:
                # We need to reload/recalc Dataset 2 since we deleted it to save memory for interpolation
                # Or we could have kept it. For max memory safety, Recalc or load just for Single.
                # If memory is the issue, recalc is safer.
                 path_dict_all_2 = load_files(root_dict, dataset_list, [v2], model, experiment, domain)
                 clim2_single, _ = calculate_climatology_for_period(
                    path_dict_all_2[dataset_list[1]][v2], 
                    v2, start_date, end_date
                 )
                 save_file_s2 = f'{save_dir}/{step}_{domain}_{dataset_list[1]}_{v2}_{model}_{experiment}_climatology_{clim_ref_start}-{clim_ref_end}_single.png'
                 fig2 = maps.single_map(
                    data1=clim2_single,
                    model_name=model,
                    experiment=experiment,
                    year=f"Climatology {clim_ref_start}-{clim_ref_end}",
                    var1_name=v2,
                    units=unit,
                    dataset1=dataset_list[1],
                    vscale_name=f'{v2}_{project}'
                )
                 plt.savefig(save_file_s2, bbox_inches='tight')
                 plt.close(fig2)
                 del clim2_single, fig2
                '''
           

    print("Climatology processing complete. Memory cleared.")
    # Remove 'climatology' from plot_types to prevent re-execution in year loop
    plot_types = [pt for pt in plot_types if pt != 'climatology']

# Process year by year to optimize memory usage
for year in year_list:
    print(f"Processing year {year}...")
    
    # Process each plot type for the current year
    for current_plot_type in plot_types:
        print(f"  - Processing plot type: {current_plot_type}")
        
        if current_plot_type in ['triple_map', 'single_map']:
            for domain in domain_list:
                dataset_list = [ds['name']for ds in datasets_cfg]
                root_dict=load_root_directories(dataset_list, domain, ["CERRA-land", "CERRA"])
                
                for ds in datasets_cfg:
                    v1_list = ds['v1_list']
                    v2_list = ds['v2_list']

                    for v1,v2 in zip(v1_list,v2_list):
                        print(f"    Processing {current_plot_type}: {v1}, {domain}, {year}, {model}, {experiment}")
                        
                        save_dir=f"/gpfs/users/garciar/work/Validations/results/{project}/"
                        os.makedirs(save_dir, exist_ok=True) 
                        
                        
                        # NORMAL PROCESSING (triple_map, single_map)
                        path_dict=load_files_year(root_dict, dataset_list, v1_list, model, experiment, domain, year)

                        
                        if current_plot_type == 'triple_map':
                            path1=path_dict[dataset_list[0]][v1][0]
                            path2=path_dict[dataset_list[1]][v2][0]
                            print(path_dict)
                            
                            ds_mean1,unit = maps.load_cds(v1,year,  path1)
                            ds_mean2,unit = maps.load_cds(v2,year,  path2)
                            
                            ds_mean2_interp = ds_mean2.interp(lat=ds_mean1.lat, lon=ds_mean1.lon, method="linear")
                            ds_mean2=ds_mean2_interp
                            
                            save_file=f'{save_dir}/{step}_{domain}_{v1}_{model}_{experiment}_{year}_triple.png'

                            fig = maps.triple_map(
                                data1=ds_mean1,
                                data2=ds_mean2,
                                model_name=model, 
                                experiment=experiment,
                                year=year,
                                var1_name=v1, 
                                var2_name=v2,
                                units=unit,
                                dataset1=f"FAO-{step}",
                                dataset2=f"CICA-{step}",
                                diff=True,
                                vscale_name=f"{v1}_{project}"
                            )
                            plt.savefig(save_file,bbox_inches='tight')
                            plt.close(fig)
                            
                            # Liberar memoria explícitamente
                            del ds_mean1, ds_mean2, ds_mean2_interp, fig
                            
                        elif current_plot_type == 'single_map':
                            for dataset_name in dataset_list:
                                path = path_dict[dataset_name][v1][0]
                                ds_mean,unit = maps.load_cds(v1,year,path)

                                save_file= f'{save_dir}/{step}_{domain}_{dataset_name}_{v1}_{model}_{experiment}_{year}_single.png'

                                fig = maps.single_map(
                                    data1=ds_mean,
                                    model_name=model,
                                    experiment=experiment,
                                    year=year,
                                    var1_name=v1,
                                    units=unit,
                                    dataset1=dataset_name,
                                    vscale_name=f'{v1}_{project}'
                                )
                                plt.savefig(save_file, bbox_inches='tight')
                                plt.close(fig)
                                
                                # Liberar memoria explícitamente
                                del ds_mean, fig
                        
        elif current_plot_type == 'timeseries':
            version_list = globals_cfg.get('version_list',[])
            lon_p = globals_cfg.get('lon_point', -3.8)
            lat_p = globals_cfg.get('lat_point', 40.4)

            for version in version_list:
                
                save_dir=f"/gpfs/users/garciar/work/Validations/results/{project}/"

                os.makedirs(save_dir, exist_ok=True)

                params = load_parameters(version)
                root_dict=load_root_directories(params['dataset_list'], params['domain'],params['project_list'])
                
                file_dict=load_files(root_dict,params['dataset_list'], params['var_list'],params['model'],params['experiment'],params['domain'])
                
                # Validar que hay archivos antes de intentar cargar datasets
                has_files = False
                for dataset in params['dataset_list']:
                    for var in params['var_list']:
                        var_check = check_varin(dataset, var)
                        if dataset in file_dict and var_check in file_dict[dataset]:
                            if file_dict[dataset][var_check]:
                                has_files = True
                                break
                    if has_files:
                        break
                
                if not has_files:
                    print(f"\n⚠️  WARNING: No files found for version '{version}'")
                    print(f"    Datasets: {params['dataset_list']}")
                    print(f"    Variables: {params['var_list']}")
                    print(f"    Domain: {params['domain']}")
                    print(f"    Skipping timeseries for this version...\n")
                    continue
                
                ds_dict=load_datasets(file_dict,params['dataset_list'], params['var_list'])
                
                # Verificar que se cargaron datasets
                if not ds_dict or "ds" not in ds_dict or not ds_dict["ds"]:
                    print(f"\n⚠️  WARNING: No datasets loaded for version '{version}'")
                    print(f"    Skipping timeseries for this version...\n")
                    continue
                
                Dict=ds_dict
                

                dataset_list = params["dataset_list"]
                var_list = params["var_list"]

                # Ejes lon/lat dinámicos
                if "CORDEX-CORE" in dataset_list[0] and version == "pre":
                    lon = "x"
                    lat = "y"
                elif "ERA5" in dataset_list[0]:
                    lon = "lon"
                    lat = "lat"
                else:
                    lon = "lon"
                    lat = "lat"	

                # Seleccionar punto
                Dict["ds_point"] = {}
                for dataset in dataset_list:
                    if dataset in Dict["ds"]:
                        Dict["ds_point"][dataset] = select_data_point(Dict["ds"][dataset],dataset,lon_p,lat_p)
                    else:
                        print(f"⚠️  WARNING: Dataset '{dataset}' not loaded, skipping point selection")

                # Solo para el primer año, hacer timeseries completa de comparación de datasets
                if year == year_list[0]:
                    # Timeseries comparación de datasets
                    for varin in var_list:
                        data_list = []
                        for dataset in dataset_list:
                            varin = check_varin(dataset, varin)
                            data_list.append(Dict["ds_point"][dataset][varin])
                            
                        title = f"timeseries {varin} dataset comparison for model:{params['model']}, experiment:{params['experiment']}, lon:{lon_p}, lat:{lat_p}"
                        save_file = f"{save_dir}/timeseries_{varin}_dataset_comparison_lon{lon_p}_lat{lat_p}_{varin}_{version}.png"
                        plot_timeseries(data_list, varin, dataset_list, title, save_file)

                # Recorte anual para el año actual
                Dict_year = {"ds_point": {}, "ds": {}}
                for dataset in dataset_list:
                    Dict_year["ds_point"][dataset] = Dict["ds_point"][dataset].sel(time=slice(f"{year}-01-01", f"{year}-12-31"))
                    Dict_year["ds"][dataset] = Dict["ds"][dataset].sel(time=slice(f"{year}-01-01", f"{year}-12-31"))

                # Timeseries anuales
                for varin in var_list:
                    data_list = []
                    for dataset in dataset_list:
                        varin = check_varin(dataset, varin)
                        data_list.append(Dict_year["ds_point"][dataset][varin])
                    title = f"timeseries {varin} dataset comparison for lon:{lon_p}, lat:{lat_p}, year:{year}"
                    save_file = f"{save_dir}/timeseries_{varin}_dataset_comparison_lon{lon_p}_lat{lat_p}_{varin}_{year}_{version}.png"
                    plot_timeseries(data_list, varin, dataset_list, title, save_file)

                # Timeseries lonlat mean
                for varin in var_list:
                    data_list = []
                    for dataset in dataset_list:
                        varin = check_varin(dataset, varin)
                        data_list.append(Dict_year["ds"][dataset][varin].mean(dim=(lat, lon)))
                    title = f"timeseries {varin} dataset daily comparison for lonlatmean, year:{year}"
                    save_file = f"{save_dir}/timeseries_{varin}_dataset_comparison_lonlatmean_{year}_{version}.png"
                    plot_timeseries(data_list, varin, dataset_list, title, save_file)
                
                # Liberar memoria explícitamente
                del Dict, Dict_year, ds_dict, file_dict

        else:
            raise ValueError(f"Tipo de plot '{current_plot_type}' no implementado.")
    
    print(f"Completed processing for year {year}")
    # Forzar limpieza de memoria entre años
    plt.close('all')  # Cerrar cualquier figura que pueda quedar abierta
    gc.collect()  # Forzar recolección de basura para liberar memoria
