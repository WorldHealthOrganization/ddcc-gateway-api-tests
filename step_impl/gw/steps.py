import base64
import json
from os import environ, path

import requests
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from getgauge.python import step, data_store

from step_impl.util import testdata, certificateFolder, verify
from step_impl.util.certificates import create_cms, create_dsc, create_certificate
from step_impl.util.testdata import get_country_cert_files, get_gateway_url_by_name


# TODO: trust/reference/uuid?
# TODO: trust/issuers/country?


def _generic_cms_for_country(data, country):
    """
        Internal:
         - get country's UPLOAD cert
         - return signed CMS
    """
    cert_file, key_file = get_country_cert_files(country, 'upload')
    upload_cert = x509.load_pem_x509_certificate(open(cert_file, "rb").read())
    upload_key = serialization.load_pem_private_key(open(key_file, "rb").read(), None)
    return create_cms(data=data, upload_cert=upload_cert, upload_key=upload_key)


@step("<country> creates CMS message with trusted issuer")
def creates_cms_message_with_trusted_issuer_certificate(country):
    data = json.dumps(data_store.scenario['trusted.issuer.raw']).encode('utf-8')
    data_store.scenario['trusted.issuer.cms'] = _generic_cms_for_country(data, country)


@step("<country> creates CMS message with trusted reference")
def creates_cms_message_with_reference(country):
    data = json.dumps(data_store.scenario['trusted.reference.raw']).encode('utf-8')
    data_store.scenario['trusted.reference.cms'] = _generic_cms_for_country(data, country)


@step("<country> creates CMS message with certificate")
def creates_cms_message_with_certificate(country):
    data = data_store.scenario['trusted.certificate.raw']
    data_store.scenario['trusted.certificate.signed_b64'] = sign(data, country).decode('utf-8')
    payload = json.dumps({
        "certificate": data_store.scenario['trusted.certificate.signed_b64'],
        "properties": {}
    })
    data_store.scenario['trusted.certificate.cms'] = payload


@step("<country> creates a certificate")
def creates_a_certificate(country):
    cert_file, key_file = get_country_cert_files(country, 'csca')
    csca_cert = x509.load_pem_x509_certificate(open(cert_file, "rb").read())
    csca_key = serialization.load_pem_private_key(open(key_file, "rb").read(), None)
    created_cert, created_key = create_certificate(csca_cert, csca_key)
    data_store.scenario['trusted.certificate.raw'] = created_cert.public_bytes(serialization.Encoding.DER)


@step("<country> downloads the federated certificate trustlist")
def downloads_the_federated_certificate_trustlist(country):
    data_store.scenario['response'] = requests.get(
        # TODO:
        url=environ.get('first_gateway_url') + '/federation/trustlist/certificates',
        cert=get_country_cert_files(country, 'auth'),
        verify=verify
    )

    try:
        data_store.scenario["downloaded.trustlist.certificates"] = data_store.scenario["response"].json()
    except:
        pass  # Fail silently because checks are performed in different functions and are expected for negative tests


@step("<country> downloads the federated issuer trustlist")
def downloads_the_federated_issuer_trustlist(country):
    data_store.scenario["response"] = requests.get(
        url=environ.get('first_gateway_url') + '/federation/trustlist/issuers',
        cert=get_country_cert_files(country, 'auth'),
        verify=verify
    )

    try:
        data_store.scenario["downloaded.trustlist.issuers"] = data_store.scenario["response"].json()
    except:
        pass  # Fail silently because checks are performed in different functions and are expected for negative tests


@step("<country> downloads federated signatures")
def downloads_federated_signatures(country):
    data_store.scenario["response"] = requests.get(
        url=environ.get('first_gateway_url') + '/federation/trustlist/signatures',
        cert=get_country_cert_files(country, 'auth'),
        verify=verify
    )

    try:
        data_store.scenario["downloaded.trustlist.signatures"] = data_store.scenario["response"].json()
    except:
        pass  # Fail silently because checks are performed in different functions and are expected for negative tests


@step("<country> downloads the federated gateway list on <gateway>")
def downloads_the_federated_gateway_list_on(country, gateway):
    gateway_url = testdata.get_gateway_url_by_name(gateway)
    data_store.scenario["response"] = requests.get(
        url=gateway_url + '/federation/gateways',
        cert=get_country_cert_files(country, 'auth'),
        verify=verify
    )


@step("check that <gateway> is in the gateway list")
def check_that_is_in_the_gateway_list(gateway):
    """TODO: Check structure of response"""
    assert get_gateway_url_by_name(gateway) in data_store.scenario[
        "response"].text, f'Gateway "{gateway}" is not in the response'


@step("<country> downloads the federated federator list on <gateway>")
def downloads_the_federated_federator_list_on(country, gateway):
    gateway_url = testdata.get_gateway_url_by_name(gateway)
    data_store.scenario["response"] = requests.get(
        url=gateway_url + '/federation/federators',
        cert=get_country_cert_files(country, 'auth'),
        verify=verify
    )


@step("check that <gateway> is in the federator list")
def check_that_is_in_the_federator_list(gateway):
    """TODO: Check structure of response"""
    assert get_gateway_url_by_name(gateway) in data_store.scenario[
        "response"].text, f'Gateway "{gateway}" is not in the response'


@step("<country> downloads the federation metadata on <gateway>")
def downloads_the_federation_metadata_on(country, gateway):
    gateway_url = testdata.get_gateway_url_by_name(gateway)
    data_store.scenario["response"] = requests.get(
        url=gateway_url + '/federation/metadata',
        cert=get_country_cert_files(country, 'auth'),
        verify=verify
    )


@step("check that meta data structure is OK")
def check_that_meta_data_structure_is_ok():
    """TODO: Meta data structure not finalized yet"""

    metadata = json.load(data_store.scenario["response"].text)


@step("<country> downloads the federated reference trustlist")
def downloads_the_federated_reference_trustlist(country):
    data_store.scenario["response"] = requests.get(
        url=environ.get('first_gateway_url') + '/federation/trustlist/references',
        cert=get_country_cert_files(country, 'auth'),
        verify=verify
    )

    try:
        data_store.scenario["downloaded.trustlist.references"] = data_store.scenario["response"].json()
    except:
        pass  # Fail silently because checks are performed in different functions and are expected for negative tests


def _generic_upload_of_data_by_country(url, data, country, delete=False, b64=True, content_type='application/cms'):
    headers = {"Content-Type": content_type}
    if b64:
        headers["Content-Transfer-Encoding"] = "base64"

    certs = get_country_cert_files(country, 'auth')
    if not delete:
        return requests.post(url=url, data=data, headers=headers, cert=certs, verify=verify)
    else:
        return requests.delete(url=url, data=data, headers=headers, cert=certs, verify=verify)


@step("<country> uploads CMS with certificate")
def uploads_cms_certificate(country):
    data = data_store.scenario['trusted.certificate.cms']
    url = get_gateway_url_by_name('firstGateway') + '/trustedCertificate'
    response = _generic_upload_of_data_by_country(url, data, country, b64=False, content_type='application/json')
    data_store.scenario["response"] = response
    if response.ok:
        data_store.scenario['trusted.certificate.last_uploader'] = country


@step("<country> downloads the certificate trustlist")
def downloads_the_certificate_trustlist(country):
    data_store.scenario["response"] = requests.get(
        url=environ.get('first_gateway_url') + '/trustedCertificate',
        cert=get_country_cert_files(country, 'auth'),
        verify=verify
    )


@step("check that the certificate is in the trustlist")
def check_that_the_certificate_is_in_the_trustlist():
    assert is_certificate_in_trustlist()


@step("check that the certificate is NOT in the trustlist")
def check_that_the_certificate_is_not_in_the_trustlist():
    assert not is_certificate_in_trustlist()


def is_certificate_in_trustlist():
    cert = data_store.scenario['trusted.certificate.signed_b64']
    r = data_store.scenario['response']
    assert r.ok, f"Trustlist should be ok, but was {r.status_code}, {r.text}"
    trustlist = data_store.scenario['response'].json()
    return filter(lambda tlist: tlist['certificate'] == cert, trustlist)


@step("Other gateway downloads the certificate trustlist")
def other_gateway_downloads_the_certificate_trustlist():
    assert False, "Add implementation code"


@step("<country> deletes uploaded certificate")
def deletes_uploaded_certificate(country):
    data = data_store.scenario['trusted.certificate.signed_b64']
    url = get_gateway_url_by_name('firstGateway') + '/trustedCertificate'
    response = _generic_upload_of_data_by_country(url, data, country, delete=True)
    data_store.scenario["response"] = response


@step("<country> deletes uploaded certificate with alternate endpoint")
def deletes_uploaded_certificate_with_alternate_endpoint(country):
    data = data_store.scenario['trusted.certificate.signed_b64']
    url = get_gateway_url_by_name('firstGateway') + '/trustedCertificate/delete'
    response = _generic_upload_of_data_by_country(url, data, country)
    data_store.scenario["response"] = response


@step("delete uploaded certificate")
def delete_uploaded_certificate():
    country = data_store.scenario['trusted.certificate.last_uploader']
    data = data_store.scenario['trusted.certificate.signed_b64']
    url = get_gateway_url_by_name('firstGateway') + '/trustedCertificate'
    response = _generic_upload_of_data_by_country(url, data, country, delete=True)
    data_store.scenario["response"] = response


@step("<country> uploads CMS with trusted issuer")
def uploads_cms_trusted_issuer_certificate(country):
    # TODO: # TODO: trust/issuers has no post endpoint
    data = data_store.scenario['trusted.issuer.cms']
    url = get_gateway_url_by_name('firstGateway') + '/trust/issuers'
    response = _generic_upload_of_data_by_country(url, data, country)
    data_store.scenario["response"] = response
    if response.ok:
        data_store.scenario['trusted.issuer.last_uploader'] = country


@step("<country> downloads the trusted issuer trustlist")
def downloads_the_trusted_issuer_trustlist(country):
    data_store.scenario["response"] = requests.get(
        url=environ.get('first_gateway_url') + '/trust/issuers',
        cert=get_country_cert_files(country, 'auth'),
        verify=verify
    )


@step("check that the trusted issuer is in the trustlist")
def check_that_the_trusted_issuer_is_in_the_trustlist():
    assert False, "Add implementation code"


@step("Other gateway downloads the trusted issuer trustlist")
def other_gateway_downloads_the_trusted_issuer_trustlist():
    assert False, "Add implementation code"


@step("<country> deletes uploaded trusted issuer entry")
def deletes_uploaded_trusted_issuer_certificate(country):
    # TODO: trust/issuers has no delete endpoint
    data = data_store.scenario['trusted.issuer.cms']
    url = get_gateway_url_by_name('firstGateway') + '/trust/issuers'
    response = _generic_upload_of_data_by_country(url, data, country, delete=True)
    data_store.scenario["response"] = response


@step("check that the trusted issuer is NOT in the trustlist")
def check_that_the_trusted_issuer_is_not_in_the_trustlist():
    assert False, "Add implementation code"


@step("<country> deletes uploaded trusted issuer entry with alternate endpoint")
def deletes_uploaded_trusted_issuer_certificate_with_alternate_endpoint(country):
    # TODO: trust/issuers has no delete endpoint
    data = data_store.scenario['trusted.issuer.cms']
    url = get_gateway_url_by_name('firstGateway') + '/trust/issuers/delete'
    response = _generic_upload_of_data_by_country(url, data, country)
    data_store.scenario["response"] = response


@step("delete uploaded trusted issuer entry")
def delete_uploaded_trusted_issuer_certificate():
    # TODO: trust/issuers has no delete endpoint
    country = data_store.scenario['trusted.issuer.last_uploader']
    data = data_store.scenario['trusted.issuer.cms']
    url = get_gateway_url_by_name('firstGateway') + '/trust/issuers'
    response = _generic_upload_of_data_by_country(url, data, country, delete=True)
    data_store.scenario["response"] = response


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
    data_store.scenario["response"] = requests.get(
        url=environ.get('first_gateway_url') + '/trust/reference',
        cert=get_country_cert_files(country, 'auth'),
        verify=verify
    )


@step("check that the reference is in the trustlist")
def check_that_the_reference_is_in_the_trustlist():
    assert is_reference_in_trustlist(), 'Reference should have been in the trustlist'


@step("check that the reference is not in the trustlist")
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


@step("Other gateway downloads the reference trustlist")
def other_gateway_downloads_the_reference_trustlist():
    assert False, "Add implementation code"


@step("<country> deletes uploaded reference")
def deletes_uploaded_reference(country):
    data = data_store.scenario['trusted.reference.cms']
    url = get_gateway_url_by_name('firstGateway') + '/trust/reference'
    response = _generic_upload_of_data_by_country(url, data, country, delete=True)
    data_store.scenario["response"] = response


@step("check that the reference is NOT in the trustlist")
def check_that_the_reference_is_not_in_the_trustlist():
    assert False, "Add implementation code"


@step("<country> deletes uploaded reference with alternate endpoint")
def deletes_uploaded_reference_with_alternate_endpoint(country):
    # TODO: trust/reference has no alternate endpoint
    data = data_store.scenario['trusted.reference.cms']
    url = get_gateway_url_by_name('firstGateway') + '/trust/reference/delete'
    response = _generic_upload_of_data_by_country(url, data, country)
    data_store.scenario["response"] = response


@step("delete uploaded reference")
def delete_uploaded_reference():
    country = data_store.scenario['trusted.reference.last_uploader']
    body = json.dumps({'uuid': data_store.scenario["trusted.reference.uuid"]})
    url = get_gateway_url_by_name('firstGateway') + '/trust/reference'
    response = _generic_upload_of_data_by_country(url, body, country, delete=True)
    data_store.scenario["response"] = response


def sign(payload, country):
    cert_file, key_file = get_country_cert_files(country, 'upload')
    upload_cert = x509.load_pem_x509_certificate(open(cert_file, "rb").read())
    upload_key = serialization.load_pem_private_key(open(key_file, "rb").read(), None)
    return create_cms(payload, upload_cert, upload_key)
