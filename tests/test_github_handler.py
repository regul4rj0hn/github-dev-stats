import unittest
from unittest.mock import patch
from github_handler import GitHubHandler

class TestGitHubHandler(unittest.TestCase):
    def setUp(self):
        self.token = "fake_token"
        self.api_url = "https://api.github.com/graphql"
        self.github_handler = GitHubHandler(self.token, self.api_url)

    @patch("github_handler.requests.post")
    def test_get_developer_metrics(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "data": {
                "user": {
                    "contributionsCollection": {
                        "totalCommitContributions": 10,
                        "totalPullRequestContributions": 5,
                        "totalIssueContributions": 2,
                        "totalRepositoryContributions": 3,
                        "pullRequestReviewContributions": {"totalCount": 1}
                    },
                    "repositoriesContributedTo": {"nodes": [], "totalCount": 2},
                    "pullRequests": {"nodes": [{"additions": 100, "deletions": 50}]},
                    "organizations": {"nodes": [{"login": "org1"}, {"login": "org2"}]}
                }
            }
        }
        metrics = self.github_handler.get_developer_metrics("user1")
        self.assertEqual(metrics['commits'], 10)
        self.assertEqual(metrics['lines_added'], 100)
        self.assertEqual(metrics['lines_removed'], 50)

    @patch("github_handler.requests.post")
    def test_get_developer_metrics_handles_empty_response(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"data": {"user": None}}
        metrics = self.github_handler.get_developer_metrics("user1")
        self.assertEqual(metrics['commits'], 0)

if __name__ == "__main__":
    unittest.main()