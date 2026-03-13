"""
Add selected new schools from candidates to schools.json.

Selection criteria:
- rating >= 4.0, reviews >= 10
- Confirmed go (圍棋) schools
- Diverse brands per city
- Clean names

Usage: python scripts/add-new-schools.py
"""

import json
import re
from pathlib import Path

SITE_PATH = Path("d:/OneDrive/Claude/go-directory-tw/src/data/schools.json")
CANDIDATES_PATH = Path("d:/OneDrive/Claude/go-directory-tw/scripts/output/candidates.json")

# Manually curated selection from candidates
# Format: (original_name_prefix, clean_name, chain, is_chain)
SELECTED = [
    # 新北 (3 → 15+) — biggest gap
    ("名人兒童圍棋板橋實踐分院", "名人兒童棋院（板橋實踐分院）", "名人兒童棋院", True),
    ("黑嘉嘉圍棋－新北汐止分校", "黑嘉嘉圍棋（新北汐止分校）", "黑嘉嘉圍棋", True),
    ("名人兒童圍棋新店中正分院", "名人兒童棋院（新店中正分院）", "名人兒童棋院", True),
    ("名人兒童圍棋土城青雲分院", "名人兒童棋院（土城青雲分院）", "名人兒童棋院", True),
    ("名人兒童圍棋永和得和分院", "名人兒童棋院（永和得和分院）", "名人兒童棋院", True),
    ("名人兒童圍棋三重重新分院", "名人兒童棋院（三重重新分院）", "名人兒童棋院", True),
    ("名人兒童圍棋中和景安分院", "名人兒童棋院（中和景安分院）", "名人兒童棋院", True),
    ("三重棋院-小小林圍棋文教", "三重棋院（小小林圍棋）", "", False),
    ("上善若水圍棋教室", "上善若水圍棋教室", "", False),
    ("只想下棋兒童棋院", "只想下棋兒童棋院", "", False),
    ("佑林棋院", "佑林棋院", "", False),

    # 台北 (16 → 22+)
    ("名人兒童圍棋台北長安分院", "名人兒童棋院（長安分院）", "名人兒童棋院", True),
    ("名人兒童圍棋台北忠孝分院", "名人兒童棋院（忠孝分院）", "名人兒童棋院", True),
    ("智多星圍棋 (仁愛分校)", "智多星圍棋（仁愛分校）", "智多星圍棋", True),
    ("棋品空間", "棋品空間", "", False),
    ("棋聖模範棋院", "棋聖模範棋院", "", False),
    ("中華民國圍棋協會", "中華民國圍棋協會", "", False),

    # 桃園 (7 → 14+)
    ("黑嘉嘉圍棋-桃園八德分校", "黑嘉嘉圍棋（桃園八德分校）", "黑嘉嘉圍棋", True),
    ("黑嘉嘉圍棋-桃園平鎮分校", "黑嘉嘉圍棋（桃園平鎮分校）", "黑嘉嘉圍棋", True),
    ("黑嘉嘉圍棋-桃園大有分校", "黑嘉嘉圍棋（桃園大有分校）", "黑嘉嘉圍棋", True),
    ("黑嘉嘉圍棋-桃園中山分校", "黑嘉嘉圍棋（桃園中山分校）", "黑嘉嘉圍棋", True),
    ("黑嘉嘉圍棋-桃園中正分校", "黑嘉嘉圍棋（桃園中正分校）", "黑嘉嘉圍棋", True),
    ("黑嘉嘉圍棋-桃園南崁分校", "黑嘉嘉圍棋（桃園南崁分校）", "黑嘉嘉圍棋", True),
    ("新銳圍棋 莊敬道場", "新銳圍棋莊敬道場", "", False),

    # 新竹 (4 → 9+)
    ("黑嘉嘉圍棋-新竹巨城分校", "黑嘉嘉圍棋（新竹巨城分校）", "黑嘉嘉圍棋", True),
    ("黑嘉嘉圍棋-新竹竹北分校", "黑嘉嘉圍棋（新竹竹北分校）", "黑嘉嘉圍棋", True),
    ("碁人圍棋竹北", "碁人圍棋（竹北分校）", "碁人圍棋", True),
    ("中華民國圍棋協會新竹推廣中心", "圍棋協會新竹推廣中心（新竹兒童棋院）", "", False),
    ("竹北兒童棋院", "竹北兒童棋院", "", False),

    # 台中 (5 → 10+)
    ("太平棋院", "太平棋院", "", False),
    ("洪門棋院", "洪門棋院", "", False),
    ("葉大明老師圍棋", "葉大明老師圍棋", "", False),
    ("黑嘉嘉圍棋 - 台中西區分校", "黑嘉嘉圍棋（台中西區分校）", "黑嘉嘉圍棋", True),
    ("卓奕佳貝圍棋教育中心", "卓奕佳貝圍棋教育中心", "", False),

    # 高雄 (7 → 11+)
    ("名人兒童圍棋鼓山大順分院", "名人兒童棋院（鼓山大順分院）", "名人兒童棋院", True),
    ("黑嘉嘉圍棋－高雄左營分校", "黑嘉嘉圍棋（高雄左營分校）", "黑嘉嘉圍棋", True),
    ("士洪圍棋教室", "士洪圍棋教室", "", False),
    ("棋樂圍棋", "棋樂圍棋", "", False),

    # 台南 (3 → 6+)
    ("立光圍棋碁院", "立光圍棋碁院", "", False),
    ("同心圓兒童棋院", "同心圓兒童棋院", "", False),
    ("碁世界圍棋", "碁世界圍棋", "", False),

    # 嘉義 (2 → 5)
    ("棋而思Cheers圍棋推廣中心 (東區本部)", "棋而思圍棋推廣中心（東區本部）", "棋而思圍棋", True),
    ("棋而思Cheers圍棋推廣中心（西區分部）", "棋而思圍棋推廣中心（西區分部）", "棋而思圍棋", True),
    ("心弈圍棋苑 嘉科分苑", "心弈圍棋苑（嘉科分苑）", "", False),
]


def find_candidate(candidates: list, name_prefix: str) -> dict | None:
    for c in candidates:
        if c["name"].startswith(name_prefix):
            return c
    return None


def make_slug(name: str) -> str:
    return name.replace(" ", "-")


def main():
    with open(SITE_PATH, "r", encoding="utf-8") as f:
        schools = json.load(f)
    with open(CANDIDATES_PATH, "r", encoding="utf-8") as f:
        candidates = json.load(f)

    existing_slugs = {s["slug"] for s in schools}
    added = 0
    not_found = []

    for orig_prefix, clean_name, chain, is_chain in SELECTED:
        candidate = find_candidate(candidates, orig_prefix)
        if not candidate:
            not_found.append(orig_prefix)
            continue

        slug = make_slug(clean_name)
        if slug in existing_slugs:
            print(f"SKIP (duplicate slug): {clean_name}")
            continue

        # Build new school record
        new_school = {
            "slug": slug,
            "name": clean_name,
            "chain": chain,
            "city": candidate["city"],
            "city_slug": candidate["city_slug"],
            "district": candidate["district"],
            "address": candidate["address"],
            "phone": candidate["phone"],
            "website": candidate["website"],
            "facebook_url": candidate["facebook_url"],
            "google_maps_url": candidate["google_maps_url"],
            "google_rating": candidate["google_rating"],
            "google_review_count": candidate["google_review_count"],
            "age_groups": candidate["age_groups"],
            "price_public": False,
            "price_range": None,
            "is_chain": is_chain,
            "school_type": candidate["school_type"],
            "notes": "",
            "data_sources": ["outscraper"],
            "last_verified": candidate["last_verified"],
            "lat": candidate["lat"],
            "lng": candidate["lng"],
            "place_id": candidate["place_id"],
            "has_trial": False,
            "line_id": candidate.get("line_id", ""),
        }

        schools.append(new_school)
        existing_slugs.add(slug)
        added += 1

    # Sort by city, then name
    city_order = ["台北", "新北", "桃園", "新竹", "台中", "嘉義", "台南", "高雄", "花蓮"]
    schools.sort(key=lambda s: (
        city_order.index(s["city"]) if s["city"] in city_order else 99,
        s["chain"] or s["name"],
        s["name"],
    ))

    with open(SITE_PATH, "w", encoding="utf-8") as f:
        json.dump(schools, f, ensure_ascii=False, indent=2)

    print(f"Added: {added} new schools")
    print(f"Total: {len(schools)} schools")

    if not_found:
        print(f"\nNot found in candidates ({len(not_found)}):")
        for n in not_found:
            print(f"  {n}")

    # City breakdown
    cities = {}
    for s in schools:
        c = s["city"]
        cities[c] = cities.get(c, 0) + 1
    print("\nCity breakdown:")
    for c in city_order:
        if c in cities:
            print(f"  {c}: {cities[c]}")


if __name__ == "__main__":
    main()
