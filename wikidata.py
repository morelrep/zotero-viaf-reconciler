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
            # Phase 2 implementation will go here
            # create_wikidata_author_item(session, author_name)
            
        elif action == 'skip':
            print(f"   ⏭️  Skipping '{author_name}'")
            continue
            
        elif action == 'quit':
            print("   👋 Exiting early")
            break

if __name__ == "__main__":
    main()