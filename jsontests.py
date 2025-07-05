import requests
import json

url = "https://pokeapi.co/api/v2/move/thunderbolt"
response = requests.get(url)
data = response.json()

# Pretty print the JSON
print(json.dumps(data, indent=2))
