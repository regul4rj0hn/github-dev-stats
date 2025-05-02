import pytest
from utils import calculate_productivity_score, categorize_developers

def test_min_values():
    """Test with all input values set to 0. The score should be 0."""
    score = calculate_productivity_score(
        commits=0,
        pull_requests=0,
        reviews=0,
        repositories_contributed=0,
        lines_added=0,
        lines_removed=0
    )
    assert score == 0

def test_max_values():
    """Test with all input values set to their respective maximum thresholds."""
    score = calculate_productivity_score(
        commits=700,
        pull_requests=100,
        reviews=100,
        repositories_contributed=30,
        lines_added=250000,
        lines_removed=250000
    )
    assert score == 100

def test_beyond_max_values():
    """Test with all input values exceeding their respective maximum thresholds."""
    score = calculate_productivity_score(
        commits=1000,
        pull_requests=200,
        reviews=200,
        repositories_contributed=50,
        lines_added=500000,
        lines_removed=500000
    )
    assert score == 100

def test_mixed_values():
    """Test with a mix of values, some at 0, some at max, and some beyond max."""
    score = calculate_productivity_score(
        commits=350,  # Half of max
        pull_requests=50,  # Half of max
        reviews=200,  # Beyond max
        repositories_contributed=15,  # Half of max
        lines_added=125000,  # Half of max
        lines_removed=300000  # Beyond max
    )
    assert score >= 0
    assert score <= 100

def test_no_contributions():
    """Test with no contributions (all values are 0)."""
    score = calculate_productivity_score(
        commits=0,
        pull_requests=0,
        reviews=0,
        repositories_contributed=0,
        lines_added=0,
        lines_removed=0
    )
    assert score == 0

def test_categorize_developers_empty():
    assert categorize_developers([]) == {}

def test_categorize_developers():
    test_developers = [
        {'fullname': 'Dev1', 'score': 100},
        {'fullname': 'Dev2', 'score': 90},
        {'fullname': 'Dev3', 'score': 80},
        {'fullname': 'Dev4', 'score': 70},
        {'fullname': 'Dev5', 'score': 60},
        {'fullname': 'Dev6', 'score': 50},
        {'fullname': 'Dev7', 'score': 40},
        {'fullname': 'Dev8', 'score': 30},
        {'fullname': 'Dev9', 'score': 20},
        {'fullname': 'Dev10', 'score': 10},
    ]
    
    categories = categorize_developers(test_developers)
    
    assert len(categories['top']) == 1  # 10%
    assert len(categories['above_average']) == 4  # 40%
    assert len(categories['below_average']) == 3  # 30%
    assert len(categories['bottom']) == 2  # 20%
    
    assert 'Dev1' in categories['top']
    assert 'Dev10' in categories['bottom']