import requests
import logging
from datetime import datetime, timedelta

class GitHubHandler:
    GRAPHQL_QUERY = """
    query($username: String!, $since: DateTime!, $privacy: RepositoryPrivacy) {
      user(login: $username) {
        organizations(first: 100) {
          nodes {
            login
          }
        }
        pullRequests(first: 100, states: MERGED, orderBy: {field: CREATED_AT, direction: DESC}) {
          nodes {
            additions
            deletions
          }
        }
        contributionsCollection(from: $since) {
          totalCommitContributions
          totalPullRequestContributions
          totalIssueContributions
          totalRepositoryContributions
          restrictedContributionsCount
          pullRequestReviewContributions(first: 100) {
            totalCount
          }
        }
        repositoriesContributedTo(first: 100, privacy: $privacy) {
          nodes {
            nameWithOwner
            owner {
              login
            }
          }
          totalCount
        }
      }
    }
    """

    def __init__(self, token, api_url):
        self.api_url = api_url
        self.headers = {"Authorization": f"token {token}"} if token else {}
        if not token:
            logging.warning("No GitHub token provided. API rate limits may apply.")

    def get_developer_metrics(self, username, days_back=365, exclude_private=False, only_organizations=False):
        since = (datetime.now() - timedelta(days=days_back)).isoformat()
        contributions = self.fetch_contributions_graphql(username, since, exclude_private)

        if not contributions:
            return self._empty_metrics(username)

        orgs = {org["login"] for org in contributions["organizations"]["nodes"]}
        repos = contributions["repositoriesContributedTo"]["nodes"]

        if only_organizations:
            logging.info(f"Filtering contributions by organizations: {orgs}")
            repos = [repo for repo in repos if repo["owner"]["login"] in orgs]

        prs = contributions["pullRequests"]["nodes"]
        total_additions = sum(pr["additions"] for pr in prs)
        total_deletions = sum(pr["deletions"] for pr in prs)

        return {
            "username": username,
            "commits": contributions["contributionsCollection"]["totalCommitContributions"],
            "pull_requests": contributions["contributionsCollection"]["totalPullRequestContributions"],
            "issues": contributions["contributionsCollection"]["totalIssueContributions"],
            "contributions": contributions["contributionsCollection"]["totalRepositoryContributions"],
            "reviews": contributions["contributionsCollection"]["pullRequestReviewContributions"]["totalCount"],
            "repositories_contributed": len(repos),
            "lines_added": total_additions,
            "lines_removed": total_deletions
        }

    def fetch_contributions_graphql(self, username, since, exclude_private):
        privacy = "PUBLIC" if exclude_private else None
        variables = {"username": username, "since": since, "privacy": privacy}
        payload = {"query": self.GRAPHQL_QUERY, "variables": variables}

        try:
            response = requests.post(self.api_url, json=payload, headers=self.headers)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            logging.error(f"HTTP error fetching data for {username}: {e}")
            return None
        except ValueError:
            logging.error(f"Invalid JSON response for {username}")
            return None

        if "errors" in data:
            logging.warning(f"GraphQL errors for {username}: {data['errors']}")
            return None

        return data.get("data", {}).get("user")

    def _empty_metrics(self, username):
        logging.info(f"No data found for {username}. Returning zeroed metrics.")
        return {
            "username": username,
            "commits": 0,
            "pull_requests": 0,
            "issues": 0,
            "contributions": 0,
            "reviews": 0,
            "repositories_contributed": 0,
            "lines_added": 0,
            "lines_removed": 0
        }
