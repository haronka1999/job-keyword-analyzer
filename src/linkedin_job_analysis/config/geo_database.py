"""LinkedIn geo ID database for location lookup with fuzzy matching."""

from difflib import get_close_matches

# Comprehensive geo ID database - ALL KEYS IN LOWERCASE
GEO_DATABASE = {
    # North America
    "united states": "103644278",
    "canada": "101174742",
    "mexico": "103323778",
    # Europe
    "united kingdom": "101165590",
    "germany": "101282230",
    "france": "105015875",
    "spain": "105646813",
    "italy": "103350119",
    "netherlands": "102890719",
    "switzerland": "106693272",
    "sweden": "105117694",
    "norway": "103819153",
    "denmark": "104514075",
    "belgium": "100565514",
    "austria": "103883259",
    "poland": "105072130",
    "ireland": "104738515",
    "portugal": "100364837",
    "greece": "104677530",
    "czech republic": "104508036",
    "romania": "106670623",
    "hungary": "100288700",
    "finland": "100456013",
    # Asia Pacific
    "australia": "101452733",
    "india": "102713980",
    "china": "102890883",
    "japan": "101355337",
    "singapore": "102454443",
    "south korea": "106779903",
    "hong kong": "102095887",
    "new zealand": "105490917",
    "indonesia": "102478259",
    "malaysia": "106808692",
    "thailand": "105149562",
    "philippines": "103121230",
    "vietnam": "104195383",
    "taiwan": "104187078",
    # Middle East & Africa
    "united arab emirates": "104305776",
    "saudi arabia": "103164761",
    "israel": "101620260",
    "south africa": "104035573",
    "egypt": "106155005",
    "nigeria": "105365761",
    "kenya": "100446943",
    # South America
    "brazil": "106057199",
    "argentina": "100876405",
    "chile": "104621616",
    "colombia": "100876405",
    "peru": "102927786",
    # Common aliases
    "usa": "103644278",
    "us": "103644278",
    "uk": "101165590",
    "uae": "104305776",
}


def get_geo_id(location_name):
    """
    Get geo ID for a location name with fuzzy matching support.

    Args:
        location_name: Location name (case-insensitive)

    Returns:
        Geo ID string

    Raises:
        ValueError: If location not found (with suggestions if available)
    """
    # Normalize input to lowercase
    location = location_name.strip().lower()

    # Exact match
    if location in GEO_DATABASE:
        return GEO_DATABASE[location]

    # Fuzzy match - find close matches
    close_matches = get_close_matches(
        location,
        GEO_DATABASE.keys(),
        n=3,  # Return top 3 matches
        cutoff=0.6,  # 60% similarity threshold
    )

    if close_matches:
        suggestions = ", ".join(f"'{match}'" for match in close_matches)
        raise ValueError(
            f"Location '{location_name}' not found in database.\n"
            f"Did you mean: {suggestions}?\n"
            f"Use list_available_locations() to see all available locations."
        )
    else:
        raise ValueError(
            f"Location '{location_name}' not found in database.\n"
            f"Use list_available_locations() to see all available locations.\n"
            f"To add a custom location, update GEO_DATABASE in "
            f"src/linkedin_job_analysis/config/geo_database.py"
        )


def list_available_locations():
    """Return sorted list of all available locations."""
    return sorted(GEO_DATABASE.keys())


def add_location(location_name, geo_id):
    """
    Add a new location to the database at runtime.

    Args:
        location_name: Display name for location (will be converted to lowercase)
        geo_id: LinkedIn geo ID string

    Example:
        add_location("Berlin, Germany", "106967730")
    """
    GEO_DATABASE[location_name.lower()] = geo_id
    print(f"[INFO] Added location '{location_name.lower()}' with geo ID {geo_id}")


def get_database_size():
    """Return the number of locations in the database."""
    return len(GEO_DATABASE)
