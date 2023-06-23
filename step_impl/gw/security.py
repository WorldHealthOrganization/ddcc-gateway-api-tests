from step_impl.gw.gateway_util import failed_response
from getgauge.python import step, data_store
from step_impl.util.testdata import get_country_cert_files
from cryptography.hazmat.primitives import serialization, hashes
from cryptography import x509
from os import environ
import requests

@step("extract subject and fingerprint from <certtype> certificate of <country>")
def extract_subject_and_fingerprint_from_certificate_of(certtype, country):
    cert_file, key_file = get_country_cert_files(country, certtype )
    cert = x509.load_pem_x509_certificate(open(cert_file, "rb").read())
    
    data_store.scenario['extracted.fingerprint'] = cert.fingerprint(hashes.SHA256()).hex() 
    data_store.scenario['extracted.subject'] = cert.subject.rfc4514_string()
    #print(data_store.scenario['extracted.subject'])
    
    

@step("<country> uses its <certtype> cert with fake headers for access")
def downloads_the_certificate_trust_list_with_fake_headers(country, certtype):
    try:
        data_store.scenario["response"] = requests.get(
            url=data_store.scenario["gateway.url"] + '/trustList/certificate',
            cert=get_country_cert_files(country, certtype),
            verify=bool(environ.get('verify_https')),
            params=data_store.scenario["search.filter"],
            headers={
               'X-SSL-Client-SHA256': data_store.scenario['extracted.fingerprint'],
               'X-SSL-Client-DN' : data_store.scenario['extracted.subject']
            }

        )
        #print(data_store.scenario["response"].text[:100])
    except IOError as error:
        failed_response(error)