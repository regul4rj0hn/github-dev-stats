def calculate_productivity_score(commits, pull_requests, issues, contributions,
                                 max_commits=700, max_pull_requests=100, max_issues=50, max_contributions=100):
    weights = {
        'commits': 0.3,
        'pull_requests': 0.4,
        'issues': 0.1,
        'contributions': 0.2
    }

    # Normalize each component and clamp it between 0 and 1
    normalized_score = (
        min(commits / max_commits, 1.0) * weights['commits'] +
        min(pull_requests / max_pull_requests, 1.0) * weights['pull_requests'] +
        min(issues / max_issues, 1.0) * weights['issues'] +
        min(contributions / max_contributions, 1.0) * weights['contributions']
    )

    return round(normalized_score * 100)
