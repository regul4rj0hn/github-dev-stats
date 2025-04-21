# GitHub Developer Productivity Tracker

This project is designed to measure software developers' productivity by pulling relevant metrics from the GitHub API and appending the calculated scores to a CSV file. 

## Project Structure

```
github-dev-stats
├── src
│   ├── main.py           # Entry point of the application
│   ├── github_handler.py # Functions to interact with the GitHub GraphQL API
│   ├── csv_handler.py    # Handles reading from and writing to the CSV file
│   └── utils.py          # Utility functions including scoring model
├── data
│   └── developers.csv    # List of developers and output
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
└── LICENSE.md            # Project license
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

5. Copy the `.env.example` file to `.env`:
```bash
cp .env.example .env
```

6. Open the `.env` file and populate the `GITHUB_TOKEN` with your GitHub personal access token. The token should have access/visibility to the organizations and repositories you want to benchmark. For example:
```bash
GITHUB_TOKEN=ghp_your_github_token_here
```

## Usage

After going through the setup, execute the following command to run the application:
```bash
python src/main.py
```

### Input Data File

The program expects a `developers.csv` file in the `data` folder. This file should include the GitHub username and the developer's full name, separated by a comma. For example:

```csv
username,fullname,commits,pull_requests,issues,contributions,reviews,repositories_contributed,lines_added,lines_removed,score,last_updated,manager
johnthedoe,John Doe
foofighter,Foo Bar
```

The program will fetch metrics for each developer that is listed in this file and calculate their productivity scores.

### Optional Parameters
- `--days-back`: Specify the number of days back to fetch metrics from the GitHub API. By default, the script fetches metrics from the past `365 days`. For example, to fetch metrics for the past 30 days run:
```bash
python src/main.py --days-back 30
```
- `--sort-by`: Specify the column to sort the CSV rows by (descending). By default, the original ordering is preserved. For example, to order the output rows by the `score` obtained run:
```bash
python src/main.py --sort-by score
```
- `--exclude-private`: Exclude contributions to private repositories. By default, the script includes both public and private repositories. For example:
```bash
python src/main.py --exclude-private
```
- `--only-organizations`: Fetch contributions only within organizations the user is a member of. By default, the script includes contributions to all repositories. For example:
```bash
python src/main.py --only-organizations
```

### Top and Bottom Developers

After calculating the productivity scores, the program identifies:
- **Top 10% Developers**: Developers with scores in the top 10% of all scores.
- **Bottom 20% Developers**: Developers with scores in the bottom 20% of all scores.

The full names of these developers are printed to the console. For example:
```plaintext
Top 10% Developers: ['Foo Bar']
Bottom 20% Developers: ['John Doe']
```

You can modify the default percentage thresholds for top and bottom developers by changing the `top_percent` and `bottom_percent` arguments passed in the `get_top_and_bottom_developers` function.

## Scoring Model and Metrics

The productivity score is calculated based on various metrics fetched from the GitHub API. Each metric reflects a specific aspect of developer performance and engagement. The scoring model uses a weighted formula to calculate the final productivity score, which is then appended to the `developers.csv` file along with the fetched metrics.

### Metrics and Weights

| Metric                     | Weight | Description                                                                                     | Use Case                                                                                     |
|----------------------------|--------|-------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **Commits**                | 20%    | Total number of commits made by the developer.                                                 | Reflects the developer's contribution to the codebase.                                      |
| **Pull Requests**          | 20%    | Number of pull requests created and merged.                                                    | Highlights the developer's role in proposing and integrating changes.                      |
| **Issues**                 | 10%    | Total issues reported and resolved.                                                            | Demonstrates the developer's involvement in identifying and addressing problems.            |
| **Contributions**          | 10%    | Overall contributions to repositories (e.g., commits, pull requests, issues).                  | Captures the developer's general activity across repositories.                             |
| **Reviews**                | 15%    | Number of pull request reviews completed.                                                      | Reflects the developer's engagement in improving code quality and collaborating with peers. |
| **Repositories Contributed** | 5%   | Total number of repositories the developer has contributed to.                                 | Indicates the breadth of the developer's contributions across projects.                    |
| **Lines Added**            | 5%     | Total number of lines of code added by the developer.                                          | Measures the developer's contribution to expanding the codebase.                           |
| **Lines Removed**          | 15%    | Total number of lines of code removed by the developer.                                        | Rewards efforts to simplify and improve the codebase by removing unnecessary code.          |

### Scoring Formula

The scoring formula normalizes each metric to a value between 0 and 1 based on its maximum possible value. Each normalized metric is then multiplied by its respective weight, and the results are summed to calculate the final score. The score is scaled to a percentage (0 to 100) and rounded to the nearest whole number.

#### Formula:
```
Score = (commits / max_commits) * 0.2 +
        (pull_requests / max_pull_requests) * 0.2 +
        (issues / max_issues) * 0.1 +
        (contributions / max_contributions) * 0.1 +
        (reviews / max_reviews) * 0.15 +
        (repositories_contributed / max_repositories_contributed) * 0.05 +
        (lines_added / max_lines_changed) * 0.05 +
        (lines_removed / max_lines_changed) * 0.15
```

### Reasoning Behind the Weights

- **Commits and Pull Requests (20% each)**: These metrics are heavily weighted because they directly reflect the developer's contributions to the codebase and their role in proposing changes.
- **Reviews (15%)**: Code reviews are critical for maintaining code quality and fostering collaboration, so they are given significant weight.
- **Lines Removed (15%)**: Removing unnecessary or redundant code is highly valued as it simplifies and improves the maintainability of the codebase.
- **Issues and Contributions (10% each)**: These metrics capture the developer's involvement in identifying problems and their overall activity across repositories.
- **Repositories Contributed (5%)**: This metric rewards developers who contribute to multiple projects, indicating versatility and collaboration.
- **Lines Added (5%)**: While adding code is important, it is weighted lower than removals to emphasize quality over quantity.

This scoring model is designed to provide a balanced view of developer performance, rewarding both productivity and engagement in collaborative activities.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.