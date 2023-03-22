import requests
import csv
import re
from crawl import crawl_commits, expand_dataset

if __name__ == "__main__":
    commits = crawl_commits("theodorusclarence", "ts-nextjs-tailwind-starter")
    # using test.csv for test crawled data before save in dataset
    expand_dataset(commits, "test.csv") # id,sha,author_name,author_email,message,is_important,summa

