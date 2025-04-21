import requests
import logging
from datetime import datetime, timedelta

class GitHubHandler:
    def __init__(self, token, api_url):
        self.token = token
        self.api_url = api_url
        self.headers = {"Authorization": f"token {self.token}"} if self.token else {}

    def get_developer_metrics(self, username, days_back=365, exclude_private=False, only_organizations=False):
        since = (datetime.now() - timedelta(days=days_back)).isoformat()
        contributions = self.fetch_contributions_graphql(username, since, exclude_private, only_organizations)
        if contributions:
            organizations = {org["login"] for org in contributions["organizations"]["nodes"]}
            repositories = contributions["repositoriesContributedTo"]["nodes"]

            if only_organizations:
                logging.info(f"Contributions from {organizations} organization(s).")
                repositories = [
                    repo for repo in repositories if repo["owner"]["login"] in organizations
                ]

            pull_requests = contributions["pullRequests"]["nodes"]
            total_additions = sum(pr["additions"] for pr in pull_requests)
            total_deletions = sum(pr["deletions"] for pr in pull_requests)

            return {
                "username": username,
                "commits": contributions["contributionsCollection"]["totalCommitContributions"],
                "pull_requests": contributions["contributionsCollection"]["totalPullRequestContributions"],
                "issues": contributions["contributionsCollection"]["totalIssueContributions"],
                "contributions": contributions["contributionsCollection"]["totalRepositoryContributions"],
                "reviews": contributions["contributionsCollection"]["pullRequestReviewContributions"]["totalCount"],
                "repositories_contributed": len(repositories),
                "lines_added": total_additions,
                "lines_removed": total_deletions
            }
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

    def fetch_contributions_graphql(self, username, since, exclude_private, only_organizations):
        query = """
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

        privacy = "PUBLIC" if exclude_private else None

        variables = {
            "username": username,
            "since": since,
            "privacy": privacy
        }

        response = requests.post(self.api_url, json={"query": query, "variables": variables}, headers=self.headers)
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
