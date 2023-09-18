import os
from cryptography.x509 import load_der_x509_certificate
from cryptography.hazmat.primitives import serialization
from base64 import b64decode
from behave import when

def env_certs(ctype, country):
    """return a tuple of certificate and key object from the environment variables
       <type>_CERT_<country>  and  <type>_KEY_<country>
    """

    def require_env(variable_name):
        value = os.environ.get(variable_name)
        if value is None: 
            raise ValueError(f'Environment variable not set: {variable_name}')
        return value
    
    country = country.upper()
    ctype = ctype.upper()
    
    cert_content = require_env(f'{ctype}_CERT_{country}')
    cert_binary = b64decode(cert_content)
    cert = load_der_x509_certificate(cert_binary)

    key_content = require_env(f'{ctype}_KEY_{country}')
    key_binary = b64decode(key_content)
    key = serialization.load_der_private_key(key_binary, None)

    return cert, key


@when('the {domain} {ctype} certificate of {country} is used')
def step_impl(context, domain, ctype, country):
    #domain = domain.upper()
    ctype = ctype.upper()
    country = country.upper()

    context.cert = ( os.path.join('certificates', country, domain, f'{ctype}.pem'),
                     os.path.join('certificates', country, domain, f'{ctype}.key'),
                    )    # env_certs(ctype, country) 
    
    for path in context.cert: 
        print('Working directory: ', os.getcwd())
        assert os.path.isfile(path), f'Not found: {path}'