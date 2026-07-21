import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Michigan Football Analytics", page_icon="🏈", layout="wide"
)

st.title("🏈 Football Analytics Dashboard")

df = pd.read_csv("data/michigan_games.csv")

# Get all unique teams
teams = sorted(pd.concat([df["homeTeam"], df["awayTeam"]]).unique())

team = st.selectbox(
    "Select Team", teams, index=teams.index("Michigan") if "Michigan" in teams else 0
)

# Filter games for the selected team
team_games = df[(df["homeTeam"] == team) | (df["awayTeam"] == team)].copy()

# Determine Team Score, Opponent Score, and Result
team_games["team_score"] = np.where(
    team_games["homeTeam"] == team,
    team_games["homePoints"],
    team_games["awayPoints"],
)
team_games["opp_score"] = np.where(
    team_games["homeTeam"] == team,
    team_games["awayPoints"],
    team_games["homePoints"],
)
team_games["opponent"] = np.where(
    team_games["homeTeam"] == team,
    team_games["awayTeam"],
    team_games["homeTeam"],
)
team_games["margin"] = team_games["team_score"] - team_games["opp_score"]
team_games["result"] = np.where(team_games["margin"] > 0, "Win", "Loss")

# ---------------------------------------------------------
# 1. Summary Metrics
# ---------------------------------------------------------
total_games = len(team_games)
wins = (team_games["result"] == "Win").sum()
losses = (team_games["result"] == "Loss").sum()
win_rate = (wins / total_games * 100) if total_games > 0 else 0
avg_pts = team_games["team_score"].mean() if total_games > 0 else 0
avg_allowed = team_games["opp_score"].mean() if total_games > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Games", total_games)
col2.metric("Record (W-L)", f"{wins}-{losses}")
col3.metric("Win Rate", f"{win_rate:.1f}%")
col4.metric("Avg Points (Scored / Allowed)", f"{avg_pts:.1f} / {avg_allowed:.1f}")

st.divider()

# ---------------------------------------------------------
# 2. Visualizations
# ---------------------------------------------------------
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("📊 Point Differential Timeline")
    fig_margin = px.bar(
        team_games,
        x=team_games.index,
        y="margin",
        color="result",
        color_discrete_map={"Win": "#2ecc71", "Loss": "#e74c3c"},
        hover_data=["opponent", "team_score", "opp_score"],
        labels={"margin": "Point Differential", "index": "Game #"},
        title="Margin of Victory / Defeat per Game",
    )
    st.plotly_chart(fig_margin, use_container_width=True)

with chart_col2:
    st.subheader("🎯 Home vs. Away Performance")
    team_games["location"] = np.where(
        team_games["homeTeam"] == team, "Home", "Away"
    )
    location_summary = (
        team_games.groupby(["location", "result"])
        .size()
        .reset_index(name="count")
    )

    fig_loc = px.bar(
        location_summary,
        x="location",
        y="count",
        color="result",
        barmode="group",
        color_discrete_map={"Win": "#2ecc71", "Loss": "#e74c3c"},
        title="Wins and Losses by Game Location",
    )
    st.plotly_chart(fig_loc, use_container_width=True)

# ---------------------------------------------------------
# 3. Game Log Table
# ---------------------------------------------------------
st.subheader("📋 Game Log")
st.dataframe(team_games, use_container_width=True)
