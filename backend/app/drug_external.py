import requests

OPENFDA_LABEL = "https://api.fda.gov/drug/label.json"

def openfda_label_by_generic_name(drug_name: str):
    search = f'openfda.generic_name:"{drug_name}"'
    r = requests.get(
        OPENFDA_LABEL,
        params={"search": search, "limit": 1},
        timeout=6,
    )
    r.raise_for_status()
    return r.json()
