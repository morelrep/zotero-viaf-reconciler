Perfect! Let's dive into the **3-hour development sprint**. Here's your step-by-step plan:

## **Hour 1: Foundation & VIAF API (60 minutes)**

### **Minutes 0-15: Basic Setup**
1. **Create `main.py`** with the code I provided
2. **Get your Zotero credentials**:
   - Go to https://www.zotero.org/settings/keys
   - Create a new private key with **all permissions**
   - Copy your **User ID** and **API Key**

3. **Update the config section**:
```python
ZOTERO_USER_ID = "1234567"  # Your actual User ID
ZOTERO_API_KEY = "abc123xyz"  # Your actual API Key
```

### **Minutes 16-30: First Test Run**
```bash
python main.py
```
**Expected output**: Should connect to Zotero and show 3 items from your library.

### **Minutes 31-45: Debug Any Issues**
- If Zotero connection fails: check credentials and library type (`user` vs `group`)
- If VIAF queries fail: test internet connection and try manual URL:
  ```bash
  curl "http://viaf.org/viaf/AutoSuggest?query=Borges"
  ```

### **Minutes 46-60: Enhance VIAF Function**
Add better error handling:
```python
def query_viaf(author_name):
    try:
        url = f"http://viaf.org/viaf/AutoSuggest?query={requests.utils.quote(author_name)}"
        print(f"Querying VIAF: {url}")  # Debug line
        response = requests.get(url, timeout=10)
        # ... rest of function
```

## **Hour 2: Zotero Integration (60 minutes)**

### **Minutes 61-75: Test Data Flow**
1. Run script again and verify it processes creators
2. Check that VIAF IDs are being found
3. **Don't uncomment the write operations yet**

### **Minutes 76-90: Add Dry-Run Mode**
Modify the main function to show what WOULD be written:
```python
# Replace the update section with:
print(f"WOULD UPDATE: Add 'VIAF ({creator_type.title()}): {viaf_id}'")
print(f"Current Extra: '{current_extra}'")
print(f"New Extra would be: '{update_extra_field(current_extra, viaf_id, creator_type.title())}'")
```

### **Minutes 91-105: Test with Real Data**
- Run on 5-10 items from your actual library
- Verify the logic handles edge cases:
  - Items with no creators
  - Items with existing VIAF IDs in Extra field
  - Multiple creators per item

### **Minutes 106-120: Enable Writing (Carefully!)**
1. **Backup your Zotero library** (Export as Zotero RDF)
2. Uncomment the update lines for **ONE test item**:
```python
# Temporarily add this condition:
if item['data'].get('title', '').lower() == 'your test item title':
    new_extra = update_extra_field(current_extra, viaf_id, creator_type.title())
    item['data']['extra'] = new_extra
    zot.update_item(item)
    print("✓ ACTUALLY UPDATED Zotero")
```

## **Hour 3: Multi-Creator Support (60 minutes)**

### **Minutes 121-135: Test Role Detection**
Verify the script correctly identifies:
- Authors vs translators vs editors
- Handles mixed creator types in one item

### **Minutes 136-155: Role-Specific Formatting**
Test the `VIAF (Author): 123456` format works and doesn't create duplicates when run multiple times.

### **Minutes 156-180: Final Integration**
1. Remove the single-item restriction and test on 3-5 items
2. Verify all updates persist correctly in Zotero
3. Create a simple **run log** to track processed items

## **Quick Status Check Commands**
```bash
# Test VIAF independently
python -c "import requests; print(requests.get('http://viaf.org/viaf/AutoSuggest?query=Borges').json())"

# Test Zotero connection  
python -c "from pyzotero import zotero; zot = zotero.Zotero('YOUR_ID', 'user', 'YOUR_KEY'); print(zot.top(limit=1))"
```

## **Troubleshooting Priority**
1. **Zotero connection issues** → Check credentials and library type
2. **VIAF timeouts** → Add longer timeout and retry logic
3. **Encoding problems** → Use `requests.utils.quote()` for special characters

**Ready to start?** Begin with Minutes 0-15 and let me know your progress or any errors you encounter!