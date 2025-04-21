import logging
import argparse
import os
from dotenv import load_dotenv
from github_handler import GitHubHandler
from csv_handler import CSVHandler
from utils import calculate_productivity_score
from datetime import datetime

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def parse_args():
    parser = argparse.ArgumentParser(description="Fetch GitHub developer metrics.")
    parser.add_argument("--days-back", type=int, default=365,
                        help="Number of days back to fetch metrics (default: 365 days)")
    parser.add_argument("--exclude-private", action="store_true", default=False,
                        help="Exclude contributions to private repositories")
    parser.add_argument("--only-organizations", action="store_true", default=False,
                        help="Fetch contributions only within organizations")
    return parser.parse_args()


def load_config():
    return {
        "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN"),
        "GITHUB_API_URL": os.getenv("GITHUB_API_URL", "https://api.github.com/graphql"),
        "DATA_FILE_PATH": os.getenv("DATA_FILE_PATH", "data/developers.csv")
    }


def process_developer(developer, github_handler, args):
    username = developer['username']
    logging.info(f"Fetching metrics for {username}...")

    metrics = github_handler.get_developer_metrics(
        username,
        days_back=args.days_back,
        exclude_private=args.exclude_private,
        only_organizations=args.only_organizations
    )
    logging.info(f"Metrics for {username}: {metrics}")

    if metrics['commits'] == 0 and (metrics['lines_added'] > 0 or metrics['lines_removed'] > 0):
        logging.warning(
            f"Suspicious data for {username}: 0 commits but significant activity "
            f"in lines_added ({metrics['lines_added']}) or lines_removed ({metrics['lines_removed']}). "
            f"Calculated score will not be accurate!"
        )

    score = calculate_productivity_score(
        metrics['commits'], metrics['pull_requests'], metrics['issues'], metrics['contributions'],
        metrics['reviews'], metrics['repositories_contributed'],
        metrics['lines_added'], metrics['lines_removed']
    )
    logging.info(f"Calculated score for {username}: {score}")

    if score > 0:
        developer.update(metrics)
        developer['score'] = score
        developer['last_updated'] = datetime.now().strftime('%Y-%m-%d')
    else:
        logging.warning(f"Score for {username} is 0. Please check your permissions on their profile.")

    return developer


def main():
    args = parse_args()
    config = load_config()

    logging.info(
        f"Starting the script with days_back={args.days_back}, "
        f"exclude_private={args.exclude_private}, only_organizations={args.only_organizations}..."
    )

    github_handler = GitHubHandler(config["GITHUB_TOKEN"], config["GITHUB_API_URL"])
    csv_handler = CSVHandler(config["DATA_FILE_PATH"])

    developers = csv_handler.filter_by_last_updated()
    updated_developers = [process_developer(dev, github_handler, args) for dev in developers]

    csv_handler.append_metrics(updated_developers)
    logging.info("Finished updating the CSV file.")

    top_devs, bottom_devs = csv_handler.get_top_and_bottom_developers(10, 20)
    print("Top 10% Developers:", top_devs)
    print("Bottom 20% Developers:", bottom_devs)


if __name__ == "__main__":
    main()
