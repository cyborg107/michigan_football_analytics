import streamlit as st
import pandas as pd

st.title("Michigan Football Analytics")

df = pd.read_csv("data/michigan_games.csv")

st.write(df.head())
