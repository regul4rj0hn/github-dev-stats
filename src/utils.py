def calculate_productivity_score(commits, pull_requests, issues, reviews, repositories_contributed,
                                 lines_added, lines_removed,
                                 max_commits=700, max_pull_requests=100, max_issues=30, max_reviews=100, 
                                 max_repositories_contributed=30, max_lines_changed=250000):
    weights = {
        'commits': 0.3,
        'pull_requests': 0.3,
        'issues': 0.02,
        'reviews': 0.15,
        'lines_added': 0.05,
        'lines_removed': 0.8,
        'repositories_contributed': 0.1,
    }

    # Normalize each component and clamp it between 0 and 1
    normalized_score = (
        min(commits / max_commits, 1.0) * weights['commits'] +
        min(pull_requests / max_pull_requests, 1.0) * weights['pull_requests'] +
        min(issues / max_issues, 1.0) * weights['issues'] +
        min(reviews / max_reviews, 1.0) * weights['reviews'] +
        min(repositories_contributed / max_repositories_contributed, 1.0) * weights['repositories_contributed'] +
        min(lines_added / max_lines_changed, 1.0) * weights['lines_added'] +
        min(lines_removed / max_lines_changed, 1.0) * weights['lines_removed']
    )

    return round(normalized_score * 100)
