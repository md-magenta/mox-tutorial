import requests
import uuid


#  1. Create an organisation called e.g. “Magenta” valid from 2017-01-01 (included) to
#  2019-12-31 (excluded).

SERVER = "http://10.0.3.113/"
ORG_URL = SERVER + "organisation/organisation/"

u = str(uuid.uuid4())

val = {
    "from": "2017-01-01",
    "from_included": True,
    "to": "2019-12-31",
    "to_included": False,
}

data = {
    "attributter": {  # required
        "organisationegenskaber": [  # required
            {
                "brugervendtnoegle": "magenta-aps",  # required
                "organisationsnavn": "Magenta ApS",
                "virkning": val,  # required
            }
        ]
    },
    "tilstande": {  # required
        "organisationgyldighed": [  # required
            {"gyldighed": "Aktiv", "virkning": val}  # required
        ]
    },
}

putr = requests.put(ORG_URL + u, json=data)
assert putr.text == '{"uuid":"%s"}\n' % u

