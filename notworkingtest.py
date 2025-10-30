import requests
import time


def debug_wikidata_search(author_name):
    """Debug Wikidata search step by step"""
    print(f"\n🔍 Searching for: '{author_name}'")
    
    # Step 1: Search for the author
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
    
    response = requests.get('https://www.wikidata.org/w/api.php', params=params)
    print(f"   Search API Status: {response.status_code}")
    
    data = response.json()
    print(f"   Search results: {len(data.get('search', []))}")
    
    if not data.get('search'):
        print(f"   ❌ No search results for '{author_name}'")
        return None
    
    # Show what we found
    entity = data['search'][0]
    print(f"   ✅ Found: '{entity['label']}' (ID: {entity['id']})")
    print(f"   Description: {entity.get('description', 'No description')}")
    
    # Step 2: Get detailed entity data
    entity_id = entity['id']
    entity_response = requests.get(f"https://www.wikidata.org/wiki/Special:EntityData/{entity_id}.json")
    entity_data = entity_response.json()
    
    claims = entity_data['entities'][entity_id]['claims']
    print(f"   Available properties: {list(claims.keys())[:5]}...")  # Show first 5 properties
    
    if 'P214' in claims:
        viaf_id = claims['P214'][0]['mainsnak']['datavalue']['value']
        print(f"   ✅ VIAF ID found: {viaf_id}")
        return viaf_id
    else:
        print(f"   ❌ No VIAF ID (P214) found for this entity")
        return None

# Test with different author formats
test_authors = [
    "Jorge Luis Borges",
    "Borges, Jorge Luis", 
    "Virginia Woolf",
    "Woolf, Virginia"
]

for author in test_authors:
    result = debug_wikidata_search(author)
    time.sleep(1)  # Rate limiting