import requests
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from getgauge.python import step, data_store, before_scenario

from step_impl.util import verify
from step_impl.util.certificates import create_cms
from step_impl.util.testdata import get_country_cert_files
import os


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

@before_scenario
def select_first_gateway():
    return select_gateway('first_gateway')

@step("select gateway <gateway_name>")
def select_gateway(gateway_name): 
    gw_name = str(gateway_name).lower().replace(' ','').replace('_','')
    gw_var_name = {
        '1' : 'first_gateway',
        '1st' : 'first_gateway',
        'first' : 'first_gateway',
        'firstgateway' : 'first_gateway_url',
        '2' : 'second_gateway_url',
        '2nd' : 'second_gateway',
        'second' : 'second_gateway_url',
        'secondgateway' : 'second_gateway_url',
        '3' : 'third_gateway',
        '3rd' : 'third_gateway',
        'third' : 'third_gateway',
        'thirdgateway' : 'third_gateway_url',
    }.get(gw_name)

    assert gw_var_name is not None, f'Unknown gateway: {gateway_name}'

    data_store.scenario["gateway.url"] = os.environ.get(gw_var_name)
    assert  data_store.scenario["gateway.url"] is not None, f'Variable not set: {gw_var_name}' 
    return data_store.scenario["gateway.url"]


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
