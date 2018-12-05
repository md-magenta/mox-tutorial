import requests
import uuid

url = "http://10.0.3.113/organisation/organisation/"
u = str(uuid.uuid4())

val = {"from" : "1999-11-01", "to" : "2018-12-04"}

data = {
    "attributter": {
        "organisationegenskaber": [{"name": "magenta-aps", "virkning": val}]
    },
    "tilstande": {"organisationgyldighed": [{"gyldighed": "Aktiv", "virkning": val}]},
}

r = requests.put(url + u, json=data)

print(r.text)
