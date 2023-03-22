import requests
import csv
import spacy
from pattern import bot_message_patterns, bot_names_pattern, bot_emails_pattern, ex_pattern

nlp = spacy.load('en_core_web_lg')
github_token = "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"
headers = {
    'Authorization': f'token {github_token}',
    'Accept': 'application/vnd.github.v3+json'
}


def crawl_commits(repo_owner, repo_name):
    # Set up variables
    global headers
    page = 1
    all_commits = []
    # Make API request to get commits
    while True:
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits?per_page=100&page={page}"
        response = requests.get(url, headers=headers)
        commits = response.json()
        commits_per_page = list(map(lambda x: [x["sha"], x["commit"]["author"]["name"], x["commit"]["author"]["email"],
                                               x["commit"]["message"]], commits))
        all_commits += commits_per_page
        if len(commits_per_page) < 100:
            break
        page += 1
    return all_commits


def calculate_important_score(text):
    # Parse the text with Spacy
    doc = nlp(text)
    # Define the important parts of speech
    important_pos = ["NOUN", "VERB", "ADJ"]
    keywords = ["fix", "add", "security", "fixed", "sync", "remove", "update", "migrate", "feature", "feat", "change",
                "changes", "refactor"]
    # Calculate the importance score for the sentence
    length = len(doc)
    important_words = sum(1 for token in doc if token.pos_ in important_pos)
    keywords = sum(1 for token in doc if token.text.lower() in keywords)
    score = (important_words * 2) + keywords - length
    if length <= 3 and score <= 1:
        return False
    return score >= 0


def classify(text):
    # define pattern for each type
    added = ["added", "feat", "add", "feated", "feature", "feat:", "new"]
    fixed = ["fixed", "fix", "fix:", "bug", "improve", "optimize", "broken"]
    changed = ["changed", "change", "refactor", "update", "breaking", "upgrade"]
    removed = ["remove", "delete", "remove:", "removed", "unused", "duplicate"]
    security = ["security", "authentication", "authenticate", "password"]
    # join them for checking
    types = [security, removed, fixed, added, changed]

    doc = nlp(text)
    for token in doc:
        for _type in types:
            if str(token).lower() in _type:
                return _type[0]

    # suppose that we haven't figured out type of commit, consider it is changed or added
    if doc[0].pos_ in ["NOUN", "VERB"]:
        return "added"
    else:
        return "changed"


def expand_dataset(commits, file):
    count = 0
    # find the current id (number of rows)
    with open(file, mode="r", newline="") as csv_file:
        reader = csv.reader(csv_file)
        for count, line in enumerate(reader):
            pass
    # add new data to dataset
    with open(file, mode="a", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        index = count
        for commit in commits:
            index += 1
            sha = commit[0]
            author_name = commit[1]
            author_email = commit[2]
            message = commit[3]
            summa = "None"
            _type = classify(message)
            # Find important ratio, default by 1. If we check that commit is from bot, decrease important ratio 0.3
            # Using spacy to tokenize a commit message then check if it is important by calculating keywords

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

            if calculate_important_score(message) is False:
                is_important = is_important - 0.3 if not is_bot else is_important - 0.5
            if type == "added":

                print(message)
            new_row = [index, sha, author_name, author_email, message, round(is_important, 1), summa, _type]
            writer.writerow([])
            writer.writerow(new_row)
