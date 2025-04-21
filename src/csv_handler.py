import pandas as pd
from datetime import datetime
import logging


class CSVHandler:
    def __init__(self, filepath):
        """
        Initialize the CSVHandler with the path to the CSV file.
        """
        self.filepath = filepath

    def load_data(self):
        """
        Load the CSV file into a DataFrame. Returns empty DataFrame if file not found.
        """
        try:
            return pd.read_csv(self.filepath)
        except FileNotFoundError:
            logging.warning(f"File not found: {self.filepath}. Creating a new file.")
            return pd.DataFrame()

    def save_data(self, data):
        """
        Save the given data (list or DataFrame) to the CSV file.
        """
        pd.DataFrame(data).to_csv(self.filepath, index=False)

    def append_metrics(self, metrics):
        """
        Update the CSV file with new metrics for developers.
        """
        existing_df = self.load_data()
        new_df = pd.DataFrame(metrics)

        # Ensure required columns exist and are properly typed
        if 'username' in existing_df.columns:
            existing_df['username'] = existing_df['username'].astype(str)
        if 'last_updated' not in existing_df.columns:
            existing_df['last_updated'] = pd.NaT
        else:
            existing_df['last_updated'] = pd.to_datetime(existing_df['last_updated'], errors='coerce')

        # Add missing columns to new_df to align with existing_df
        for col in existing_df.columns:
            if col not in new_df.columns:
                new_df[col] = None

        # Merge on 'username' — update existing or append new
        new_df['username'] = new_df['username'].astype(str)
        combined_df = pd.concat([existing_df[~existing_df['username'].isin(new_df['username'])], new_df], ignore_index=True)

        # Ensure 'last_updated' is in string format for saving
        if 'last_updated' in combined_df.columns:
            combined_df['last_updated'] = combined_df['last_updated'].astype(str)

        self.save_data(combined_df)

    def get_top_and_bottom_developers(self, top_percent=10, bottom_percent=20):
        """
        Return lists of top and bottom performing developers based on score percentile.
        """
        df = self.load_data()
        if df.empty or 'score' not in df.columns:
            return [], []

        top_thresh = df['score'].quantile(1 - top_percent / 100)
        bottom_thresh = df['score'].quantile(bottom_percent / 100)

        top_devs = df[df['score'] >= top_thresh]['fullname'].tolist()
        bottom_devs = df[df['score'] <= bottom_thresh]['fullname'].tolist()

        return top_devs, bottom_devs

    def filter_by_last_updated(self):
        """
        Return a list of developer records that need processing based on 'last_updated'.
        """
        df = self.load_data()
        today = pd.Timestamp(datetime.now().date())

        if 'last_updated' not in df.columns:
            df['last_updated'] = pd.NaT
        else:
            df['last_updated'] = pd.to_datetime(df['last_updated'], errors='coerce')

        skip_df = df[df['last_updated'].notna() & (df['last_updated'] >= today)]
        for username in skip_df['username']:
            logging.info(f"Skipping {username}: score is up to date.")

        process_df = df[df['last_updated'].isna() | (df['last_updated'] < today)]
        return process_df.to_dict(orient='records')
