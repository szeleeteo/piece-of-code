import requests
import streamlit as st

DATA_GOV_SG_API_KEY = "https://api.data.gov.sg"
TOKEN = st.secrets["DATA_GOV_SG_API_KEY"]

url = f"{DATA_GOV_SG_API_KEY}/v1/environment/24-hour-weather-forecast"
headers = {"X-Api-Key": TOKEN}
response = requests.get(url, headers=headers)

print(response.json())
