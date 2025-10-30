import requests
import time
from pyzotero import zotero

# Zotero configuration
ZOTERO_USER_ID = "14926246"
ZOTERO_API_KEY = "DrDt6mymNKhQMIDLNgasx6dG"
LIBRARY_TYPE = "user"

def get_viaf_from_wikidata(author_name):
    """Get VIAF ID via Wikidata"""
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
    """Main Zotero reconciliation function"""
    zot = zotero.Zotero(ZOTERO_USER_ID, LIBRARY_TYPE, ZOTERO_API_KEY)
    items = zot.top(limit=5)

    for item in items:
        print(f"\nProcessing: {item['data'].get('title', 'Untitled')}")
        
        # DEBUG: Show what's actually in the creators field
        creators = item['data'].get('creators', [])
        print(f"  Creators found: {len(creators)}")
        
        for i, creator in enumerate(creators):
            print(f"  Creator {i}: {creator}")
            
            # Zotero creators can have 'name' OR 'firstName' + 'lastName'
            if 'name' in creator:
                author_name = creator['name']
                print(f"    Processing as 'name': {author_name}")
                
                viaf_id = get_viaf_from_wikidata(author_name)
                
                if viaf_id:
                    print(f"      ✅ VIAF ID: {viaf_id}")
                else:
                    print(f"      ❌ No VIAF found")
                    
            elif 'firstName' in creator and 'lastName' in creator:
                author_name = f"{creator['firstName']} {creator['lastName']}"
                print(f"    Processing as 'firstName+lastName': {author_name}")
                
                viaf_id = get_viaf_from_wikidata(author_name)
                
                if viaf_id:
                    print(f"      ✅ VIAF ID: {viaf_id}")
                else:
                    print(f"      ❌ No VIAF found")
            
            time.sleep(1)

if __name__ == "__main__":
    main()