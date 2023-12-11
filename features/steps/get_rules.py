from os import path

import requests
from cryptography import x509
from cryptography.x509.oid import NameOID
from behave import *
from requests import Response
from datetime import datetime
from requests.exceptions import SSLError
from steps.util import FailedResponse, certificates
from countries import Country
from steps.util.certificates import get_own_country_name
from steps.util.rules import (download_rule_of_country,
                                  get_rules_from_rulelist)

@step("check that country {country_code} {is_or_not} in onboared countries list")
def step_impl(context, country_code, is_or_not):
    country = Country(context, country_code)
    response: requests.Response = context.response
    countries = response.json()
    if is_or_not.lower() == 'is':
        assert country.alpha_2 in countries, f"country: {country.alpha_2} not in country list: {', '.join(countries)}"
    elif is_or_not.lower() == 'is not':
        assert country.alpha_2 not in countries, f"country: {country.alpha_2} not in country list: {', '.join(countries)}"
    else:
        raise ValueError('Must be "is" or "is not"')

@step("download rules of all countries with country {country_code}")
def step_impl(context, country_code):
    country = Country(context, country_code)
    response: requests.Response = context.response
    try:
        response.raise_for_status()
        countries = response.json()
    except requests.exceptions.HTTPError:
        context.response = response
        return
    cert_location = path.join('certificates', country.alpha_3, 'DCC', 'TLS.pem')
    key_location = path.join('certificates', country.alpha_3, 'DCC', 'TLS.key')
    responses = [download_rule_of_country(_country, cert_location, key_location) for _country in countries]
    context.response = responses[0]


@step("get acceptance Rule from Rule list of own country")
def step_impl(context):
    countryName = get_own_country_name()
    cert_location = path.join("certificates", "XXC", "DCC", "TLS.pem")
    key_location = path.join("certificates", "XXC", "DCC", "TLS.key")
    response = download_rule_of_country(
        countryName, cert_location, key_location)
    assert response.ok, f"response had an error. Status code {response.status_code}"
    rules = get_rules_from_rulelist(response.json())
    rule = [rule for rule in rules if rule["Type"] == "Acceptance"][0]
    context.rule = rule


@step("get Rules of own Country")
def step_impl(context):
    countryName = get_own_country_name()
    cert_location = path.join("certificates", "XXC", "DCC", "TLS.pem")
    key_location = path.join("certificates", "XXC", "DCC", "TLS.key")
    response = download_rule_of_country(
        countryName, cert_location, key_location)
    context.response = response
    if response.ok:
        ruleList = response.json()
        rules = get_rules_from_rulelist(ruleList)
        context.rule = rules