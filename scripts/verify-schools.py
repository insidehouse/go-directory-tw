"""Verify school data freshness and accuracy.

Checks:
1. Website URLs — HEAD request to detect dead sites
2. Google Maps place_id — verify via Maps URL redirect
3. Flag potentially closed schools

Output: scripts/output/verification-report.txt + updates last_verified
"""

import json
import os
import sys
import time
from datetime import datetime
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

SCHOOLS_PATH = os.path.join(os.path.dirname(__file__), '..', 'src', 'data', 'schools.json')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')
TIMEOUT = 10


def check_url(url, method='HEAD'):
    """Check if URL is reachable. Returns (status_code, redirect_url | error_msg)."""
    try:
        req = Request(url, method=method)
        req.add_header('User-Agent', 'Mozilla/5.0 (compatible; GoDirectoryBot/1.0)')
        resp = urlopen(req, timeout=TIMEOUT)
        return resp.status, resp.url
    except HTTPError as e:
        return e.code, str(e.reason)
    except URLError as e:
        return 0, str(e.reason)
    except Exception as e:
        return 0, str(e)


def main():
    dry_run = '--dry-run' in sys.argv
    skip_web = '--skip-web' in sys.argv

    with open(SCHOOLS_PATH, 'r', encoding='utf-8') as f:
        schools = json.load(f)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    today = datetime.now().strftime('%Y-%m-%d')

    lines = []
    lines.append(f"=== School Verification Report ===")
    lines.append(f"Date: {today}")
    lines.append(f"Total schools: {len(schools)}")
    lines.append(f"Mode: {'dry-run' if dry_run else 'live'}, web checks: {'skip' if skip_web else 'enabled'}")
    lines.append("")

    website_issues = []
    maps_issues = []
    verified_count = 0

    for i, school in enumerate(schools):
        name = school['name']
        issues = []

        # Check website
        if not skip_web and school.get('website'):
            url = school['website']
            if not url.startswith('http'):
                url = f'https://{url}'
            status, detail = check_url(url)
            if status == 0 or status >= 400:
                issues.append(f"website {status}: {detail}")
                website_issues.append((name, school['city'], url, status, detail))
            time.sleep(0.3)

        # Check Google Maps URL
        if not skip_web and school.get('google_maps_url'):
            status, detail = check_url(school['google_maps_url'])
            if status == 0 or status >= 400:
                issues.append(f"maps {status}: {detail}")
                maps_issues.append((name, school['city'], status, detail))
            time.sleep(0.3)

        # Data completeness flags
        missing = []
        if not school.get('phone'):
            missing.append('phone')
        if not school.get('address'):
            missing.append('address')
        if not school.get('google_rating'):
            missing.append('rating')
        if not school.get('lat') or not school.get('lng'):
            missing.append('geo')
        if not school.get('place_id'):
            missing.append('place_id')

        if issues:
            lines.append(f"[ISSUE] {name} ({school['city']})")
            for issue in issues:
                lines.append(f"  - {issue}")
        elif missing:
            lines.append(f"[INCOMPLETE] {name} ({school['city']}) — missing: {', '.join(missing)}")
        else:
            verified_count += 1

        # Update last_verified for schools with no issues
        if not issues and not dry_run:
            school['last_verified'] = today

        progress = f"[{i+1}/{len(schools)}]"
        status_icon = "x" if issues else ("~" if missing else "ok")
        print(f"  {progress} {status_icon} {name}", flush=True)

    # Summary
    lines.append("")
    lines.append("--- Website Issues ---")
    if website_issues:
        for name, city, url, status, detail in website_issues:
            lines.append(f"  {name} ({city}): {url} -> {status} {detail}")
    else:
        lines.append("  None")

    lines.append("")
    lines.append("--- Google Maps Issues ---")
    if maps_issues:
        for name, city, status, detail in maps_issues:
            lines.append(f"  {name} ({city}): {status} {detail}")
    else:
        lines.append("  None")

    lines.append("")
    lines.append("--- Summary ---")
    lines.append(f"  Fully verified: {verified_count}/{len(schools)}")
    lines.append(f"  Website issues: {len(website_issues)}")
    lines.append(f"  Maps issues: {len(maps_issues)}")

    report = "\n".join(lines)

    output_path = os.path.join(OUTPUT_DIR, 'verification-report.txt')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\nReport saved to {output_path}")

    if not dry_run:
        with open(SCHOOLS_PATH, 'w', encoding='utf-8') as f:
            json.dump(schools, f, ensure_ascii=False, indent=2)
        print(f"Updated last_verified for {verified_count} schools")
    else:
        print("Dry run — no files modified")


if __name__ == '__main__':
    main()
