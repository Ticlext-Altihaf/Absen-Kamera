import requests

host = "http://localhost:8080"

assert requests.get(host).text == "Alive"


