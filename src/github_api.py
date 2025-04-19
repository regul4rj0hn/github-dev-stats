import requests
import logging
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

GITHUB_API_URL = "https://api.github.com/graphql"
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}"
} if GITHUB_TOKEN else {}

def fetch_contributions_graphql(username, since, exclude_private, only_organizations):
    query = """
    query($username: String!, $since: DateTime!, $privacy: RepositoryPrivacy) {
      user(login: $username) {
        contributionsCollection(from: $since) {
          totalCommitContributions
          totalPullRequestContributions
          totalIssueContributions
          totalRepositoryContributions
          restrictedContributionsCount
        }
        repositoriesContributedTo(first: 100, privacy: $privacy) {
          totalCount
        }
      }
    }
    """

    privacy = "PUBLIC" if exclude_private else None

    variables = {
        "username": username,
        "since": since,
        "privacy": privacy
    }

    response = requests.post(GITHUB_API_URL, json={"query": query, "variables": variables}, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        if "errors" in data:
            logging.warning(f"GraphQL errors for {username}: {data['errors']}")
            return None
        return data["data"]["user"]
    else:
        try:
            error_details = response.json()
            logging.error(f"Failed to fetch contributions for {username}: {response.status_code} - {error_details.get('message', 'No message provided')}")
        except ValueError:
            logging.error(f"Failed to fetch contributions for {username}: {response.status_code} - Unable to parse error details.")
        return None

def get_developer_metrics(username, days_back=365, exclude_private=False, only_organizations=False):
    since = (datetime.now() - timedelta(days=days_back)).isoformat()
    contributions = fetch_contributions_graphql(username, since, exclude_private, only_organizations)
    if contributions:
        return {
            "username": username,
            "commits": contributions["contributionsCollection"]["totalCommitContributions"],
            "pull_requests": contributions["contributionsCollection"]["totalPullRequestContributions"],
            "issues": contributions["contributionsCollection"]["totalIssueContributions"],
            "contributions": contributions["contributionsCollection"]["totalRepositoryContributions"]
        }
    return {
        "username": username,
        "commits": 0,
        "pull_requests": 0,
        "issues": 0,
        "contributions": 0
    }