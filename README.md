# Bundesliga Team Data Analysis and Visualization

This repository contains a Python script for retrieving Bundesliga team data from fbref.com, processing this data, and visualizing Expected Goals (xG) over time.

## Features

- **Data Retrieval**: Fetches team-specific data for multiple seasons from fbref.com.
- **Data Processing**: Processes the retrieved data to prepare for visualization.
- **Visualization**: Creates plots of the team's xG over time, providing insights into team performance.

## Scripts

- `get_team_data`: Retrieves data for a specific team for the 2022-2023 and 2023-2024 Bundesliga seasons and optionally saves it as a JSON file.
- `process_team_data`: Processes the retrieved data, focusing on calculating 5 game rolling averages for xG.
- `create_team_plot`: Generates a plot showing the rolling xG averages, with an option to save the plot as a PNG file.

## Usage

1. **Get Team Data**:
   ```python
   df = get_team_data("Team-Name", save_as_json=True)

   # Replace `"Team-Name"` with the desired team's name.

2. **Process Team Data**:
   ```python
   X, Y_for, Y_ag = process_team_data(df)
   
   # Takes the DataFrame returned from get_team_data.

3. **Create Team Plot:**:
   ```python
   create_team_plot('Team-Name', X, Y_for, Y_ag, save_as_png=True)
   
   # Generates and displays a plot for the specified team. Set save_as_png to True to save the plot.
  
## Team Configuration
Edit the teams_info dictionary in the script to add or modify team-specific information like logo number and color preferences.

## Example for a single team
```python
teamname = 'Union-Berlin'
df = get_team_data(teamname, save_as_json=True)
X, Y_for, Y_ag = process_team_data(df)
create_team_plot(teamname, X, Y_for, Y_ag, save_as_png=True)
```

## Example for all teams
```python  
for team in teams_info:
    df = get_team_data(team, save_as_json=True)
    X, Y_for, Y_ag = process_team_data(df)
    create_team_plot(team, X, Y_for, Y_ag, save_as_png=True)
```

## Thanks
This addition gives proper credit to sonofacorner.com for the help with visualization.
