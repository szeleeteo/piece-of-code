import numpy as np
import pandas as pd
import streamlit as st

st.title("Tabular Elements Example")

random_data = [
    {
        "Preview": f"https://picsum.photos/400/200?lock={i}",
        "Views": np.random.randint(0, 1000),
        "Active": np.random.choice([True, False]),
        "Category": np.random.choice(["🤖 LLM", "📊 Data", "⚙️ Tool"]),
        "Progress": np.random.randint(1, 100),
    }
    for i in range(1000)
]

random_df = pd.DataFrame(random_data)
random_df.index += 1  # Start index from 1
column_config = {
    "Preview": st.column_config.ImageColumn(),
    "Progress": st.column_config.ProgressColumn(),
}

if st.toggle("Enable editing"):
    edited_data = st.data_editor(
        data=random_df, width="stretch", height="stretch", column_config=column_config
    )
else:
    st.dataframe(
        data=random_df, width="stretch", height="stretch", column_config=column_config
    )
