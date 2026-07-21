import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Michigan Football Analytics & AI", page_icon="🏈", layout="wide"
)

st.title("🏈 Daniel's Football Analytics & Prediction Dashboard")

df = pd.read_csv("data/michigan_games.csv")

# ---------------------------------------------------------
# Sidebar Controls
# ---------------------------------------------------------
st.sidebar.header("Filter Settings")

teams = sorted(pd.concat([df["homeTeam"], df["awayTeam"]]).unique())

selected_team = st.sidebar.selectbox(
    "Select Team",
    teams,
    index=teams.index("Michigan") if "Michigan" in teams else 0,
)

# Process Team Data
team_games = df[
    (df["homeTeam"] == selected_team) | (df["awayTeam"] == selected_team)
].copy()

team_games["team_score"] = np.where(
    team_games["homeTeam"] == selected_team,
    team_games["homePoints"],
    team_games["awayPoints"],
)
team_games["opp_score"] = np.where(
    team_games["homeTeam"] == selected_team,
    team_games["awayPoints"],
    team_games["homePoints"],
)
team_games["opponent"] = np.where(
    team_games["homeTeam"] == selected_team,
    team_games["awayTeam"],
    team_games["homeTeam"],
)
team_games["margin"] = team_games["team_score"] - team_games["opp_score"]
team_games["result"] = np.where(team_games["margin"] > 0, "Win", "Loss")
team_games["location"] = np.where(
    team_games["homeTeam"] == selected_team, "Home", "Away"
)

# ---------------------------------------------------------
# Streamlit Tabs
# ---------------------------------------------------------
tab_analytics, tab_ai = st.tabs(["📊 Past Performance", "🤖 AI Predictor"])

# =========================================================
# TAB 1: Analytics & Historical Performance
# =========================================================
with tab_analytics:
    st.header(f"Historical Performance: {selected_team}")

    # Key Metrics
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
    col4.metric(
        "Avg Scored / Allowed", f"{avg_pts:.1f} / {avg_allowed:.1f}"
    )

    st.divider()

    # Visualizations
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("Point Differential Timeline")
        fig_margin = px.bar(
            team_games,
            x=team_games.index,
            y="margin",
            color="result",
            color_discrete_map={"Win": "#2ecc71", "Loss": "#e74c3c"},
            hover_data=["opponent", "team_score", "opp_score"],
            labels={"margin": "Margin", "index": "Game #"},
            title="Margin of Victory / Defeat",
        )
        st.plotly_chart(fig_margin, use_container_width=True)

    with chart_col2:
        st.subheader("Home vs. Away Breakdown")
        loc_summary = (
            team_games.groupby(["location", "result"])
            .size()
            .reset_index(name="count")
        )
        fig_loc = px.bar(
            loc_summary,
            x="location",
            y="count",
            color="result",
            barmode="group",
            color_discrete_map={"Win": "#2ecc71", "Loss": "#e74c3c"},
            title="Performance by Location",
        )
        st.plotly_chart(fig_loc, use_container_width=True)

    # Raw Data Table
    st.subheader("Game Log")
    st.dataframe(team_games, use_container_width=True)

# =========================================================
# TAB 2: AI Win Predictor
# =========================================================
with tab_ai:
    st.header(f"🤖 Match Outcome Prediction for {selected_team}")
    st.caption("Input matchup variables to estimate win probability based on past trends.")

    col_input, col_results = st.columns([1, 1])

    with col_input:
        st.subheader("Game Setup")
        opp_name = st.selectbox("Opponent", [t for t in teams if t != selected_team])
        game_loc = st.radio("Game Location", ["Home", "Away"], horizontal=True)
        is_conference = st.checkbox("Conference Game", value=True)
        rest_days = st.slider("Rest Days Prior to Game", 0, 14, 7)

    with col_results:
        st.subheader("Prediction Result")
        
        if st.button("Run AI Prediction Model", type="primary"):
            # Mock / Simple Baseline AI Logic (Replace with trained model inference)
            base_prob = win_rate / 100 if total_games > 0 else 0.50
            location_bonus = 0.08 if game_loc == "Home" else -0.05
            rest_bonus = 0.03 if rest_days > 7 else 0.0

            predicted_prob = min(max(base_prob + location_bonus + rest_bonus, 0.05), 0.95)
            predicted_win = predicted_prob >= 0.50

            # Output display
            if predicted_win:
                st.success(f"**Predicted Result:** WIN ({predicted_prob * 100:.1f}% Probability)")
            else:
                st.error(f"**Predicted Result:** LOSS ({(1 - predicted_prob) * 100:.1f}% Probability)")

            st.progress(predicted_prob)

            # Key Factors
            st.markdown("### 🔍 Model Insights")
            st.write(f"- **Historical Base Win Rate:** `{win_rate:.1f}%`")
            st.write(f"- **Location Impact:** `{game_loc}` ({'+8%' if game_loc == 'Home' else '-5%'})")
            st.write(f"- **Rest Advantage:** `{rest_days} days` ({'+3%' if rest_days > 7 else '0%'})")
