def calculate_productivity_score(commits, pull_requests, reviews, repositories_contributed,
                                 lines_added, lines_removed,
                                 max_commits=700, max_pull_requests=100, max_reviews=100, 
                                 max_repositories_contributed=30, max_lines_changed=250000):
    weights = {
        'commits': 0.3,
        'pull_requests': 0.3,
        'reviews': 0.15,
        'lines_added': 0.07,
        'lines_removed': 0.8,
        'repositories_contributed': 0.1,
    }

    # Normalize each component and clamp it between 0 and 1
    normalized_score = (
        min(commits / max_commits, 1.0) * weights['commits'] +
        min(pull_requests / max_pull_requests, 1.0) * weights['pull_requests'] +
        min(reviews / max_reviews, 1.0) * weights['reviews'] +
        min(repositories_contributed / max_repositories_contributed, 1.0) * weights['repositories_contributed'] +
        min(lines_added / max_lines_changed, 1.0) * weights['lines_added'] +
        min(lines_removed / max_lines_changed, 1.0) * weights['lines_removed']
    )

    return round(min(normalized_score, 1.0) * 100)

def categorize_developers(developers):
    """
    Categorize developers based on score percentiles:
    - Top (10%)
    - Above Average (next 40%)
    - Below Average (next 30%)
    - Bottom (20%)
    """
    if not developers:
        return {}

    sorted_devs = sorted(developers, key=lambda x: x['score'], reverse=True)
    total = len(sorted_devs)
    
    top_count = max(1, round(total * 0.1))  # 10%
    above_count = round(total * 0.4)  # 40%
    below_count = round(total * 0.3)  # 30%

    categories = {
        'top': [d['fullname'] for d in sorted_devs[:top_count]],
        'above_average': [d['fullname'] for d in sorted_devs[top_count:top_count + above_count]],
        'below_average': [d['fullname'] for d in sorted_devs[top_count + above_count:top_count + above_count + below_count]],
        'bottom': [d['fullname'] for d in sorted_devs[top_count + above_count + below_count:]]
    }

    return categories
