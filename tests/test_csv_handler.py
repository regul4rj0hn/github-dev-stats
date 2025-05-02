import pytest
import pandas as pd
import os
from csv_handler import CSVHandler

@pytest.fixture
def test_filepath():
    return "test_developers.csv"

@pytest.fixture
def csv_handler(test_filepath):
    return CSVHandler(test_filepath, "fullname")

@pytest.fixture
def test_data():
    return [
        {
            "username": "user1",
            "fullname": "User One",
            "commits": 10,
            "pull_requests": 5,
            "reviews": 1,
            "repositories_contributed": 2,
            "lines_added": 100,
            "lines_removed": 50,
            "score": 20,
            "last_updated": "2025-04-20",
            "manager": "Manager A"
        },
        {
            "username": "user2",
            "fullname": "User Two",
            "commits": 0,
            "pull_requests": 0,
            "reviews": 0,
            "repositories_contributed": 0,
            "lines_added": 0,
            "lines_removed": 0,
            "score": 0,
            "last_updated": None,
            "manager": "Manager B"
        }
    ]

@pytest.fixture(autouse=True)
def cleanup(test_filepath):
    yield
    if os.path.exists(test_filepath):
        os.remove(test_filepath)

def test_load_data_creates_empty_file(csv_handler):
    df = csv_handler.load_data()
    assert df.empty
    assert list(df.columns) == [
        'username', 'fullname', 'commits', 'pull_requests', 'reviews', 
        'repositories_contributed', 'lines_added', 'lines_removed', 'score', 
        'last_updated', 'manager'
    ]

def test_save_data_sorts_by_fullname(csv_handler, test_data):
    csv_handler.save_data(test_data)
    df = pd.read_csv(csv_handler.filepath)
    assert df.iloc[0]['fullname'] == "User One"
    assert df.iloc[1]['fullname'] == "User Two"

def test_append_metrics_updates_existing_data(csv_handler, test_data):
    csv_handler.save_data(test_data)
    updated_data = [
        {
            "username": "user1",
            "fullname": "User One Updated",
            "commits": 20,
            "pull_requests": 10,
            "reviews": 2,
            "repositories_contributed": 4,
            "lines_added": 200,
            "lines_removed": 100,
            "score": 40,
            "last_updated": "2025-04-21",
            "manager": "Manager A"
        }
    ]
    csv_handler.append_metrics(updated_data)
    df = pd.read_csv(csv_handler.filepath)
    assert len(df) == 2
    assert df[df['username'] == "user1"].iloc[0]['fullname'] == "User One Updated"

def test_filter_by_last_updated(csv_handler, test_data):
    csv_handler.save_data(test_data)
    developers_to_process = csv_handler.filter_by_last_updated()
    assert len(developers_to_process) == 2
    usernames = [dev['username'] for dev in developers_to_process]
    assert "user1" in usernames
    assert "user2" in usernames

def test_get_developers_with_scores(csv_handler):
    test_data = [
        {'username': 'dev1', 'fullname': 'Developer 1', 'score': 90},
        {'username': 'dev2', 'fullname': 'Developer 2', 'score': 80}
    ]
    csv_handler.save_data(test_data)

    developers = csv_handler.get_developers_with_scores()
    
    assert len(developers) == 2
    assert developers[0]['fullname'] == 'Developer 1'
    assert developers[0]['score'] == 90
    assert developers[1]['fullname'] == 'Developer 2'
    assert developers[1]['score'] == 80

def test_get_developers_with_scores_empty(csv_handler):
    csv_handler.save_data([])
    developers = csv_handler.get_developers_with_scores()
    assert developers == []