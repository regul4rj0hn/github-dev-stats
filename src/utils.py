def calculate_productivity_score(commits, pull_requests, issues, contributions):
    # Define weights for each metric
    weights = {
        'commits': 0.4,
        'pull_requests': 0.3,
        'issues': 0.2,
        'contributions': 0.1
    }
    
    # Calculate the weighted score
    score = (commits * weights['commits'] +
             pull_requests * weights['pull_requests'] +
             issues * weights['issues'] +
             contributions * weights['contributions'])
    
    return score

def normalize_score(score, max_score):
    if max_score > 0:
        return (score / max_score) * 100
    return 0