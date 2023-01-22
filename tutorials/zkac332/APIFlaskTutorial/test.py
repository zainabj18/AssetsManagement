import requests

BASE = "http://127.0.0.1:5000/helloworld"

response = requests.get(BASE)
print(response.json())
