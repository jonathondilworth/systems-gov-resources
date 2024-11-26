import os
import re
from github import Github

# Retrieve the GitHub token from the environment
token = os.getenv('GITHUB_TOKEN')
if not token:
    print("Error: GITHUB_TOKEN is not set.")
    exit(1)

# Retrieve the repository name from the environment
repo_name = os.getenv('GITHUB_REPOSITORY')
if not repo_name:
    print("Error: GITHUB_REPOSITORY is not set.")
    exit(1)

# Initialize GitHub API client
g = Github(token)
repo = g.get_repo(repo_name)

# Fetch the issue that triggered the workflow
event_path = os.getenv('GITHUB_EVENT_PATH')
if not event_path:
    print("Error: GITHUB_EVENT_PATH is not set.")
    exit(1)

with open(event_path, 'r') as f:
    event = eval(f.read())
issue = repo.get_issue(event['issue']['number'])

# Extract details from the issue body
body = issue.body
title_match = re.search(r"## Resource Title\s*<!--.*-->\s*(.+)", body)
url_match = re.search(r"## URL\s*<!--.*-->\s*(.+)", body)
description_match = re.search(r"## Description\s*<!--.*-->\s*(.+)", body)
category_match = re.search(r"## Category\s*<!--.*-->\s*(.+)", body)

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