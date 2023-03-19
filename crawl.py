import requests
import csv
import re
from pattern import bot_message_patterns, bot_names_pattern, bot_emails_pattern, ex_pattern

def crawl_commits(repo_owner, repo_name):
    # Set up variables
    repo_owner = repo_owner
    repo_name = repo_name
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits"
    headers = {"Accept": "application/vnd.github.v3+json"}
    params = {"per_page": 30}  # Number of commits to fetch per page
    auth_token = "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"

    # Make API request to get commits
    response = requests.get(api_url, headers=headers, params=params, auth=(auth_token, ""))
    commits = response.json()
    all_commits = []

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

    return commits

def expand_dataset(commits, file):
    # find the current id (number of rows)
    with open(file, mode="r", newline="") as csv_file:
        reader = csv.reader(csv_file)
        cur_id = sum(1 for row in reader) - 1

    # add new data to dataset
    with open(file, mode="a", newline="") as csv_file:
        writer = csv.writer(csv_file)
        id = cur_id
        for commit in commits:
            id += 1
            sha = commit["sha"]
            author_name = commit["commit"]["author"]["name"]
            author_email = commit["commit"]["author"]["email"]
            message = commit["commit"]["message"]
            summa = "None"

            # Check if commit is from a bot
            is_important = 1
            for bot_name in bot_names_pattern:
                if bot_name.lower() in author_name.lower() or ex_pattern.search(author_name):
                    is_important = 0.7
                    break
            for bot_email in bot_emails_pattern:
                if bot_email in author_email or ex_pattern.search(author_email):
                    is_important = 0.7
                    break
            for pattern in bot_message_patterns:
                if pattern.search(message):
                    is_important = 0.7
                    break

            new_row = [id, sha, author_name, author_email, message, is_important, summa]
            writer.writerow([])
            writer.writerow(new_row)





