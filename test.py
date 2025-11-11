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
    """Get VIAF ID via Wikidata - CURRENT WORKING VERSION"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
        'Accept': 'application/json',
    }

    params = {
        'action': 'wbsearchentities',
        'search': author_name,
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

def main():
    """Process only a specific collection"""
    zot = zotero.Zotero(ZOTERO_USER_ID, LIBRARY_TYPE, ZOTERO_API_KEY)
    
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
    
    # Get items from the specific collection
    items = zot.collection_items(collection_id, limit=50)
    
    for item in items:
        print(f"\nProcessing: {item['data'].get('title', 'Untitled')}")
        
        creators = item['data'].get('creators', [])
        print(f"  Creators found: {len(creators)}")
        
        for creator in creators:
            if 'name' in creator:
                author_name = creator['name']
                print(f"    Author: {author_name}")
                
                viaf_id = get_viaf_from_wikidata(author_name)
                
                if viaf_id:
                    print(f"      ✅ VIAF ID: {viaf_id}")
                else:
                    print(f"      ❌ No VIAF found")
                    
            elif 'firstName' in creator and 'lastName' in creator:
                author_name = f"{creator['firstName']} {creator['lastName']}"
                print(f"    Author: {author_name}")
                
                viaf_id = get_viaf_from_wikidata(author_name)
                
                if viaf_id:
                    print(f"      ✅ VIAF ID: {viaf_id}")
                else:
                    print(f"      ❌ No VIAF found")
            
            time.sleep(1)  # Rate limiting

if __name__ == "__main__":
    main()