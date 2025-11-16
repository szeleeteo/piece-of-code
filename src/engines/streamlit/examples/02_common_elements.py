from enum import StrEnum

import numpy as np
import pandas as pd
import streamlit as st

st.title("Common Elements Example")

np.random.seed(42)

users = ["Alice", "Bob", "Charlie", "David", "Eve"]


class ChartType(StrEnum):
    LINE = "Line"
    BAR = "Bar"
    SCATTER = "Scatter"
    AREA = "Area"


height = 250
n_points = 150

selected_users = st.multiselect("Select Users", users, default=users[:3])
left_col, right_col = st.columns(2)

with left_col:
    chart_type = st.radio("Select Chart Type", ChartType, horizontal=True)
    rolling_average = st.checkbox("Rolling average")
with right_col:
    random_df = pd.DataFrame(
        np.random.randn(height, len(selected_users)), columns=selected_users
    )
    if rolling_average:
        window = st.slider("Rolling window size", 1, 20, 7)
        random_df = random_df.rolling(window).mean().dropna()

chart_tab, df_tab = st.tabs(["Chart", "Dataframe"])


with chart_tab:
    if chart_type == ChartType.BAR:
        st.bar_chart(random_df, height=height)
    elif chart_type == ChartType.LINE:
        st.line_chart(random_df, height=height)
    elif chart_type == ChartType.AREA:
        st.area_chart(random_df, height=height)
    else:
        st.scatter_chart(random_df, height=height)

with df_tab:
    st.dataframe(random_df, height=height, width="stretch")
