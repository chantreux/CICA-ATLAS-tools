"""
Unified parameter files for CICA-ATLAS Products module.
Compatible with workflow/generation_scripts/ structure for future unification.
"""

from .projects import (
    # Core definitions
    CANONICAL_PROJECTS,
    PROJECT_ALIASES,
    SUPPORTED_PROJECTS,
    OBSERVATION_PROJECTS,
    PROJECTION_PROJECTS,
    
    # Project properties
    PROJECT_ROOTS,
    PROJECT_EXPERIMENTS,
    PROJECT_PERIODS,
    PROJECT_DOMAINS,
    PROJECT_IDS,
    PROJECT_GRIDS,
    
    # Products-specific
    PROJECT_DATA_TYPE,
    PROJECT_TRENDS,
    PROJECT_ROBUSTNESS,
    BASELINES,
    CLIMATOLOGY_PERIODS,
    
    # Helper functions
    get_project_root,
    is_observation_project,
    is_projection_project,
    get_project_experiments,
    get_project_periods,
    get_project_domains,
    get_scenario_lines,
    get_warming_levels,
    get_spatial_mask,
    get_baseline_dict,
    get_period_climatology_dict,
    get_period_experiments_dict,
    get_scenario_lines_dict,
    get_data_type,
    get_trend_enabled,
)

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
    get_time_filters_dict,
    
    # Variable lists
    VAR_NOT_CALCULATED,
    URBAN_VARS,
    LAND_ONLY_VARS,
    OCEAN_ONLY_VARS,
    VERSION_VARIABLES,
    get_variables_for_version,
)

from .regions import (
    REGION_MASKS,
    TIME_FILTERS,
    AR6_REGIONS,
    get_region_mask,
    get_time_filters,
)

__all__ = [
    # Projects
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
    "PROJECT_TRENDS",
    "PROJECT_ROBUSTNESS",
    "BASELINES",
    "CLIMATOLOGY_PERIODS",
    "get_project_root",
    "is_observation_project",
    "is_projection_project",
    "get_project_experiments",
    "get_project_periods",
    "get_project_domains",
    "get_scenario_lines",
    "get_warming_levels",
    "get_spatial_mask",
    "get_baseline_dict",
    "get_period_climatology_dict",
    "get_period_experiments_dict",
    "get_scenario_lines_dict",
    "get_data_type",
    "get_trend_enabled",
    
    # Variables
    "RELATIVE_ANOMALY_VARS",
    "get_anomaly_dict",
    "AGG_FUNCTIONS_FILE",
    "get_time_aggregation",
    "EXTREME_PERIOD_AGGREGATION",
    "get_period_aggregation",
    "ANNUAL_ONLY_VARS",
    "get_time_filters_dict",
    "VAR_NOT_CALCULATED",
    "URBAN_VARS",
    "LAND_ONLY_VARS",
    "OCEAN_ONLY_VARS",
    "VERSION_VARIABLES",
    "get_variables_for_version",
    
    # Regions
    "REGION_MASKS",
    "TIME_FILTERS",
    "AR6_REGIONS",
    "get_region_mask",
    "get_time_filters",
]
