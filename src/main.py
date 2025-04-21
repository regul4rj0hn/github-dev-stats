import logging
import argparse
import os
from dotenv import load_dotenv
from github_handler import GitHubHandler
from csv_handler import append_metrics_to_csv, get_top_and_bottom_developers, filter_developers_by_last_updated
from utils import calculate_productivity_score
from datetime import datetime, timedelta

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    config = {
        "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN"),
        "GITHUB_API_URL": os.getenv("GITHUB_API_URL", "https://api.github.com/graphql"),
        "DATA_FILE_PATH": os.getenv("DATA_FILE_PATH", "data/developers.csv")
    }

    github_handler = GitHubHandler(config["GITHUB_TOKEN"], config["GITHUB_API_URL"])

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Fetch GitHub developer metrics.")
    parser.add_argument(
        "--days-back",
        type=int,
        default=365,
        help="Number of days back to fetch metrics (default: 365 days)"
    )
    parser.add_argument(
        "--exclude-private",
        action="store_true",
        default=False,
        help="Exclude contributions to private repositories"
    )
    parser.add_argument(
        "--only-organizations",
        action="store_true",
        default=False,
        help="Fetch contributions only within organizations"
    )
    args = parser.parse_args()

    logging.info(f"Starting the script with days_back={args.days_back}, exclude_private={args.exclude_private}, only_organizations={args.only_organizations}...")

    # Filter developers by 'last_updated' field
    developers = filter_developers_by_last_updated(config["DATA_FILE_PATH"])

    updated_developers = []
    for developer in developers:
        username = developer['username']
        logging.info(f"Fetching metrics for {username}...")
        metrics = github_handler.get_developer_metrics(
            username,
            days_back=args.days_back,
            exclude_private=args.exclude_private,
            only_organizations=args.only_organizations
        )
        logging.info(f"Metrics for {username}: {metrics}")
        
        score = calculate_productivity_score(
            metrics['commits'], metrics['pull_requests'], metrics['issues'], metrics['contributions'],
            metrics['reviews'], metrics['repositories_contributed'],
            metrics['lines_added'], metrics['lines_removed']
        )
        logging.info(f"Calculated score for {username}: {score}")

        # Update metrics and 'last_updated' field if score is non-zero
        if score > 0:
            developer.update(metrics)
            developer['score'] = score
            developer['last_updated'] = datetime.now().strftime('%Y-%m-%d')
        else:
            logging.warning(f"Score for {username} is 0. Please check your permissions on their profile.")

        updated_developers.append(developer)

    append_metrics_to_csv(config["DATA_FILE_PATH"], updated_developers)
    logging.info("Finished updating the CSV file.")

    # Get top and bottom developers
    top_developers, bottom_developers = get_top_and_bottom_developers(config["DATA_FILE_PATH"], 10, 20)
    print("Top 10% Developers:", top_developers)
    print("Bottom 20% Developers:", bottom_developers)

if __name__ == "__main__":
    main()