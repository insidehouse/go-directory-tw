"""
Merge research data (176 records from Outscraper) with site data (48 records).

Outputs:
1. enrichment.json  — matched records with fields to update
2. candidates.json  — unmatched research records as new school candidates
3. report.txt       — summary statistics

Usage: python scripts/merge-research-data.py
"""

import json
import re
from pathlib import Path

RESEARCH_PATH = Path("d:/OneDrive/Claude/go-directory-research/data/schools.json")
SITE_PATH = Path("d:/OneDrive/Claude/go-directory-tw/src/data/schools.json")
OUTPUT_DIR = Path("d:/OneDrive/Claude/go-directory-tw/scripts/output")

NON_GO_KEYWORDS = ["象棋", "西洋棋", "將棋", "跳棋"]

CITY_SLUG_MAP = {
    "台北": "taipei",
    "新北": "newtaipei",
    "桃園": "taoyuan",
    "新竹": "hsinchu",
    "台中": "taichung",
    "台南": "tainan",
    "高雄": "kaohsiung",
    "嘉義": "chiayi",
    "花蓮": "hualien",
    "基隆": "keelung",
    "宜蘭": "yilan",
    "苗栗": "miaoli",
    "彰化": "changhua",
    "南投": "nantou",
    "雲林": "yunlin",
    "屏東": "pingtung",
    "台東": "taitung",
}


def normalize_addr(a: str) -> str:
    return (
        a.replace("臺", "台")
        .replace("（", "(")
        .replace("）", ")")
        .replace(" ", "")
        .replace("　", "")
        .replace("号", "號")
    )


def normalize_phone(p: str) -> str:
    p = p.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    p = re.sub(r"^\+886\s*", "0", p)
    return p


def is_non_go(record: dict) -> bool:
    name = record.get("name", "") + record.get("name_full", "")
    return any(kw in name for kw in NON_GO_KEYWORDS)


def extract_street_number(addr: str) -> str:
    """Extract street name + number for matching (e.g. '信義路三段202號')."""
    m = re.search(r"[^\d區鄉鎮市縣里村]+(路|街|大道|巷|弄)[^號]*\d+號", addr)
    return m.group(0) if m else ""


def match_records(site: list, research: list) -> tuple[list, list, list]:
    """Returns (matches, unmatched_research, unmatched_site)."""
    site_index = []
    for s in site:
        addr = normalize_addr(s.get("address", ""))
        site_index.append({
            "record": s,
            "addr": addr,
            "street_num": extract_street_number(addr),
            "phone": normalize_phone(s.get("phone", "")),
            "name": s["name"],
            "matched": False,
        })

    matches = []
    unmatched_research = []

    for r in research:
        if is_non_go(r):
            continue

        ra = normalize_addr(r.get("address", ""))
        ra_sn = extract_street_number(ra)
        rp = normalize_phone(r.get("phone", ""))

        best_match = None
        for si in site_index:
            if si["matched"]:
                continue

            # Street + number exact match (e.g. both have "信義路三段202號")
            if ra_sn and si["street_num"] and ra_sn == si["street_num"]:
                best_match = si
                break

            # Phone exact match
            if rp and si["phone"] and rp == si["phone"]:
                best_match = si
                break

            # Name containment match (require 4+ chars to avoid false positives)
            rn = r["name"]
            sn = si["name"]
            if len(rn) >= 4 and len(sn) >= 4 and (rn in sn or sn in rn):
                best_match = si
                break

        if best_match:
            best_match["matched"] = True
            matches.append({"site": best_match["record"], "research": r})
        else:
            unmatched_research.append(r)

    unmatched_site = [si["record"] for si in site_index if not si["matched"]]
    return matches, unmatched_research, unmatched_site


def build_enrichment(matches: list) -> list:
    """Build enrichment data from matched pairs."""
    enrichments = []
    for m in matches:
        s = m["site"]
        r = m["research"]

        updates = {}

        # Fill missing google_rating
        if not s.get("google_rating") and r.get("google_rating"):
            updates["google_rating"] = r["google_rating"]
            updates["google_review_count"] = r.get("google_reviews_count", 0)

        # Fill missing google_maps_url
        if not s.get("google_maps_url") and r.get("place_id"):
            updates["google_maps_url"] = (
                f"https://www.google.com/maps/place/?q=place_id:{r['place_id']}"
            )

        # New fields from research
        if r.get("lat"):
            updates["lat"] = r["lat"]
        if r.get("lng"):
            updates["lng"] = r["lng"]
        if r.get("place_id"):
            updates["place_id"] = r["place_id"]
        if r.get("facebook_url") and not s.get("facebook_url"):
            updates["facebook_url"] = r["facebook_url"]
        if r.get("line_id") and not s.get("line_id"):
            updates["line_id"] = r["line_id"]

        if updates:
            enrichments.append({
                "slug": s["slug"],
                "name": s["name"],
                "research_name": r["name"],
                "updates": updates,
            })

    return enrichments


def build_candidates(unmatched: list) -> list:
    """Convert unmatched research records to site-format candidates."""
    candidates = []
    for r in unmatched:
        if not r.get("city"):
            continue

        city = r["city"]
        city_slug = CITY_SLUG_MAP.get(city, city.lower())

        name = r["name"]
        # Clean up long Outscraper names
        if "｜" in name:
            name = name.split("｜")[0].strip()
        if "|" in name:
            name = name.split("|")[0].strip()

        slug = name.replace(" ", "-").replace("（", "(").replace("）", ")")

        age_groups = []
        if r.get("teaches_children"):
            age_groups.append("children")
        if r.get("teaches_adults"):
            age_groups.append("adults")
        if not age_groups:
            age_groups = ["children"]  # default assumption for go schools

        addr = r.get("address", "")
        # Remove postal code prefix
        addr = re.sub(r"^\d{3,5}", "", addr)

        candidates.append({
            "slug": slug,
            "name": name,
            "chain": "",
            "city": city,
            "city_slug": city_slug,
            "district": r.get("district", ""),
            "address": addr,
            "phone": r.get("phone", ""),
            "website": r.get("website", ""),
            "facebook_url": r.get("facebook_url", ""),
            "google_maps_url": (
                f"https://www.google.com/maps/place/?q=place_id:{r['place_id']}"
                if r.get("place_id")
                else ""
            ),
            "google_rating": r.get("google_rating"),
            "google_review_count": r.get("google_reviews_count", 0),
            "age_groups": age_groups,
            "price_public": False,
            "price_range": None,
            "is_chain": False,
            "school_type": r.get("school_type", "classroom"),
            "notes": r.get("notes", ""),
            "data_sources": [r.get("source", "outscraper")],
            "last_verified": r.get("scraped_at", ""),
            "lat": r.get("lat"),
            "lng": r.get("lng"),
            "place_id": r.get("place_id", ""),
            "has_trial": False,
            "line_id": r.get("line_id", ""),
            # metadata for review
            "_research_name_full": r.get("name_full", ""),
            "_google_reviews_count": r.get("google_reviews_count", 0),
            "_photos_count": r.get("photos_count", 0),
        })

    # Sort by rating (highest first)
    candidates.sort(
        key=lambda x: (x.get("google_rating") or 0, x.get("_google_reviews_count", 0)),
        reverse=True,
    )
    return candidates


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(RESEARCH_PATH, "r", encoding="utf-8") as f:
        research = json.load(f)
    with open(SITE_PATH, "r", encoding="utf-8") as f:
        site = json.load(f)

    matches, unmatched_research, unmatched_site = match_records(site, research)
    enrichments = build_enrichment(matches)
    candidates = build_candidates(unmatched_research)

    # Write outputs
    with open(OUTPUT_DIR / "enrichment.json", "w", encoding="utf-8") as f:
        json.dump(enrichments, f, ensure_ascii=False, indent=2)

    with open(OUTPUT_DIR / "candidates.json", "w", encoding="utf-8") as f:
        json.dump(candidates, f, ensure_ascii=False, indent=2)

    # Report
    report_lines = [
        "=== Merge Report ===",
        f"Research records: {len(research)}",
        f"Site records: {len(site)}",
        f"Non-go filtered: {sum(1 for r in research if is_non_go(r))}",
        f"Matched: {len(matches)}",
        f"Unmatched research (candidates): {len(unmatched_research)}",
        f"Unmatched site (no research match): {len(unmatched_site)}",
        "",
        f"Enrichments to apply: {len(enrichments)}",
        "",
        "--- Candidates by city ---",
    ]

    city_counts = {}
    for c in candidates:
        city = c["city"]
        city_counts[city] = city_counts.get(city, 0) + 1
    for city, count in sorted(city_counts.items(), key=lambda x: -x[1]):
        report_lines.append(f"  {city}: {count}")

    report_lines.extend([
        "",
        "--- Top 20 candidates (by rating) ---",
    ])
    for c in candidates[:20]:
        rating = c.get("google_rating") or "N/A"
        reviews = c.get("_google_reviews_count", 0)
        report_lines.append(
            f"  [{c['city']}] {c['name']} — rating:{rating} reviews:{reviews}"
        )

    report_lines.extend([
        "",
        "--- Unmatched site records (no research data found) ---",
    ])
    for s in unmatched_site:
        report_lines.append(f"  {s['name']} ({s['city']} {s['district']})")

    report = "\n".join(report_lines)
    with open(OUTPUT_DIR / "report.txt", "w", encoding="utf-8") as f:
        f.write(report)

    print(report)


if __name__ == "__main__":
    main()
