import json
import requests


#  1. Create an organisation called e.g. “Magenta” valid from 2017-01-01 (included) to
#  2019-12-31 (excluded).

SERVER = "http://10.0.3.113/"
ORG_URL = SERVER + "organisation/organisation"

org_val = {
    "from": "2017-01-01",  # required
    "from_included": True,
    "to": "2019-12-31",  # required
    "to_included": False,
}

org_data = {
    "attributter": {  # required
        "organisationegenskaber": [  # required
            {
                "brugervendtnoegle": "magenta-aps",  # required
                "organisationsnavn": "Magenta ApS",
                "virkning": org_val,  # requiredg
            }
        ]
    },
    "tilstande": {  # required
        "organisationgyldighed": [  # required
            {"gyldighed": "Aktiv", "virkning": org_val}  # required
        ]
    },
}

org_r = requests.post(ORG_URL, json=org_data)
org_u = json.loads(org_r.text)["uuid"]


#  2. Make a query searching for all organisations in LoRa - confirm that Magenta exists
#  in the system.

org_gr = requests.get(ORG_URL, params={"brugervendtnoegle": "%"})
assert org_u in json.loads(org_gr.text)["results"][0]


#  3. Create an organisationenhed called “Copenhagen” (which should be a subunit to
#  Magenta) active from 2017-01-01 (included) to 2018-03-14 (excluded). Consider which
#  attributes and relations to set.

EN_URL = SERVER + "organisation/organisationenhed"


cph_val = {
    "from": "2017-01-01",  # required
    "from_included": True,
    "to": "2019-03-14",  # required
    "to_included": False,
}

cph_data = {
    "attributter": {  # required
        "organisationenhedegenskaber": [  # required
            {
                "brugervendtnoegle": "copenhagen",  # required
                "enhedsnavn": "Copenhagen",
                "virkning": cph_val,  # required
            }
        ]
    },
    "tilstande": {  # required
        "organisationenhedgyldighed": [  # required
            {"gyldighed": "Aktiv", "virkning": cph_val}  # required
        ]
    },
    "relationer": {
        "overordnet": [{"uuid": org_u, "virkning": cph_val}],
        "tilhoerer": [{"uuid": org_u, "virkning": cph_val}],
    },
}

cph_r = requests.post(EN_URL, json=cph_data)
cph_u = json.loads(cph_r.text)["uuid"]


#  4. Create an organisationenhed called “Aarhus” (which should be a subunit of Magenta)
#  active from 2018-01-01 (included) to 2019-09-01 (excluded). Consider which attributes
#  and relations to set.

aar_val = {
    "from": "2018-01-01",  # required
    "from_included": True,
    "to": "2019-09-01",  # required
    "to_included": False,
}

aar_data = {
    "attributter": {  # required
        "organisationenhedegenskaber": [  # required
            {
                "brugervendtnoegle": "aarhus",  # required
                "enhedsnavn": "Aarhus",
                "virkning": aar_val,  # required
            }
        ]
    },
    "tilstande": {  # required
        "organisationenhedgyldighed": [  # required
            {"gyldighed": "Aktiv", "virkning": aar_val}  # required
        ]
    },
    "relationer": {
        "overordnet": [{"uuid": org_u, "virkning": aar_val}],
        "tilhoerer": [{"uuid": org_u, "virkning": aar_val}],
    },
}

aar_r = requests.post(EN_URL, json=aar_data)
aar_u = json.loads(aar_r.text)["uuid"]

#  5. Make a query searching for all organisationenheder in LoRa - confirm that
#  Copenhagen and Aarhus exist in the system.

en_gr = requests.get(EN_URL, params={"brugervendtnoegle": "%"})
assert cph_u in json.loads(en_gr.text)["results"][0]
assert aar_u in json.loads(en_gr.text)["results"][0]

#  6. Add an address to the org unit in Aarhus (valid within the period where the org
#  unit is active).

aar_addr_data = {
    "relationer": {
        "adresser": [
            {
                "urn": "dawa:0a3f50c4-379f-32b8-e044-0003ba298018",  # required
                "virkning": aar_val,  # required
            }
        ]
    }
}
aar_addr_r = requests.patch(EN_URL + "/" + aar_u, json=aar_addr_data)


#  7. Fetch the org unit Aarhus and verify that the newly added address is present in
#  the response.

aar_addr2_gr = requests.get(EN_URL + "/" + aar_u)
assert json.loads(aar_addr2_gr.text)[aar_u][0]["registreringer"][0]["relationer"][
    "adresser"
]

#  8. Add another address to the org unit in Aarhus (valid in a period exceeding the
#  period where the org unit is active). What happens in this case?


old_addr = json.loads(aar_addr2_gr.text)[aar_u][0]["registreringer"][0]["relationer"][
    "adresser"
]
aar_addr3_data = {
    "relationer": {
        "adresser": old_addr
        + [
            {
                "urn": "dawa:0a3f50c4-379f-32b8-e044-0003ba298019",  # required
                "virkning": {  # required
                    "from": "2018-01-01",  # required
                    "from_included": True,
                    "to": "2020-08-01",  # required
                    "to_included": False,
                },
            }
        ]
    }
}


aar_addr3_r = requests.patch(EN_URL + "/" + aar_u, json=aar_addr3_data)


#  9. Remove all addresses from the Aarhus org unit and confirm that they are gone
#  afterwards.
aar_addr4_gr = requests.get(EN_URL + "/" + aar_u)
aar_addr4_data = json.loads(aar_addr4_gr.text)[aar_u][0]["registreringer"][0]

aar_addr4_data["relationer"].pop("adresser")

aar_addr4_r = requests.put(EN_URL + "/" + aar_u, json=aar_addr4_data)

aar_addr4_gr = requests.get(EN_URL + "/" + aar_u)
assert (
    "adresser"
    not in json.loads(aar_addr4_gr.text)[aar_u][0]["registreringer"][0]["relationer"]
)

# 10. Make a small script capable of adding n new org units (e.g. where 10 < n < 20)
# named orgEnhed1, orgEnhed2, orgEnhed3,… These org units should all be subunits of the
# Copenhagen org unit and they should be active in random intervals ranging from
# 2017-01-01 (included) to 2019-12-31 (excluded).


def addUnits(n):
    for i in range(1, n + 1):
        enh_val = {
            "from": "2017-01-%02d" % i,  # required
            "from_included": True,
            "to": "2019-03-%02d" % i,  # required
            "to_included": False,
        }

        enh_data = {
            "attributter": {  # required
                "organisationenhedegenskaber": [  # required
                    {
                        "brugervendtnoegle": "orgEnhed%d" % i,  # required
                        "virkning": enh_val,  # required
                    }
                ]
            },
            "tilstande": {  # required
                "organisationenhedgyldighed": [  # required
                    {"gyldighed": "Aktiv", "virkning": enh_val}  # required
                ]
            },
            "relationer": {
                "overordnet": [{"uuid": cph_u, "virkning": enh_val}],
                "tilhoerer": [{"uuid": org_u, "virkning": enh_val}],
            },
        }

        enh_r = requests.post(EN_URL, json=enh_data)
        enh_u = json.loads(enh_r.text)["uuid"]


addUnits(15)


# 11. Find all active org (if any) in the period from 2017-12-01 to 2019-06-01.

# 12. What are the names of the org units from above?
