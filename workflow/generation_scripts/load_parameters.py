import numpy as np
from dataclasses import dataclass
from pathlib import Path
import importlib
from commons.yml import read_yaml_file
# Import aliased project settings
from aliases import (
    SUPPORTED_PROJECTS,         # Includes canonical + alias projects
    OBSERVATION_PROJECTS,       # Includes canonical + alias projects
    PROJECT_STEP_VARIABLES,     # Variables per step, canonical + aliases
    PROJECT_EXPERIMENTS,        # Experiments per project, canonical + aliases
    PROJECT_PERIODS,            # Periods per project, canonical + aliases
    PROJECT_DOMAINS,            # Domains per project, canonical + aliases
    PROJECT_IDS,                # Standard project IDs, canonical + aliases
    PROJECT_GRIDS,              # Reference grids, canonical + aliases
    get_project_root            # Function to get root path for canonical or alias project
)



@dataclass
class Dataset:
    project: str

    def __post_init__(self):
        if self.project not in SUPPORTED_PROJECTS:
            raise ValueError(f"Unsupported project '{self.project}'")
        self.project_type = self.load_project_type()
        self.available_exp = PROJECT_EXPERIMENTS.get(self.project, [])
        self.domain_list = PROJECT_DOMAINS.get(self.project, ["None"])

    # --- Step properties ---
    @property
    def homogenization_list(self):
        return self.get_step_variables("homogenization")

    @property
    def bias_correction_list(self):
        return self.get_step_variables("biasadjustment")

    @property
    def indices_list(self):
        return self.get_step_variables("indices")

    @property
    def range_list(self):
        return self.get_step_variables("range-skewness")

    @property
    def tasmaxba_list(self):
        return self.get_step_variables("tasmaxba-tasminba")

    @property
    def root(self) -> str:
        """Return the project root, resolving aliases automatically."""
        return get_project_root(self.project)

    def get_step_variables(self, step: str):
        """Return variables for a given step; None if step doesn't exist"""
        step_vars = PROJECT_STEP_VARIABLES.get(self.project, {}).get(step)
        return step_vars

    # --- Project type ---
    def load_project_type(self):
        return "observations" if self.project in OBSERVATION_PROJECTS else "projections"

    # --- Periods ---
    def load_period(self):
        periods = PROJECT_PERIODS.get(self.project)
        if periods is None:
            raise ValueError(f"No period defined for project '{self.project}'")
        hist = np.arange(periods["hist"][0], periods["hist"][1]+1)
        fut = np.arange(periods["fut"][0], periods["fut"][1]+1) if periods["fut"] else None
        return hist, fut

    def load_years(self, experiment):
        hist_period, fut_period = self.load_period()
        if experiment in ["historical", "None"]:
            return [hist_period[0], hist_period[-1]]
        elif fut_period is not None:
            return [fut_period[0], fut_period[-1]]
        else:
            return [hist_period[0], hist_period[-1]]

    # --- Variable mapping ---
    def var_mapping(self):
        """Return variable mapping from YAML"""
        variable_mapping_file = (
            Path(importlib.import_module("commons.resources.configurations").__file__).parent
            / "variable_config.yml"
        )
        map_variables = read_yaml_file(str(variable_mapping_file))
        configuration_variable = map_variables.get(self.load_project_id())
        return configuration_variable, variable_mapping_file

    def load_project_id(self):
        return PROJECT_IDS.get(self.project, self.project)

    # --- Reference grid ---
    def get_int_grid(self):
        project_info = PROJECT_GRIDS.get(self.project)
        grid_name = project_info.get("grid")
        interpolation_step = project_info.get("interpolation_step")
        if not grid_name:
            return None,None
        
        grid_path = Path(importlib.import_module("commons.resources.reference_grids").__file__).parent / grid_name
        return str(grid_path), interpolation_step

    # --- Index helper ---
    @staticmethod
    def index_only(index: str):
        """Strip 'ba' suffix if present"""
        return index.split("ba")[0] if "ba" in index else index