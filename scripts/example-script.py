# Example Script: Update Index
# This script generates an index of all links in the `bookmarks/` directory.

import os

def generate_index(directory):
    print(f"Scanning directory: {directory}")
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                print(f"Found: {os.path.join(root, file)}")

generate_index("bookmarks")