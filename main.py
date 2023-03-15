import requests
import csv
import re
# Set up variables
repo_owner = "sous-chefs"
repo_name = "aws"
api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits"
headers = {"Accept": "application/vnd.github.v3+json"}
params = {"per_page": 100}  # Number of commits to fetch per page
auth_token = "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"

# Define bot-related keywords
bot_names = ["bot", "build", "deploy", "jenkins", "travis", "circleci", "github", "gitlab"]
bot_emails = ["noreply@github.com", "noreply@github.com.invalid"]
bot_patterns = [re.compile(r"\[skip ci\]", re.IGNORECASE),
                re.compile(r"\[ci skip\]", re.IGNORECASE),
                re.compile(r"no\s+tests?", re.IGNORECASE),
                re.compile(r"auto-generated", re.IGNORECASE),
                re.compile(r"automated\s+build", re.IGNORECASE),
                re.compile(r"continuous\s+integration", re.IGNORECASE),
                re.compile(r"test\s+automation", re.IGNORECASE),
                re.compile(r"ci/cd", re.IGNORECASE),
                re.compile(r"pipeline", re.IGNORECASE),
                re.compile(r"dependenc", re.IGNORECASE),
                re.compile(r"jenkinsfile", re.IGNORECASE),
                re.compile(r"travis\.yml", re.IGNORECASE),
                re.compile(r"circle\.yml", re.IGNORECASE),
                re.compile(r"bump", re.IGNORECASE),
                re.compile(r"gitlab-ci\.yml", re.IGNORECASE)]
ex_pattern = re.compile(r"\b.*bot.*\b", re.IGNORECASE)

# Make API request to get commits
response = requests.get(api_url, headers=headers, params=params, auth=(auth_token, ""))
commits = response.json()
all_commits = []
count = 0
# # Fetch all pages of commits
# while response.status_code == 200:
#     all_commits.extend(commits)
#     link_header = response.headers.get("Link")
#     if link_header is None:
#         break
#     links = link_header.split(",")
#     for link in links:
#         if "rel=\"next\"" in link:
#             next_url = link.split(";")[0].strip("<>")
#             response = requests.get(next_url, headers=headers, params=params, auth=(auth_token, ""))
#             commits = response.json()
#             break

# Extract commit details and save them in CSV file
with open("dataset.csv", mode="w", newline="") as csv_file:
    fieldnames = ["id", "sha", "author_name", "author_email", "message", "is_bot"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    id = 0
    for commit in commits:
        id += 1
        sha = commit["sha"]
        author_name = commit["commit"]["author"]["name"]
        author_email = commit["commit"]["author"]["email"]
        message = commit["commit"]["message"]

        # Check if commit is from a bot
        is_bot = False
        for bot_name in bot_names:
            if bot_name.lower() in author_name.lower() or ex_pattern.search(author_name):
                is_bot = True
                break
        for bot_email in bot_emails:
            if bot_email in author_email or ex_pattern.search(author_email):
                is_bot = True
                break
        for pattern in bot_patterns:
            if pattern.search(message):
                is_bot = True
                break
        writer.writerow({"id": id, "sha": sha, "author_name": author_name, "author_email": author_email, "message": message, "is_bot": is_bot})

