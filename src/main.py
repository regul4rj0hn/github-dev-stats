import csv
import requests
import logging
import argparse
from github_api import get_developer_metrics
from csv_handler import load_developers, append_metrics_to_csv
from utils import calculate_productivity_score

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    parser = argparse.ArgumentParser(description="Fetch GitHub developer metrics.")
    parser.add_argument(
        "--days-back",
        type=int,
        default=365,
        help="Number of days back to fetch metrics (default: 365 days)"
    )
    args = parser.parse_args()

    logging.info(f"Starting the script with days_back={args.days_back}...")
    developers = load_developers('data/people.csv')
    
    for developer in developers:
        username = developer['username']
        logging.info(f"Fetching metrics for {username}...")
        metrics = get_developer_metrics(username, days_back=args.days_back)
        logging.info(f"Metrics for {username}: {metrics}")
        
        score = calculate_productivity_score(
            metrics['commits'], metrics['pull_requests'], metrics['issues'], metrics['contributions']
        )
        logging.info(f"Calculated score for {username}: {score}")
        developer.update(metrics)
        developer['score'] = score

    append_metrics_to_csv('data/people.csv', developers)
    logging.info("Finished updating the CSV file.")

if __name__ == "__main__":
    main()