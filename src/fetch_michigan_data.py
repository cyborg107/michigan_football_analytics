import requests
import pandas as pd

API_KEY = "MsxVPy7goZPeM2s1xdr+lfny6/4yeM3gmYig1JRDjJrnSw8e3j4PtREPyQsPV4LE"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

url = "https://api.collegefootballdata.com/games"

years = [2023, 2024, 2025]

all_games = []

for year in years:
    params = {
        "year": year,
        "team": "Michigan"
    }

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    if response.status_code == 200:
        games = response.json()
        all_games.extend(games)
        print(f"Retrieved {len(games)} games.")
    else:
        print(f"Error retrieving {year}: {response.status_code}")

df = pd.DataFrame(all_games)

display(df.head())
display(df[["homeTeam", "awayTeam"]])

df.info()
df.columns
df.describe()

df[["homeTeam", "awayTeam"]]
df[df["homeTeam"] == "Michigan"]

df.to_csv(
    "data/michigan_games.csv",
    index=False
)

wins = 0

for _, game in df.iterrows():

    if game["homeTeam"] == "Michigan":

        if game["homePoints"] > game["awayPoints"]:
            wins += 1

    elif game["awayTeam"] == "Michigan":

        if game["awayPoints"] > game["homePoints"]:
            wins += 1

print(f"Michigan won {wins} games.")
