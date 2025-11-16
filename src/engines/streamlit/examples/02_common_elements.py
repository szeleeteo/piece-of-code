import numpy as np
import pandas as pd
import streamlit as st

np.random.seed(42)

users = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Heidi"]
selected_users = st.multiselect("Select Users", users, default=users[:2])

left_col, right_col = st.columns(2)

with left_col:
    n = st.slider("Set number of data points", 1, 100, 25)
with right_col:
    chart_type = st.radio(
        "Select Chart Type", ["Line", "Bar", "Scatter", "Area"], horizontal=True
    )

random_df = pd.DataFrame(
    np.random.randn(n, len(selected_users)), columns=selected_users
)

tab1, tab2 = st.tabs(["Chart", "Dataframe"])
if chart_type == "Bar":
    tab1.bar_chart(random_df, height=250)
elif chart_type == "Line":
    rolling_average = st.checkbox("Rolling average")
    if rolling_average:
        random_df = random_df.rolling(7).mean().dropna()
    tab1.line_chart(random_df, height=250)
elif chart_type == "Area":
    rolling_average = st.checkbox("Rolling average")
    if rolling_average:
        random_df = random_df.rolling(7).mean().dropna()
    tab1.area_chart(random_df, height=250)
else:
    tab1.scatter_chart(random_df, height=250)

tab2.dataframe(random_df, height=250, width="stretch")
