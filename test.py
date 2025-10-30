import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
    'Accept': 'application/json',
}

params = {
    'action': 'wbsearchentities',
    'search': 'Jorge Luis Borges',
    'language': 'en',  # Required parameter
    'format': 'json'
}

response = requests.get(
    "https://www.wikidata.org/w/api.php",
    headers=headers,
    params=params
)

print(f"Status: {response.status_code}")
data = response.json()

if 'search' in data and data['search']:
    entity = data['search'][0]
    print(f"✅ Found: {entity['label']} (ID: {entity['id']})")
    
    # Now get VIAF ID from this entity
    entity_id = entity['id']
    entity_response = requests.get(
        f"https://www.wikidata.org/wiki/Special:EntityData/{entity_id}.json",
        headers=headers
    )
    entity_data = entity_response.json()
    
    # Check for VIAF ID (property P214)
    claims = entity_data['entities'][entity_id]['claims']
    if 'P214' in claims:
        viaf_id = claims['P214'][0]['mainsnak']['datavalue']['value']
        print(f"✅ VIAF ID: {viaf_id}")
    else:
        print("❌ No VIAF ID found in Wikidata")
else:
    print("❌ No results found")