import pytest
from github_handler import GitHubHandler

@pytest.fixture
def github_handler():
    return GitHubHandler("fake_token", "https://api.github.com/graphql")

@pytest.fixture
def mock_response(mocker):
    mock = mocker.patch("github_handler.requests.post")
    mock.return_value.status_code = 200
    mock.return_value.json.return_value = {
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
    return mock

def test_get_developer_metrics(github_handler, mock_response):
    metrics = github_handler.get_developer_metrics("user1")
    assert metrics['commits'] == 10
    assert metrics['lines_added'] == 100
    assert metrics['lines_removed'] == 50

def test_get_developer_metrics_handles_empty_response(github_handler, mocker):
    mock = mocker.patch("github_handler.requests.post")
    mock.return_value.status_code = 200
    mock.return_value.json.return_value = {"data": {"user": None}}
    
    metrics = github_handler.get_developer_metrics("user1")
    assert metrics['commits'] == 0