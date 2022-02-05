import requests

BASE = "http://127.0.0.1:5000/"

response = requests.patch(BASE + "playerstats/2", {"hr":99, "gp": 120})
print(response.json())