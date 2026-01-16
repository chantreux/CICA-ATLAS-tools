"""
Unified parameter files for CICA-ATLAS Products module.
Compatible with workflow/generation_scripts/ structure for future unification.
"""

# =============================================================================
# IMPORTS FROM projects.py
# =============================================================================
from .projects import (
    # Core project definitions
    CANONICAL_PROJECTS,
    PROJECT_ALIASES,
    SUPPORTED_PROJECTS,
    OBSERVATION_PROJECTS,
    PROJECTION_PROJECTS,
    
    # Project configuration dictionaries
    PROJECT_ROOTS,
    PROJECT_EXPERIMENTS,
    PROJECT_PERIODS,
    PROJECT_DOMAINS,
    PROJECT_IDS,
    PROJECT_GRIDS,
    PROJECT_DATA_TYPE,
    PROJECT_MEMBERS_SUBSET,
    
    # Helper functions from projects.py
    get_project_root,
    is_observation_project,
    is_projection_project,
    get_project_experiments,
    get_project_periods,
    get_project_domains,
    get_data_type,
    get_members_subset,
)

# =============================================================================
# IMPORTS FROM projects_products.py
# =============================================================================
from .projects_products import (
    # Generated dictionaries
    PROJECT_TRENDS,
    PROJECT_BASELINES,
    PROJECT_ROBUSTNESS,
    CLIMATOLOGY_FUTURE_PERIODS,
    REGION_MASKS,
    
    # Helper functions from projects_products.py
    generate_baselines_project,
    get_baseline_project,
    get_scenario_lines,
    get_scenario_lines_project_var,
    get_warming_levels,
    get_spatial_mask,
    get_period_climatology,
    get_period_experiments,
    get_region_mask,
)

# =============================================================================
# IMPORTS FROM variables.py
# =============================================================================
from .variables import (
    # Anomaly configuration
    RELATIVE_ANOMALY_VARS,
    get_anomaly_dict,
    
    # Time aggregation
    AGG_FUNCTIONS_FILE,
    get_time_aggregation,
    
    # Period aggregation
    EXTREME_PERIOD_AGGREGATION,
    get_period_aggregation,
    
    # Time filters
    ANNUAL_ONLY_VARS,
    get_time_filters_variable,
    
    # Variable lists
    VAR_NOT_CALCULATED,
    URBAN_VARS,
    LAND_ONLY_VARS,
    OCEAN_ONLY_VARS,
    VERSION_VARIABLES,
    get_variables_for_version,
)

# =============================================================================
# IMPORTS FROM regions.py  
# =============================================================================
from .regions import (
    AR6_REGIONS,
)

# =============================================================================
# IMPORTS FROM cluster_resources.py
# =============================================================================
from .cluster_resources import (
    PROJECT_RESOURCES,
    PROJECT_CHUNKS,
    get_cluster_resources,
    get_chunk_config,
)

# =============================================================================
# PUBLIC API
# =============================================================================
__all__ = [
    # -------------------------------------------------------------------------
    # From projects.py - Core definitions
    # -------------------------------------------------------------------------
    "CANONICAL_PROJECTS",
    "PROJECT_ALIASES",
    "SUPPORTED_PROJECTS",
    "OBSERVATION_PROJECTS",
    "PROJECTION_PROJECTS",
    "PROJECT_ROOTS",
    "PROJECT_EXPERIMENTS",
    "PROJECT_PERIODS",
    "PROJECT_DOMAINS",
    "PROJECT_IDS",
    "PROJECT_GRIDS",
    "PROJECT_DATA_TYPE",
    "PROJECT_MEMBERS_SUBSET",
    
    # -------------------------------------------------------------------------
    # From projects.py - Helper functions
    # -------------------------------------------------------------------------
    "get_project_root",
    "is_observation_project",
    "is_projection_project",
    "get_project_experiments",
    "get_project_periods",
    "get_project_domains",
    "get_data_type",
    "get_members_subset",
    
    # -------------------------------------------------------------------------
    # From projects_products.py - Generated dictionaries
    # -------------------------------------------------------------------------
    "PROJECT_TRENDS",
    "PROJECT_BASELINES",
    "PROJECT_ROBUSTNESS",
    "CLIMATOLOGY_FUTURE_PERIODS",
    "REGION_MASKS",
    
    # -------------------------------------------------------------------------
    # From projects_products.py - Helper functions
    # -------------------------------------------------------------------------
    "generate_baselines_project",
    "get_baseline_project",
    "get_scenario_lines",
    "get_scenario_lines_project_var",
    "get_warming_levels",
    "get_spatial_mask",
    "get_period_climatology",
    "get_period_experiments",
    "get_region_mask",
    
    # -------------------------------------------------------------------------
    # From variables.py - Variable configuration
    # -------------------------------------------------------------------------
    "RELATIVE_ANOMALY_VARS",
    "get_anomaly_dict",
    "AGG_FUNCTIONS_FILE",
    "get_time_aggregation",
    "EXTREME_PERIOD_AGGREGATION",
    "get_period_aggregation",
    "ANNUAL_ONLY_VARS",
    "get_time_filters_variable",
    "VAR_NOT_CALCULATED",
    "URBAN_VARS",
    "LAND_ONLY_VARS",
    "OCEAN_ONLY_VARS",
    "VERSION_VARIABLES",
    "get_variables_for_version",
    
    # -------------------------------------------------------------------------
    # From regions.py - Regional configuration
    # -------------------------------------------------------------------------
    "AR6_REGIONS",
    
    # -------------------------------------------------------------------------
    # From cluster_resources.py - Cluster resource configuration
    # -------------------------------------------------------------------------
    "PROJECT_RESOURCES",
    "PROJECT_CHUNKS",
    "get_cluster_resources",
    "get_chunk_config",
]
