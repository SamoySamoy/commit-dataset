import requests
import csv
import re
from crawl import crawl_commits, expand_dataset

if __name__ == "__main__":
    commits = crawl_commits("npm", "cli")
    # using test.csv for test crawled data before save in dataset
    with open (file="index.txt", mode="r") as f:
        cur = int(f.read())


    expand_dataset(commits, "temp.csv", cur) # id,sha,author_name,author_email,message,is_important,summa

