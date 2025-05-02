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
├── tests
│   └── test_main.csv     # Unit and functional tests
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
username,fullname,commits,pull_requests,issues,reviews,repositories_contributed,lines_added,lines_removed,score,last_updated,manager
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

### Developer Categories

After calculating the productivity scores, the program categorizes developers into four groups:
- **Top**: Developers with scores in the top 10% of all scores
- **Above Average**: The next 40% of developers
- **Below Average**: The following 30% of developers
- **Bottom**: The remaining 20% of developers

The full names of these developers are printed to the console. For example:
```plaintext
Developer Categories:
Top (10%): ['Luke Skywalker']
Above Average (40%): ['Obi-Wan Kenobi', 'Han Solo', 'Leia Organa', 'Padme Amidala']
Below Average (30%): ['Lando Calrissian', 'Chewbacca', 'C-3PO']
Bottom (20%): ['R2-D2', 'Jar Jar Binks']
```

## Scoring Model and Metrics

The productivity score is calculated based on various metrics fetched from the GitHub API. Each metric reflects a specific aspect of developer performance and engagement. The scoring model uses a weighted formula to calculate the final productivity score, which is then appended to the `developers.csv` file along with the fetched metrics.

### Metrics and Weights

| Metric                     | Weight | Description                                                                                     | Use Case                                                                                     |
|----------------------------|--------|-------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **Commits**                | 30%    | Total number of commits made by the developer.                                                 | Reflects the developer's contribution to the codebase.                                      |
| **Pull Requests**          | 30%    | Number of pull requests created and merged.                                                    | Highlights the developer's role in proposing and integrating changes.                      |
| **Issues**                 | 2%    | Total issues reported and resolved.                                                            | Demonstrates the developer's involvement in identifying and addressing problems.            |
| **Reviews**                | 15%    | Number of pull request reviews completed.                                                      | Reflects the developer's engagement in improving code quality and collaborating with peers. |
| **Repositories Contributed** | 10%   | Total number of repositories the developer has contributed to.                                 | Indicates the breadth of the developer's contributions across projects.                    |
| **Lines Added**            | 5%     | Total number of lines of code added by the developer.                                          | Measures the developer's contribution to expanding the codebase.                           |
| **Lines Removed**          | 8%    | Total number of lines of code removed by the developer.                                        | Rewards efforts to simplify and improve the codebase by removing unnecessary code.          |

### Scoring Formula

The scoring formula normalizes each metric to a value between 0 and 1 based on its maximum possible value. Each normalized metric is then multiplied by its respective weight, and the results are summed to calculate the final score. The score is scaled to a percentage (0 to 100) and rounded to the nearest whole number.

### Reasoning Behind the Weights

- **Commits and Pull Requests (30% each)**: These metrics are heavily weighted because they directly reflect the developer's contributions to the codebase and their role in proposing changes.
- **Reviews (15%)**: Code reviews are critical for maintaining code quality and fostering collaboration, so they are given significant weight.
- **Lines Removed (8%)**: Removing unnecessary or redundant code is highly valued as it simplifies and improves the maintainability of the codebase.
- **Repositories Contributed (5%)**: This metric rewards developers who contribute to multiple projects, indicating versatility and broad collaboration.
- **Lines Added (5%)**: While adding code is important, it is weighted lower than removals to emphasize quality over quantity.
- **Issues (2%)**: These metrics capture the developer's involvement in identifying problems and their activity on issues. Bear in mind that most issue tracking happens in Jira so this metric gets a low weight.

This scoring model is designed to provide a balanced view of developer performance, rewarding both productivity and engagement in collaborative activities.

## Testing

This project includes unit and functional tests to ensure the correctness of its functionality. The tests are located in the `tests` directory and assume that you've already gone through the setup steps.

### Running the Tests

To run all tests, make sure you are you've activated the venv and use the following command:
```bash
python -m pytest tests/
```

## License

This project is licensed under the MIT License. See the LICENSE file for more details.