import requests
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from getgauge.python import data_store

from step_impl.util import verify
from step_impl.util.certificates import create_cms
from step_impl.util.testdata import get_country_cert_files


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


def _generic_upload_of_data_by_country(url, data, country, delete=False, b64=True, content_type='application/cms'):
    headers = {"Content-Type": content_type}
    if b64:
        headers["Content-Transfer-Encoding"] = "base64"

    certs = get_country_cert_files(country, 'auth')
    if not delete:
        return requests.post(url=url, data=data, headers=headers, cert=certs, verify=verify)
    else:
        return requests.delete(url=url, data=data, headers=headers, cert=certs, verify=verify)


def sign(payload, country):
    cert_file, key_file = get_country_cert_files(country, 'upload')
    upload_cert = x509.load_pem_x509_certificate(open(cert_file, "rb").read())
    upload_key = serialization.load_pem_private_key(open(key_file, "rb").read(), None)
    return create_cms(payload, upload_cert, upload_key)


def failed_response(error):
    class FailedResponse:
        def __init__(self, err):
            self.ok = False
            self.status_code = 418
            self.text = f"Dummy Response for {err}"

    data_store.scenario["response"] = FailedResponse(error)
