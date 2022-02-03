from getgauge.python import step, data_store
from step_impl.util import testdata
from uuid import uuid4
import json


@step("<country> creates a reference")
def creates_a_reference(country):
    reference = {
        'UUID' : str(uuid4()),
        'URL' : 'https://does.not.exist/123', 
        'Type' : 'FHIR', 
        'Version' : '1.3.0',
        'Country' : testdata.get_country_code(country),
        'Service' : 'ValueSet', # ValueSet, PlanDefinition, etc.
        'Thumbprint' : 'abcdefghijklmnopqrstuvqxyz', # TODO: HEX or base64?
        'SSLPublicKey' : testdata.get_ssl_public_key(country),
        'Content-Type' : 'application/json',
        'SignatureType' : 'CMS'
    }

    data_store.scenario["trusted.reference.raw"] = reference
    return reference


@step("<country> creates a trusted issuer entry")
def creates_a_trusted_issuer_certificate(country):
    trusted_issuer = {
        'URL' : 'https://does.not.exist/123', 
        'Type' : 'FHIR', 
        'Country' : testdata.get_country_code(country),
        'Thumbprint' : 'abcdefghijklmnopqrstuvqxyz', # TODO: HEX or base64?
        'Name' : 'ValueSet',
        'SSLPublicKey' : testdata.get_ssl_public_key(country),
        'KeyStorageType' : 'JWKS', # or DIDDocument, JKS, etc.
    }

    data_store.scenario["trusted.issuer.raw"] = trusted_issuer
    return trusted_issuer

