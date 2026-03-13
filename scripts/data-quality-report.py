"""Data quality report for schools.json.

Generates per-field fill rates, high-value missing data list,
and per-city breakdown. Output to scripts/output/quality-report.txt.
"""

import json
import os
from collections import defaultdict
from datetime import datetime

SCHOOLS_PATH = os.path.join(os.path.dirname(__file__), '..', 'src', 'data', 'schools.json')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')

FIELDS = [
    ('slug', 'Slug', 'required'),
    ('name', 'Name', 'required'),
    ('chain', 'Chain', 'optional'),
    ('city', 'City', 'required'),
    ('city_slug', 'City Slug', 'required'),
    ('district', 'District', 'important'),
    ('address', 'Address', 'required'),
    ('phone', 'Phone', 'important'),
    ('website', 'Website', 'important'),
    ('facebook_url', 'Facebook', 'optional'),
    ('google_maps_url', 'Google Maps URL', 'important'),
    ('google_rating', 'Google Rating', 'important'),
    ('google_review_count', 'Review Count', 'optional'),
    ('lat', 'Latitude', 'important'),
    ('lng', 'Longitude', 'important'),
    ('place_id', 'Place ID', 'important'),
    ('age_groups', 'Age Groups', 'required'),
    ('price_public', 'Price Public', 'optional'),
    ('price_range', 'Price Range', 'high_value'),
    ('has_trial', 'Has Trial', 'optional'),
    ('line_id', 'LINE ID', 'optional'),
    ('last_verified', 'Last Verified', 'required'),
]


def is_filled(value):
    if value is None or value == '' or value is False:
        return False
    if isinstance(value, list) and len(value) == 0:
        return False
    return True


def main():
    with open(SCHOOLS_PATH, 'r', encoding='utf-8') as f:
        schools = json.load(f)

    total = len(schools)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    lines = []
    lines.append(f"=== Data Quality Report ===")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"Total schools: {total}")
    lines.append("")

    # Field fill rates
    lines.append("--- Field Fill Rates ---")
    lines.append(f"{'Field':<20} {'Filled':>8} {'Rate':>6}  Priority")
    lines.append("-" * 55)

    field_stats = {}
    for key, label, priority in FIELDS:
        filled = sum(1 for s in schools if is_filled(s.get(key)))
        rate = filled / total * 100 if total > 0 else 0
        field_stats[key] = (filled, rate)
        marker = " !!!" if priority in ('required', 'important') and rate < 90 else ""
        lines.append(f"{label:<20} {filled:>5}/{total:<3} {rate:>5.1f}%  {priority}{marker}")

    # Per-city breakdown
    lines.append("")
    lines.append("--- Per-City Breakdown ---")
    cities = defaultdict(list)
    for s in schools:
        cities[s['city']].append(s)

    lines.append(f"{'City':<8} {'Count':>5} {'Rating':>7} {'Lat/Lng':>8} {'Phone':>6} {'Web':>5} {'Price':>6}")
    lines.append("-" * 55)

    for city in sorted(cities.keys(), key=lambda c: len(cities[c]), reverse=True):
        items = cities[city]
        n = len(items)
        rating_n = sum(1 for s in items if is_filled(s.get('google_rating')))
        latlng_n = sum(1 for s in items if is_filled(s.get('lat')) and is_filled(s.get('lng')))
        phone_n = sum(1 for s in items if is_filled(s.get('phone')))
        web_n = sum(1 for s in items if is_filled(s.get('website')))
        price_n = sum(1 for s in items if is_filled(s.get('price_range')))
        lines.append(
            f"{city:<8} {n:>5} "
            f"{rating_n:>3}/{n:<3} "
            f"{latlng_n:>4}/{n:<3} "
            f"{phone_n:>3}/{n:<2} "
            f"{web_n:>3}/{n:<2} "
            f"{price_n:>3}/{n:<2}"
        )

    # High-value missing data
    lines.append("")
    lines.append("--- High-Value Missing Data ---")
    lines.append("Schools missing google_rating, lat/lng, or phone:")
    lines.append("")

    for s in schools:
        missing = []
        if not is_filled(s.get('google_rating')):
            missing.append('rating')
        if not is_filled(s.get('lat')) or not is_filled(s.get('lng')):
            missing.append('lat/lng')
        if not is_filled(s.get('phone')):
            missing.append('phone')
        if not is_filled(s.get('place_id')):
            missing.append('place_id')
        if missing:
            lines.append(f"  {s['name']} ({s['city']}) — missing: {', '.join(missing)}")

    # Chain analysis
    lines.append("")
    lines.append("--- Chain Analysis ---")
    chains = defaultdict(list)
    for s in schools:
        if s.get('chain'):
            chains[s['chain']].append(s)

    for chain in sorted(chains.keys(), key=lambda c: len(chains[c]), reverse=True):
        items = chains[chain]
        cities_list = sorted(set(s['city'] for s in items))
        lines.append(f"  {chain}: {len(items)} schools in {', '.join(cities_list)}")

    # Summary
    lines.append("")
    lines.append("--- Summary ---")
    rating_rate = field_stats['google_rating'][1]
    latlng_rate = field_stats['lat'][1]
    price_rate = field_stats['price_range'][1]
    lines.append(f"  google_rating coverage: {rating_rate:.1f}% (target: >= 90%)")
    lines.append(f"  lat/lng coverage: {latlng_rate:.1f}% (target: >= 90%)")
    lines.append(f"  price_range coverage: {price_rate:.1f}% (target: >= 20%)")

    report = "\n".join(lines)
    print(report)

    output_path = os.path.join(OUTPUT_DIR, 'quality-report.txt')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\nSaved to {output_path}")


if __name__ == '__main__':
    main()
