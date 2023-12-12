from datetime import datetime, timedelta
from os import getcwd, path

from cryptography import x509
from cryptography.x509.oid import NameOID
from behave import *
from steps.util.certificates import get_own_country_name
from countries import Country

@step("create a valid {ruletype} Rule for country {country_code}")
def create_a_valid_rule(context, ruletype, country_code):
    country = Country(context, country_code)
    if ruletype.lower() == "invalidation":
        ValidFrom = datetime.now() + timedelta(seconds=10)
    else:
        ValidFrom = datetime.now() + timedelta(days=2, seconds=10)
    ValidTo = ValidFrom + timedelta(days=5)
    RuleID = "GR" if ruletype.lower()=="acceptance" else "IR"
    # rule mostly from examole in specification
    rule = {
        "Identifier": f"{RuleID}-{country.alpha_2}-1001", # very high serial number (1001) 
                                                          # to ensure that ID is unused
        "Type": ruletype,
        "Country": country.alpha_2,
        "Version": "1.0.0",
        "SchemaVersion": "1.0.0",
        "Engine": "CERTLOGIC",
        "EngineVersion": "2.0.1",
        "CertificateType": "General",
        "Description": [{"lang": "en", "desc": "api-test-rule for use in api test"}],
        "ValidFrom": ValidFrom,
        "ValidTo": ValidTo,
        "AffectedFields": ["dt", "nm"],
        "Logic": {
            "and": [
                {">=": [{"var": "dt"}, "23.12.2012"]},
                {">=": [{"var": "nm"}, "ABC"]}
            ]
        }
    }
    context.rule = rule
