import requests
import csv
import re
from crawl import crawl_commits, expand_dataset

if __name__ == "__main__":
    commits = crawl_commits("facebook", "facebook-android-sdk")
    expand_dataset(commits, "test.csv") # id,sha,author_name,author_email,message,is_important,summa


