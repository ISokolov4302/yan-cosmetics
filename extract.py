import requests
import json
import re

url = "https://yankonstantinovich.taplink.ws/m/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
html = response.text

# Extract window.data
match = re.search(r'window\.data\s*=\s*(\{.*?\});', html, re.DOTALL)
if match:
    data_str = match.group(1)
    try:
        data = json.loads(data_str)
        with open("taplink_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("Data extracted successfully.")
    except Exception as e:
        print("Error parsing JSON:", e)
else:
    print("Could not find window.data")
