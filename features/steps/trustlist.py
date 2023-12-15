from behave import step
from countries import Country
from base64 import b64encode, b64decode
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.x509 import load_pem_x509_certificate
from asn1crypto import cms
from cryptography.exceptions import InvalidSignature 
from cryptography.hazmat.primitives.asymmetric import ec
import requests
from hashlib import sha256


@step('the trust list for {cert_type} and {country_code} is queried')
def step_impl(context, cert_type, country_code):
    country = Country(context, country_code)
    context.response = requests.get(f'{context.base_url}/trustList/{cert_type}/{country.alpha_2}', cert=context.cert)

@step('only certificates of type {ctype_classic} should be in the downloaded list')
def step_impl(context, ctype_classic):
    trust_list = context.response.json()
    for cert_info in trust_list:
        assert cert_info['certificateType'] == ctype_classic, f'Found a certificate of different type than {ctype_classic}'

@step('the downloaded list should have more than {count} entries')
def step_impl(context, count):
    trust_list = context.response.json()
    assert len(trust_list) > int(count)

@step('only certificates of country {country_code} should be in the downloaded list')
def step_impl(context, country_code):
    country = Country(context, country_code)
    trust_list = context.response.json()
    for cert_info in trust_list:
        assert cert_info['country'] == country.alpha_2, f'Found a certificate of different country than {country.alpha_2}'


@step('the created cert is found in the trust list')
def step_impl(context):
    created_cert_b64 = b64encode(context.created_cert.public_bytes(serialization.Encoding.DER))
    created_cert_b64 = str(created_cert_b64,'utf-8') 

    trust_list = context.response.json()
    for cert_info in trust_list:
        # EU trust list uses 'rawData' key, WHO trust list uses 'certificate' key
        if cert_info.get('rawData') == created_cert_b64 \
        or cert_info.get('certificate') == created_cert_b64:
            return 
        
    assert False, 'Created cert not found in trust list'

@step('the created cert is NOT found in the trust list')
def step_impl(context):
    created_cert_b64 = b64encode(context.created_cert.public_bytes(serialization.Encoding.DER))
    created_cert_b64 = str(created_cert_b64,'utf-8') 

    trust_list = context.response.json()
    for cert_info in trust_list:
        # EU trust list uses 'rawData' key, WHO trust list uses 'certificate' key
        if cert_info.get('rawData') == created_cert_b64\
        or cert_info.get('certificate') == created_cert_b64:
            assert False, 'Created cert unexpectedly found in trust list'


@step('every CMS should be signed by the trust anchor')
def step_impl(context):
    trust_list = context.response.json()
    for cert_info in trust_list:
        cert_raw = cert_info.get('rawData') or cert_info.get('certificate')
        cert = load_pem_x509_certificate(bytes(
            f'''-----BEGIN CERTIFICATE-----
            {cert_raw}
            -----END CERTIFICATE-----''','utf-8'))        
        cert_der_format = cert.public_bytes(encoding=serialization.Encoding.DER)

        cms_message = cms.ContentInfo.load(b64decode(cert_info.get('signature')))       
        signed_data = cms_message['content']
        payload = signed_data['encap_content_info']['content'].native
        signature = signed_data['signer_infos'][0]['signature'].native       
        signed_attributes = signed_data['signer_infos'][0]['signed_attrs']
        signed_attributes_hash = hashes.Hash(hashes.SHA256())
        signed_attributes_hash.update(signed_attributes.dump())

        # TODO: Support more signature algorithms
        signature_algorithm = signed_data['signer_infos'][0]['signature_algorithm']['algorithm']
        assert str(signature_algorithm) == '1.2.840.10045.4.3.2', "Supporting only ECDSA with SHA256 at this moment"
        
        assert payload == cert_der_format, 'Raw cert and CMS payload do not match'
        
        context.trust_anchor_public_key.verify(signature, signed_attributes_hash.finalize(), ec.ECDSA(hashes.SHA256()))