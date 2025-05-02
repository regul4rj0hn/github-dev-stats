import pytest
from datetime import datetime
from unittest.mock import MagicMock
from main import process_developer

def test_process_developer(mocker):
    mock_handler = MagicMock()
    mock_handler.get_developer_metrics.return_value = {
        "commits": 10,
        "pull_requests": 5,
        "issues": 2,
        "reviews": 1,
        "repositories_contributed": 2,
        "lines_added": 100,
        "lines_removed": 50
    }

    developer = {"username": "user1"}
    args = type("Args", (), {"days_back": 365, "exclude_private": False, "only_organizations": False})
    updated_developer = process_developer(developer, mock_handler, args)

    assert updated_developer['score'] == 3
    assert updated_developer['last_updated'] == datetime.now().strftime('%Y-%m-%d')