from pyzotero import zotero

# Your credentials
ZOTERO_USER_ID = "14926246"
ZOTERO_API_KEY = "DrDt6mymNKhQMIDLNgasx6dG"
LIBRARY_TYPE = "user"

def test_full_name_capture():
    """Test how creator names are stored in your Zotero"""
    zot = zotero.Zotero(ZOTERO_USER_ID, LIBRARY_TYPE, ZOTERO_API_KEY)
    
    # Get one test item
    items = zot.top(limit=1)
    if not items:
        print("❌ No items found")
        return
        
    test_item = items[0]
    print(f"Item: {test_item['data'].get('title', 'Untitled')}")
    print(f"Creators: {len(test_item['data'].get('creators', []))}")
    
    for i, creator in enumerate(test_item['data'].get('creators', [])):
        print(f"\nCreator {i}:")
        print(f"  All keys: {creator.keys()}")
        
        if 'name' in creator:
            print(f"  Format: 'name'")
            print(f"  Full name: '{creator['name']}'")
            
        elif 'firstName' in creator and 'lastName' in creator:
            print(f"  Format: 'firstName + lastName'") 
            print(f"  First: '{creator['firstName']}'")
            print(f"  Last: '{creator['lastName']}'")
            full_name = f"{creator['firstName']} {creator['lastName']}"
            print(f"  Combined: '{full_name}'")
            
        else:
            print(f"  Unknown format: {creator}")

if __name__ == "__main__":
    test_full_name_capture()