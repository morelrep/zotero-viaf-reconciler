#!/usr/bin/env python3
"""
Zotero-VIAF Reconciliation Tool
Basic prototype - Days 1-2 Development
"""

import requests
import time
from pyzotero import zotero
import json

# Configuration - UPDATE THESE!
ZOTERO_USER_ID = "14926246"  # Get from https://www.zotero.org/settings/keys
ZOTERO_API_KEY = "DrDt6mymNKhQMIDLNgasx6dG"  # Get from same page
LIBRARY_TYPE = "user"  # "user" or "group"

def get_viaf_from_wikidata(author_name):
    """Get VIAF ID via Wikidata (working approach)"""
    try:
        params = {
            'action': 'wbsearchentities',
            'search': author_name,
            'language': 'en', 
            'format': 'json'
        }
        
        response = requests.get('https://www.wikidata.org/w/api.php', params=params)
        data = response.json()
        
        if data.get('search'):
            entity_id = data['search'][0]['id']
            entity_data = requests.get(f"https://www.wikidata.org/wiki/Special:EntityData/{entity_id}.json").json()
            
            claims = entity_data['entities'][entity_id]['claims']
            if 'P214' in claims:  # P214 = VIAF ID
                return claims['P214'][0]['mainsnak']['datavalue']['value']
        
        return None
        
    except Exception as e:
        print(f"Error getting VIAF from Wikidata: {e}")
        return None

def get_zotero_client():
    """Initialize and return Zotero client"""
    return zotero.Zotero(ZOTERO_USER_ID, LIBRARY_TYPE, ZOTERO_API_KEY)

def read_zotero_items(zot, limit=5):
    """Read items from Zotero library"""
    try:
        items = zot.top(limit=limit)
        print(f"Retrieved {len(items)} items from Zotero")
        return items
    except Exception as e:
        print(f"Error reading Zotero items: {e}")
        return []

def extract_existing_viaf_ids(extra_field):
    """Parse existing VIAF IDs from Extra field"""
    if not extra_field:
        return []
    
    viaf_ids = []
    for part in extra_field.split(';'):
        part = part.strip()
        if part.startswith('VIAF:'):
            viaf_ids.append(part.replace('VIAF:', '').strip())
    return viaf_ids

def update_extra_field(current_extra, new_viaf_id, role="Author"):
    """Add new VIAF ID to Extra field"""
    new_entry = f"VIAF ({role}): {new_viaf_id}"
    
    if not current_extra:
        return new_entry
    else:
        return f"{current_extra}; {new_entry}"

def main():
    """Main execution function"""
    print("=== Zotero-VIAF Reconciliation Tool ===")
    print("Starting development prototype...")
    
    # Initialize Zotero client
    zot = get_zotero_client()
    
    # Read test items from Zotero
    items = read_zotero_items(zot, limit=3)  # Start with just 3 items
    
    for item in items:
        print(f"\n--- Processing Item: {item['data'].get('title', 'Untitled')} ---")
        
        # Check if item has creators
        if 'creators' not in item['data'] or not item['data']['creators']:
            print("No creators found, skipping...")
            continue
            
        # Get current Extra field
        current_extra = item['data'].get('extra', '')
        existing_viaf_ids = extract_existing_viaf_ids(current_extra)
        print(f"Existing VIAF IDs: {existing_viaf_ids}")
        
        # Process each creator
        for creator in item['data']['creators']:
            if 'name' in creator:
                author_name = creator['name']
                creator_type = creator.get('creatorType', 'author')
                
                print(f"Checking {creator_type}: {author_name}")
                
                # Query VIAF
                viaf_id = get_viaf_from_wikidata(author_name)  # Working Wikidata approach
                
                if viaf_id:
                    if viaf_id in existing_viaf_ids:
                        print(f"  ✓ VIAF ID {viaf_id} already exists")
                    else:
                        print(f"  ✓ Found VIAF ID: {viaf_id}")
                        # Update Extra field (commented for safety during testing)
                        # new_extra = update_extra_field(current_extra, viaf_id, creator_type.title())
                        # item['data']['extra'] = new_extra
                        # zot.update_item(item)
                else:
                    print(f"  ✗ No VIAF match found")
                
                # Rate limiting - be nice to VIAF servers
                time.sleep(1)
    
    print("\n=== Development prototype completed ===")
    print("Next steps:")
    print("1. Uncomment the update lines to enable writing to Zotero")
    print("2. Add user prompts for conflicts")
    print("3. Expand to handle multiple matches")

if __name__ == "__main__":
    main()