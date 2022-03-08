import base64
import json
from os import environ

import requests
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from getgauge.python import step, data_store

from step_impl.gw.gateway_util import _generic_upload_of_data_by_country, sign, failed_response
from step_impl.util import testdata, verify
from step_impl.util.certificates import create_certificate
from step_impl.util.testdata import get_country_cert_files

if not verify: 
    import urllib3
    urllib3.disable_warnings()



@step("<country> creates a certificate with expiry <days> days")
def creates_a_certificate_with_expiry_days(country, days):
    cert_file, key_file = get_country_cert_files(country, 'csca')
    csca_cert = x509.load_pem_x509_certificate(open(cert_file, "rb").read())
    csca_key = serialization.load_pem_private_key(open(key_file, "rb").read(), None)
    created_cert, created_key = create_certificate(csca_cert, csca_key, valid_seconds=24*60*60*int(days))
    data_store.scenario['trusted.certificate.raw'] = created_cert.public_bytes(serialization.Encoding.DER)

@step("<country> creates a certificate")
def creates_a_certificate(country):
    cert_file, key_file = get_country_cert_files(country, 'csca')
    csca_cert = x509.load_pem_x509_certificate(open(cert_file, "rb").read())
    csca_key = serialization.load_pem_private_key(open(key_file, "rb").read(), None)
    created_cert, created_key = create_certificate(csca_cert, csca_key)
    data_store.scenario['trusted.certificate.raw'] = created_cert.public_bytes(serialization.Encoding.DER)


@step("<country> creates a certificate with wrong CSCA")
def creates_a_certificate(country):
    cert_file, key_file = get_country_cert_files('wrong', 'csca')
    csca_cert = x509.load_pem_x509_certificate(open(cert_file, "rb").read())
    csca_key = serialization.load_pem_private_key(open(key_file, "rb").read(), None)
    created_cert, created_key = create_certificate(csca_cert, csca_key, common_name='SignedWrongCsca')
    data_store.scenario['trusted.certificate.raw'] = created_cert.public_bytes(serialization.Encoding.DER)



@step("<country> creates CMS message with certificate")
def creates_cms_message_with_certificate(country):
    data = data_store.scenario['trusted.certificate.raw']
    data_store.scenario['trusted.certificate.signed_b64'] = sign(data, country).decode('utf-8')
    payload = json.dumps({
        "cms": data_store.scenario['trusted.certificate.signed_b64'],
        "properties": {}
    })
    data_store.scenario['trusted.certificate.cms'] = payload


@step("<country> uploads CMS with certificate")
def uploads_cms_certificate(country):
    data = data_store.scenario['trusted.certificate.cms']
    url = data_store.scenario["gateway.url"] + '/trustedCertificate'
    response = _generic_upload_of_data_by_country(url, data, country, b64=False, content_type='application/json')
    data_store.scenario["response"] = response
    #print(f"{response.status_code}, {response.text}")
    if response.ok:
        data_store.scenario['trusted.certificate.last_uploader'] = country


@step("<country> downloads the certificate trustlist")
def downloads_the_certificate_trustlist(country):
    try:
        data_store.scenario["response"] = requests.get(
            url=data_store.scenario["gateway.url"] + '/trustList/certificate',
            cert=get_country_cert_files(country, 'auth'),
            verify=verify
        )
    except IOError as error:
        failed_response(error)


@step("<country> downloads the federated certificate trustlist")
def downloads_the_federated_certificate_trustlist(country):
    data_store.scenario['response'] = requests.get(
        url=data_store.scenario["gateway.url"] + '/trustList/certificate',
        cert=get_country_cert_files(country, 'auth'),
        verify=verify,
        params={"withFederation": True}
    )

    try:
        data_store.scenario["downloaded.trustlist.certificates"] = data_store.scenario["response"].json()
    except:
        pass  # Fail silently because checks are performed in different functions and are expected for negative tests


@step("check that the certificate is in the trustlist")
def check_that_the_certificate_is_in_the_trustlist():
    assert is_certificate_in_trustlist(), "Certificate should have been in trustlist"


@step("check that the certificate is NOT in the trustlist")
def check_that_the_certificate_is_not_in_the_trustlist():
    assert not is_certificate_in_trustlist(), "Certificate shouldn't have been in trustlist"


def is_certificate_in_trustlist():
    cert = base64.b64encode(data_store.scenario['trusted.certificate.raw']).decode('utf-8')
    r = data_store.scenario['response']
    assert r.ok, f"Trustlist should be ok, but was {r.status_code}, {r.text}"
    trustlist = data_store.scenario['response'].json()
    return any(certificate['certificate'] == cert for certificate in trustlist)


@step("<country> deletes uploaded certificate")
def deletes_uploaded_certificate(country):
    data = data_store.scenario['trusted.certificate.signed_b64']
    url = data_store.scenario["gateway.url"] + '/trustedCertificate'
    response = _generic_upload_of_data_by_country(url, data, country, delete=True)
    data_store.scenario["response"] = response
    if response.ok:
        data_store.scenario.pop('trusted.certificate.last_uploader', None)


@step("<country> deletes uploaded certificate with alternate endpoint")
def deletes_uploaded_certificate_with_alternate_endpoint(country):
    data = data_store.scenario['trusted.certificate.signed_b64']
    url = data_store.scenario["gateway.url"] + '/trustedCertificate/delete'
    response = _generic_upload_of_data_by_country(url, data, country)
    data_store.scenario["response"] = response
    if response.ok:
        data_store.scenario.pop('trusted.certificate.last_uploader', None)


@step("delete uploaded certificate")
def delete_uploaded_certificate():
    if 'trusted.certificate.last_uploader' not in data_store.scenario:
        print(' (S)', end='') # No certificate has been uploaded successfully, skipping deletion
        return
    country = data_store.scenario['trusted.certificate.last_uploader']
    deletes_uploaded_certificate(country)
