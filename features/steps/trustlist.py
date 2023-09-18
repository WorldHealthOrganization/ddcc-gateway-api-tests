from behave import then
import json
import pycountry
from countries import Country


@then('only certificates of type {ctype_classic} should be in the downloaded list')
def step_impl(context, ctype_classic):
    trust_list = context.response.json()
    for cert_info in trust_list:
        assert cert_info['certificateType'] == ctype_classic, f'Found a certificate of different type than {ctype_classic}'

@then('the downloaded list should have more than {count} entries')
def step_impl(context, count):
    trust_list = context.response.json()
    assert len(trust_list) > int(count)

@then('only certificates of country {country_code} should be in the downloaded list')
def step_impl(context, country_code):
    country = Country(country_code)
    trust_list = context.response.json()
    for cert_info in trust_list:
        assert cert_info['country'] == country.alpha_2, f'Found a certificate of different country than {country.alpha_2}'

    