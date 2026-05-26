"""
Tracks and reports coverage gaps across features.
Run after pytest --cov to correlate gaps with test results.
"""
import json
import subprocess
import sys

GAPS_FILE = "coverage_gaps.json"

def load_gaps():
    with open(GAPS_FILE) as f:
        return json.load(f)

def save_gaps(data):
    with open(GAPS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def list_gaps(status_filter=None):
    data = load_gaps()
    gaps = data["gaps"]
    if status_filter:
        gaps = [g for g in gaps if g["status"] == status_filter]
    
    print(f"\n{'='*50}")
    print(f"COVERAGE GAPS ({len(gaps)} found)")
    print(f"{'='*50}")
    for gap in gaps:
        print(f"\n[{gap['id']}] {gap['feature']} — {gap['area']}")
        print(f"  Status  : {gap['status']}")
        print(f"  Priority: {gap['priority']}")
        print(f"  Notes   : {gap['notes']}")
    print()

def close_gap(gap_id: str):
    data = load_gaps()
    for gap in data["gaps"]:
        if gap["id"] == gap_id:
            gap["status"] = "closed"
            print(f"Closed gap: {gap_id}")
    save_gaps(data)

def add_gap(feature: str, area: str, priority: str, notes: str):
    data = load_gaps()
    existing_ids = [g["id"] for g in data["gaps"]]
    next_num = len(existing_ids) + 1
    new_gap = {
        "id": f"GAP-{next_num:03d}",
        "feature": feature,
        "area": area,
        "status": "open",
        "priority": priority,
        "notes": notes
    }
    data["gaps"].append(new_gap)
    save_gaps(data)
    print(f"Added: {new_gap['id']}")

def run_coverage_report():
    """Run pytest with coverage and print summary."""
    print("Running tests with coverage...\n")
    result = subprocess.run(
        ["pytest", "tests/python/", "--cov=tests/python", "--cov-report=term-missing", "-v"],
        capture_output=False
    )
    return result.returncode

if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else "list"

    if command == "list":
        list_gaps()
    elif command == "open":
        list_gaps(status_filter="open")
    elif command == "close" and len(sys.argv) > 2:
        close_gap(sys.argv[2])
    elif command == "add":
        add_gap(
            feature=sys.argv[2],
            area=sys.argv[3],
            priority=sys.argv[4],
            notes=sys.argv[5]
        )
    elif command == "report":
        code = run_coverage_report()
        list_gaps(status_filter="open")
        sys.exit(code)
    else:
        print("Usage: python coverage_gap_tracker.py [list|open|close GAP-ID|add <feature> <area> <priority> <notes>|report]")