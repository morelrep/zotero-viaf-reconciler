# run_workflow.py
import subprocess
import sys

def main():
    print("=== Phase 1: VIAF Matching ===")
    result1 = subprocess.run([sys.executable, "viaf.py"])
    
    if result1.returncode == 0:
        print("\n=== Phase 2: Wikidata Creation ===")
        subprocess.run([sys.executable, "wikidata.py"])
    else:
        print("Phase 1 failed, skipping Phase 2")

if __name__ == "__main__":
    main()