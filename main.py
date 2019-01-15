import json
import requests


# 1. Create an ``organisation`` called e.g. “Magenta” valid from 2017-01-01 (included)
# to 2025-12-31 (excluded).

SERVER = "http://192.168.50.2:5000/"
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


# 2. Make a query searching for all ``organisation`` in LoRa - confirm that Magenta
# exists in the system.

org_gr = requests.get(ORG_URL, params={"brugervendtnoegle": "%"})
assert org_u in json.loads(org_gr.text)["results"][0]


# 3. Create an ``organisationenhed`` called “Magenta” (which should be a subunit to the
# ``organisation`` Magenta) active from 2017-01-01 (included) to 2024-03-14 (excluded).
# Consider which attributes and relations to set.


# 4. Create an ``organisationenhed`` called “Copenhagen” (which should be a subunit to
# the ``organisationenhed`` Magenta) active from 2017-01-01 (included) to 2024-03-14
# (excluded). Consider which attributes and relations to set.

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


# 5. Create an ``organisationenhed`` called “Aarhus” (which should be a subunit of the
# ``organisationenhed`` Magenta) active from 2018-01-01 (included) to 2025-09-01
# (excluded). Consider which attributes and relations to set.

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

# 6. Make a query searching for all ``organisationenhed`` in LoRa - confirm that
# Copenhagen and Aarhus exist in the system.

en_gr = requests.get(EN_URL, params={"brugervendtnoegle": "%"})
assert cph_u in json.loads(en_gr.text)["results"][0]
assert aar_u in json.loads(en_gr.text)["results"][0]

# 7. Add an ``address`` to the ``organisationenhed`` Aarhus (valid within the period
# where the ``organisationenhed`` is active).

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


# 8. Fetch the ``organisationenhed`` Aarhus and verify that the newly added ``address``
# is present in the response.

aar_addr2_gr = requests.get(EN_URL + "/" + aar_u)
assert json.loads(aar_addr2_gr.text)[aar_u][0]["registreringer"][0]["relationer"][
    "adresser"
]

# 9. Add another ``address`` to the ``organisationenhed`` Aarhus (valid in a period
# exceeding the period where the ``organisationenhed`` is active). What happens in this
# case?


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


# 10. Remove all ``address`` from the ``organisationenhed`` Aarhus and confirm that
# they are gone afterwards.

aar_addr4_gr = requests.get(EN_URL + "/" + aar_u)
aar_addr4_data = json.loads(aar_addr4_gr.text)[aar_u][0]["registreringer"][0]

aar_addr4_data["relationer"].pop("adresser")

aar_addr4_r = requests.put(EN_URL + "/" + aar_u, json=aar_addr4_data)

aar_addr4_gr = requests.get(EN_URL + "/" + aar_u)
assert (
    "adresser"
    not in json.loads(aar_addr4_gr.text)[aar_u][0]["registreringer"][0]["relationer"]
)

# 11. Make a small script capable of adding ``n`` new ``organisationenhed`` (e.g. where
# 10 < ``n`` < 20) named orgEnhed1, orgEnhed2, orgEnhed3,... These ``organisationenhed``
# should all be subunits of the ``organisationenhed`` Copenhagen and they should be
# active in random intervals ranging from 2017-01-01 (included) to 2025-12-31
# (excluded).


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
                        "enhedsnavn": "orgEnhed%d" % i,
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


# 12. Find all active ``organisation`` (if any) in the period from 2017-12-01 to
# 2025-06-01.

org2_gr = requests.get(
    ORG_URL,
    params={"bvn": "%", "virkningFra": "2017-12-01", "virkningTil": "2019-06-01"},
)
print(org2_gr.url)
org2_res = json.loads(org2_gr.text)["results"][0]

# 13. What are the names of the ``organisationenhed`` from above?

for uuid in org2_res:
    org3_gr = requests.get(EN_URL, params={"overordnet": uuid})
    org3_res = json.loads(org3_gr.text)["results"][0]  # aarhus and copenhagen
    for uuid in org3_res:
        org4_gr = requests.get(EN_URL, params={"overordnet": uuid})
        org4_res = json.loads(org4_gr.text)["results"][0]  # orgEnhed%0d
        for uuid in org4_res:
            org5_gr = requests.get(EN_URL, params={"uuid": uuid})
            name = json.loads(org5_gr.text)["results"][0][0]["registreringer"][0][
                "attributter"
            ]["organisationenhedegenskaber"][0]["enhedsnavn"]
            print(name)
