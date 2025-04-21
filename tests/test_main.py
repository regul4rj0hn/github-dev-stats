import unittest
from unittest.mock import patch, MagicMock
from main import process_developer

class TestMain(unittest.TestCase):
    @patch("main.GitHubHandler")
    def test_process_developer(self, MockGitHubHandler):
        mock_handler = MockGitHubHandler.return_value
        mock_handler.get_developer_metrics.return_value = {
            "commits": 10,
            "pull_requests": 5,
            "issues": 2,
            "contributions": 3,
            "reviews": 1,
            "repositories_contributed": 2,
            "lines_added": 100,
            "lines_removed": 50
        }

        developer = {"username": "user1"}
        args = type("Args", (), {"days_back": 365, "exclude_private": False, "only_organizations": False})
        updated_developer = process_developer(developer, mock_handler, args)

        self.assertEqual(updated_developer['score'], 2)
        self.assertEqual(updated_developer['last_updated'], "2025-04-21")

if __name__ == "__main__":
    unittest.main()