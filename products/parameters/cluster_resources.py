"""
Cluster resource configuration for CICA-ATLAS products.

This module defines CPU, memory, and time allocation requirements
for different projects and product types. This centralized configuration
allows easy adjustment of cluster resources without modifying job templates.
"""

# =============================================================================
# CLUSTER RESOURCE CONFIGURATION BY PROJECT
# =============================================================================

PROJECT_RESOURCES = {
    # High memory projects
    'ORAS5': {
        'cpus': 1,
        'mem_per_cpu': '160gb',
        'time': '72:00:00',
        'partition': 'meteo_long'
    },
    'CORDEX-EUR-11': {
        'cpus': 1,
        'mem_per_cpu': '80gb',
        'time': '72:00:00',
        'partition': 'meteo_long'
    },
    'CERRA': {
        'cpus': 1,
        'mem_per_cpu': '60gb',
        'time': '72:00:00',
        'partition': 'meteo_long'
    },
    
    # Medium memory projects (40gb)
    'E-OBS': {
        'cpus': 1,
        'mem_per_cpu': '40gb',
        'time': '72:00:00',
        'partition': 'meteo_long'
    },
    'ERA5': {
        'cpus': 1,
        'mem_per_cpu': '40gb',
        'time': '72:00:00',
        'partition': 'meteo_long'
    },
    'ERA5-Land': {
        'cpus': 1,
        'mem_per_cpu': '20gb',
        'time': '72:00:00',
        'partition': 'meteo_long'
    },
    'CORDEX-CORE': {
        'cpus': 1,
        'mem_per_cpu': '40gb',
        'time': '72:00:00',
        'partition': 'meteo_long'
    },
    'CORDEX-CORERUR': {
        'cpus': 1,
        'mem_per_cpu': '40gb',
        'time': '72:00:00',
        'partition': 'meteo_long'
    },
    'CORDEX-COREURB': {
        'cpus': 1,
        'mem_per_cpu': '40gb',
        'time': '72:00:00',
        'partition': 'meteo_long'
    },
    'CORDEX-EUR-11RUR': {
        'cpus': 1,
        'mem_per_cpu': '40gb',
        'time': '72:00:00',
        'partition': 'meteo_long'
    },
    'CORDEX-EUR-11URB': {
        'cpus': 1,
        'mem_per_cpu': '40gb',
        'time': '72:00:00',
        'partition': 'meteo_long'
    },
    
    # Low memory projects
    'CMIP5': {
        'cpus': 1,
        'mem_per_cpu': '20gb',
        'time': '72:00:00',
        'partition': 'meteo_long'
    },
    
    # Multi-core projects with lower memory per CPU
    'CMIP6': {
        'cpus': 4,
        'mem_per_cpu': '8G',
        'time': '72:00:00',
        'partition': 'meteo_long'
    },
    'CPC': {
        'cpus': 4,
        'mem_per_cpu': '16gb',
        'time': '72:00:00',
        'partition': 'meteo_long'
    },
    'BERKELEY': {
        'cpus': 4,
        'mem_per_cpu': '16gb',
        'time': '72:00:00',
        'partition': 'meteo_long'
    },
    'CERRARUR': {
        'cpus': 4,
        'mem_per_cpu': '16gb',
        'time': '72:00:00',
        'partition': 'meteo_long'
    },
    'CERRAURB': {
        'cpus': 4,
        'mem_per_cpu': '16gb',
        'time': '72:00:00',
        'partition': 'meteo_long'
    },
    'SSTSAT': {
        'cpus': 4,
        'mem_per_cpu': '16gb',
        'time': '72:00:00',
        'partition': 'meteo_long'
    },
}

# =============================================================================
# CHUNK CONFIGURATION BY PROJECT
# =============================================================================

PROJECT_CHUNKS = {
    'ORAS5': {'lat': 90, 'lon': 180, 'chunknum': 8},
    'CORDEX-EUR-11': {'lat': 30, 'lon': 60, 'chunknum': 16},
    'CERRA': {'lat': 300, 'lon': 600, 'chunknum': 8},
    'E-OBS': {'lat': 30, 'lon': 60, 'chunknum': 16},
    'ERA5': {'lat': 70, 'lon': 140, 'chunknum': 3},
    'ERA5-Land': {'lat': 70, 'lon': 140, 'chunknum': 3},
    'CORDEX-CORE': {'lat': 70, 'lon': 140, 'chunknum': 3},
    'CMIP5': {'lat': 70, 'lon': 140, 'chunknum': 3},
    'CMIP6': {'lat': 30, 'lon': 60, 'chunknum': 3},
    'CPC': {'lat': 70, 'lon': 140, 'chunknum': 3},
    'BERKELEY': {'lat': 300, 'lon': 600, 'chunknum': 8},
    'SSTSAT': {'lat': 300, 'lon': 600, 'chunknum': 8},
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_cluster_resources(project: str, product_type: str = None) -> dict:
    """
    Get cluster resource configuration for a given project.
    
    Args:
        project: Project name (e.g., 'ORAS5', 'CMIP6', 'E-OBS')
        product_type: Product type (e.g., 'climatology', 'temporal_series', 'trends')
                     Currently not used but reserved for future customization
    
    Returns:
        Dictionary with keys: 'cpus', 'mem_per_cpu', 'time', 'partition'
    
    Raises:
        KeyError: If project is not found in PROJECT_RESOURCES
    
    Examples:
        >>> get_cluster_resources('ORAS5')
        {'cpus': 1, 'mem_per_cpu': '160gb', 'time': '72:00:00', 'partition': 'meteo_long'}
        
        >>> get_cluster_resources('CMIP6', 'temporal_series')
        {'cpus': 4, 'mem_per_cpu': '8G', 'time': '72:00:00', 'partition': 'meteo_long'}
    """
    if project not in PROJECT_RESOURCES:
        raise KeyError(
            f"Project '{project}' not found in cluster resources configuration. "
            f"Available projects: {', '.join(sorted(PROJECT_RESOURCES.keys()))}"
        )
    
    # Return a copy to prevent accidental modification
    return PROJECT_RESOURCES[project].copy()


def get_chunk_config(project: str) -> dict:
    """
    Get chunk configuration for a project.
    
    Args:
        project: Project name (e.g., 'ORAS5', 'CMIP6', 'E-OBS')
    
    Returns:
        Dictionary with keys: 'lat', 'lon', 'chunknum'
        Returns default configuration if project not found
    
    Examples:
        >>> get_chunk_config('ORAS5')
        {'lat': 90, 'lon': 180, 'chunknum': 8}
        
        >>> get_chunk_config('CMIP6')
        {'lat': 30, 'lon': 60, 'chunknum': 3}
    """
    # Default configuration if project not found
    default = {'lat': 70, 'lon': 140, 'chunknum': 3}
    return PROJECT_CHUNKS.get(project, default)
