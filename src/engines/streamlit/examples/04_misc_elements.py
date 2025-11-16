import numpy as np
import pandas as pd
import streamlit as st

st.title("Misc Elements Example")

if "counter" not in st.session_state:
    st.session_state.counter = 0


def increase_counter():
    st.session_state.counter += 1


def reset_counter():
    st.session_state.counter = 0


@st.dialog("Number and Color")
def show_meaning_of_life(number: int, color: str):
    st.write(f"Selected number: {number} and color:{color}")


left_col, right_col = st.columns(2)

with left_col:
    st.button(
        f"Increase counter: {st.session_state.counter}",
        on_click=increase_counter,
    )
    st.date_input("Pick a date")
    num = st.number_input("Pick a number", min_value=0, max_value=100, value=42)

with right_col:
    st.button("Reset counter", on_click=reset_counter)
    st.time_input("Pick a time")
    color = st.color_picker("Pick a colour", "#ae5630")

if st.button("Click to open modal dialog"):
    show_meaning_of_life(num, color)

st.text_input("Enter some text")
st.text_area("Enter a longer text")
st.file_uploader("Upload a file")

random_df = pd.DataFrame(np.random.randn(3, 3), columns=["A", "B", "C"])
st.download_button("Download data", data=random_df.to_csv(), file_name="data.csv")

audio_value = st.audio_input("Record high quality audio")
if audio_value:
    st.audio(audio_value)
