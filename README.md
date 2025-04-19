# GitHub Developer Productivity Tracker

This project is designed to measure software developers' productivity by pulling relevant metrics from the GitHub API and appending the calculated scores to a CSV file. 

## Project Structure

```
github-stats
├── src
│   ├── main.py          # Entry point of the application
│   ├── github_api.py    # Functions to interact with the GitHub API
│   ├── csv_handler.py    # Handles reading from and writing to the CSV file
│   └── utils.py         # Utility functions including scoring model
├── data
│   └── people.csv       # Initial list of developers
├── requirements.txt      # Project dependencies
└── README.md            # Project documentation
```

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd github-stats
```

2. Create a virtual environment for this project using the command:
```bash
python -m venv github-stats-venv
```

3. Activate the virtual environment using the command:
```bash
source github-stats-venv/bin/activate
```

4. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

To run the application, execute the following command:
```bash
python src/main.py
```

### Optional Parameters
- `--days-back`: Specify the number of days back to fetch metrics from the GitHub API. By default, the script fetches metrics from the past `365 days`. For example, to fetch metrics for the past 30 days run:
```bash
python src/main.py --days-back 30
```

## Scoring Model and Metrics

The productivity score is calculated based on the following metrics fetched from the GitHub API:

- **Commits**: Total number of commits made by the developer.
- **Pull Requests**: Number of pull requests created and merged.
- **Issues**: Total issues reported and resolved.
- **Contributions**: Overall contributions to repositories.

The scoring model uses a weighted formula to calculate the final productivity score, which is then appended to the `people.csv` file along with the fetched metrics.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.