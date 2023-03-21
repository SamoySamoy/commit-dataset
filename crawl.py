import requests
import csv
import re
import spacy
from pattern import bot_message_patterns, bot_names_pattern, bot_emails_pattern, ex_pattern

nlp = spacy.load('en_core_web_sm')

def calculate_important_score(text):
    # Parse the text with Spacy
    doc = nlp(text)
    # Define the important parts of speech
    important_pos = ["NOUN", "VERB", "ADJ"]
    keywords = ["fix", "add", "security", "fixed", "sync", "remove", "update", "migrate", "feature", "feat", "change", "changes", "refactor"]
    # Calculate the importance score for the sentence
    score = 0
    length = len(doc)
    important_words = sum(1 for token in doc if token.pos_ in important_pos)
    keywords = sum(1 for token in doc if token.text.lower() in keywords)
    score = (important_words * 2) + keywords - length
    if length <= 3 and score <= 1:
        return False
    return score >= 0

def crawl_commits(repo_owner, repo_name): # need fixed to crawl all commits one time
    # Set up variables
    repo_owner = repo_owner
    repo_name = repo_name
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits"
    headers = {"Accept": "application/vnd.github.v3+json"}
    params = {"per_page": 100}  # Number of commits to fetch per page
    auth_token = "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"

    # Make API request to get commits
    response = requests.get(api_url, headers=headers, params=params, auth=(auth_token, ""))
    commits = response.json()

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
            type = "None"

            # Find important ratio, default by 1
            # If we check that commit is from bot, decrease 0.3
            # Using spacy to tokenize a commit message then check it's importance by
            # calculate key words
            is_important = 1
            is_bot = False
            for bot_name in bot_names_pattern:
                if bot_name.lower() in author_name.lower() or ex_pattern.search(author_name):
                    is_bot = True
                    break
            for bot_email in bot_emails_pattern:
                if bot_email in author_email or ex_pattern.search(author_email):
                    is_bot = True
                    break
            for pattern in bot_message_patterns:
                if pattern.search(message):
                    is_bot = True
                    break

            if is_bot:
                is_important -= 0.3

            if calculate_important_score(message) == False:
                if is_bot == False:
                    is_important -= 0.3
                else:
                    is_important -= 0.5
            if is_important == 1:
                print(message)
            new_row = [id, sha, author_name, author_email, message, round(is_important,1), summa, type]
            writer.writerow([])
            writer.writerow(new_row)







