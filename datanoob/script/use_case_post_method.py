import requests
from requests.structures import CaseInsensitiveDict
import json

url = "http://localhost:80/predict"

headers = CaseInsensitiveDict()
# headers["Accept"] = "application/json"
headers["Content-Type"] = "application/json"

data = {
    "CHAS": 0,
    "DIS": 5.2146,
    "RAD": 4,
    "TAX": 430.0,
    "B": 382.44,
    "INDUS": 3.24,
    "LSTAT": 9.97,
    "PTRATIO": 16.9,
    "RM": 5.868,
    "ZN":0.0,
    "NOX": 0.460
}

resp = requests.post(url, headers=headers, data=json.dumps(data))

print("text", json.loads(resp.text))
print("json", resp.json)
print("status", resp.status_code)