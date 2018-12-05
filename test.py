import json
import requests
import uuid


#  1. Create an organisation called e.g. “Magenta” valid from 2017-01-01 (included) to
#  2019-12-31 (excluded).

SERVER = "http://10.0.3.113/"
ORG_URL = SERVER + "organisation/organisation/"

org_u = str(uuid.uuid4())

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

org_r = requests.put(ORG_URL + org_u, json=org_data)
assert json.loads(org_r.text)["uuid"] == org_u


#  2. Make a query searching for all organisations in LoRa - confirm that Magenta exists
#  in the system.

#  3. Create an organisationenhed called “Copenhagen” (which should be a subunit to
#  Magenta) active from 2017-01-01 (included) to 2018-03-14 (excluded). Consider which
#  attributes and relations to set.

#  4. Create an organisationenhed called “Aarhus” (which should be a subunit of Magenta)
#  active from 2018-01-01 (included) to 2019-09-01 (excluded). Consider which attributes
#  and relations to set.

#  5. Make a query searching for all organisationenheder in LoRa - confirm that
#  Copenhagen and Aarhus exist in the system.

#  6. Add an address to the org unit in Aarhus (valid within the period where the org
#  unit is active).

#  7. Fetch the org unit Aarhus and verify that the newly added address is present in
#  the response.

#  8. Add another address to the org unit in Aarhus (valid in a period exceeding the
#  period where the org unit is active). What happens in this case?

#  9. Remove all addresses from the Aarhus org unit and confirm that they are gone
#  afterwards.

# 10. Make a small script capable of adding n new org units (e.g. where 10 < n < 20)
# named orgEnhed1, orgEnhed2, orgEnhed3,… These org units should all be subunits of the
# Copenhagen org unit and they should be active in random intervals ranging from
# 2017-01-01 (included) to 2019-12-31 (excluded).

# 11. Find all active org (if any) in the period from 2017-12-01 to 2019-06-01.

# 12. What are the names of the org units from above?
