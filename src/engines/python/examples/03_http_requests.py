import requests

DATA_GOV_SG_API_KEY = "https://api.data.gov.sg"

url = f"{DATA_GOV_SG_API_KEY}/v1/environment/24-hour-weather-forecast"
response = requests.get(url)

print(response.json())
