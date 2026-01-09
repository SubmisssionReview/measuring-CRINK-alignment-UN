#!/usr/bin/env python3
"""Switch notebook database to UNGA."""

import json
from pathlib import Path

notebook_path = Path(__file__).parent / "notebooks" / "02_alignment_metrics.ipynb"

with open(notebook_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

changes_made = 0
for cell in nb["cells"]:
    if cell["cell_type"] == "code":
        new_source = []
        for line in cell["source"]:
            # Change commented UNGA to active
            if line.strip() == "#database = 'UNGA'       # <<< CHANGE THIS LINE TO SWITCH DATASETS":
                new_source.append("database = 'UNGA'       # <<< CHANGE THIS LINE TO SWITCH DATASETS\n")
                changes_made += 1
            # Change active First Committee to commented
            elif line.strip() == "database = 'First Committee'":
                new_source.append("#database = 'First Committee'\n")
                changes_made += 1
            else:
                new_source.append(line)
        cell["source"] = new_source

with open(notebook_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)

print(f"Changes made: {changes_made}")
print("Database switched to UNGA")
