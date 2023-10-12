import os
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

@step('the created cert is wrapped in a CMS message')
# Requires cert attribute set by
# 'the {domain} {ctype} certificate of {country_code} is used'
def step_impl(context):
    data = context.created_cert.public_bytes(serialization.Encoding.DER)
    cert_path, key_path = context.cert
    with open(cert_path,'rb') as cert_file:
        cms_cert = load_pem_x509_certificate(cert_file.read())
    with open(key_path,'rb') as key_file:
        cms_key = serialization.load_pem_private_key(key_file.read(),None)

    options = [pkcs7.PKCS7Options.Binary]

    builder = pkcs7.PKCS7SignatureBuilder().set_data(data)
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