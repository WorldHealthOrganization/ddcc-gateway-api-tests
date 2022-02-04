

from os import environ
import json
from urllib import response
import requests
from getgauge.python import step, data_store
from step_impl.util import testdata
from step_impl.util.testdata import get_country_code, get_country_cert_files, get_gateway_url_by_name
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from step_impl.util.certificates import create_certificate, create_cms, create_dsc


def _generic_cms_for_country( data, country ):
    '''Internal:
         - get country's UPLOAD cert
         - return signed CMS'''
    cert_file, key_file = get_country_cert_files(country, 'upload')
    upload_cert = x509.load_pem_x509_certificate(open(cert_file, "rb").read())
    upload_key = serialization.load_pem_private_key(open(key_file, "rb").read(), None)        
    return create_cms( data=data, upload_cert=upload_cert, upload_key=upload_key)
    
@step("<country> creates CMS message with trusted issuer")
def creates_cms_message_with_trusted_issuer_certificate(country):
    data = json.dumps(data_store.scenario['trusted.issuer.raw']).encode('utf-8')
    data_store.scenario['trusted.issuer.cms'] = _generic_cms_for_country( data, country )

@step("<country> creates CMS message with trusted reference")
def creates_cms_message_with_reference(country):
    data = json.dumps(data_store.scenario['trusted.reference.raw']).encode('utf-8')
    data_store.scenario['trusted.reference.cms'] = _generic_cms_for_country( data, country )

@step("<country> creates CMS message with certificate") 
def creates_cms_message_with_certificate(country):
    data = data_store.scenario['trusted.certificate.raw']    
    data_store.scenario['trusted.certificate.cms'] = _generic_cms_for_country( data, country )
    

@step("<country> creates a certificate")
def creates_a_certificate(country):
    cert_file, key_file = get_country_cert_files(country, 'csca')
    csca_cert = x509.load_pem_x509_certificate(open(cert_file, "rb").read())
    csca_key = serialization.load_pem_private_key(open(key_file, "rb").read(), None)        
    data_store.scenario['trusted.certificate.raw'] = create_dsc(csca_cert, csca_key)

@step("<country> downloads the federated certificate trustlist")
def downloads_the_federated_certificate_trustlist(country):
    data_store.scenario["response"] = requests.get(
        url=environ.get('first_gateway_url')+'/federation/trustlist/certificates',
        certs=get_country_cert_files(country, 'auth')
    )

    try: 
        data_store.scenario["downloaded.trustlist.certificates"] = data_store.scenario["response"].json()
    except:
        pass # Fail silently because checks are performed in different function and are expected for negative test steps


@step("<country> downloads the federated issuer trustlist")
def downloads_the_federated_issuer_trustlist(country):
    data_store.scenario["response"] = requests.get(
        url=environ.get('first_gateway_url')+'/federation/trustlist/issuers',
        certs=get_country_cert_files(country, 'auth')
    )

    try: 
        data_store.scenario["downloaded.trustlist.issuers"] = data_store.scenario["response"].json()
    except:
        pass # Fail silently because checks are performed in different function and are expected for negative test steps

@step("<country> downloads federated signatures")
def downloads_federated_signatures(country):
    data_store.scenario["response"] = requests.get(
        url=environ.get('first_gateway_url')+'/federation/trustlist/signatures',
        certs=get_country_cert_files(country, 'auth')
    )

    try: 
        data_store.scenario["downloaded.trustlist.signatures"] = data_store.scenario["response"].json()
    except:
        pass # Fail silently because checks are performed in different function and are expected for negative test steps

@step("<country> downloads the federated gateway list on <gateway>")
def downloads_the_federated_gateway_list_on(country, gateway):
    gateway_url = testdata.get_gateway_url_by_name(gateway)
    data_store.scenario["response"] = requests.get(
        url=gateway_url+'/federation/gateways',
        certs=get_country_cert_files(country, 'auth')
    )


@step("check that <gateway> is in the gateway list")
def check_that_is_in_the_gateway_list(gateway):
    'TODO: Check structure of response'    
    assert get_gateway_url_by_name(gateway) in data_store.scenario["response"].text , f'Gateway "{gateway}" is not in the response'


@step("<country> downloads the federated federator list on <gateway>")
def downloads_the_federated_federator_list_on(country, gateway):
    gateway_url = testdata.get_gateway_url_by_name(gateway)
    data_store.scenario["response"] = requests.get(
        url=gateway_url+'/federation/federators',
        certs=get_country_cert_files(country, 'auth')
    )

@step("check that <gateway> is in the federator list")
def check_that_is_in_the_federator_list(gateway):
    'TODO: Check structure of response'    
    assert get_gateway_url_by_name(gateway) in data_store.scenario["response"].text , f'Gateway "{gateway}" is not in the response'

@step("<country> downloads the federation metadata on <gateway>")
def downloads_the_federation_metadata_on(country, gateway):
    gateway_url = testdata.get_gateway_url_by_name(gateway)
    data_store.scenario["response"] = requests.get(
        url=gateway_url+'/federation/metadata',
        certs=get_country_cert_files(country, 'auth')
    )

@step("check that meta data structure is OK")
def check_that_meta_data_structure_is_ok():
    'TODO: Meta data structure not finalized yet'
    
    metadata = json.load(data_store.scenario["response"].text)


@step("<country> downloads the federated reference trustlist")
def downloads_the_federated_reference_trustlist(country):
    data_store.scenario["response"] = requests.get(
        url=environ.get('first_gateway_url')+'/federation/trustlist/references',
        certs=get_country_cert_files(country, 'auth')
    )

    try: 
        data_store.scenario["downloaded.trustlist.references"] = data_store.scenario["response"].json()
    except:
        pass # Fail silently because checks are performed in different function and are expected for negative test steps


def _generic_upload_of_b64_data_by_country( url, data, country, delete=False ):
    headers = {"Content-Type": "application/cms",
               "Content-Transfer-Encoding": "base64"}

    certs = get_country_cert_files(country, 'auth')
    if not delete:
        return requests.post(url=url, data=data, headers=headers, cert=certs)
    else:
        return requests.delete(url=url, data=data, headers=headers, cert=certs)

@step("<country> uploads CMS with certificate")
def uploads_cms_certificate(country):
    data=data_store.scenario['trusted.certificate.cms']
    url = get_gateway_url_by_name('firstGateway') + '/trust/certificate'
    response = _generic_upload_of_b64_data_by_country( url, data, country )
    data_store.scenario["response"] = response
    if response.ok:
        data_store.scenario['trusted.certificate.last_uploader'] = country

@step("<country> downloads the certificate trustlist")
def downloads_the_certificate_trustlist(country):
    assert False, "Add implementation code"

@step("check that the certificate is in the trustlist")
def check_that_the_certificate_is_in_the_trustlist():
    assert False, "Add implementation code"

@step("Other gateway downloads the certificate trustlist")
def other_gateway_downloads_the_certificate_trustlist():
    assert False, "Add implementation code"

@step("<country> deletes uploaded certificate")
def deletes_uploaded_certificate(country):
    data=data_store.scenario['trusted.certificate.cms']
    url = get_gateway_url_by_name('firstGateway') + '/trust/certificate'
    response = _generic_upload_of_b64_data_by_country( url, data, country, delete=True )
    data_store.scenario["response"] = response

@step("check that the certificate is NOT in the trustlist")
def check_that_the_certificate_is_not_in_the_trustlist():
    assert False, "Add implementation code"

@step("<country> deletes uploaded certificate with alternate endpoint")
def deletes_uploaded_certificate_with_alternate_endpoint(country):
    data=data_store.scenario['trusted.certificate.cms']
    url = get_gateway_url_by_name('firstGateway') + '/trust/certificate/delete'
    response = _generic_upload_of_b64_data_by_country( url, data, country )
    data_store.scenario["response"] = response

@step("delete uploaded certificate")
def delete_uploaded_certificate():
    country = data_store.scenario['trusted.certificate.last_uploader']
    data = data_store.scenario['trusted.certificate.cms']
    url = get_gateway_url_by_name('firstGateway') + '/trust/certificate'
    response = _generic_upload_of_b64_data_by_country( url, data, country, delete=True )
    data_store.scenario["response"] = response


@step("<country> uploads CMS with trusted issuer")
def uploads_cms_trusted_issuer_certificate(country):
    data=data_store.scenario['trusted.issuer.cms']
    url = get_gateway_url_by_name('firstGateway') + '/trust/issuer'
    response = _generic_upload_of_b64_data_by_country( url, data, country )
    data_store.scenario["response"] = response
    if response.ok:
        data_store.scenario['trusted.issuer.last_uploader'] = country

@step("<country> downloads the trusted issuer trustlist")
def downloads_the_trusted_issuer_trustlist(country):
    assert False, "Add implementation code"

@step("check that the trusted issuer is in the trustlist")
def check_that_the_trusted_issuer_is_in_the_trustlist():
    assert False, "Add implementation code"

@step("Other gateway downloads the trusted issuer trustlist")
def other_gateway_downloads_the_trusted_issuer_trustlist():
    assert False, "Add implementation code"

@step("<country> deletes uploaded trusted issuer entry")
def deletes_uploaded_trusted_issuer_certificate(country):
    data=data_store.scenario['trusted.issuer.cms']
    url = get_gateway_url_by_name('firstGateway') + '/trust/issuer'
    response = _generic_upload_of_b64_data_by_country( url, data, country, delete=True )
    data_store.scenario["response"] = response

@step("check that the trusted issuer is NOT in the trustlist")
def check_that_the_trusted_issuer_is_not_in_the_trustlist():
    assert False, "Add implementation code"

@step("<country> deletes uploaded trusted issuer entry with alternate endpoint")
def deletes_uploaded_trusted_issuer_certificate_with_alternate_endpoint(country):
    data=data_store.scenario['trusted.issuer.cms']
    url = get_gateway_url_by_name('firstGateway') + '/trust/issuer/delete'
    response = _generic_upload_of_b64_data_by_country( url, data, country )
    data_store.scenario["response"] = response

@step("delete uploaded trusted issuer entry")
def delete_uploaded_trusted_issuer_certificate():
    country = data_store.scenario['trusted.issuer.last_uploader']
    data = data_store.scenario['trusted.issuer.cms']
    url = get_gateway_url_by_name('firstGateway') + '/trust/issuer'
    response = _generic_upload_of_b64_data_by_country( url, data, country, delete=True )
    data_store.scenario["response"] = response


@step("<country> uploads CMS reference")
def uploads_cms_reference(country):
    data=data_store.scenario['trusted.reference.cms']
    url = get_gateway_url_by_name('firstGateway') + '/trust/reference'
    response = _generic_upload_of_b64_data_by_country( url, data, country )
    data_store.scenario["response"] = response
    if response.ok:
        data_store.scenario['trusted.reference.last_uploader'] = country

@step("<country> downloads the reference trustlist")
def downloads_the_reference_trustlist(country):
    assert False, "Add implementation code"

@step("check that the reference is in the trustlist")
def check_that_the_reference_is_in_the_trustlist():
    referece_uuid = data_store.scenario["trusted.reference.raw"]['UUID']

@step("Other gateway downloads the reference trustlist")
def other_gateway_downloads_the_reference_trustlist():
    assert False, "Add implementation code"

@step("<country> deletes uploaded reference")
def deletes_uploaded_reference(country):
    data=data_store.scenario['trusted.reference.cms']
    url = get_gateway_url_by_name('firstGateway') + '/trust/reference'
    response = _generic_upload_of_b64_data_by_country( url, data, country, delete=True )
    data_store.scenario["response"] = response

@step("check that the reference is NOT in the trustlist")
def check_that_the_reference_is_not_in_the_trustlist():
    assert False, "Add implementation code"

@step("<country> deletes uploaded reference with alternate endpoint")
def deletes_uploaded_reference_with_alternate_endpoint(country):
    data=data_store.scenario['trusted.reference.cms']
    url = get_gateway_url_by_name('firstGateway') + '/trust/reference/delete'
    response = _generic_upload_of_b64_data_by_country( url, data, country )
    data_store.scenario["response"] = response

@step("delete uploaded reference")
def delete_uploaded_reference():
    country = data_store.scenario['trusted.reference.last_uploader']
    data = data_store.scenario['trusted.reference.cms']
    url = get_gateway_url_by_name('firstGateway') + '/trust/reference'
    response = _generic_upload_of_b64_data_by_country( url, data, country, delete=True )
    data_store.scenario["response"] = response
