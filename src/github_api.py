import requests
import logging
import os

GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}"
} if GITHUB_TOKEN else {}

def fetch_commits(username, repo):
    url = f"{GITHUB_API_URL}/repos/{username}/{repo}/commits"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        logging.info(f"Fetched commits for {username}/{repo}")
        return len(response.json())
    logging.warning(f"Failed to fetch commits for {username}/{repo}: {response.status_code}")
    return 0

def fetch_pull_requests(username, repo):
    url = f"{GITHUB_API_URL}/repos/{username}/{repo}/pulls"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        logging.info(f"Fetched pull requests for {username}/{repo}")
        return len(response.json())
    logging.warning(f"Failed to fetch pull requests for {username}/{repo}: {response.status_code}")
    return 0

def fetch_issues(username, repo):
    url = f"{GITHUB_API_URL}/repos/{username}/{repo}/issues"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        logging.info(f"Fetched issues for {username}/{repo}")
        return len(response.json())
    logging.warning(f"Failed to fetch issues for {username}/{repo}: {response.status_code}")
    return 0

def fetch_contributions(username):
    url = f"{GITHUB_API_URL}/users/{username}/repos"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        repos = response.json()
        total_commits = 0
        total_pull_requests = 0
        total_issues = 0

        for repo in repos:
            total_commits += fetch_commits(username, repo['name'])
            total_pull_requests += fetch_pull_requests(username, repo['name'])
            total_issues += fetch_issues(username, repo['name'])

        logging.info(f"Fetched contributions for {username}")
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

def get_developer_metrics(username):
    metrics = fetch_contributions(username)
    metrics["username"] = username
    return metrics