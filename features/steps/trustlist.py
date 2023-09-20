from behave import then
from countries import Country
from base64 import b64encode
from cryptography.hazmat.primitives import serialization


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


@then('the created cert is found in the trust list')
def step_impl(context):
    created_cert_b64 = b64encode(context.created_cert.public_bytes(serialization.Encoding.DER))
    created_cert_b64 = str(created_cert_b64,'utf-8') 

    trust_list = context.response.json()
    for cert_info in trust_list:
        if cert_info.get('rawData') == created_cert_b64:
            return 
        
    assert False, 'Created cert not found in trust list'

@then('the created cert is NOT found in the trust list')
def step_impl(context):
    created_cert_b64 = b64encode(context.created_cert.public_bytes(serialization.Encoding.DER))
    created_cert_b64 = str(created_cert_b64,'utf-8') 

    trust_list = context.response.json()
    for cert_info in trust_list:
        if cert_info.get('rawData') == created_cert_b64:
            assert False, 'Created cert unexpectedly found in trust list'
