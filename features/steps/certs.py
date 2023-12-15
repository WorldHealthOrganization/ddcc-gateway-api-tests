import os
import json
from base64 import b64decode, b64encode
from behave import *
from hashlib import sha256
from countries import Country
from datetime import datetime, timedelta
from cryptography import x509
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.serialization import pkcs7
from cryptography.hazmat.primitives.asymmetric import rsa, dsa, ec
from cryptography.x509.oid import NameOID
from util.json import DateTimeEncoder

@step('the {domain} {ctype} certificate of country {country_code} is used')
def step_impl(context, domain, ctype, country_code):
    #domain = domain.upper()
    ctype = ctype.upper()
    country = Country(context, country_code)

    context.cert = ( os.path.join('certificates', country.alpha_3, domain, f'{ctype}.pem'),
                     os.path.join('certificates', country.alpha_3, domain, f'{ctype}.key'),
                    )    # env_certs(ctype, country) 
    
    for path in context.cert: 
        #print('Working directory: ', os.getcwd())
        assert os.path.isfile(path), f'Not found: {path}'

@when('an RSA key with {bitsize} bits is created')
def step_impl(context, bitsize):
    context.created_key = rsa.generate_private_key(public_exponent=65537, key_size=int(bitsize))

@when('a DSA key with {bitsize} bits is created')
def step_impl(context, bitsize):
    context.created_key = dsa.generate_private_key(key_size=int(bitsize))

@when('an EC key from curve {curve} is created')
# curve examples: SECP256R1, SECP384R1, SECP521R1
def step_impl(context, curve):
    curve_object = getattr(ec, curve.upper() )()
    context.created_key = ec.generate_private_key(curve_object)

@step('country {country_code} is set in the certificate subject')
def step_impl(context, country_code):
    country = Country(context, country_code)
    context.x509_subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, country.alpha_2),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Somewhere"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Someplace"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Fictional Testing Company"),
        x509.NameAttribute(NameOID.COMMON_NAME, f"Test Data {int(datetime.utcnow().timestamp())}"),
    ])
  
@step('the created key and subject are being signed')
# Requires cert attribute set by
# 'the {domain} {ctype} certificate of {country_code} is used'
def step_impl(context):
    cert_path, key_path = context.cert
    with open(cert_path,'rb') as cert_file:
        signing_cert = load_pem_x509_certificate(cert_file.read())
    with open(key_path,'rb') as key_file:
        signing_key = serialization.load_pem_private_key(key_file.read(),None)
    
    context.created_cert = x509.CertificateBuilder()\
            .subject_name(context.x509_subject)\
            .issuer_name(signing_cert.issuer)\
            .public_key(context.created_key.public_key())\
            .serial_number(x509.random_serial_number())\
            .not_valid_before(datetime.utcnow())\
            .not_valid_after(datetime.utcnow() + timedelta(days=1))\
            .sign(signing_key, hashes.SHA256())    

@step("the created {itemtype} is wrapped in a CMS message with extra data")
def step_impl(context, itemtype):
    return build_cms(context, itemtype, extra_data=b"foobar123")

@step('the created {itemtype} is wrapped in a CMS message')
# Requires cert attribute set by
# 'the {domain} {ctype} certificate of {country_code} is used'
def build_cms(context, itemtype, extra_data=b""):
    if itemtype.lower() in ['cert', 'certificate']:
        data = context.created_cert.public_bytes(serialization.Encoding.DER)
    elif itemtype.lower() == 'rule': 
        data = bytes( json.dumps(context.rule, cls=DateTimeEncoder ), 'utf-8' )
        #print(context.rule)
    else: 
        raise ValueError('Item type must be "cert" or "rule" ')

    cert_path, key_path = context.cert
    with open(cert_path,'rb') as cert_file:
        cms_cert = load_pem_x509_certificate(cert_file.read())
    with open(key_path,'rb') as key_file:
        cms_key = serialization.load_pem_private_key(key_file.read(),None)

    options = [pkcs7.PKCS7Options.Binary]

    builder = pkcs7.PKCS7SignatureBuilder().set_data(data + extra_data)
    cms_bytes = builder.add_signer(cms_cert, cms_key, hash_algorithm=hashes.SHA256()).sign(
        encoding=serialization.Encoding.DER, options=options)

    context.created_cms = cms_bytes

@step('the CMS is wrapped in a JSON object')
def step_impl(context):
    context.json_object = {
        'cms' : str(b64encode(context.created_cms),'utf-8'),
        'properties' : {}
    }

@step('the JSON {attr} attribute is set to {value}')
def step_impl(context, attr, value):
    context.json_object[attr] = value

@step('the JSON kid attribute is derived from the cert hash')
def step_impl(context):
    cert_fingerprint = sha256(context.created_cert.public_bytes(serialization.Encoding.DER)).digest()
    context.json_object['kid'] = str(b64encode(cert_fingerprint[:8]),'utf-8')
    print(f"KID = {context.json_object['kid']}")


@step('set the created certificate as the default')
def step_impl(context):
    context.default_cert = context.created_cert

@step('the default certificate is used')
def step_impl(context):
    context.created_cert = context.default_cert

@step('the trust anchor is loaded from the environment config')
def step_impl(context):
    
    context.trust_anchor_public_key = serialization.load_pem_public_key(
        bytes(f"-----BEGIN PUBLIC KEY-----\n{context.testenv.get('trust_anchor')}\n-----END PUBLIC KEY-----",'utf-8'))

@step("the re-downloaded cert's KID is the first {bytecount} bytes of the thumbprint")
def step_impl(context, bytecount):
    created_cert = context.created_cert.public_bytes(serialization.Encoding.DER)
    created_cert_b64 = b64encode(created_cert)
    created_cert_b64 = str(created_cert_b64,'utf-8') 
    created_cert_hash = b64encode(sha256(created_cert).digest()[:int(bytecount)])
    created_cert_hash = str(created_cert_hash, 'utf-8')


    trust_list = context.response.json()
    for cert_info in trust_list:
        # EU trust list uses 'rawData' key, WHO trust list uses 'certificate' key
        if cert_info.get('rawData') == created_cert_b64 \
        or cert_info.get('certificate') == created_cert_b64:
            assert cert_info.get('kid') == created_cert_hash, f'KID is not the first {bytecount} bytes of the thumbprint'
            return True
        
    assert False, 'Created cert not found in trust list'