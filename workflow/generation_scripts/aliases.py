from variables import PROJECT_STEPS as PROJECT_STEPS_CANONICAL, PROJECT_STEP_VARIABLES as PROJECT_STEP_VARIABLES_CANONICAL

from projects import (
    SUPPORTED_PROJECTS,
    PROJECT_ALIASES,
    PROJECT_ROOTS,
    PROJECT_ROOT_ALIASES,
    PROJECT_EXPERIMENTS,
    PROJECT_PERIODS,
    PROJECT_DOMAINS,
    PROJECT_IDS,
    PROJECT_GRIDS,
    OBSERVATION_PROJECTS as OBSERVATION_PROJECTS_CANONICAL,
)

def propagate_aliases():
    """Return all dictionaries with aliases automatically filled in, except roots."""
    # Make copies to avoid modifying originals
    steps = dict(PROJECT_STEPS_CANONICAL)
    step_vars = dict(PROJECT_STEP_VARIABLES_CANONICAL)
    experiments = dict(PROJECT_EXPERIMENTS)
    periods = dict(PROJECT_PERIODS)
    domains = dict(PROJECT_DOMAINS)
    ids = dict(PROJECT_IDS)
    grids = dict(PROJECT_GRIDS)
    observation_projects = list(OBSERVATION_PROJECTS_CANONICAL)

    for alias, canonical in PROJECT_ALIASES.items():
        if canonical not in PROJECT_STEPS_CANONICAL:
            raise ValueError(f"Alias '{alias}' references unknown canonical project '{canonical}'")
        # Propagate for every dictionary except roots
        steps[alias] = steps[canonical]
        step_vars[alias] = step_vars[canonical]
        if canonical in experiments: experiments[alias] = experiments[canonical]
        if canonical in periods: periods[alias] = periods[canonical]
        if canonical in domains: domains[alias] = domains[canonical]
        if canonical in ids: ids[alias] = ids[canonical]
        if canonical in grids: grids[alias] = grids[canonical]

        # Append alias to observation projects if canonical is in it
        if canonical in observation_projects:
            observation_projects.append(alias)

    return {
        "PROJECT_STEPS": steps,
        "PROJECT_STEP_VARIABLES": step_vars,
        "PROJECT_EXPERIMENTS": experiments,
        "PROJECT_PERIODS": periods,
        "PROJECT_DOMAINS": domains,
        "PROJECT_IDS": ids,
        "PROJECT_GRIDS": grids,
        "OBSERVATION_PROJECTS": observation_projects,
    }

def get_project_root(project: str) -> str:
    """
    Return root path for a project or its alias.
    
    Logic:
    1. If project is canonical and has a root, return it.
    2. If project is an alias:
       - Check if PROJECT_ROOT_ALIASES overrides root for this alias.
       - Otherwise return the canonical project's root.
    """
    if project in PROJECT_ROOTS:
        return PROJECT_ROOTS[project]

    if project in PROJECT_ALIASES:
        canonical = PROJECT_ALIASES[project]
        # If alias has a custom root, use it; else fallback to canonical
        return PROJECT_ROOT_ALIASES.get(project, PROJECT_ROOTS.get(canonical))

    raise ValueError(f"Unknown project: {project}")


# Automatically populate dictionaries on import
ALIASED = propagate_aliases()
PROJECT_STEPS = ALIASED["PROJECT_STEPS"]
PROJECT_STEP_VARIABLES = ALIASED["PROJECT_STEP_VARIABLES"]
PROJECT_EXPERIMENTS = ALIASED["PROJECT_EXPERIMENTS"]
PROJECT_PERIODS = ALIASED["PROJECT_PERIODS"]
PROJECT_DOMAINS = ALIASED["PROJECT_DOMAINS"]
PROJECT_IDS = ALIASED["PROJECT_IDS"]
PROJECT_GRIDS = ALIASED["PROJECT_GRIDS"]
OBSERVATION_PROJECTS = ALIASED["OBSERVATION_PROJECTS"]
