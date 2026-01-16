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
from typing import Dict, Any, List, Optional
from Product_configs import get_version_config, get_output_path, check_existing_files

# Import from unified parameter files
from parameters import (
    # Project functions (from projects.py)
    is_observation_project,
    get_project_experiments,
    get_data_type,
    get_members_subset,
    
    # Project-product functions (from projects_products.py)
    get_baseline_project,
    get_scenario_lines_project_var,
    get_warming_levels,
    get_spatial_mask,
    get_period_climatology,
    get_period_experiments,
    get_region_mask,
    
    # Project parameters (from projects_products.py)
    PROJECT_ROBUSTNESS,
    PROJECT_TRENDS,
    
    # Variable functions (from variables_products.py)
    get_variables_for_version,
    get_anomaly_dict,
    get_time_aggregation,
    get_period_aggregation,
    get_time_filters_variable,
    
    # Cluster resources (from cluster_resources.py)
    get_cluster_resources,
    get_chunk_config,
    # Variable parameters (from variables_products.py)
    VERSION_VARIABLES
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
yaml.representer.add_representer(type(None), lambda self, data: self.represent_scalar('tag:yaml.org,2002:null', 'null'))

# Template files directory
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template_files')

class Product_Config:
    def __init__(self, project, variable, cfile_in=None, jobfile_in=None, 
                 main_proj_experiment="None", type="climatology", set="None",
                 input_folder="None", output_folder="None", extreme=False):
        # Store only essential input parameters
        self.project = project
        self.variable = variable
        self.set = set 
        self.extreme = extreme
        self.type = type
        self.main_experiment = main_proj_experiment
        self.input_folder = input_folder
        self.output_folder = output_folder
        
        # File paths - use TEMPLATE instead of project-specific
        self.cfile_in = cfile_in if cfile_in else os.path.join(TEMPLATE_DIR, f"refconfiguration-remote_TEMPLATE_{type}.yml")
        self.jobfile_in = jobfile_in if jobfile_in else os.path.join(TEMPLATE_DIR, "refJob_products_TEMPLATE.job")
        self.cfile_out = self.file_output(self.cfile_in, variable, project)
        self.jobfile_out = self.file_output(self.jobfile_in, variable, project)


    def file_output(self, file_in, var, project):
        # Get the base filename from the template
        base_name = os.path.basename(file_in)
        base_name = base_name.replace(f"_{self.type}", "")
        
        # Create output filename
        output_name = base_name.replace(
            "TEMPLATE", f"{var}_{project}_{self.main_experiment}_{self.type}_{self.set}"
        )
        if self.extreme:
            output_name = output_name.replace(f"{self.set}", f"{self.set}_extreme")
        output_name = output_name.replace("ref", "")
        
        # Place output file in project-specific directory
        output_dir = f"/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/{project}/"
        os.makedirs(output_dir, exist_ok=True)
        
        return os.path.join(output_dir, output_name)
    
    def display_info(self):
        """Display configuration info (calls functions on-the-fly)."""
        logger.info(f"Project: {self.project}")
        logger.info(f"Data Type: {get_data_type(self.project)}")
        logger.info(f"Variable: {self.variable}")
        logger.info(f"Trend: {PROJECT_TRENDS.get(self.project, False)}")
        logger.info(f"Anomaly: {get_anomaly_dict(self.variable, self.project)}")
        logger.info(f"Time Aggregation: {get_time_aggregation(self.variable)}")
        logger.info(f"cfile_in: {self.cfile_in}")
        logger.info(f"cfile_out: {self.cfile_out}")
        logger.info(f"jobfile_in: {self.jobfile_in}")
        logger.info(f"jobfile_out: {self.jobfile_out}")
        logger.info(f"list_experiments: {get_project_experiments(self.project)}")
        logger.info(f"robustness: {PROJECT_ROBUSTNESS.get(self.project, False)}")
        logger.info(f"historical: {self.main_experiment == 'historical'}")
        logger.info(f"scenarios: {get_scenario_lines_project_var(self.project, self.main_experiment, self.variable)}")

    def get_experiments_list(self) -> List[str]:
        """Get list of experiments for this product."""
        if is_observation_project(self.project):
            return []
        
        experiments_list = get_project_experiments(self.project)
        
        if self.main_experiment != "ssp119" and "ssp119" in experiments_list:
            experiments_list.remove("ssp119")
            
        if self.variable in ["spei6fullperiod", "spi6fullperiod"] and "historical" in experiments_list:
            experiments_list.remove("historical")
        
        return experiments_list

    def build_config_dict(self) -> Dict[str, Any]:
        """Build configuration dictionary, calling functions directly."""
        # Load base configuration
        with open(self.cfile_in) as f:
            config = yaml.load(f)
        
        # Variables used multiple times
        period_aggregation = get_period_aggregation(self.variable, self.extreme)
        baselines = get_baseline_project(self.project)
        anomaly = get_anomaly_dict(self.variable, self.project)
        scenarios_lines = get_scenario_lines_project_var(self.project, self.main_experiment, self.variable)
        spatial_mask = get_spatial_mask(self.project, self.variable)
        chunk_config = get_chunk_config(self.project)
        members = get_members_subset(self.project)
        
        # === UPDATE DIRECTORIES SECTION ===   
        config['directories']['input'] = self.input_folder
        config['directories']['output'] = self.output_folder
        config['directories']['temporary'] = f"{self.output_folder}/temporal_products/{self.project}/{self.variable}/{self.main_experiment}/{self.type}/{self.set}"
        if config['directories'].get('validation') is not None:
            config['directories']['validation'] = f"{self.output_folder}/validation/"

        # === REMOVE NOTIFICATIONS IF PRESENT ===
        if 'notifications' in config:
            del config['notifications']

        # === UPDATE DATA SECTION ===
        if 'data' in config and isinstance(config['data'], list) and len(config['data']) > 0:
            data_config = config['data'][0]
            data_config['type'] = get_data_type(self.project)
            data_config['project'] = self.project
            data_config['period'] = get_period_experiments(self.project, self.variable, self.main_experiment)
            data_config['scenario'] = get_project_experiments(self.project)
            data_config['variable'] = [self.variable]
            
            # Set members_subset
            if members is not None:
                data_config['members_subset'] = members
            elif 'members_subset' in data_config:
                data_config['members_subset'] = None
            
            if spatial_mask is not None:
                data_config['spatial_mask'] = spatial_mask
            elif 'spatial_mask' in data_config:
                del data_config['spatial_mask']
    
        # === UPDATE PRODUCTS SECTION ===
        product_key = f"{self.type}-user"
        if product_key not in config.get('products', {}):
            raise KeyError(f"Product key '{product_key}' not found in configuration file.")
        
        product_config = config['products'][product_key]
        
        # Update basic parameters
        product_config['variable'] = self.variable
        
        # Update scenarios
        product_config['scenarios']['main'] = scenarios_lines["main"]
        product_config['scenarios']['baseline'] = scenarios_lines["baseline"]
        product_config['scenarios']['fill_baseline'] = scenarios_lines["fill_baseline"]
    
        # Update magnitudes section  
        magnitudes = product_config['magnitudes']
        magnitudes['anom'] = anomaly["anom"]
        magnitudes['relanom'] = anomaly["relanom"]        
        magnitudes['anom_agreement'] = anomaly["anom_consensus"]
        magnitudes['anom_emergence'] = PROJECT_ROBUSTNESS.get(self.project, False)
        if 'trends' in magnitudes:
            magnitudes['trends'] =  PROJECT_TRENDS.get(self.project, False)
            magnitudes['trend_consensus'] = False

        # Update periods and baselines
        product_config['periods'] = get_period_climatology(self.project, self.type, 
                                                                self.main_experiment == "historical", baselines)
        product_config['baselines'] = baselines
        product_config['time_filters'] = get_time_filters_variable(self.variable)
        
        # Update warming levels
        if 'warming_levels' in product_config and 'levels' in product_config['warming_levels']:
            levels, warming_file = get_warming_levels(self.project)
            product_config['warming_levels']['levels'] = levels
            product_config['warming_levels']['file'] = warming_file
        
        # Update aggregations
        product_config['time_aggregation_stat'] = get_time_aggregation(self.variable)
        product_config['period_aggregation_stat'] = period_aggregation
    
        # Update region aggregation for temporal series
        if product_config.get('region_aggregation'):
            product_config['region_aggregation']['mask_file'] = get_region_mask(self.set) if self.type == "temporal_series" else None
            product_config['region_aggregation']['set'] = self.set
            product_config['region_aggregation']['period_aggregation_stat'] = period_aggregation
        
        # Update chunking configuration
        if 'chunksize' in product_config:
            product_config['chunksize']['lat'] = chunk_config['lat']
            product_config['chunksize']['lon'] = chunk_config['lon']
        if 'chunknum' in product_config:
            product_config['chunknum'] = chunk_config['chunknum']
        
        return config
    
    def build_job_file(self) -> str:
        """Build job file content by replacing placeholders in bash script."""
        with open(self.jobfile_in, 'r') as f:
            job_content = f.read()
        
        # Get cluster resources for this project
        resources = get_cluster_resources(self.project, self.type)
        
        # Define replacements for bash script placeholders
        replacements = {
            'var_replace': self.variable,
            'project_replace': self.project,
            'main_replace': self.main_experiment,
            'data_type_replace': get_data_type(self.project),
            'product_type_replace': self.type,
            'set_replace': self.set,
            'cfile_out_replace': self.cfile_out,
            # Cluster resource placeholders
            'cpus_replace': str(resources['cpus']),
            'mem_replace': resources['mem_per_cpu'],
            'time_replace': resources['time'],
            'partition_replace': resources['partition'],
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

    
    #if check_existing_files(path_data, var, experiment, project, is_observation_project(project)):
        #return
    
    logger.info(f"Producing climatology for {project}/{var}/{experiment}")
    
        # Standard climatology
    product = Product_Config(
        project, var, 
        cfile_in=cfile_climatology, 
        jobfile_in=jobfile,
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
            cfile_in=cfile_climatology, 
            jobfile_in=jobfile,
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
    if not is_observation_project(project):
        logger.debug(f"Skipping trends for {project} (not an observation dataset)")
        return
    
    path_data = get_output_path(version, "trends", project, var)
    is_obs = True
    
    if check_existing_files(path_data, var, experiment, project, is_obs):
        return
    
    logger.info(f"Producing trends for {project}/{var}/{experiment}")
    
    product = Product_Config(
        project, var, 
        cfile_in=cfile_trends, 
        jobfile_in=jobfile,
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

    
    if check_existing_files(path_data, var, experiment, project, is_observation_project(project), 
                          file_extension="csv", set_name=set_name):
        return
    
    logger.info(f"Producing temporal series for {project}/{var}/{experiment}/{set_name}")
        
    product = Product_Config(
        project, var, 
        cfile_in=cfile_timeseries, 
        jobfile_in=jobfile,
        main_proj_experiment=experiment,
        type="temporal_series",
        set=set_name,
        input_folder=input_folder,
        output_folder=output_folder
    )
    product.produce_files()


# Main execution
if __name__ == "__main__":
    version = "dry"

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
        
        # Use TEMPLATE files from template_files directory
        cfile_climatology = os.path.join(TEMPLATE_DIR, "refconfiguration-remote_TEMPLATE_climatology.yml")
        cfile_timeseries = os.path.join(TEMPLATE_DIR, "refconfiguration-remote_TEMPLATE_temporal_series.yml")
        cfile_trends = os.path.join(TEMPLATE_DIR, "refconfiguration-remote_TEMPLATE_trends.yml")
        jobfile = os.path.join(TEMPLATE_DIR, "refJob_products_TEMPLATE.job")
        
        root = f"/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/{project}/"

        experiment_list = get_project_experiments(project)
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

                if is_observation_project(project) and trends:
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