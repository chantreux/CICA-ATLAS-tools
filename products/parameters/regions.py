"""
Regional masks and configurations for CICA-ATLAS Products module.

This module contains:
- Regional mask file paths
- Time filter configurations
- AR6 region definitions
- Helper functions for accessing region parameters
"""

# ============================================================================
# Region Masks
# ============================================================================

# Regional mask file paths per set
# Used in config['products'][product_key]['region_aggregation']['mask_file']
REGION_MASKS = {
    "AR6": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/resources/resources/reference-regions/IPCC-WGI-reference-regions-v4_areas.geojson",
    "eucra": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/resources/resources/reference-regions/EUCRA_areas.geojson",
    "european-countries": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/resources/resources/reference-regions/european-countries_areas.geojson",
    "megacities": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/resources/resources/reference-regions/megacities.geojson",
    "cities-rural": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/resources/resources/reference-regions/cities_contour.geojson",
    "cities-urban": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/resources/resources/reference-regions/cities_contour.geojson"
}

# ============================================================================
# Time Filters
# ============================================================================

# Time filter configurations per region set
# (Currently not used in the original code, but kept for compatibility)
TIME_FILTERS = {
    "default": {
        "Annual": "01-12",
        "DecFeb": "12-02",
        "MarMay": "03-05",
        "JunAug": "06-08",
        "SepNov": "09-11"
    }
}

# ============================================================================
# AR6 Regions
# ============================================================================

# AR6 reference region definitions
# Used for validation and region identification
AR6_REGIONS = {
    "Name": [
        'Greenland/Iceland', 'N.W.North-America', 'N.E.North-America',
        'W.North-America', 'C.North-America', 'E.North-America',
        'N.Central-America', 'S.Central-America', 'Caribbean',
        'N.W.South-America', 'N.South-America', 'N.E.South-America',
        'South-American-Monsoon', 'S.W.South-America', 'S.E.South-America',
        'S.South-America', 'N.Europe', 'West&Central-Europe', 'E.Europe',
        'Mediterranean', 'Sahara', 'Western-Africa', 'Central-Africa',
        'N.Eastern-Africa', 'S.Eastern-Africa', 'W.Southern-Africa',
        'E.Southern-Africa', 'Madagascar', 'Russian-Arctic', 'W.Siberia',
        'E.Siberia', 'Russian-Far-East', 'W.C.Asia', 'E.C.Asia',
        'Tibetan-Plateau', 'E.Asia', 'Arabian-Peninsula', 'S.Asia',
        'S.E.Asia', 'N.Australia', 'C.Australia', 'E.Australia',
        'S.Australia', 'New-Zealand', 'E.Antarctica', 'W.Antarctica',
        'Arctic-Ocean', 'N.Pacific-Ocean', 'Equatorial.Pacific-Ocean',
        'S.Pacific-Ocean', 'N.Atlantic-Ocean', 'Equatorial.Atlantic-Ocean',
        'S.Atlantic-Ocean', 'Arabian-Sea', 'Bay-of-Bengal',
        'Equatorial.Indic-Ocean', 'S.Indic-Ocean', 'Southern-Ocean'
    ],
    "Id": list(range(58)),
    "Acronym": [
        'GIC', 'NWN', 'NEN', 'WNA', 'CNA', 'ENA', 'NCA', 'SCA', 'CAR',
        'NWS', 'NSA', 'NES', 'SAM', 'SWS', 'SES', 'SSA', 'NEU', 'WCE',
        'EEU', 'MED', 'SAH', 'WAF', 'CAF', 'NEAF', 'SEAF', 'WSAF', 'ESAF',
        'MDG', 'RAR', 'WSB', 'ESB', 'RFE', 'WCA', 'ECA', 'TIB', 'EAS',
        'ARP', 'SAS', 'SEA', 'NAU', 'CAU', 'EAU', 'SAU', 'NZ', 'EAN',
        'WAN', 'ARO', 'NPO', 'EPO', 'SPO', 'NAO', 'EAO', 'SAO', 'ARS',
        'BOB', 'EIO', 'SIO', 'SOO'
    ],
    "Ocean": [
        "ARO", "NPO", "EPO", "SPO", "NAO", "EAO", "SAO", "ARS", "BOB",
        "EIO", "SIO", "SOO"
    ],
    "Continent": [
        "GIC", "NWN", "NEN", "WNA", "CNA", "ENA", "NCA", "SCA", "NWS",
        "NSA", "NES", "SAM", "SWS", "SES", "SSA", "NEU", "WCE", "EEU",
        "SAH", "WAF", "CAF", "NEAF", "SEAF", "WSAF", "ESAF", "MDG", "RAR",
        "WSB", "ESB", "RFE", "WCA", "ECA", "TIB", "EAS", "ARP", "SAS",
        "NAU", "CAU", "EAU", "SAU", "NZ", "EAN", "WAN"
    ],
    "Continent_and_ocean": ["CAR", "MED", "SEA"],
    "Russia": ["EEU", "WSB", "ESB", "RAR"],
    "Europe": ["MED", "WCE", "NEU"],
    "Not_Europe": [
        'GIC', 'NWN', 'NEN', 'WNA', 'CNA', 'ENA', 'NCA', 'SCA', 'CAR',
        'NWS', 'NSA', 'NES', 'SAM', 'SWS', 'SES', 'SSA', 'EEU', 'SAH',
        'WAF', 'CAF', 'NEAF', 'SEAF', 'WSAF', 'ESAF', 'MDG', 'RAR', 'WSB',
        'ESB', 'RFE', 'WCA', 'ECA', 'TIB', 'EAS', 'ARP', 'SAS', 'SEA',
        'NAU', 'CAU', 'EAU', 'SAU', 'NZ', 'EAN', 'WAN', 'ARO', 'NPO',
        'EPO', 'SPO', 'NAO', 'EAO', 'SAO', 'ARS', 'BOB', 'EIO', 'SIO', 'SOO'
    ],
    "Antarctica": ["WAN", "EAN"]
}

# ============================================================================
# Helper Functions
# ============================================================================


def get_region_mask(set_name):
    """
    Get region mask file path for a given set.
    
    Used in config['products'][product_key]['region_aggregation']['mask_file']
    
    Args:
        set_name: Name of the region set (e.g., "AR6", "eucra")
        
    Returns:
        str or None: Path to region mask file, or None if set not found
    """
    return REGION_MASKS.get(set_name)


def get_time_filters(filter_type="default"):
    """
    Get time filters for a given filter type.
    
    Args:
        filter_type: Type of time filter configuration
        
    Returns:
        dict: Dictionary mapping filter names to month ranges
    """
    return TIME_FILTERS.get(filter_type, TIME_FILTERS["default"])
