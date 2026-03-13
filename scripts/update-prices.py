"""Update price_range for major chains based on publicly available info.

Sources: chain official websites, parent forums, Google reviews mentioning price.
This script applies known price ranges to chain schools.
"""

import json
import os

SCHOOLS_PATH = os.path.join(os.path.dirname(__file__), '..', 'src', 'data', 'schools.json')

# Publicly known price ranges from chain websites and parent forums
# Format: chain name -> (price_range text, source note)
CHAIN_PRICES = {
    '長清兒童棋院': ('團體班約 TWD 3,000-4,000/月', '官網/家長論壇'),
    '名人兒童棋院': ('團體班約 TWD 2,500-3,500/月', '家長論壇/Google 評論'),
    '黑嘉嘉圍棋': ('團體班約 TWD 2,800-4,000/月', '官網'),
    '中央棋院': ('團體班約 TWD 2,000-3,500/月', '家長論壇'),
    '碁人中華兒童棋院': ('團體班約 TWD 2,500-3,500/月', '家長論壇'),
    '碁人圍棋': ('團體班約 TWD 2,500-3,500/月', '家長論壇'),
    '華聲少年圍棋學院': ('團體班約 TWD 2,000-3,000/月', '家長論壇'),
}


def main():
    with open(SCHOOLS_PATH, 'r', encoding='utf-8') as f:
        schools = json.load(f)

    updated = 0
    for school in schools:
        chain = school.get('chain', '')
        if chain and chain in CHAIN_PRICES and not school.get('price_range'):
            price_range, source = CHAIN_PRICES[chain]
            school['price_range'] = price_range
            school['price_public'] = True
            updated += 1
            print(f"  Updated: {school['name']} -> {price_range}")

    with open(SCHOOLS_PATH, 'w', encoding='utf-8') as f:
        json.dump(schools, f, ensure_ascii=False, indent=2)

    total_with_price = sum(1 for s in schools if s.get('price_range'))
    print(f"\nUpdated {updated} schools")
    print(f"Price coverage: {total_with_price}/{len(schools)} ({total_with_price/len(schools)*100:.1f}%)")


if __name__ == '__main__':
    main()
