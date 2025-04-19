import pandas as pd

def load_developers(filepath):
    df = pd.read_csv(filepath)
    return df.to_dict(orient='records')

def append_metrics_to_csv(filepath, metrics):
    df = pd.read_csv(filepath)
    new_data = pd.DataFrame(metrics)
    new_data = new_data[df.columns]

    for _, new_row in new_data.iterrows():
        username = new_row['username']
        if username in df['username'].values:
            df.loc[df['username'] == username, :] = new_row.values
        else:
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(filepath, index=False)

def save_updated_data(filepath, data):
    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False)

def get_top_and_bottom_developers(filepath, top_percent=10, bottom_percent=20):
    """
    Calculate the top N% and bottom N% developers based on their scores.

    Args:
        filepath (str): Path to the CSV file.
        top_percent (int): Percentage threshold for top developers.
        bottom_percent (int): Percentage threshold for bottom developers.

    Returns:
        tuple: (list of top developers' full names, list of bottom developers' full names)
    """
    df = pd.read_csv(filepath)
    top_threshold = df['score'].quantile(1 - top_percent / 100)
    bottom_threshold = df['score'].quantile(bottom_percent / 100)

    top_developers = df[df['score'] >= top_threshold]['fullname'].tolist()
    bottom_developers = df[df['score'] <= bottom_threshold]['fullname'].tolist()

    return top_developers, bottom_developers