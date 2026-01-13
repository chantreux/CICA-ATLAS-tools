"""
Product configuration file generator for CICA-ATLAS climate products.

This module has been refactored to separate parameters from logic:
- All parameter declarations are now in products/parameters/
- Product_cfile.py only contains orchestration logic
- This structure is compatible with workflow/generation_scripts/ for future unification

For parameter modifications, see:
- products/parameters/projects.py - Project-level parameters (experiments, periods, baselines, etc.)
- products/parameters/variables.py - Variable-level parameters (anomaly types, aggregations, filters, etc.)
- products/parameters/regions.py - Regional masks and configurations
"""

import os
import logging
from ruamel.yaml import YAML
from pathlib import Path
from typing import Dict, Any, List, Optional
from Product_configs import get_version_config, get_output_path, check_existing_files
from Product_variables import get_variables_for_version, VERSION_VARIABLES
import load_parameters
from ruamel.yaml.comments import CommentedSeq

# Import from unified parameter files
from parameters import (
    # Project functions
    get_data_type,
    get_trend_enabled,
    get_project_experiments,
    get_period_experiments_dict,
    get_scenario_lines_dict,
    get_warming_levels,
    get_spatial_mask,
    get_baseline_dict,
    get_period_climatology_dict,
    # Project parameters
    PROJECT_ROBUSTNESS,
    # Variable functions
    get_anomaly_dict,
    get_time_aggregation,
    get_period_aggregation,
    get_time_filters_dict,
    # Region functions
    get_region_mask,
)

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
        self.variable = variable
        self.set = set
        self.extreme = extreme
        self.type = type
        self.main_experiment = main_proj_experiment
        self.input_folder = input_folder
        self.output_folder = output_folder
        
        # Load Dataset class (still needed for load_period method)
        self.dataset = load_parameters.Dataset(project, "")
        self.historical = main_proj_experiment == "historical"
        
        # === Load ALL parameters from parameters module (NO HARDCODING) ===
        
        # Data type (used in config['data'][0]['type'])
        self.data_type = get_data_type(project)
        
        # Trend (used in config['products'][product_key]['magnitudes']['trends'])
        self.trend = get_trend_enabled(project, type)
        
        # Anomaly configuration (used in config['products'][product_key]['magnitudes'])
        self.anomaly = get_anomaly_dict(variable, project)
        
        # Time aggregation (used in config['products'][product_key]['time_aggregation_stat'])
        self.time_aggregation = get_time_aggregation(variable)
        
        # Period aggregation (used in config['products'][product_key]['period_aggregation_stat'])
        self.period_aggregation = get_period_aggregation(variable, extreme)
        
        # Experiments (used in config['data'][0]['scenario'])
        self.list_experiments = self.dataset.load_experiments()
        
        # Period for experiments (used in config['data'][0]['period'])
        self.period_experiments = get_period_experiments_dict(project, variable, main_proj_experiment, self.dataset)
        
        # Robustness (used in config['products'][product_key]['magnitudes']['anom_emergence'])
        self.robustness = PROJECT_ROBUSTNESS.get(project, False)
        
        # Scenario lines (used in config['products'][product_key]['scenarios'])
        self.scenarios_lines = get_scenario_lines_dict(project, main_proj_experiment, variable)
        
        # Spatial mask (used in config['data'][0]['spatial_mask'])
        self.spatial_mask = get_spatial_mask(project, variable)
        
        # Warming levels (used in config['products'][product_key]['warming_levels'])
        self.levels, self.warming_file = get_warming_levels(project)
        
        # Region mask (used in config['products'][product_key]['region_aggregation']['mask_file'])
        self.region_mask = get_region_mask(set) if type == "temporal_series" else None
        
        # Time filters (used in config['products'][product_key]['time_filters'])
        self.time_filters = get_time_filters_dict(variable)
        
        # Baselines (used in config['products'][product_key]['baselines'])
        self.baselines = get_baseline_dict(project)
        
        # Climatology periods (used in config['products'][product_key]['periods'])
        self.climatology_periods = get_period_climatology_dict(project, type, self.historical, self.baselines)
        
        # File paths
        self.cfile_in = cfile_in or f"configuration-remote_{project}.yml"
        self.jobfile_in = jobfile_in or f"configuration-remote_{project}.yml"
        self.cfile_out = self.file_output(self.cfile_in, variable, project)
        self.jobfile_out = self.file_output(self.jobfile_in, variable, project)

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