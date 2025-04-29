import unittest
from utils import calculate_productivity_score

class TestUtils(unittest.TestCase):
    def test_min_values(self):
        """
        Test with all input values set to 0.
        The score should be 0.
        """
        score = calculate_productivity_score(
            commits=0,
            pull_requests=0,
            issues=0,
            reviews=0,
            repositories_contributed=0,
            lines_added=0,
            lines_removed=0
        )
        self.assertEqual(score, 0)

    def test_max_values(self):
        """
        Test with all input values set to their respective maximum thresholds.
        The score should be 100.
        """
        score = calculate_productivity_score(
            commits=700,
            pull_requests=100,
            issues=30,
            reviews=100,
            repositories_contributed=30,
            lines_added=250000,
            lines_removed=250000
        )
        self.assertEqual(score, 100)

    def test_beyond_max_values(self):
        """
        Test with all input values exceeding their respective maximum thresholds.
        The score should still be clamped to 100.
        """
        score = calculate_productivity_score(
            commits=1000,
            pull_requests=200,
            issues=50,
            reviews=200,
            repositories_contributed=50,
            lines_added=500000,
            lines_removed=500000
        )
        self.assertEqual(score, 100)

    def test_mixed_values(self):
        """
        Test with a mix of values, some at 0, some at max, and some beyond max.
        The score should be within the range of 0-100.
        """
        score = calculate_productivity_score(
            commits=350,  # Half of max
            pull_requests=50,  # Half of max
            issues=15,  # Half of max
            reviews=200,  # Beyond max
            repositories_contributed=15,  # Half of max
            lines_added=125000,  # Half of max
            lines_removed=300000  # Beyond max
        )
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

    def test_no_contributions(self):
        """
        Test with no contributions (all values are 0).
        The score should be 0.
        """
        score = calculate_productivity_score(
            commits=0,
            pull_requests=0,
            issues=0,
            reviews=0,
            repositories_contributed=0,
            lines_added=0,
            lines_removed=0
        )
        self.assertEqual(score, 0)

if __name__ == "__main__":
    unittest.main()