import csv
import requests
import logging
from github_api import get_developer_metrics
from csv_handler import load_developers, append_metrics_to_csv
from utils import calculate_productivity_score

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    logging.info("Starting the script...")
    developers = load_developers('data/people.csv')
    
    for developer in developers:
        username = developer['username']
        logging.info(f"Fetching metrics for {username}...")
        metrics = get_developer_metrics(username)
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