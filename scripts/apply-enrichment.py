"""
Apply enrichment data to schools.json.
Adds new fields (lat, lng, place_id, has_trial, line_id) and fills missing values.

Usage: python scripts/apply-enrichment.py
"""

import json
from datetime import date
from pathlib import Path

SITE_PATH = Path("d:/OneDrive/Claude/go-directory-tw/src/data/schools.json")
ENRICHMENT_PATH = Path("d:/OneDrive/Claude/go-directory-tw/scripts/output/enrichment.json")
TODAY = date.today().isoformat()


def main():
    with open(SITE_PATH, "r", encoding="utf-8") as f:
        schools = json.load(f)
    with open(ENRICHMENT_PATH, "r", encoding="utf-8") as f:
        enrichments = json.load(f)

    # Build enrichment lookup by slug
    enrich_map = {e["slug"]: e["updates"] for e in enrichments}

    updated_count = 0
    for school in schools:
        # Add new fields with defaults if missing
        school.setdefault("lat", None)
        school.setdefault("lng", None)
        school.setdefault("place_id", "")
        school.setdefault("has_trial", False)
        school.setdefault("line_id", "")

        # Apply enrichment if available
        updates = enrich_map.get(school["slug"])
        if updates:
            for key, value in updates.items():
                school[key] = value
            # Update data_sources
            if "outscraper" not in school.get("data_sources", []):
                school.setdefault("data_sources", []).append("outscraper")
            school["last_verified"] = TODAY
            updated_count += 1

    # Write back
    with open(SITE_PATH, "w", encoding="utf-8") as f:
        json.dump(schools, f, ensure_ascii=False, indent=2)

    print(f"Updated {updated_count}/{len(schools)} schools")
    print(f"All {len(schools)} schools now have new schema fields")

    # Quick stats
    has_rating = sum(1 for s in schools if s.get("google_rating"))
    has_latlng = sum(1 for s in schools if s.get("lat"))
    has_place = sum(1 for s in schools if s.get("place_id"))
    print(f"  google_rating: {has_rating}/{len(schools)}")
    print(f"  lat/lng: {has_latlng}/{len(schools)}")
    print(f"  place_id: {has_place}/{len(schools)}")


if __name__ == "__main__":
    main()
