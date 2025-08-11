import requests

url = "https://api.gleif.org/api/v1/lei-records/529900W18LQJJN6SJ336"
headers = {
    "Accept": "application/vnd.api+json"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()  # Captures JSON output
    print(data)
else:
    print(f"Request failed: {response.status_code}")
