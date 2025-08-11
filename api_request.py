import requests

url = "https://api.gleif.org/api/v1/lei-records/529900W18LQJJN6SJ336"
headers = {
    "Accept": "application/vnd.api+json"
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)

    data = response.json()  # Captures JSON output
    print(data)

except requests.exceptions.ProxyError as e:
    print(f"Proxy error: {e} — Possible tunnel connection failure.")
except requests.exceptions.ConnectionError as e:
    print(f"Connection error: {e}")
except requests.exceptions.Timeout as e:
    print(f"Request timed out: {e}")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
