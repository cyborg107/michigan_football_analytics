import streamlit as st
import pandas as pd

st.title("Daniel's Michigan Football Analytics")

df = pd.read_csv("data/michigan_games.csv")

st.write(df.head())
