"""
Regional parameters for CICA-ATLAS Products module.


"""




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

