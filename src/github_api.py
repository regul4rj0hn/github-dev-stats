import requests
import logging
import os
from datetime import datetime, timedelta

GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}"
} if GITHUB_TOKEN else {}

def fetch_commits(username, repo, since):
    url = f"{GITHUB_API_URL}/repos/{username}/{repo}/commits?since={since}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        logging.info(f"Fetched commits for {username}/{repo} since {since}")
        return len(response.json())
    logging.warning(f"Failed to fetch commits for {username}/{repo}: {response.status_code}")
    return 0

def fetch_pull_requests(username, repo, since):
    url = f"{GITHUB_API_URL}/repos/{username}/{repo}/pulls?state=all&since={since}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        logging.info(f"Fetched pull requests for {username}/{repo} since {since}")
        return len(response.json())
    logging.warning(f"Failed to fetch pull requests for {username}/{repo}: {response.status_code}")
    return 0

def fetch_issues(username, repo, since):
    url = f"{GITHUB_API_URL}/repos/{username}/{repo}/issues?since={since}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        logging.info(f"Fetched issues for {username}/{repo} since {since}")
        return len(response.json())
    logging.warning(f"Failed to fetch issues for {username}/{repo}: {response.status_code}")
    return 0

def fetch_contributions(username, since):
    url = f"{GITHUB_API_URL}/users/{username}/repos"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        repos = response.json()
        total_commits = 0
        total_pull_requests = 0
        total_issues = 0

        for repo in repos:
            total_commits += fetch_commits(username, repo['name'], since)
            total_pull_requests += fetch_pull_requests(username, repo['name'], since)
            total_issues += fetch_issues(username, repo['name'], since)

        logging.info(f"Fetched contributions for {username} since {since}")
        return {
            "commits": total_commits,
            "pull_requests": total_pull_requests,
            "issues": total_issues,
            "contributions": total_commits + total_pull_requests + total_issues
        }
    logging.warning(f"Failed to fetch repositories for {username}: {response.status_code}")
    return {
        "commits": 0,
        "pull_requests": 0,
        "issues": 0,
        "contributions": 0
    }

def get_developer_metrics(username, days_back=365):
    since = (datetime.now() - timedelta(days=days_back)).isoformat()
    metrics = fetch_contributions(username, since)
    metrics["username"] = username
    return metrics