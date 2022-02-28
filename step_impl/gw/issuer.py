from os import environ

import requests
from getgauge.python import step, data_store

from step_impl.gw.gateway_util import failed_response
from step_impl.util import testdata, verify
from step_impl.util.testdata import get_country_cert_files


@step("<country> downloads the trusted issuer trustlist")
def downloads_the_trusted_issuer_trustlist(country):
    try:
        data_store.scenario["response"] = requests.get(
            url=environ.get('first_gateway_url') + '/trustList/issuers',
            cert=get_country_cert_files(country, 'auth'),
            verify=verify
        )
    except IOError as err:
        failed_response(err)


@step("<country> downloads the federated issuer trustlist")
def downloads_the_federated_issuer_trustlist(country):
    data_store.scenario["response"] = requests.get(
        url=testdata.get_country_gateway_url(country) + '/trustList/issuers',
        cert=get_country_cert_files(country, 'auth'),
        verify=verify,
        params={"withFederation": True}
    )

    try:
        data_store.scenario["downloaded.trustlist.issuers"] = data_store.scenario["response"].json()
    except:
        pass  # Fail silently because checks are performed in different functions and are expected for negative tests


@step("check that the trusted issuer is in the trustlist")
def check_that_the_trusted_issuer_is_in_the_trustlist():
    assert is_trusted_issuer_in_trustlist(), f"{data_store.scenario['issuer.url']} should have been trustlist"


@step("check that the trusted issuer is NOT in the trustlist")
def check_that_the_trusted_issuer_is_not_in_the_trustlist():
    assert not is_trusted_issuer_in_trustlist(), f"{data_store.scenario['issuer.url']} shouldn't have been trustlist"


def is_trusted_issuer_in_trustlist():
    for issuer in data_store.scenario['response'].json():
        if data_store.scenario['trustlist.issuer'] == issuer['url']:
            return True
    return False


@step("Other gateway downloads the trusted issuer trustlist")
def other_gateway_downloads_the_trusted_issuer_trustlist():
    assert False, "Add implementation code"  # TODO: simulate other gateway
