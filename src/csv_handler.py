import pandas as pd
from datetime import datetime
import logging

SCHEMA = [
    'username', 'fullname', 'commits', 'pull_requests', 'reviews', 'repositories_contributed',
    'lines_added', 'lines_removed', 'score', 'last_updated', 'manager'
]

class CSVHandler:
    def __init__(self, filepath, order_by):
        self.filepath = filepath
        self.order_by = order_by

    def load_data(self):
        try:
            df = pd.read_csv(self.filepath)
        except FileNotFoundError:
            logging.warning(f"File not found: {self.filepath}. Creating a new file.")
            df = pd.DataFrame(columns=SCHEMA)
        return df.reindex(columns=SCHEMA)

    def save_data(self, data):
        df = pd.DataFrame(data).reindex(columns=SCHEMA)
        if self.order_by in df.columns:
            df = df.sort_values(by=self.order_by, na_position="last") 
        df.to_csv(self.filepath, index=False)

    def append_metrics(self, metrics):
        """
        Update the CSV file with new metrics for developers.
        """
        existing_df = self.load_data()
        new_df = pd.DataFrame(metrics).reindex(columns=SCHEMA)

        # Normalize types
        existing_df['username'] = existing_df['username'].astype(str)
        new_df['username'] = new_df['username'].astype(str)

        # Merge existing and new data
        merged_df = pd.concat(
            [existing_df[~existing_df['username'].isin(new_df['username'])], new_df],
            ignore_index=True
        ).reindex(columns=SCHEMA)

        if 'last_updated' in merged_df.columns:
            merged_df['last_updated'] = merged_df['last_updated'].astype(str)

        self.save_data(merged_df)

    def filter_by_last_updated(self):
        """
        Return a list of developer records that need processing based on 'last_updated'.
        """
        df = self.load_data()
        today = pd.Timestamp(datetime.now().date())

        df['last_updated'] = pd.to_datetime(df['last_updated'], errors='coerce')
        skip_df = df[df['last_updated'].notna() & (df['last_updated'] >= today)]

        for username in skip_df['username']:
            logging.info(f"Skipping {username}: score is up to date.")

        process_df = df[df['last_updated'].isna() | (df['last_updated'] < today)]
        return process_df.to_dict(orient='records')

    def get_developers_with_scores(self):
        """
        Return all developers with their scores as a list of dictionaries.
        """
        df = self.load_data()
        if df.empty or 'score' not in df.columns:
            return []
        
        df['score'] = pd.to_numeric(df['score'], errors='coerce')
        return df[['fullname', 'score']].to_dict(orient='records')