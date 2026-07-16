import streamlit as st
import pandas as pd

st.title("Daniel's Michigan Football Analytics")

df = pd.read_csv("data/michigan_games.csv")

# Get all teams
teams = sorted(
    pd.concat([df["homeTeam"], df["awayTeam"]]).unique()
)

team = st.selectbox(
    "Select Team",
    teams,
    index=teams.index("Michigan")   # default selection
)

st.write(f"Selected Team: {team}")
