import pandas as pd
from datetime import datetime
import logging


class CSVHandler:
    def __init__(self, filepath):
        """
        Initialize the CSVHandler with the path to the CSV file.

        Args:
            filepath (str): Path to the CSV file.
        """
        self.filepath = filepath

    def load_data(self):
        """
        Load the CSV file into a DataFrame.

        Returns:
            pd.DataFrame: The loaded DataFrame.
        """
        try:
            df = pd.read_csv(self.filepath)
        except FileNotFoundError:
            logging.warning(f"File not found: {self.filepath}. Creating a new file.")
            df = pd.DataFrame()
        return df

    def save_data(self, data):
        """
        Save the given data to the CSV file.

        Args:
            data (list or pd.DataFrame): The data to save.
        """
        df = pd.DataFrame(data)
        df.to_csv(self.filepath, index=False)

    def append_metrics(self, metrics):
        """
        Update the CSV file with new metrics for developers.

        Args:
            metrics (list): List of updated developer metrics.
        """
        df = self.load_data()

        # Ensure 'last_updated' column exists in the DataFrame
        if 'last_updated' not in df.columns:
            df['last_updated'] = None

        # Ensure correct data types for critical columns
        if 'username' in df.columns:
            df['username'] = df['username'].astype(str)
        if 'last_updated' in df.columns:
            df['last_updated'] = pd.to_datetime(df['last_updated'], errors='coerce')

        new_data = pd.DataFrame(metrics)

        # Ensure new_data has the same columns as df
        for col in df.columns:
            if col not in new_data.columns:
                new_data[col] = None

        for _, new_row in new_data.iterrows():
            username = new_row['username']
            if username in df['username'].values:
                # Update the row for the developer
                for col in df.columns:
                    df.loc[df['username'] == username, col] = new_row[col]
            else:
                # Add a new row for the developer
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        # Ensure 'last_updated' column is saved as string
        if 'last_updated' in df.columns:
            df['last_updated'] = df['last_updated'].astype(str)

        df.to_csv(self.filepath, index=False)

    def get_top_and_bottom_developers(self, top_percent=10, bottom_percent=20):
        """
        Calculate the top N% and bottom N% developers based on their scores.

        Args:
            top_percent (int): Percentage threshold for top developers.
            bottom_percent (int): Percentage threshold for bottom developers.

        Returns:
            tuple: (list of top developers' full names, list of bottom developers' full names)
        """
        df = self.load_data()
        top_threshold = df['score'].quantile(1 - top_percent / 100)
        bottom_threshold = df['score'].quantile(bottom_percent / 100)

        top_developers = df[df['score'] >= top_threshold]['fullname'].tolist()
        bottom_developers = df[df['score'] <= bottom_threshold]['fullname'].tolist()

        return top_developers, bottom_developers

    def filter_by_last_updated(self):
        """
        Filter developers whose 'last_updated' date is more recent than today.

        Returns:
            list: List of developers to process.
        """
        today = pd.Timestamp(datetime.now().date())
        df = self.load_data()

        # Ensure 'last_updated' column exists and is of type datetime
        if 'last_updated' not in df.columns:
            df['last_updated'] = None
        else:
            df['last_updated'] = pd.to_datetime(df['last_updated'], errors='coerce')

        # Identify developers to skip
        developers_to_skip = df[
            (df['last_updated'].notna()) & (df['last_updated'] >= today)
        ]

        for username in developers_to_skip['username']:
            logging.info(f"Skipping {username}: score is up to date.")

        # Filter developers whose 'last_updated' is not today
        developers_to_process = df[
            (df['last_updated'].isna()) | (df['last_updated'] < today)
        ]

        return developers_to_process.to_dict(orient='records')