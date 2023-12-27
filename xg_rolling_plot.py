import datetime
import os
import urllib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
from PIL import Image
from highlight_text import fig_text

# Dictionary with team information
teams_info = {
    'Union-Berlin': {'fbref_team_id': '7a41008f', 'teamlogonumber': '8149', 'color1': '#EB1923'},
    'Bayer-Leverkusen': {'fbref_team_id': 'c7a9f859', 'teamlogonumber': '8178', 'color1': '#E32221'},
    'Bayern-Munich': {'fbref_team_id': '054efa67', 'teamlogonumber': '9823', 'color1': '#DC052D'},
    'Dortmund': {'fbref_team_id': 'add600ae', 'teamlogonumber': '9789', 'color1': '#FFD700'},
    'Stuttgart': {'fbref_team_id': '598bc722', 'teamlogonumber': '10269', 'color1': '#E32219'},
    'Bochum': {'fbref_team_id': 'b42c6323', 'teamlogonumber': '9911', 'color1': '#005CA9'},
    # Add more teams here in the same format
}

def get_team_data(teamname, save_as_json=False):
    fbref = teams_info[teamname]['fbref_team_id']

    # fbref table link for the 23-24 season
    base_url = 'https://fbref.com/de/mannschaften/{}/{}/spielprotokolle/c20/schedule/{}-Punkte-und-Eckdaten-Bundesliga'

    # fbref table link for the 23-24 season
    url_df_2324 = base_url.format(fbref, '2023-2024', teamname)
    df_2324 = pd.read_html(url_df_2324)[0]

    # fbref table link for the 22-23 season
    url_df_2223 = base_url.format(fbref, '2022-2023', teamname)
    df_2223 = pd.read_html(url_df_2223)[0]

    # Combine both DataFrames
    df = pd.concat([df_2223, df_2324], axis=0).reset_index(drop=True)

    print('Data for ' + teamname + ' successfully loaded.')

    # Optionally save as JSON in the 'data' subfolder
    if save_as_json:
        file_path = os.path.join('data', teamname + '.json')
        os.makedirs(os.path.dirname(file_path), exist_ok=True) # Create directory if it doesn't exist
        df.to_json(file_path, orient='records')
        print('Data for ' + teamname + ' successfully saved as JSON.')
    return df

# Data processing function
def process_team_data(df):
    games_index = 0

    for index, row in df.iterrows():
        if pd.notna(row['xG']): # check if there is a xG value
            games_index += 1
        else: # delete the row where xG is NaN
            df.drop(index, inplace=True)

    df['Datum'] = df['Datum'].apply(lambda x: pd.to_datetime(x, format='%d.%m.%Y'))
    df = df.sort_values(by="Datum")
    df.index = df.index + 1

    Y_for = df['xG'].rolling(window=5, min_periods=0).mean()
    Y_ag = df['xGA'].rolling(window=5, min_periods=0).mean()
    # Y_for = df['xG']
    # Y_ag = df['xGA']
    X = pd.Series(range(1, len(Y_for) + 1))

    print('Data successfully processed.')
    return X, Y_for, Y_ag

# Function to create the team plot
def create_team_plot(teamname, X, Y_for, Y_ag, save_as_png=False):
    teamlogonumber = teams_info[teamname]['teamlogonumber']
    color1 = teams_info[teamname]['color1']
    color2 = '#A9A9A9'

    fig, ax = plt.subplots(figsize=(5, 2.5), dpi=200, facecolor="#EFE9E6")
    ax.set_facecolor("#EFE9E6")

    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("grey")

    ax.grid(visible=True, lw=0.75, ls=":", color="lightgrey")

    line_1 = ax.plot(X, Y_for, color=color1, zorder=4)
    line_2 = ax.plot(X, Y_ag, color=color2, zorder=4)

    ax.set_ylim(0)

    ax.plot([34, 34], [ax.get_ylim()[0], ax.get_ylim()[1]], ls=":", lw=1.25, color="grey", zorder=2)

    ax.annotate(
        xy=(34, 0.15),
        xytext=(-90, 16),
        textcoords="offset points",
        text="Bundesliga Season Change",
        size=6,
        color="grey",
        arrowprops=dict(arrowstyle="->", shrinkA=0, shrinkB=5, color="grey", linewidth=0.75, connectionstyle="angle3,angleA=50,angleB=-30"),
        zorder=4
    )

    ax.fill_between(X, Y_ag, Y_for, where=Y_for > Y_ag, interpolate=True, alpha=0.85, zorder=3, color=line_1[0].get_color())
    ax.fill_between(X, Y_ag, Y_for, where=Y_ag >= Y_for, interpolate=True, alpha=0.85, color=line_2[0].get_color())

    ax.tick_params(color="grey", length=5, which="major", labelsize=6, labelcolor="grey", zorder=3)

    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.5))

    fig_text(x=0.12, y=1.1, s=teamname.replace('-', ' '), color="black", weight="bold", size=10, annotationbbox_kw={"xycoords": "figure fraction"})
    fig_text(x=0.12, y=1.02, s="Expected goals <for> and <against> // 5-game average\nBundesliga Season 22/23 & 23/24", highlight_textprops=[{"color": color1, "weight": "bold"}, {"color": color2, "weight": "bold"}], color="black", size=6, annotationbbox_kw={"xycoords": "figure fraction"})

    fotmob_url = "https://images.fotmob.com/image_resources/logo/teamlogo/"
    logo_ax = fig.add_axes([0.65, .9, 0.2, 0.2], zorder=1)
    club_icon = Image.open(urllib.request.urlopen(f"{fotmob_url}{teamlogonumber}.png"))
    logo_ax.imshow(club_icon)
    logo_ax.axis("off")

    # Save the plot as PNG in the 'plots' subfolder
    if save_as_png:
        output_folder = 'plots'
        output_filename = os.path.join(output_folder, f'{teamname}.png')
        plt.savefig(output_filename, dpi=200, bbox_inches='tight')
        print(f'Plot for {teamname} successfully saved as PNG.')
    plt.show()

# # Example usage for Union Berlin
# teamname = 'Stuttgart'
# df = get_team_data(teamname, save_as_json=True)
# X, Y_for, Y_ag = process_team_data(df)
# create_team_plot(teamname, X, Y_for, Y_ag, save_as_png=True)

# Loop through all teams in the dictionary
for teamname in teams_info.keys():
    df = get_team_data(teamname, save_as_json=False)
    X, Y_for, Y_ag = process_team_data(df)
    create_team_plot(teamname, X, Y_for, Y_ag, save_as_png=True)