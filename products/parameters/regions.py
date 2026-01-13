"""
Regional parameters for CICA-ATLAS Products module.

This module contains all region-specific parameters including:
- Regional mask file paths
- Time filters configuration
- AR6 reference regions

Compatible with workflow/generation_scripts/ structure for future unification.
"""


# =============================================================================
# REGION MASKS
# =============================================================================

# Region mask files per set
# (used in config['products'][product_key]['region_aggregation']['mask_file'])
REGION_MASKS = {
    "AR6": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/resources/resources/reference-regions/IPCC-WGI-reference-regions-v4_areas.geojson",
    "eucra": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/resources/resources/reference-regions/EUCRA_areas.geojson",
    "european-countries": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/resources/resources/reference-regions/european-countries_areas.geojson",
    "megacities": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/resources/resources/reference-regions/megacities.geojson",
    "cities-rural": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/resources/resources/reference-regions/cities_contour.geojson",
    "cities-urban": "/lustre/gmeteo/WORK/chantreuxa/cica/Products/products/resources/resources/reference-regions/cities_contour.geojson"
}


# =============================================================================
# TIME FILTERS
# =============================================================================

# Time filters configuration
TIME_FILTERS = {
    "Annual": "01-12",
    "DecFeb": "12-02",
    "MarMay": "03-05",
    "JunAug": "06-08",
    "SepNov": "09-11",
    "Jan": "01-01",
    "Feb": "02-02",
    "Mar": "03-03",
    "Apr": "04-04",
    "May": "05-05",
    "Jun": "06-06",
    "Jul": "07-07",
    "Aug": "08-08",
    "Sep": "09-09",
    "Oct": "10-10",
    "Nov": "11-11",
    "Dec": "12-12"
}


# =============================================================================
# AR6 REFERENCE REGIONS
# =============================================================================

# AR6 reference regions configuration
AR6_REGIONS = {
    "acronyms": [
        'GIC', 'NWN', 'NEN', 'WNA', 'CNA', 'ENA', 'NCA', 'SCA', 'CAR',
        'NWS', 'NSA', 'NES', 'SAM', 'SWS', 'SES', 'SSA',
        'NEU', 'WCE', 'EEU', 'MED',
        'SAH', 'WAF', 'CAF', 'NEAF', 'SEAF', 'WSAF', 'ESAF', 'MDG',
        'RAR', 'WSB', 'ESB', 'RFE',
        'WCA', 'ECA', 'TIB', 'EAS', 'ARP', 'SAS', 'SEA',
        'NAU', 'CAU', 'EAU', 'SAU', 'NZ',
        'EAN', 'WAN',
        'ARO', 'NPO', 'EPO', 'SPO', 'NAO', 'EAO', 'SAO', 'ARS', 'BOB', 'EIO', 'SIO', 'SOO'
    ],
    "names": [
        'Greenland/Iceland', 'N.W.North-America', 'N.E.North-America',
        'W.North-America', 'C.North-America', 'E.North-America',
        'N.Central-America', 'S.Central-America', 'Caribbean',
        'N.W.South-America', 'N.South-America', 'N.E.South-America',
        'South-American-Monsoon', 'S.W.South-America', 'S.E.South-America', 'S.South-America',
        'N.Europe', 'West&Central-Europe', 'E.Europe', 'Mediterranean',
        'Sahara', 'Western-Africa', 'Central-Africa', 'N.Eastern-Africa',
        'S.Eastern-Africa', 'W.Southern-Africa', 'E.Southern-Africa', 'Madagascar',
        'Russian-Arctic', 'W.Siberia', 'E.Siberia', 'Russian-Far-East',
        'W.C.Asia', 'E.C.Asia', 'Tibetan-Plateau', 'E.Asia', 'Arabian-Peninsula',
        'S.Asia', 'S.E.Asia',
        'N.Australia', 'C.Australia', 'E.Australia', 'S.Australia', 'New-Zealand',
        'E.Antarctica', 'W.Antarctica',
        'Arctic-Ocean', 'N.Pacific-Ocean', 'Equatorial.Pacific-Ocean', 'S.Pacific-Ocean',
        'N.Atlantic-Ocean', 'Equatorial.Atlantic-Ocean', 'S.Atlantic-Ocean',
        'Arabian-Sea', 'Bay-of-Bengal', 'Equatorial.Indic-Ocean', 'S.Indic-Ocean', 'Southern-Ocean'
    ],
    "ids": list(range(58)),
    "groups": {
        "Ocean": ["ARO", "NPO", "EPO", "SPO", "NAO", "EAO", "SAO", "ARS", "BOB", "EIO", "SIO", "SOO"],
        "Continent": [
            "GIC", "NWN", "NEN", "WNA", "CNA", "ENA", "NCA", "SCA",
            "NWS", "NSA", "NES", "SAM", "SWS", "SES", "SSA",
            "NEU", "WCE", "EEU", "SAH", "WAF", "CAF", "NEAF", "SEAF", "WSAF", "ESAF", "MDG",
            "RAR", "WSB", "ESB", "RFE", "WCA", "ECA", "TIB", "EAS", "ARP", "SAS",
            "NAU", "CAU", "EAU", "SAU", "NZ", "EAN", "WAN"
        ],
        "Continent_and_ocean": ["CAR", "MED", "SEA"],
        "Russia": ["EEU", "WSB", "ESB", "RAR"],
        "Europe": ["MED", "WCE", "NEU"],
        "Not_Europe": [
            'GIC', 'NWN', 'NEN', 'WNA', 'CNA', 'ENA', 'NCA', 'SCA', 'CAR',
            'NWS', 'NSA', 'NES', 'SAM', 'SWS', 'SES', 'SSA',
            'EEU', 'SAH', 'WAF', 'CAF', 'NEAF', 'SEAF', 'WSAF', 'ESAF', 'MDG',
            'RAR', 'WSB', 'ESB', 'RFE', 'WCA', 'ECA', 'TIB', 'EAS', 'ARP', 'SAS', 'SEA',
            'NAU', 'CAU', 'EAU', 'SAU', 'NZ', 'EAN', 'WAN',
            'ARO', 'NPO', 'EPO', 'SPO', 'NAO', 'EAO', 'SAO', 'ARS', 'BOB', 'EIO', 'SIO', 'SOO'
        ],
        "Antarctica": ["WAN", "EAN"]
    }
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_region_mask(set_name: str) -> str:
    """
    Get region mask file path for a set.
    
    Used in config['products'][product_key]['region_aggregation']['mask_file'].
    
    Parameters
    ----------
    set_name : str
        Set name (e.g., "AR6", "eucra", "european-countries")
        
    Returns
    -------
    str or None
        Path to region mask file, or None if not found
    """
    return REGION_MASKS.get(set_name)


def get_time_filters() -> dict:
    """
    Get time filters dictionary.
    
    Returns
    -------
    dict
        Dictionary mapping time filter names to month ranges
    """
    return TIME_FILTERS.copy()
