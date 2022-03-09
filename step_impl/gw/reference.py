import json
from os import environ,urandom

import requests
from hashlib import sha256
from getgauge.python import step, data_store

from step_impl.gw.gateway_util import _generic_upload_of_data_by_country, _generic_cms_for_country, failed_response, \
    sign
from step_impl.util import testdata, verify
from step_impl.util.testdata import get_country_cert_files

if not verify: 
    import urllib3
    urllib3.disable_warnings()



@step("<country> creates a reference")
def creates_a_reference(country):
    # using pseudo-random thumbprint as identifier to find an uploaded reference in the trust list 
    data_store.scenario["trusted.reference.thumbprint"] = sha256(urandom(16)).hexdigest()
    reference = {
        # 'uuid': str(uuid4()), TODO: if set an existing reference can be updated, Test-Cases for this?
        "version": 1,
        "url": "https://testing.only.this/does/not/exist",
        "country": testdata.get_country_code(country),
        "domain": "DCC",
        "type": "DCC",
        "service": "ValueSet",  # ValueSet, PlanDefinition, etc.
        "thumbprint": data_store.scenario["trusted.reference.thumbprint"],
        "name": "TestReference",
        "sslPublicKey": testdata.get_ssl_public_key(country),
        "contentType": 'application/json',
        "signatureType": "CMS",
        "referenceVersion": "1.3.0"
    }

    data_store.scenario["trusted.reference.raw"] = reference
    return reference

@step("modify reference set <fieldname> to <value>")
def modify_reference(fieldname, value):
    data_store.scenario["trusted.reference.raw"][fieldname] = value


@step("<country> creates CMS message with trusted reference")
def creates_cms_message_with_reference(country):
    data = json.dumps(data_store.scenario['trusted.reference.raw']).encode('utf-8')
    data_store.scenario['trusted.reference.cms'] = _generic_cms_for_country(data, country)


@step("<country> uploads CMS reference")
def uploads_cms_reference(country):
    data = data_store.scenario['trusted.reference.cms']
    url = data_store.scenario["gateway.url"] + '/trust/reference'
    response = _generic_upload_of_data_by_country(url, data, country)
    data_store.scenario["response"] = response
    if response.ok:
        data_store.scenario['trusted.reference.last_uploader'] = country


@step("<country> downloads the reference trustlist")
def downloads_the_reference_trustlist(country):
    try:
        data_store.scenario["response"] = requests.get(
            url=data_store.scenario["gateway.url"] + '/trustList/references',
            cert=get_country_cert_files(country, 'auth'),
            verify=verify,
            params=data_store.scenario["search.filter"]
        )
    except IOError as err:
        failed_response(err)


@step("check that the reference is in the trustlist")
def check_that_the_reference_is_in_the_trustlist():
    assert is_reference_in_trustlist(), 'Reference should have been in the trustlist'


@step("check that the reference is NOT in the trustlist")
def check_that_the_reference_is_not_in_the_trustlist():
    # TODO: make use of this?
    assert not is_reference_in_trustlist(), 'Reference should not have been in the trustlist'


def is_reference_in_trustlist():
    thumbprint = data_store.scenario["trusted.reference.thumbprint"]
    for reference in data_store.scenario["response"].json():
        if reference['thumbprint'] == thumbprint: # using pseudo-random thumbprint as identifier
            data_store.scenario["trusted.reference.uuid"] = reference['uuid']
            return True
    return False


@step("<country> deletes uploaded reference")
def deletes_uploaded_reference(country):
    body = json.dumps({'uuid': str(data_store.scenario["trusted.reference.uuid"])})
    print(f'\nDEBUG: Attempt deleting {body}\n')
    data = sign(bytes(body, 'utf-8'), country).decode('utf-8')
    url = data_store.scenario["gateway.url"] + '/trust/reference'
    response = _generic_upload_of_data_by_country(url, data, country, delete=True)
    data_store.scenario["response"] = response
    if response.ok:
        data_store.scenario.pop('trusted.reference.last_uploader', None)


@step("delete uploaded reference")
def delete_uploaded_reference():
    if 'trusted.reference.last_uploader' not in data_store.scenario:
        print( '(S)', end='') # skipping deletion
        return
    country = data_store.scenario['trusted.reference.last_uploader']
    deletes_uploaded_reference(country)


