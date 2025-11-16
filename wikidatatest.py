# wikidata_creator.py
import csv
import requests
import json

# Your Wikidata authentication
USERNAME = "Morelrep@VIAF-reconciler"
PASSWORD = "h3944bqrd86e403hr37jcuv40t7acm5k"
TEST_WIKIDATA_API = "https://test.wikidata.org/w/api.php"
USER_AGENT = "VIAFReconciler/1.0 (https://example.org/viaf-bot/; email@example.org) python-requests/2.31.0"

def display_wikidata_warning():
    """Display Wikidata editing warning and check user experience"""
    print("\n" + "⚠️" * 50)
    print("⚠️  BEFORE CONTINUING:")
    print("⚠️" * 50)
    print("\nThis tool can make multiple edits to Wikidata very quickly.")
    print("If you're not familiar with Wikidata's rules, you may accidentally")
    print("create non-notable items or incorrect statements.")
    print("\n")
    print("If you are not shure, you can add the required entities manually")
    print("using the informationin the CSV available in the program folder (wikidata_candidates.csv).\n")
    print("\n")
    print("If you're new to Wikidata, please take a moment to read:")
    print('"Ten Simple Rules for Editing Wikidata" (doi:10.1371/journal.pcbi.1006942)\n')
    
    while True:
        response = input("Are you familiar with Wikidata's core editing guidelines? [Y(es)/n(o)]: ").strip().lower()
        if response in ['', 'y', 'yes']:
            return True
        elif response in ['n', 'no']:
            print("\n📚 Please review the guidelines before using this tool.")
            print("You can use the CSV file for manual Wikidata editing instead.")
            return False
        else:
            print("Please enter Y or n")

def create_author_item(api_url, session, edit_token, author_name):
    """Create a basic author item in Wikidata"""
    
    # Extract last name for description
    last_name = author_name.split()[-1] if author_name.split() else author_name
    
    # Prepare the item data - SIMPLIFIED without claims first
    item_data = {
        'labels': {
            'en': {'language': 'en', 'value': author_name}
        },
        'descriptions': {
            'en': {'language': 'en', 'value': f'author {last_name}'}
        }
    }
    
    # Create the item
    params = {
        'action': 'wbeditentity',
        'new': 'item',
        'data': json.dumps(item_data),
        'token': edit_token,
        'format': 'json'
    }
    
    response = session.post(api_url, data=params)
    return response.json()

def get_login_token(api_url, session):
    """Get login token from Wikidata API"""
    params = {
        'action': 'query',
        'meta': 'tokens',
        'type': 'login',
        'format': 'json'
    }
    response = session.get(api_url, params=params)
    data = response.json()
    return data['query']['tokens']['logintoken']

def login(api_url, session, username, password, login_token):
    """Login to Wikidata"""
    params = {
        'action': 'login',
        'lgname': username,
        'lgpassword': password,
        'lgtoken': login_token,
        'format': 'json'
    }
    response = session.post(api_url, data=params)
    return response.json()

def get_edit_token(api_url, session):
    """Get CSRF token for editing"""
    params = {
        'action': 'query',
        'meta': 'tokens',
        'format': 'json'
    }
    response = session.get(api_url, params=params)
    data = response.json()
    return data['query']['tokens']['csrftoken']

def load_wikidata_candidates(filename="wikidata_candidates.csv"):
    """Load the authors that need Wikidata creation"""
    candidates = []
    try:
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                candidates.append(row)
        print(f"📖 Loaded {len(candidates)} Wikidata candidates from {filename}")
        return candidates
    except FileNotFoundError:
        print(f"❌ No {filename} found. Run VIAF matcher first.")
        return []

def prompt_wikidata_creation(author_name, work_title):
    """Ask user if they want to proceed with Wikidata creation"""
    print(f"\n--- Wikidata Creation ---")
    print(f"Author: {author_name}")
    print(f"Work: {work_title}")
    
    while True:
        response = input("Create Wikidata item for this author? [y(yes)/s(skip)/q(quit)]: ").lower().strip()
        if response in ['y', 'yes']:
            return 'create'
        elif response in ['s', 'skip']:
            return 'skip'
        elif response in ['q', 'quit']:
            return 'quit'
        else:
            print("Please enter y, s, or q")

def main():
    """Process Wikidata candidates"""
    # Check user experience first
    if not display_wikidata_warning():
        print("\nExiting Wikidata creator.")
        return
    
    candidates = load_wikidata_candidates()
    
    if not candidates:
        return
    
    # Your Wikidata authentication code from earlier would go here
    session = requests.Session()
    session.headers.update({'User-Agent': USER_AGENT})
    
    print(f"\n=== Starting Wikidata Creation ===")
    
    for candidate in candidates:
        author_name = candidate['Author Name']
        work_title = candidate['Work Title']
        
        action = prompt_wikidata_creation(author_name, work_title)
        
        if action == 'create':
            print(f"   🚧 Creating Wikidata item for '{author_name}'...")
            
            try:
                # Authenticate using the functions we added
                login_token = get_login_token(TEST_WIKIDATA_API, session)
                login_result = login(TEST_WIKIDATA_API, session, USERNAME, PASSWORD, login_token)
                
                if login_result.get('login', {}).get('result') == 'Success':
                    edit_token = get_edit_token(TEST_WIKIDATA_API, session)
                    # Create the author item using the function we added
                    result = create_author_item(TEST_WIKIDATA_API, session, edit_token, author_name)
                    
                    if result.get('success') == 1:
                        item_id = result.get('entity', {}).get('id')
                        print(f"   ✅ Successfully created item: {item_id}")
                        print(f"   🔗 https://test.wikidata.org/wiki/{item_id}")
                    else:
                        print(f"   ❌ Failed to create item: {result}")
                else:
                    print(f"   ❌ Login failed")
                    
            except Exception as e:
                print(f"   ❌ Error creating item: {e}")
            
        elif action == 'skip':
            print(f"   ⏭️  Skipping '{author_name}'")
            continue
            
        elif action == 'quit':
            print("   👋 Exiting early")
            break

if __name__ == "__main__":
    main()