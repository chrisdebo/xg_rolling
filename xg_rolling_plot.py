import datetime
import os
import urllib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
from PIL import Image
from highlight_text import fig_text

# teamname in json file
teamname = 'Union-Berlin'

# date in json file
date = "20231226"

#teamlogonumber in fotmob
teamlogonumber = '8149'

# url for fotmob logo
fotmob_url = "https://images.fotmob.com/image_resources/logo/teamlogo/"


# Function to get today's date
def get_today_date():
    return datetime.datetime.now().strftime("%Y%m%d")

# get today's date
today_date = get_today_date()

# set the file path
file_path = os.path.join('data', teamname + '_' + date + '.json')

# read the JSON file into a DataFrame
df = pd.read_json(file_path)

games_index = 0

for value in df['Ergebnis']:
    if pd.notna(value):  # check if value is not nan
        games_index += 1
    else:
        print('Reached NaN value at ' + str(games_index))
        break

df.drop(df.index[games_index:], inplace=True)
df['Datum'] = df['Datum'].apply(lambda x: pd.to_datetime(x, format='%d.%m.%Y'))
df = df.sort_values(by="Datum")
df.index = df.index + 1

# xG conceded and xG created
Y_for = df.xG.rename('value', inplace=True)
Y_ag = df.xGA.rename('value', inplace=True)
X = pd.Series(range(len(Y_for)))

X = X + 1

X.index = X.index + 1

# Compute the rolling average (min_periods is used for the partial average)
# Here we're using a 5 game rolling average
Y_for = Y_for.rolling(window=5, min_periods=0).mean()
Y_ag = Y_ag.rolling(window=5, min_periods=0).mean()

fig = plt.figure(figsize=(5, 2.5), dpi=200, facecolor="#EFE9E6")
ax = plt.subplot(111, facecolor="#EFE9E6")

# Remove top & right spines and change the color.
ax.spines[["top", "right"]].set_visible(False)
ax.spines[["left", "bottom"]].set_color("grey")

# Set the grid
ax.grid(
    visible=True,
    lw=0.75,
    ls=":",
    color="lightgrey"
)

line_1 = ax.plot(X, Y_for, color="#ED1C24", zorder=4)
line_2 = ax.plot(X, Y_ag, color="#989898", zorder=4)
ax.set_ylim(0)

# Add a line to mark the division between seasons
ax.plot(
    [34, 34],  # 34 games per season
    [ax.get_ylim()[0], ax.get_ylim()[1]],
    ls=":",
    lw=1.25,
    color="grey",
    zorder=2
)

# Annotation with data coordinates and offset points.
ax.annotate(
    xy=(34, 0.15),
    xytext=(-90, 16),
    textcoords="offset points",
    text="Bundesliga Season Change",
    size=6,
    color="grey",
    arrowprops=dict(
        arrowstyle="->", shrinkA=0, shrinkB=5, color="grey", linewidth=0.75,
        connectionstyle="angle3,angleA=50,angleB=-30"
    )  # Arrow to connect annotation
)

# Fill between
ax.fill_between(
    X,
    Y_ag,
    Y_for,
    where=Y_for > Y_ag,
    interpolate=True,
    alpha=0.85,
    zorder=3,
    color=line_1[0].get_color()
)

ax.fill_between(
    X,
    Y_ag,
    Y_for,
    where=Y_ag >= Y_for,
    interpolate=True,
    alpha=0.85,
    color=line_2[0].get_color()
)

# Customize the ticks to match spine color and adjust label size.
ax.tick_params(
    color="grey",
    length=5,
    which="major",
    labelsize=6,
    labelcolor="grey",
    zorder=3
)

# Set x-axis major tick positions to only 5 game multiples.
ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
# Set y-axis major tick positions to only 0.5 xG multiples.
ax.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
ax.set_ylim(0)

# Title and subtitle for the legend
fig_text(
    x=0.12, y=1.1,
    s=teamname.replace('-', ' '),
    color="black",
    weight="bold",
    size=10,
    annotationbbox_kw={"xycoords": "figure fraction"}
)

fig_text(
    x=0.12, y=1.02,
    s="Expected goals <for> and <against> // 5-game average\nBundesliga Season 22/23 & 23/24",
    highlight_textprops=[
        {"color": line_1[0].get_color(), "weight": "bold"},
        {"color": line_2[0].get_color(), "weight": "bold"}
    ],
    color="black",
    size=6,
    annotationbbox_kw={"xycoords": "figure fraction"}
)

# Add the club logo
logo_ax = fig.add_axes([0.65, .9, 0.3, 0.3], zorder=1)
club_icon = Image.open(urllib.request.urlopen(f"{fotmob_url}{teamlogonumber}.png"))
logo_ax.imshow(club_icon)
logo_ax.axis("off")

# Create the filename using teamname and today_date
output_folder = 'plots'
output_filename = os.path.join(output_folder, f'{teamname}_{today_date}.png')

plt.savefig(output_filename, dpi=200, bbox_inches='tight')  # Save the plot

plt.show()

#%%
