from variables import PROJECT_STEPS, PROJECT_STEP_VARIABLES

# Canonical projects
CANONICAL_PROJECTS = [
    "ERA5",
    "CERRA-Land",
    "E-OBS",
]

# Aliases: alias -> canonical project
PROJECT_ALIASES = {
    "E-OBSv26": "E-OBS",
}

# Build SUPPORTED_PROJECTS including aliases
SUPPORTED_PROJECTS = CANONICAL_PROJECTS + list(PROJECT_ALIASES.keys())

# Roots for canonical projects
PROJECT_ROOTS = {
    "ERA5": "None",
    "CERRA-Land":"/gpfs/projects/meteo/WORK/PROYECTOS/2022_C3S_Atlas/workflow/datasets/CICAv2/CERRA-land/",
    "E-OBS": "/lustre/gmeteo/WORK/PROYECTOS/2022_C3S_Atlas/workflow/datasets/C3S-ATLAS-climate-pipeline/",
}
# If not specified, alias inherits canonical project root
PROJECT_ROOT_ALIASES = {
    "E-OBSv26": "/lustre/gmeteo/WORK/PROYECTOS/2022_C3S_Atlas/workflow/datasets/C3S-ATLAS-climate-pipeline/E-OBSv26/", 
}


OBSERVATION_PROJECTS = [
    "ERA5",
    "CERRA-Land",
    "E-OBS",
]

# Available experiments per project
PROJECT_EXPERIMENTS = {
    "CORDEX-CORE": ["historical", "rcp26", "rcp85"],
    "ERA5": ["None"],
    "CERRA-Land": ["None"],
    "E-OBS": ["None"]
}

# Historical and future periods per project
PROJECT_PERIODS = {
    "CORDEX-CORE": {"hist": (1970, 2005), "fut": (2006, 2100)},
    "ERA5": {"hist": (1940, 2022), "fut": None},
    "CERRA-Land": {"hist": (1985, 2020), "fut": None},
    "E-OBS": {"hist": (1950, 2024), "fut": None}
}

# Domains per project
PROJECT_DOMAINS = {
    "CORDEX-CORE": ["AFR-22","AUS-22","CAM-22","EAS-22","EUR-22",
                    "NAM-22","SAM-22","SEA-22","WAS-22","CAS-22"],
    "ERA5": ["None"],
    "CERRA-Land": ["None"],
    "E-OBS": ["None"]
}

# Standard project IDs for variable mapping
PROJECT_IDS = {
    "ERA5": "reanalysis-era5-single-levels",
    "CERRA-Land": "reanalysis-cerra-land",
    "E-OBS": "insitu-gridded-observations-europe",
    "CORDEX-CORE": "projections-cordex-domains-single-levels"
}

# Reference grids per project
PROJECT_GRIDS = {
    "CERRA-Land": {
        "grid": "land_sea_mask_grd006p25",
        "interpolation_step": "previous"  # or "posterior"
    },
    "E-OBS": {
        "grid": "land_sea_mask_grd012_EOBS_EUR11-CORDEX",
        "interpolation_step": "posterior"  # or "previous"
    }
}


def validate_project_constants():
    """Check that all SUPPORTED_PROJECTS are defined in all project constants."""
    dicts_to_check = {
        "PROJECT_ROOTS": PROJECT_ROOTS,
        "PROJECT_EXPERIMENTS": PROJECT_EXPERIMENTS,
        "PROJECT_PERIODS": PROJECT_PERIODS,
        "PROJECT_DOMAINS": PROJECT_DOMAINS,
        "PROJECT_IDS": PROJECT_IDS,
    }

    missing = {}
    for project in SUPPORTED_PROJECTS:
        for dict_name, dict_obj in dicts_to_check.items():
            if project not in dict_obj:
                missing.setdefault(project, []).append(dict_name)

    if missing:
        error_msg = "Missing project definitions detected:\n"
        for proj, dicts in missing.items():
            error_msg += f" - {proj} missing in: {', '.join(dicts)}\n"
        raise ValueError(error_msg)

    print("✅ All supported projects are properly defined in all constants.")
    return True



# Example usage
if __name__ == "__main__":
    validate_project_constants()

