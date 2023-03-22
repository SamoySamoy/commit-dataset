
from crawl import crawl_commits, expand_dataset

if __name__ == "__main__":
    commits = crawl_commits("apache", "flink")
    # using test.csv for test crawled data before save in dataset
    # id,sha,author_name,author_email,message,is_important,summa
    expand_dataset(commits, "test.csv")

