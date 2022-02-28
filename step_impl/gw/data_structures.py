import os
import random
from hashlib import sha256

from getgauge.python import step, data_store
from step_impl.util import testdata
from uuid import uuid4
import json


@step("<country> creates a reference")
def creates_a_reference(country):
    data_store.scenario["trusted.reference.thumbprint"] = sha256(os.urandom(8)).hexdigest()
    reference = {
        # 'uuid': str(uuid4()), TODO: if set an existing reference can be updated, Test-Cases for this?
        "version": 1,
        "country": testdata.get_country_code(country),
        "type": "DCC",
        "service": "ValueSet",  # ValueSet, PlanDefinition, etc.
        "thumbprint": data_store.scenario["trusted.reference.thumbprint"],
        "name": "TestReference",
        "sslPublicKey": testdata.get_ssl_public_key(country),
        "contentType": 'application/json',
        "signatureType": "CMS",
        "referenceVersion": "1.3.0"
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

