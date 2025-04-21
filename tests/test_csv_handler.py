import unittest
import pandas as pd
from datetime import datetime
from csv_handler import CSVHandler

class TestCSVHandler(unittest.TestCase):
    def setUp(self):
        self.filepath = "test_developers.csv"
        self.sort_by = "fullname"
        self.csv_handler = CSVHandler(self.filepath, self.sort_by)
        self.test_data = [
            {
                "username": "user1",
                "fullname": "User One",
                "commits": 10,
                "pull_requests": 5,
                "issues": 2,
                "contributions": 3,
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
                "issues": 0,
                "contributions": 0,
                "reviews": 0,
                "repositories_contributed": 0,
                "lines_added": 0,
                "lines_removed": 0,
                "score": 0,
                "last_updated": None,
                "manager": "Manager B"
            }
        ]

    def tearDown(self):
        # Clean up the test file after each test
        import os
        if os.path.exists(self.filepath):
            os.remove(self.filepath)

    def test_load_data_creates_empty_file(self):
        df = self.csv_handler.load_data()
        self.assertTrue(df.empty)
        self.assertListEqual(list(df.columns), [
            'username', 'fullname', 'commits', 'pull_requests', 'issues', 'contributions', 'reviews',
            'repositories_contributed', 'lines_added', 'lines_removed', 'score', 'last_updated', 'manager'
        ])

    def test_save_data_sorts_by_fullname(self):
        self.csv_handler.save_data(self.test_data)
        df = pd.read_csv(self.filepath)
        self.assertEqual(df.iloc[0]['fullname'], "User One")
        self.assertEqual(df.iloc[1]['fullname'], "User Two")

    def test_append_metrics_updates_existing_data(self):
        self.csv_handler.save_data(self.test_data)
        updated_data = [
            {
                "username": "user1",
                "fullname": "User One Updated",
                "commits": 20,
                "pull_requests": 10,
                "issues": 5,
                "contributions": 6,
                "reviews": 2,
                "repositories_contributed": 4,
                "lines_added": 200,
                "lines_removed": 100,
                "score": 40,
                "last_updated": "2025-04-21",
                "manager": "Manager A"
            }
        ]
        self.csv_handler.append_metrics(updated_data)
        df = pd.read_csv(self.filepath)
        self.assertEqual(len(df), 2)
        self.assertEqual(df[df['username'] == "user1"].iloc[0]['fullname'], "User One Updated")

    def test_filter_by_last_updated(self):
        self.csv_handler.save_data(self.test_data)
        developers_to_process = self.csv_handler.filter_by_last_updated()
        self.assertEqual(len(developers_to_process), 2)
        usernames = [dev['username'] for dev in developers_to_process]
        self.assertIn("user1", usernames)
        self.assertIn("user2", usernames)

if __name__ == "__main__":
    unittest.main()