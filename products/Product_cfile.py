import os
import logging
from ruamel.yaml import YAML
from pathlib import Path
from typing import Dict, Any, List, Optional
from Product_configs import get_version_config, get_output_path, check_existing_files
from Product_variables import get_variables_for_version, VERSION_VARIABLES
import load_parameters
from ruamel.yaml.comments import CommentedSeq

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
yaml = YAML()
yaml.preserve_quotes = True
yaml.default_flow_style = False

class Product_Config:
    def __init__(self, project, variable, cfile_in=None, jobfile_in=None, 
                 main_proj_experiment="None", type="climatology", set="None",
                 input_folder="None", output_folder="None", extreme=False):
        self.project = project
        self.dataset = load_parameters.Dataset(project, "")
        self.set = set 
        self.extreme = extreme

        self.historical = main_proj_experiment == "historical"
        
        # Set type and mask
        if type == "climatology":
            self.type = "climatology"
            self.region_mask = None
        elif type == "trends":
            self.type = "trends"
            self.region_mask = None
        elif type == "temporal_series":
            self.type = "temporal_series"
            self.region_mask = self.load_region_mask()
        else:
            self.type = type
            self.region_mask = None
            
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.main_experiment = main_proj_experiment
        self.variable = variable

        # Load configurations
        self.data_type = self.load_data_type(project)
        self.trend = self.load_trend(project)
        self.anomaly = self.load_anomaly(variable)
        self.time_aggregation = self.load_aggregation(variable)
        
        # File paths
        if cfile_in is None:
            self.cfile_in = f"configuration-remote_{project}.yml"
        else:
            self.cfile_in = cfile_in
            
        if jobfile_in is None:
            self.jobfile_in = f"configuration-remote_{project}.yml"
        else:
            self.jobfile_in = jobfile_in
            
        self.cfile_out = self.file_output(self.cfile_in, variable, project)
        self.jobfile_out = self.file_output(self.jobfile_in, variable, project)
        
        # Load other parameters
        self.list_experiments = self.dataset.load_experiments()
        self.period_experiments = self.get_period_experiments()
        self.robustness = self.load_robustness(project)
        self.scenarios_lines = self.load_scenarios(project, main_proj_experiment)
        self.levels, self.warming_file = self.load_levels(project)
        self.spatial_mask = self.load_spatial_mask()
        self.period_aggregation = self.load_period_aggregation(extreme)
        self.baselines = self.get_baseline_dict()
        self.climatology_periods = self.get_period_climatology_dict()
        self.time_filters = self.get_time_filters_dict()

    def load_period_aggregation(self, extreme):
        if not extreme:
            return "mean"
        else:
            if self.variable == "tnn":
                return "one_in_20_year_event_min"
            else:
                return "one_in_20_year_event_max"

    def file_output(self, file_in, var, project):
        directory, base_name = os.path.split(file_in)
        base_name = base_name.replace(f"_{self.type}", "")
        file_out = os.path.join(directory, base_name.replace(
            project, f"{var}_{project}_{self.main_experiment}_{self.type}_{self.set}"
        ))
        if self.extreme:
            file_out = file_out.replace(f"{self.set}", f"{self.set}_extreme")
        file_out = file_out.replace("/ref", "/")
        return file_out
    
    def load_spatial_mask(self):
        if "CORDEX-EUR-11" in self.project:
            if "bals" in self.variable or "baisimip" in self.variable:
                return "/lustre/gmeteo/WORK/chantreuxa/cica/data/resources/reference-grids/CORDEX-EUR-11_EuropeOnly.nc"
            else:
                return "/lustre/gmeteo/WORK/chantreuxa/cica/data/resources/reference-grids/CORDEX-EUR-11_domain_simplified.nc"
        elif self.project == "E-OBS":
            return "/lustre/gmeteo/WORK/chantreuxa/cica/data/resources/reference-grids/EOBS_EuropeOnly.nc"  
        else:
            return None

    def load_region_mask(self):
        mask_map = {
            "AR6": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/resources/resources/reference-regions/IPCC-WGI-reference-regions-v4_areas.geojson",
            "eucra": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/resources/resources/reference-regions/EUCRA_areas.geojson",
            "european-countries": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/resources/resources/reference-regions/european-countries_areas.geojson",
            "megacities": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/resources/resources/reference-regions/megacities.geojson",
            "cities-rural": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/resources/resources/reference-regions/cities_contour.geojson",
            "cities-urban": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/resources/resources/reference-regions/cities_contour.geojson"
        }
        return mask_map.get(self.set)


    def display_info(self):
        logger.info(f"Project: {self.project}")
        logger.info(f"Data Type: {self.data_type}")
        logger.info(f"Variable: {self.variable}")
        logger.info(f"Trend: {self.trend}")
        logger.info(f"Anomaly: {self.anomaly}")
        logger.info(f"Time Aggregation: {self.time_aggregation}")
        logger.info(f"cfile_in: {self.cfile_in}")
        logger.info(f"cfile_out: {self.cfile_out}")
        logger.info(f"jobfile_in: {self.jobfile_in}")
        logger.info(f"jobfile_out: {self.jobfile_out}")
        logger.info(f"list_experiments: {self.list_experiments}")
        logger.info(f"robustness: {self.robustness}")
        logger.info(f"historical: {self.historical}")
        logger.info(f"scenarios: {self.scenarios_lines}")

    def get_time_filters_dict(self) -> Dict[str, str]:
        """Return time filters as a structured dictionary."""
        if self.variable in ["cd", "hd", "cdd", "cdbals", "hdbals", 
                            "cdbaisimip", "hdbaisimip", "cddbaisimip"]:
            return {"Annual": "01-12"}
        else:        
            return {
                "Annual": "01-12",
                "DecFeb": "12-02",
                "MarMay": "03-05",
                "JunAug": "06-08",
                "SepNov": "09-11",
                "Jan": "01-01",
                "Feb": "02-02",
                "Mar": "03-03",
                "Apr": "04-04",
                "May": "05-05",
                "Jun": "06-06",
                "Jul": "07-07",
                "Aug": "08-08",
                "Sep": "09-09",
                "Oct": "10-10",
                "Nov": "11-11",
                "Dec": "12-12"
            }
    def get_baseline_dict(self) -> Dict[str, str]:
        """Return baseline periods as a dictionary."""
        dict_baselines = {}
        if project in ["CMIP6","CMIP5","CORDEX-EUR-11","CORDEX-CORE","CORDEX-CORERUR","CORDEX-COREURB"]:
            dict_baselines = {
                "preIndustrial": "1850-1900",
                "AR5": "1986-2005",
                "AR6": "1995-2014",
                "WMO1": "1961-1990",
                "WMO2": "1981-2010",
                "WMO3": "1991-2020"
            }
        elif project in ["CMIP6","CMIP5","CORDEX-EUR-11","CORDEX-CORE","CORDEX-CORERUR","CORDEX-COREURB","CERRA","BERKELEY","CPC","SSTSAT"]:
            dict_baselines = {
                "AR5": "1986-2005",
                "AR6": "1995-2014",
                "WMO2": "1981-2010",
                "WMO3": "1991-2020"
            }
        elif project in ["ERA5","ERA5-Land","CPC","E-OBS","ORAS5"]:
            dict_baselines = {
                "AR5": "1986-2005",
                "AR6": "1995-2014",
                "WMO1": "1961-1990",
                "WMO2": "1981-2010",
                "WMO3": "1991-2020"
            }

            
        else:
            raise ValueError(f"Baselines not defined for project {project}")
        return dict_baselines

    def get_period_climatology_dict(self) -> Dict[str, str]:
        """Return period climatology as a dictionary."""
        if self.type == "climatology":
            key_calculation="climatology-user"
        elif self.type == "temporal_series":
            key_calculation="temporal_series-user"
        elif self.type == "trends":
            key_calculation="trends-user"
            raise ValueError("Climatology periods not applicable for trends type")
        else:
            assert self.type  in ["climatology","temporal_series","trends"], f"Invalid type {self.type}"
        

        if self.project in load_parameters.proj_datasets() and not self.historical:
            return {
                "near": "2021-2040",
                "medium": "2041-2060",
                "long": "2081-2100"
            }
        else:
            return self.baselines


    def get_period_experiments(self) -> Dict[str, str]:
        """Return period information as a dictionary."""
        hist, fut = self.dataset.load_period(self.variable, version="v2")
        
        hist_period = f"{hist[0]}-{hist[-1]}"
        
        if self.project in load_parameters.obs_datasets():
            if self.project == "BERKELEY":
                return "1960-2017"
            return  hist_period
        
        if self.project in load_parameters.proj_datasets():
            if "fullperiod" in self.variable:
                fut_period = f"{hist[0]}-{fut[-1]}"
            else:
                fut_period = f"{fut[0]}-{fut[-1]}"
            
            period_dict = {}
            
            if self.project == "CMIP6":
                if self.main_experiment == "ssp119":
                    period_dict = {
                        "historical": hist_period,
                        "ssp119": fut_period,
                        "ssp126": fut_period,
                        "ssp245": fut_period,
                        "ssp370": fut_period,
                        "ssp585": fut_period
                    }
                else:
                    period_dict = {
                        "historical": hist_period,
                        "ssp126": fut_period,
                        "ssp245": fut_period,
                        "ssp370": fut_period,
                        "ssp585": fut_period
                    }
            elif "CORDEX-EUR-11" in self.project or "CORDEX-CORE" in self.project or self.project == "CMIP5":
                period_dict = {
                    "historical": hist_period,
                    "rcp26": fut_period,
                    "rcp45": fut_period,
                    "rcp85": fut_period
                }
            
            # Remove historical for fullperiod variables
            if "fullperiod" in self.variable and "historical" in period_dict:
                del period_dict["historical"]
            
            return period_dict
        
        else:
            raise ValueError(f"Period not defined for project {self.project}")


    def load_robustness(self, project):
        return project in load_parameters.proj_datasets()

    def load_aggregation(self, var):
        agg_file = "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/resources/resources/metadata/agg-functions.yaml"
        with open(agg_file) as f:
            agg_dict = yaml.load(f)
        
        if var in agg_dict["mean"]:
            return "mean"
        elif var in agg_dict["min"]:
            return "min"
        elif var in agg_dict["max"]:
            return "max" 
        elif var in agg_dict["sum"]:
            return "sum"
        else:
            raise ValueError(f"Variable {var} not found in aggregation file {agg_file}")

    def load_data_type(self, project):
        if project in load_parameters.obs_datasets():
            return "observation"
        else:
            return "projection"

    def load_trend(self, project):
        return project in load_parameters.obs_datasets() and self.type == "trends"

    def load_anomaly(self, var):
        list_relanom = ["pr", "rx1day", "rx5day", "huss", "sfcwind", "evspsbl", 
                       "mrsos", "mrro", "rsds", "rlds", "tr", "r01mm", "r10mm", 
                       "r20mm", "sdii", "pethg"]
        Dict = {}
        
        var = load_parameters.index_only(var)
        
        if var in list_relanom:
            Dict["anomaly"] = "relative"
        else:
            Dict["anomaly"] = "absolute"

        # Always calculate abs anomaly
        Dict["anom"] = True
        Dict["anom_consensus"] = True

        # Activate relanom if needed
        if Dict["anomaly"] == "relative":
            Dict["relanom"] = True            
            Dict["relanom_consensus"] = True
        else:
            Dict["relanom"] = False            
            Dict["relanom_consensus"] = False

        # Deactivate consensus when not needed    
        if self.project not in load_parameters.proj_datasets():
            Dict["anom_consensus"] = False
            Dict["relanom_consensus"] = False

        return Dict
    
    def load_levels(self, project):

        if project in load_parameters.proj_datasets():
            warming_levels = [1.5, 2, 3, 4]
            if project=="CMIP6":
                warming_file= "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/resources/resources/warming_levels/CMIP6_WarmingLevels.csv"
            else:
                warming_file= "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/resources/resources/warming_levels/CMIP5_WarmingLevels.csv"
            return warming_levels,warming_file
        else: 
            return [],None

    def load_scenarios(self, project, experiment="None"):
        Dict = {}
        
        if project in load_parameters.obs_datasets():
            Dict["main"] = None
            Dict["baseline"] = None           
            Dict["fill_baseline"] = None
            
        elif project in load_parameters.proj_datasets():
            Dict["main"] = experiment
            
            if "fullperiod" in self.variable:
                Dict["baseline"] = experiment
            else:
                Dict["baseline"] = "historical"
            
            if project == "CMIP6":
                if self.main_experiment == "ssp119":
                    Dict["fill_baseline"] = ["ssp119", "ssp126", "ssp245", "ssp370", "ssp585"]
                else:
                    Dict["fill_baseline"] = ["ssp126", "ssp245", "ssp370", "ssp585"]
            elif project in ["CORDEX-CORE", "CORDEX-CORERUR", "CORDEX-COREURB"]:
                Dict["fill_baseline"] = ["rcp26", "rcp85"]
            else:
                Dict["fill_baseline"] = ["rcp26", "rcp45", "rcp85"]
        else:
            raise ValueError(f"Scenarios not defined for project {project}")
                
        return Dict

    def get_experiments_list(self) -> List[str]:
        """Get list of experiments for this product."""
        if self.project not in load_parameters.proj_datasets():
            return []
        
        experiments_list = self.list_experiments.copy()
        
        if self.main_experiment != "ssp119" and "ssp119" in experiments_list:
            experiments_list.remove("ssp119")
            
        if self.variable in ["spei6fullperiod", "spi6fullperiod"] and "historical" in experiments_list:
            experiments_list.remove("historical")
        
        return experiments_list

    def build_config_dict(self) -> Dict[str, Any]:
        """Build configuration dictionary with all parameters using pure dictionary operations."""
        # Load base configuration
        with open(self.cfile_in) as f:
            config = yaml.load(f)
        
        # === UPDATE DIRECTORIES SECTION ===   
        config['directories']['input'] = self.input_folder
        config['directories']['output'] = self.output_folder
        config['directories']['temporary'] = f"{self.output_folder}/temporal_products/{self.project}/{self.variable}/{self.main_experiment}/{self.type}/{self.set}"
        if config['directories'].get('validation') is not None:
            config['directories']['validation'] = f"{self.output_folder}/validation/"

        # === UPDATE DATA SECTION ===
        if 'data' in config and isinstance(config['data'], list) and len(config['data']) > 0:
            data_config = config['data'][0]
            data_config['type'] = self.data_type
            data_config['project'] = self.project
            data_config['period'] =  self.period_experiments    
            data_config['scenario'] = self.list_experiments
            data_config['variable'] = [self.variable]
            
            if self.spatial_mask is not None:
                data_config['spatial_mask'] = self.spatial_mask
            elif 'spatial_mask' in data_config:
                del data_config['spatial_mask']
    
        # === UPDATE PRODUCTS SECTION ===
        product_key = f"{self.type}-user"
        if product_key not in config.get('products', {}):
            raise KeyError(f"Product key '{product_key}' not found in configuration file.")
        
        product_config = config['products'][product_key]
        
        # Update basic parameters
        product_config['variable'] = self.variable
        # Update scenarios for projections

        product_config['scenarios']['main'] = self.scenarios_lines["main"]
        product_config['scenarios']['baseline'] = self.scenarios_lines["baseline"]
        product_config['scenarios']['fill_baseline'] = self.scenarios_lines["fill_baseline"]
    
        # Update magnitudes section  
        magnitudes = product_config['magnitudes']
        magnitudes['anom'] = self.anomaly["anom"]
        magnitudes['relanom'] = self.anomaly["relanom"]        
        magnitudes['anom_agreement'] = self.anomaly["anom_consensus"]
        magnitudes['anom_emergence'] = self.robustness
        if 'trends' in product_config:
            magnitudes['trends'] = self.trend
            magnitudes['trend_consensus'] = False

        # Update periods section (for data periods, not climatology baselines)
        product_config['periods'] = self.climatology_periods
        # Update warming levels
        if 'warming_levels' in product_config and 'levels' in product_config['warming_levels']:
            product_config['warming_levels']['levels'] = self.levels
            product_config['warming_levels']['file'] = self.warming_file
        #Baseline periods
        product_config['baselines'] = self.baselines
        product_config['time_filters'] = self.time_filters
        # Update time_aggregation_stat
        product_config['time_aggregation_stat'] = self.time_aggregation    
        # Update period_aggregation_stat
        product_config['period_aggregation_stat'] = self.period_aggregation
    
        if product_config['region_aggregation']:
            # Update region_aggregation for temporal series
                product_config['region_aggregation']['mask_file'] = self.region_mask
                product_config['region_aggregation']['set'] = self.set
                product_config['region_aggregation']['period_aggregation_stat'] = self.period_aggregation
        return config
    
    def build_job_file(self) -> str:
        """Build job file content by replacing placeholders in bash script."""
        with open(self.jobfile_in, 'r') as f:
            job_content = f.read()
        
        # Define replacements for bash script placeholders
        replacements = {
            'var_replace': self.variable,
            'project_replace': self.project,
            'main_replace': self.main_experiment,
            'data_type_replace': self.data_type,
            'product_type_replace': self.type,
            'set_replace': self.set,
            'cfile_out_replace': self.cfile_out
        }
        
        # Apply all replacements
        for placeholder, value in replacements.items():
            job_content = job_content.replace(placeholder, str(value))
        
        return job_content
    
    def produce_files(self):
        """Produce configuration and job files."""
        logger.info(f"Producing files for project={self.project}, variable={self.variable}")
        
        # Generate and save configuration file (YAML)
        config_dict = self.build_config_dict()
        with open(self.cfile_out, 'w') as f:
            yaml.dump(config_dict, f)
        logger.info(f"Created config file: {self.cfile_out}")
        
        # Generate and save job file (bash script)
        job_content = self.build_job_file()
        with open(self.jobfile_out, 'w') as f:
            f.write(job_content)
        
        # Make job file executable
        os.chmod(self.jobfile_out, 0o755)
        logger.info(f"Created job file: {self.jobfile_out}")


def produce_climatology_product(project, var, experiment, root, cfile_climatology, 
                                jobfile, input_folder, output_folder, version):
    """Produce climatology product for a variable."""
    path_data = get_output_path(version, "climatology", project, var)
    is_obs = project in load_parameters.obs_datasets()
    
    if check_existing_files(path_data, var, experiment, project, is_obs):
        return
    
    logger.info(f"Producing climatology for {project}/{var}/{experiment}")
    
    # Standard climatology
    product = Product_Config(
        project, var, 
        cfile_in=root + cfile_climatology, 
        jobfile_in=root + jobfile,
        main_proj_experiment=experiment,
        type="climatology",
        input_folder=input_folder,
        output_folder=output_folder,
        extreme=False
    )
    product.display_info()
    product.produce_files()
    
    # Extreme climatology if applicable
    if var in VERSION_VARIABLES["extremes"]["default"]:
        logger.info(f"Producing extreme climatology for {project}/{var}/{experiment}")
        product_extreme = Product_Config(
            project, var, 
            cfile_in=root + cfile_climatology, 
            jobfile_in=root + jobfile,
            main_proj_experiment=experiment,
            type="climatology",
            input_folder=input_folder,
            output_folder=output_folder,
            extreme=True
        )
        product_extreme.display_info()
        product_extreme.produce_files()


def produce_trends_product(project, var, experiment, root, cfile_trends, 
                           jobfile, version):
    """Produce trends product for a variable."""
    if project not in load_parameters.obs_datasets():
        logger.debug(f"Skipping trends for {project} (not an observation dataset)")
        return
    
    path_data = get_output_path(version, "trends", project, var)
    is_obs = True
    
    if check_existing_files(path_data, var, experiment, project, is_obs):
        return
    
    logger.info(f"Producing trends for {project}/{var}/{experiment}")
    
    product = Product_Config(
        project, var, 
        cfile_in=root + cfile_trends, 
        jobfile_in=root + jobfile,
        main_proj_experiment=experiment,
        type="trends"
    )
    product.display_info()
    product.produce_files()


def produce_temporal_series_product(project, var, experiment, set_name, 
                                   root, cfile_timeseries, jobfile,
                                   input_folder, output_folder, version):
    """Produce temporal series product for a variable."""
    path_data = get_output_path(version, "temporal_series", project, var)
    is_obs = project in load_parameters.obs_datasets()
    
    if check_existing_files(path_data, var, experiment, project, is_obs, 
                          file_extension="csv", set_name=set_name):
        return
    
    logger.info(f"Producing temporal series for {project}/{var}/{experiment}/{set_name}")
    
    product = Product_Config(
        project, var, 
        cfile_in=root + cfile_timeseries, 
        jobfile_in=root + jobfile,
        main_proj_experiment=experiment,
        type="temporal_series",
        set=set_name,
        input_folder=input_folder,
        output_folder=output_folder
    )
    product.produce_files()


# Main execution
if __name__ == "__main__":
    version = "extremes"

    # Get version configuration
    version_config = get_version_config(version)

    project_list = version_config.projects
    list_set = version_config.sets
    trends = version_config.trends
    climatology = version_config.climatology
    input_folder = version_config.input_folder
    output_folder = version_config.output_folder

    logger.info(f"Starting product generation for version: {version}")
    logger.info(f"Projects to process: {project_list}")

    for project in project_list:
        if "RUR" in project:
            list_set = ["cities-rural"]
        elif "URB" in project:
            list_set = ["cities-urban"]
        
        cfile_climatology = f"refconfiguration-remote_{project}_climatology.yml"
        cfile_timeseries = f"refconfiguration-remote_{project}_temporal_series.yml"
        cfile_trends = f"refconfiguration-remote_{project}_trends.yml"

        root = f"/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/{project}/"
        jobfile = f"refJob_products_{project}.job"

        dataset = load_parameters.Dataset(project, root)
        experiment_list = dataset.load_experiments()
        list_index = get_variables_for_version(project, version)

        logger.info("="*60)
        logger.info(f"Processing Project: {project}")
        logger.info(f"Variables: {list_index}")
        logger.info(f"Experiments: {experiment_list}")
        logger.info("="*60)
            
        for experiment in experiment_list:
            logger.info(f"--- Experiment: {experiment} ---")
            
            for var in list_index:
                logger.info(f"Processing variable: {var}")
                
                if climatology:
                    produce_climatology_product(
                        project, var, experiment, root, 
                        cfile_climatology, jobfile,
                        input_folder, output_folder, version
                    )

                if project in load_parameters.obs_datasets() and trends:
                    produce_trends_product(
                        project, var, experiment, root, 
                        cfile_trends, jobfile, version
                    )
                    
                for set in list_set:
                    produce_temporal_series_product(
                        project, var, experiment, set,
                        root, cfile_timeseries, jobfile,
                        input_folder, output_folder, version
                    )

    logger.info("Product generation completed successfully")