import load_parameters
from variables import temporal_agg, SUPPORTED_STEPS,MONTHLY_INPUT_INDEXES
from cluster import get_cluster_config,SUPPORTED_CLUSTERS
from aliases import PROJECT_STEPS,SUPPORTED_PROJECTS, PROJECT_ALIASES

import yaml
import os
from pathlib import Path
import importlib
import shutil
from dataclasses import dataclass
import argparse
import logging
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def load_template(project,step):
    """Load a YAML template from a file."""
    if project in SUPPORTED_PROJECTS:

            canonical_project = PROJECT_ALIASES.get(project, project)
            template_dir = root_generation() / "config_files_template"
            template_path = template_dir / f"config_template_{canonical_project}_{step}.yml"
            # If specific step template is missing, try using the project's 'all' template as a fallback
            if not os.path.exists(template_path):
                fallback_path = template_dir / f"config_template_{canonical_project}_all.yml"
                if os.path.exists(fallback_path):
                    template_path = fallback_path
                else:
                    raise FileNotFoundError(f"Neither {template_dir / f'config_template_{canonical_project}_{step}.yml'} nor {fallback_path} exist. Check step and project templates")
    else:
            raise ValueError(f"Unsupported project: {project}")

    with open(template_path) as f:
        return yaml.safe_load(f)



def load_models_core(domain):
    """Load core models for a given domain."""
    core_list = load_parameters.core_list()
    domain_core_list = [model for model in core_list if domain in model]
    return [model.replace(domain + '_', '') for model in domain_core_list]


def root_generation():
    """Get the root directory of the project."""
    return Path(__file__).resolve().parent.parent

def replace_string_in_file(input_file, output_file, replacements):
    """Replace strings in a file."""
    with open(input_file, 'r') as file:
        content = file.read()

    for search_string, replacement_string in replacements.items():
        content = content.replace(search_string, str(replacement_string))

    with open(output_file, 'w') as file:
        file.write(content)
    logger.info("Job written to %s", output_file)


def job_parameters(step,experiment):
    """Get job parameters for a given step."""
    if step == "homogenization":
        return {"procs": "1", "time_limit": "72:00:00", "ram": "20G"}
    if step == "biasadjustment":
        if "historical" in experiment:
            return {"procs": "4", "time_limit": "72:00:00", "ram": "5G"}
        elif "rcp" in experiment:
            return {"procs": "4", "time_limit": "72:00:00", "ram": "10G"}

    if step in ["indices","range-skewness","tasmaxba-tasminba"]:
        if step in  ["range-skewness","tasmaxba-tasminba"]:
            if "historical" in experiment:
                return {"procs": "1", "time_limit": "72:00:00", "ram": "30G"}
            elif "rcp" in experiment:
                return {"procs": "1", "time_limit": "72:00:00", "ram": "50G"}
        else:
            return {"procs": "1", "time_limit": "72:00:00", "ram": "30G"}
    return {}

def write_jfile(project,experiment,varout,domain,model="None",step="homogenization", cluster_cfg=None):
    """Write a job file."""

    params = job_parameters(step,experiment)
    jfile_in= root_generation() / "config_files_template" / f"Job_template_{cluster_cfg.name}.sh"
    jfile_out=load_jfile_path(step,project,domain,varout,experiment,model).resolve()
    os.makedirs(os.path.dirname(jfile_out), exist_ok=True)
    source_file = str(root_generation() / "tools" / "bash_scripts" / "run_jobs.sh")
    destination_file = os.path.dirname(jfile_out)+"/run_jobs.sh"
    shutil.copy(source_file, destination_file)
    cfile_name=load_cfile_path(step,project,domain,varout,experiment,model).resolve()
    # Use safe defaults in case job_parameters returns an incomplete dict
    replacements = {
        "project_replace": project,
        "domain_replace": domain,
        "index_replace": varout,
        "model_replace": model,
        "experiment_replace": experiment,
        "n_procs_replace": params.get("procs", "1"),
        "time_replace": params.get("time_limit", "72:00:00"),
        "ram_replace": params.get("ram", "20G"),
        "config_var_replace": cfile_name,
        "job_file_replace": jfile_out,
        "root_replace": root_generation()
    }
    replace_string_in_file(jfile_in, jfile_out, replacements)


def load_existing_input(root,project,experiment,varin_list,domain,model="None",step="homogenization",varout=None):
    truncate=False
    varin=varin_list[0]
    project = PROJECT_ALIASES.get(project, project)
    if step=="homogenization":
        if project == "CERRA-Land":
            # CERRA-Land stored similarly under RODRI copy; use its own folder
            path = Path(f"{root}/download/Global/{project}/{varin}/")

        elif "E-OBS" in project:
            if "EOBSv26" in root:
                # E-OBS v26
                path =  Path(f"/lustre/gmeteo/WORK/PROYECTOS/2022_C3S_Atlas/workflow/datasets/CICAv2/download/insitu-gridded-observations-europe/E-OBS/")
            else:
                # E-OBS
                path =  Path(f"/lustre/gmeteo/WORK/DATA/C3S-CDS/ERA5_temp/raw/insitu-gridded-observations-europe/daily/native/")
    elif step=="interpolation":
        if project in ["CERRA-Land","E-OBS"]:
            path=build_step_path(root, "homogenization")+f"Global/{project}/day/{varin}/gridded/day/"
    elif step=="indices":
        if project == "E-OBS":
            if "EOBSv26" in project:
                # E-OBS v26
                path =  Path(f"/lustre/gmeteo/WORK/PROYECTOS/2022_C3S_Atlas/workflow/datasets/C3S-ATLAS-climate-pipeline/EOBSv26/final_products/")
            else:
                # E-OBS
                path =  Path(f"/lustre/gmeteo/WORK/PROYECTOS/2022_C3S_Atlas/workflow/datasets/C3S-ATLAS-climate-pipeline/final_products/")
        elif project in ["CERRA-Land","E-OBS"]:
            if varout in MONTHLY_INPUT_INDEXES:
                path=build_step_path(root, "final_products")
            else:
                path=build_step_path(root, "interpolation")
    else:
        raise ValueError(f"Unsupported step for existing input: {step}")

    if len(varin_list)>1 and truncate:
        path = Path(path)
        parts = path.parts
        try:
            index = parts.index(varin)
            path = Path(*parts[:index])
        except ValueError:
            print("The value of 'varin' is not in the path.")
    return str(path)
   



def build_step_path(root, step):
    return f"{root}{step}/"

def general_parameters(root,project,experiment,varout,domain,model="None",step="homogenization"):
    """Get the general parameters for the configuration."""
    parameters = load_parameters.Dataset(project)
    id = parameters.load_project_id()      
    template = load_template(project,step)
    years=parameters.load_years(experiment)
    if parameters.project_type=="observations":
        project_name = PROJECT_ALIASES.get(project, project)
        level = ""
        template["requests"][0]["configuration"]["timeCoverage"]["start"] = f"{years[0]}-01-01"
        template["requests"][0]["configuration"]["timeCoverage"]["end"] = f"{years[1]}-12-31"
        template["requests"][0]["configuration"]["models"] =None

    elif project == "CORDEX-CORE":
        project_name = "CORDEX"
        level = "single_levels"
        template["requests"][0]["configuration"]["experiments"][0]["name"] = experiment
        template["requests"][0]["configuration"]["experiments"][0]["start"] = f"{years[0]}-01-01"
        template["requests"][0]["configuration"]["experiments"][0]["end"] = f"{years[1]}-12-31"
        template["requests"][0]["configuration"]["models"] = [model.split("_v")[0]]

    template["directories"]["temporal"] = f"{root}temporal_files/{step}/{project}/{domain}/{model}/{experiment}/{varout}/"
    template["requests"][0]["identifier"] = f"{project}_{domain}_{varout}_{model}_{experiment}_{step}_C3S-ATLAS"
    template["requests"][0]["project"]["name"] = project_name
    template["requests"][0]["project"]["type"] = parameters.project_type
    template["requests"][0]["project"]["format"] = "gridded"
    template["requests"][0]["configuration"]["temporalResolution"] = "daily"
    template["requests"][0]["configuration"]["level"] = level
    template["requests"][0]["configuration"]["domain"] = domain
    template["requests"][0]["configuration"]["filter_paths"] = True
    template["requests"][0]["configuration"]["id"] = id
    template["requests"][0]["configuration"]["source"] = "CDS"
    template["requests"][0]["configuration"]["area"]["name"] = "Global"
    template["requests"][0]["configuration"]["area"]["coords"] = [-90, -180, 90, 180]
    if varout in  get_var_list(parameters, "homogenization"):
        varin_list = [varout]
    else:
        varin_list = get_index_varin(varout)
    template["requests"][0]["configuration"]["variables"] = varin_list    
    return template



def homogenization(template,root,project,experiment,varout,domain,model="None",existing_input="step"):
    """Prepare homogenization configuration."""
    parameters = load_parameters.Dataset(project)
    configuration_variable,variable_mapping_file =  parameters.var_mapping()
    varin = configuration_variable["dataset_variable"][varout]  
    # pass the concrete step name to load_existing_input to avoid using the global
    # `step` variable (which may be 'all' when produce_cfile runs multiple stages)
    if existing_input == "homogenization":       
        template["directories"]["existing_input"] = load_existing_input(root, project, experiment, [varin], domain, model=model, step="homogenization")
    out_dir = build_step_path(root, "homogenization")

    template["directories"]["homogenization"] = out_dir
    template["requests"][0]["configuration"]["variable_mapping"] = str(variable_mapping_file.resolve())

    return template

def interpolation(template,root,project,experiment,varout,domain,model="None",existing_input="step"):
    """Prepare interpolation configuration."""
    parameters = load_parameters.Dataset(project)
    grid_path, interpolation_step = parameters.get_int_grid()
    varout_list=[varout]
    out_dir =build_step_path(root, "interpolation")
    template["directories"]["interpolation"] = out_dir
    template["requests"][0]["interpolation"]["grid_type"]["custom_grid"] = "None"
    template["requests"][0]["interpolation"]["grid_type"]["grid_path"] = grid_path
    template["requests"][0]["interpolation"]["method"] = "conservative_normed"
    template["requests"][0]["interpolation"]["apply_reference_mask"] = False
    if existing_input == "interpolation" and interpolation_step=="previous":
        template["directories"]["existing_input"] =load_existing_input(root,project,experiment,varout_list,domain,model=model,step="interpolation")
    elif existing_input == "interpolation" and interpolation_step=="posterior":
        template["directories"]["existing_input"] =load_existing_input(root,project,experiment,varout_list,domain,model=model,step="indices")
    return template

def biasadjustment(template,root,project,experiment,varout,domain,model="None",existing_input="step"):
    """Prepare bias adjustment configuration."""
    varout_list=[varout]
    out_dir = build_step_path(root, "biasadjustment")
    template["directories"]["biasadjustment"] = out_dir
    if existing_input == "biasadjustment":
        template["directories"]["existing_input"] =load_existing_input(root,project,experiment,varout_list,domain,model=model,step="biasadjustment_sim")
    template["requests"][0]["bias_adjustment"]["method"] = "ibicus-isimip"
    if experiment=="historical":
        n_procesors=4
    else:
        n_procesors=4
    template["requests"][0]["bias_adjustment"]["processors"] = n_procesors
    template["requests"][0]["bias_adjustment"]["multiprocessing"] = True
    template["requests"][0]["bias_adjustment"]["chunk_size"]["x"] = 50
    template["requests"][0]["bias_adjustment"]["chunk_size"]["y"] = 50
    template["requests"][0]["bias_adjustment"]["parameters"]["observations"]["path"] =load_existing_input(root,project,experiment,varout_list,domain,model=model,step="biasadjustment_obs")
    template["requests"][0]["bias_adjustment"]["parameters"]["observations"]["period"]["start"] = "1970-01-01"
    template["requests"][0]["bias_adjustment"]["parameters"]["observations"]["period"]["end"] = "2005-12-31"
    template["requests"][0]["bias_adjustment"]["parameters"]["observations"]["project_name"] = "CICA"
    template["requests"][0]["bias_adjustment"]["parameters"]["historical"] = load_existing_input(root,project,"historical",varout_list,domain,model=model,step="biasadjustment_hist")
    return template


def get_index_varin(index):
    name_list=[]
    module_name = 'climate_data_indices.index_definitions.definitions'
    module_name2 = 'xrindices.definitions'
    definitions_module1 = importlib.import_module(module_name)
    definitions_module2 = importlib.import_module(module_name2)
    # Try the first module; if not found, try the second
    try:
        vars2use = getattr(definitions_module1, index).vars2use
    except AttributeError:
        try:
            vars2use = getattr(definitions_module2, index).vars2use
        except AttributeError:
            raise ValueError(f"Index '{index}' not found in either module.")
    for var in vars2use:
        name_list.append(var.short_name)
    return name_list

def indices(template,root,project,experiment,varout,domain,model="None",step="indices",existing_input="step"):
    """Prepare indices configuration."""
    if step in [ "range-skewness","tasmaxba-tasminba"]:
        temp_agg=["D"]
        final_folder="intermediate_indices"
        processors=1
    else:
        
        temp_agg=temporal_agg(varout)
        final_folder="final_products"
        processors=4
    varin_list = get_index_varin(varout)
    template["requests"][0]["configuration"]["variables"] = varin_list    
    template["requests"][0]["configuration"]["filter_paths"] = True
    if existing_input in ["indices","range-skewness","tasmaxba-tasminba"]:
        template["directories"]["existing_input"] =load_existing_input(root,project,experiment,varin_list,domain,model=model,step=step,varout= varout)
    out_dir = build_step_path(root, final_folder)
    template["directories"]["indices"] = out_dir
    template["requests"][0]["indices"][0]["name"] = varout
    template["requests"][0]["indices"][0]["params"]["temporal_aggregation"] = temp_agg
    template["requests"][0]["indices"][0]["params"]["processors"] = processors
    template["requests"][0]["indices"][0]["params"]["chunksize"] = {"x": 60, "y": 60}

    return template

def load_cfile_path(step, project, domain, var, experiment, model):
    """Get the path for the configuration file."""
    return Path(f"../{step}/cfiles/{project}/{var}/cfile_{project}_{domain}_{var}_{experiment}_{model}.yml")

def load_jfile_path(step, project, domain, var, experiment, model):
    """Get the path for the job file."""
    return Path(f"../{step}/jfiles/{project}/{var}/Job_{project}_{domain}_{var}_{experiment}_{model}.job")

def expand_steps(project, step,variable):
    """Return the list of steps and the existing input step based on project and step."""
    if step != "all":
        return [step], step

    if variable in MONTHLY_INPUT_INDEXES:
        return ["indices"], "indices"
    if project not in PROJECT_STEPS:
        raise ValueError(f"Unsupported project for 'all' steps: {project}")

    return PROJECT_STEPS[project], "homogenization"

def get_var_list(parameters, step):
    """Return the variable list corresponding to the given processing step."""
    mapping = {
        "all": parameters.indices_list,
        "homogenization": parameters.homogenization_list,
        "biasadjustment": parameters.bias_correction_list,
        "interpolation": parameters.homogenization_list,
        "indices": parameters.indices_list,
        "range-skewness": parameters.range_list,
        "tasmaxba-tasminba": parameters.tasmaxba_list,
    }
    return mapping.get(step, [])


def build_cfile(cfile_dict, step, root, project, experiment, var, domain, model, existing_input):
    """
    Construct or update the cfile dictionary for the given step.
    If cfile_dict is provided, update it in place.
    """
    logger.info("Building cfile for step: %s, project: %s, variable: %s", step, project, var)
    if cfile_dict is None:
        cfile_dict = {}

    if step == "homogenization":
        update = homogenization(cfile_dict,root, project, experiment, var, domain, model, existing_input)
    elif step == "interpolation":
        update = interpolation(cfile_dict,root, project, experiment, var, domain, model, existing_input)
    elif step == "biasadjustment":
        update = biasadjustment(cfile_dict,root, project, experiment, var, domain, model, existing_input)
    elif step in ["indices", "range-skewness", "tasmaxba-tasminba"]:
        update = indices(cfile_dict,root, project, experiment, var, domain, model, step=step, existing_input=existing_input)
    else:
        raise ValueError(f"Unsupported step: {step}")

    # Merge dictionaries (in-place update)
    cfile_dict.update(update)
    return cfile_dict


def write_cfile(path_out, cfile_dict):
    """Write a cfile YAML to disk."""
    os.makedirs(os.path.dirname(path_out), exist_ok=True)
    with open(path_out, "w") as outfile:
        yaml.dump(cfile_dict, outfile, default_flow_style=False, sort_keys=False)
    logger.info("Configuration file written to %s", os.path.abspath(path_out))


def produce_cfile(project, step="homogenization", cluster_cfg=None):
    """Produce configuration files for all processing steps."""
    parameters = load_parameters.Dataset(project)
    root= parameters.root
    var_list = get_var_list(parameters, step)
    logger.info("Producing cfiles for project: %s, step: %s", project, step)
    for domain in parameters.domain_list:
        # Select model list based on project
        if project == "CORDEX-CORE":
            model_list = load_models_core(domain)
        else:
            model_list = ["None"]

        for experiment in parameters.available_exp:
            for model in model_list:
                
                for var in var_list:
                    steps_to_run, existing_input = expand_steps(project, step, var)

                    if step == "all":
                        # Shared cumulative dictionary
                        cfile_dict_all =general_parameters(root,project,experiment,var,domain,model="None",step=step)

                    for cur_step in steps_to_run:
                        
                        logger.info("Processing step: %s for variable: %s", cur_step, var)
                        if step == "all":
                            if cur_step in ["homogenization","interpolation", "biasadjustment"]:
                                varin_list= get_index_varin(var)
                            else:
                                varin_list=[var]
                            varin=varin_list[0]
                            # Each function updates the existing dict in place
                            cfile_dict_all = build_cfile(cfile_dict_all,
                                cur_step, root, project, experiment, varin, domain, model, existing_input )

                        else:
                            
                            varin=var
                        template=general_parameters(root,project,experiment,var,domain,model="None",step=step)

                        # Normal mode — each step gets its own dict
                        cfile_dict = build_cfile(template,
                            cur_step, root, project, experiment, varin, domain, model, cur_step
                        )

                        cfile_dict["requests"][0]["STAGES"] = [cur_step]
                        path_out = load_cfile_path(cur_step, project, domain, varin, experiment, model)
                        write_cfile(path_out, cfile_dict)
                        write_jfile(project, experiment, varin, domain, step=cur_step, model=model, cluster_cfg=cluster_cfg)

                    if step == "all":
                        # Write the combined cfile once
                        cfile_dict_all["requests"][0]["STAGES"] = steps_to_run
                        path_out = load_cfile_path(step, project, domain, var, experiment, model)
                        write_cfile(path_out, cfile_dict_all)
                        write_jfile(project, experiment, var, domain, step="all", model=model, cluster_cfg=cluster_cfg)
    

def parse_args():
    """
    Parse command-line arguments for the CICA climate pipeline configuration.

    This function uses argparse to handle user inputs from the command line.

    Command-line arguments
    ----------------------
    project : str
        The project name. Must be one of SUPPORTED_PROJECTS, e.g., "ERA5", "CERRA-Land", "E-OBS".
    step : str
        The processing step to run. Must be one of SUPPORTED_STEPS, e.g., "homogenization", "indices", or "all".
    cluster : str
        The HPC cluster where jobs will run. Must be one of SUPPORTED_CLUSTERS.

    Returns
    -------
    argparse.Namespace
        Namespace object containing the parsed arguments: project, step, and cluster.

    """
    parser = argparse.ArgumentParser(
        description="Produce CICA climate pipeline configuration and job files"
    )

    parser.add_argument(
        "project",
        choices=SUPPORTED_PROJECTS,
        help="Project name"
    )

    parser.add_argument(
        "step",
        choices=SUPPORTED_STEPS,
        help="Processing step or 'all'"
    )

    parser.add_argument(
        "cluster",
        choices=SUPPORTED_CLUSTERS,
        help="HPC cluster where jobs will run"
    )
    return parser.parse_args()


def main():
    """
    Main entry point for producing CICA climate pipeline configuration 
    (cfile) and job files.

    The script takes the following command-line arguments:
        project : str
            The project name. Must be one of SUPPORTED_PROJECTS, e.g., "ERA5", "CERRA-Land", "E-OBS".
        step : str
            The processing step to run. Must be one of SUPPORTED_STEPS, e.g., "homogenization", "indices", or "all".
        cluster : str
            The HPC cluster where jobs will be executed. Must be one of SUPPORTED_CLUSTERS.

    For each project, step, experiment, variable, domain, and model, the function:
        1. Loads the appropriate YAML configuration template.
        2. Generates or updates configuration dictionaries for each processing step.
        3. Writes the configuration files (cfiles) and associated job scripts (jfiles)
           to the correct directories.
        4. Handles special cases such as aliases, multiple steps ("all"), and existing input paths.

    Example usage from command line:
        python produce_cfile.py E-OBS homogenization gpfs

    Returns
    -------
    None
        Outputs are written to disk (cfiles and jfiles) but nothing is returned.
    """
    args = parse_args()
    project = args.project
    step = args.step
    cluster = args.cluster
    cluster_cfg = get_cluster_config(cluster)
    logger.info("====================================")
    logger.info("Project : %s | Step : %s | Cluster : %s", project, step, cluster)
    logger.info("====================================")
    produce_cfile(
        project=project,
        step=step,
        cluster_cfg=cluster_cfg
    )


if __name__ == "__main__":
    main()




