import re
import requests
import time
from pyzotero import zotero

# Zotero configuration
ZOTERO_USER_ID = "14926246"
ZOTERO_API_KEY = "DrDt6mymNKhQMIDLNgasx6dG"
LIBRARY_TYPE = "user"

def get_collection_id(zot, collection_name):
    """Find collection ID by name"""
    collections = zot.collections()
    for collection in collections:
        if collection['data']['name'].lower() == collection_name.lower():
            return collection['data']['key']
    return None

def get_viaf_from_wikidata(author_name):
    """Smart search with automatic fallback for name variations"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
        'Accept': 'application/json',
    }

    # Try original name first
    viaf_id = try_wikidata_search(author_name, headers)
    if viaf_id:
        return viaf_id
    
    print(f"      DEBUG: Original search failed, trying variations...")
    
    # Generate systematic name variations
    variations = generate_name_variations(author_name)
    
    for variation in variations:
        print(f"      DEBUG: Trying variation: '{variation}'")
        viaf_id = try_wikidata_search(variation, headers)
        if viaf_id:
            print(f"      DEBUG: ✅ Variation worked!")
            # Found via variation - prompt user to confirm
            original_entity = get_wikidata_entity(variation, headers)
            if original_entity:
                wikidata_label = original_entity['labels'].get('en', {}).get('value', 'Unknown')
                return prompt_close_match(author_name, wikidata_label, viaf_id)
            return viaf_id
    
    print(f"      DEBUG: ❌ All variations failed")
    return None

def try_wikidata_search(search_name, headers):
    """Try a single Wikidata search and return VIAF ID if found"""
    params = {
        'action': 'wbsearchentities',
        'search': search_name,
        'language': 'en',
        'format': 'json'
    }

    try:
        response = requests.get(
            "https://www.wikidata.org/w/api.php",
            headers=headers,
            params=params,
            timeout=10
        )
        
        if response.status_code != 200:
            return None
            
        data = response.json()
        
        if not data.get('search'):
            return None
            
        entity = data['search'][0]
        entity_id = entity['id']
        
        entity_response = requests.get(
            f"https://www.wikidata.org/wiki/Special:EntityData/{entity_id}.json",
            headers=headers,
            timeout=10
        )
        
        entity_data = entity_response.json()
        claims = entity_data['entities'][entity_id]['claims']
        
        if 'P214' in claims:
            return claims['P214'][0]['mainsnak']['datavalue']['value']
        else:
            return None
            
    except Exception as e:
        return None

def generate_name_variations(name):
    """Generate common name variations for fallback searching"""
    variations = []
    
    # Remove middle initials: "Fiódor M. Dostoievski" -> "Fiódor Dostoievski"
    if '.' in name:
        variations.append(re.sub(r'\s+[A-Z]\.\s*', ' ', name).strip())
    
    # Remove all punctuation and extra spaces
    variations.append(re.sub(r'[^\w\s]', ' ', name).strip())
    variations.append(re.sub(r'\s+', ' ', name).strip())
    
    # Try last name first if it appears to be "First Last" format
    parts = name.split()
    if len(parts) >= 2 and not ',' in name:
        variations.append(f"{parts[-1]}, {' '.join(parts[:-1])}")
    
    # Try ASCII-fied version (remove accents)
    ascii_name = name.replace('í', 'i').replace('ó', 'o').replace('á', 'a').replace('é', 'e').replace('ú', 'u')
    if ascii_name != name:
        variations.append(ascii_name)
    
    return variations

def get_wikidata_entity(search_name, headers):
    """Get entity data for a successful variation search"""
    params = {
        'action': 'wbsearchentities',
        'search': search_name,
        'language': 'en',
        'format': 'json'
    }

    try:
        response = requests.get("https://www.wikidata.org/w/api.php", headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get('search'):
                entity_id = data['search'][0]['id']
                entity_response = requests.get(f"https://www.wikidata.org/wiki/Special:EntityData/{entity_id}.json", headers=headers)
                return entity_response.json()['entities'][entity_id]
    except:
        pass
    return None

def prompt_close_match(zotero_name, wikidata_label, viaf_id):
    """Prompt user when match found via variation"""
    print(f"\n⚠️  POTENTIAL MATCH FOUND:")
    print(f"   Your Zotero: '{zotero_name}'")
    print(f"   Wikidata:    '{wikidata_label}'") 
    print(f"   VIAF ID:     {viaf_id}")
    
    while True:
        response = input("   Use this VIAF ID? [y(yes)/s(skip)]: ").lower().strip()
        if response in ['y', 'yes']:
            return viaf_id
        elif response in ['s', 'skip']:
            return 'skip'  # ← Changed from None to 'skipped'
        else:
            print("   Please enter y or skip")

def extract_last_name(creator):
    """Extract last name from creator object"""
    if 'lastName' in creator:
        return creator['lastName']
    elif 'name' in creator:
        # Try to extract last name from full name
        parts = creator['name'].split()
        return parts[-1] if parts else ''
    return ''

def main():
    """Process only a specific collection"""
    zot = zotero.Zotero(ZOTERO_USER_ID, LIBRARY_TYPE, ZOTERO_API_KEY)

    # NEW: Storage for results
    item_results = {}

    # LIST ALL COLLECTIONS FIRST (run this once to see your collections)
    print("=== Your Collections ===")
    collections = zot.collections()
    for collection in collections[:10]:  # Show first 10
        print(f"{collection['data']['name']}: {collection['data']['key']}")
    
    # SPECIFY YOUR TARGET COLLECTION
    collection_name = "VIAF test"  # ← CHANGE THIS
    collection_id = get_collection_id(zot, collection_name)
    
    if not collection_id:
        print(f"Collection '{collection_name}' not found!")
        return
    
    print(f"\n=== Processing collection: {collection_name} ===")
    
    # Get only top-level items, not attachments, from specific collection
    items = [item for item in zot.collection_items(collection_id, limit=50) 
         if item['data'].get('itemType') not in ['attachment', 'note']]
    
    for item in items:
        item_key = item['key']
        print(f"\nProcessing: {item['data'].get('title', 'Untitled')}")
        
        # NEW: Initialize storage for this item
        item_results[item_key] = {
            'item': item,
            'csv_rows': [['FULL NAME', 'NATIONALITY', 'VIAF']],  # Header
            'viaf_tags': []
        }

        creators = item['data'].get('creators', [])
        print(f"  Creators found: {len(creators)}")
        
        for creator in creators:
            if 'name' in creator:
                author_name = creator['name']
                print(f"    Author: {author_name}")
                
                viaf_id = get_viaf_from_wikidata(author_name)

                # DEBUG LINE:
                print(f"      DEBUG: viaf_id = {viaf_id} (type: {type(viaf_id)})")  
                
                # NEW: Store results
                if viaf_id == 'skip':
                    print(f"      ⏭️  Match skipped by user")
                    item_results[item_key]['csv_rows'].append([author_name, '', viaf_id])
                elif viaf_id:
                    print(f"      ✅ VIAF ID: {viaf_id}")
                    item_results[item_key]['csv_rows'].append([author_name, '', ''])
                    item_results[item_key]['viaf_tags'].append(f"VIAF{viaf_id}")
                else:
                    print(f"      ❌ No VIAF found")
                    item_results[item_key]['csv_rows'].append([author_name, '', ''])
                    
            elif 'firstName' in creator and 'lastName' in creator:
                author_name = f"{creator['firstName']} {creator['lastName']}"
                print(f"    Author: {author_name}")
                
                viaf_id = get_viaf_from_wikidata(author_name)
                
                # ADD THE SAME STORAGE LOGIC AS THE FIRST BLOCK
                if viaf_id == 'skip':
                    print(f"      ⏭️  Match skipped by user")
                    item_results[item_key]['csv_rows'].append([author_name, '', ''])
                elif viaf_id:
                    print(f"      ✅ VIAF ID: {viaf_id}")
                    item_results[item_key]['csv_rows'].append([author_name, '', viaf_id])
                    item_results[item_key]['viaf_tags'].append(f"VIAF{viaf_id}")
                else:
                    print(f"      ❌ No VIAF found")
                    item_results[item_key]['csv_rows'].append([author_name, '', ''])
            
            time.sleep(1)  # Rate limiting
    # DEBUG: Check what we collected
    print(f"\n=== DEBUG: Collected Data ===")
    for item_key, result in item_results.items():
        print(f"Item: {result['item']['data'].get('title')}")
        print(f"CSV Rows: {result['csv_rows']}")
        print(f"VIAF Tags: {result['viaf_tags']}")
        print("---")

    # NEW: Write all results to Zotero
    print(f"\n=== Writing results to Zotero ===")
    for item_key, result in item_results.items():
        try:
            # Convert CSV rows to string
            csv_content = '\n'.join([','.join(row) for row in result['csv_rows']])
            
            # Update item
            result['item']['data']['extra'] = csv_content
            if result['viaf_tags']:
                viaf_tag_objects = [{'tag': tag} for tag in result['viaf_tags']]
                result['item']['data']['tags'] = result['item']['data'].get('tags', []) + viaf_tag_objects            
            zot.update_item(result['item'])
            print(f"✅ Updated: {result['item']['data'].get('title', 'Untitled')}")
            
        except Exception as e:
            print(f"❌ Failed to update {result['item']['data'].get('title', 'Untitled')}: {e}")
if __name__ == "__main__":
    main()