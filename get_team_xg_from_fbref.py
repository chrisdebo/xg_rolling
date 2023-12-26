import datetime
import os
import pandas as pd

# Function to get today's date
def get_today_date():
    return datetime.datetime.now().strftime("%Y%m%d")

# Set the team name
teamname = 'Union-Berlin'

# Base URL with placeholders for the season and team name
base_url = 'https://fbref.com/de/mannschaften/7a41008f/{}/spielprotokolle/c20/schedule/{}-Punkte-und-Eckdaten-Bundesliga'

# fbref table link for the 23-24 season
url_df_2324 = base_url.format('2023-2024', teamname)
df_2324 = pd.read_html(url_df_2324)[0]

# fbref table link for the 22-23 season
url_df_2223 = base_url.format('2022-2023', teamname)
df_2223 = pd.read_html(url_df_2223)[0]

# Combine both DataFrames
df = pd.concat([df_2223, df_2324], axis=0).reset_index(drop=True)

# Save as JSON in the 'data' subfolder
today_date = get_today_date()
file_path = os.path.join('data', teamname + '_' + today_date + '.json')
df.to_json(file_path, orient='records')