def load_developers(filepath):
    import pandas as pd
    df = pd.read_csv(filepath)
    return df.to_dict(orient='records')

def append_metrics_to_csv(filepath, metrics):
    import pandas as pd
    df = pd.read_csv(filepath)
    new_data = pd.DataFrame(metrics)
    new_data = new_data[df.columns]
    # Update rows in the existing DataFrame based on the 'username' column
    for _, new_row in new_data.iterrows():
        username = new_row['username']
        if username in df['username'].values:
            df.loc[df['username'] == username, :] = new_row.values
        else:
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(filepath, index=False)

def save_updated_data(filepath, data):
    import pandas as pd
    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False)