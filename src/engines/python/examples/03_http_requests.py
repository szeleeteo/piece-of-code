import requests

url = "https://api-open.data.gov.sg/v2/real-time/api/two-hr-forecast"
response = requests.get(url)

print(response.json())
