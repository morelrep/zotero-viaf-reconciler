import requests
import json

# Wikidata test instance credentials
USERNAME = "Morelrep@VIAF-reconciler"
PASSWORD = "h3944bqrd86e403hr37jcuv40t7acm5k"

# Only using test instance for sandbox development
TEST_WIKIDATA_API = "https://test.wikidata.org/w/api.php"

# Define a descriptive User-Agent as required by Wikimedia policy
USER_AGENT = "VIAFReconciler/1.0 (https://example.org/viaf-bot/; email@example.org) python-requests/2.31.0"

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

def create_sandbox_item(api_url, session, edit_token, label, description):
    """Create a simple test item in Wikidata sandbox"""
    # Create a new item
    params = {
        'action': 'wbeditentity',
        'new': 'item',
        'data': json.dumps({
            'labels': {
                'en': {'language': 'en', 'value': label}
            },
            'descriptions': {
                'en': {'language': 'en', 'value': description}
            }
        }),
        'token': edit_token,
        'format': 'json'
    }
    
    response = session.post(api_url, data=params)
    return response.json()

def main():
    """Test Wikidata sandbox editing"""
    # Use session to maintain cookies with proper User-Agent
    session = requests.Session()
    session.headers.update({'User-Agent': USER_AGENT})
    
    try:
        # Step 1: Login token
        print("1. Getting login token...")
        login_token = get_login_token(TEST_WIKIDATA_API, session)
        print(f"   Login token: {login_token[:20]}...")
        
        # Step 2: Login
        print("2. Logging in...")
        login_result = login(TEST_WIKIDATA_API, session, USERNAME, PASSWORD, login_token)
        print(f"   Login result: {login_result.get('login', {}).get('result', 'Unknown')}")
        
        if login_result.get('login', {}).get('result') != 'Success':
            print(f"   ❌ Login failed: {login_result}")
            return
        
        # Step 3: Get edit token
        print("3. Getting edit token...")
        edit_token = get_edit_token(TEST_WIKIDATA_API, session)
        print(f"   Edit token: {edit_token[:20]}...")
        
        # Step 4: Create a test item
        print("4. Creating test item...")
        result = create_sandbox_item(
            TEST_WIKIDATA_API, 
            session, 
            edit_token,
            label="Test Item from Python Script",
            description="This is a test item created via API"
        )
        
        print("5. Result:", result)
        
        if 'success' in result and result['success'] == 1:
            item_id = result.get('entity', {}).get('id')
            print(f"✅ Successfully created item: {item_id}")
        else:
            print("❌ Failed to create item")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()