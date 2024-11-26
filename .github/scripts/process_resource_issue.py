import os
import re
import json
from github import Github

# Retrieve the GitHub token and repository name from the environment
token = os.getenv('GITHUB_TOKEN')
if not token:
    print("Error: GITHUB_TOKEN is not set.")
    exit(1)

repo_name = os.getenv('GITHUB_REPOSITORY')
if not repo_name:
    print("Error: GITHUB_REPOSITORY is not set.")
    exit(1)

# Initialize GitHub API client
g = Github(token)
repo = g.get_repo(repo_name)

# Fetch the event payload from the GitHub-provided file
event_path = os.getenv('GITHUB_EVENT_PATH')
if not event_path:
    print("Error: GITHUB_EVENT_PATH is not set.")
    exit(1)

with open(event_path, 'r') as f:
    event = json.load(f)  # Use JSON parser instead of eval

# Extract issue details
issue_number = event.get('issue', {}).get('number')
if not issue_number:
    print("Error: No issue number found in event payload.")
    exit(1)

issue = repo.get_issue(issue_number)

# Now process the issue as required...
print(f"Processing issue #{issue.number}: {issue.title}")

# Extract details from the issue body
body = issue.body
title_match = re.search(r"## Resource Title\s*<!--.*-->\s*(.+)", body)
url_match = re.search(r"## URL\s*<!--.*-->\s*(.+)", body)
description_match = re.search(r"## Description\s*<!--.*-->\s*(.+)", body)
category_match = re.search(r"## Category\s*<!--.*-->\s*(.+)", body)

print(f"Issue Body:\n{body}")
print(f"Title Match: '{title_match.group(1) if title_match else 'Not Found'}'")
print(f"URL Match: '{url_match.group(1) if url_match else 'Not Found'}'")
print(f"Description Match: '{description_match.group(1) if description_match else 'Not Found'}'")
print(f"Category Match: '{category_match.group(1) if category_match else 'Not Found'}'")

if not (title_match and url_match and description_match and category_match):
    print("Error: Missing required fields in the issue.")
    exit(1)

title = title_match.group(1).strip()
url = url_match.group(1).strip()
description = description_match.group(1).strip()
category = category_match.group(1).strip().lower()

# Map category to directory
category_dirs = {
    "academic": "bookmarks/academic/academic-papers.md",
    "blog post": "bookmarks/blog-posts/blog-posts.md",
    "article": "bookmarks/articles/articles.md",
    "video": "bookmarks/videos/videos.md",
    "general": "bookmarks/general/general-links.md",
}

if category not in category_dirs:
    print(f"Error: Unknown category '{category}'.")
    exit(1)

file_path = category_dirs[category]

# Append the resource to the correct file
entry = f"- [{title}]({url}) - {description}\n"
with open(file_path, 'a') as f:
    f.write(entry)

print(f"Successfully added resource to {file_path}.")