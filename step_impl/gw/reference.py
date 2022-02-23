import json
from os import environ

import requests
from getgauge.python import step, data_store

from step_impl.gw.gateway_util import _generic_upload_of_data_by_country, _generic_cms_for_country, failed_response
from step_impl.util import testdata, verify
from step_impl.util.testdata import get_country_cert_files, get_gateway_url_by_name


@step("<country> creates CMS message with trusted reference")
def creates_cms_message_with_reference(country):
    data = json.dumps(data_store.scenario['trusted.reference.raw']).encode('utf-8')
    data_store.scenario['trusted.reference.cms'] = _generic_cms_for_country(data, country)


@step("<country> uploads CMS reference")
def uploads_cms_reference(country):
    data = data_store.scenario['trusted.reference.cms']
    url = get_gateway_url_by_name('firstGateway') + '/trust/reference'
    response = _generic_upload_of_data_by_country(url, data, country)
    data_store.scenario["response"] = response
    if response.ok:
        data_store.scenario['trusted.reference.last_uploader'] = country


@step("<country> downloads the reference trustlist")
def downloads_the_reference_trustlist(country):
    try:
        data_store.scenario["response"] = requests.get(
            url=environ.get('first_gateway_url') + '/trustList/references',
            cert=get_country_cert_files(country, 'auth'),
            verify=verify
        )
    except IOError as err:
        failed_response(err)


@step("<country> downloads the federated reference trustlist")
def downloads_the_federated_reference_trustlist(country):
    data_store.scenario["response"] = requests.get(
        url=testdata.get_country_gateway_url(country) + '/trustList/references',
        cert=get_country_cert_files(country, 'auth'),
        verify=verify,
        params={"withFederation": True}
    )

    try:
        data_store.scenario["downloaded.trustlist.references"] = data_store.scenario["response"].json()
    except:
        pass  # Fail silently because checks are performed in different functions and are expected for negative tests


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
        if reference['thumbprint'] == thumbprint:
            data_store.scenario["trusted.reference.uuid"] = reference['uuid']
            return True
    return False


@step("<country> deletes uploaded reference")
def deletes_uploaded_reference(country):
    body = json.dumps({'uuid': data_store.scenario["trusted.reference.uuid"]})
    url = get_gateway_url_by_name('firstGateway') + '/trust/reference'
    response = _generic_upload_of_data_by_country(url, body, country, delete=True)
    data_store.scenario["response"] = response
    if response.ok:
        data_store.scenario.pop('trusted.reference.last_uploader', None)


@step("delete uploaded reference")
def delete_uploaded_reference():
    if 'trusted.reference.last_uploader' not in data_store.scenario:
        print('No reference has been uploaded successfully, skipping deletion')
        return
    country = data_store.scenario['trusted.reference.last_uploader']
    deletes_uploaded_reference(country)


@step("Other gateway downloads the reference trustlist")
def other_gateway_downloads_the_reference_trustlist():
    assert False, "Add implementation code"  # TODO: simulate other gateway
