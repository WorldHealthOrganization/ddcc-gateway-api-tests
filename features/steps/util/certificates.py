# ---license-start
# eu-digital-green-certificates / dgc-api-tests
# ---
# Copyright (C) 2021 T-Systems International GmbH and all other contributors
# ---
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ---license-end

from base64 import b64encode
from datetime import datetime, timedelta
from os import path

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.serialization import pkcs7
from cryptography.x509 import Certificate
from cryptography.x509.oid import NameOID


def get_country_name_from_certificate(cert: Certificate) -> str:
    return cert.subject.get_attributes_for_oid(NameOID.COUNTRY_NAME)[0].value

def get_own_country_name(country_code) -> str:
    csca_cert = x509.load_pem_x509_certificate(
        open(path.join("certificates", f"XX{country_code}", "DCC", "SCA.pem"), "rb").read())
    return get_country_name_from_certificate(csca_cert)

def create_certificate(signing_cert: Certificate = None, signing_key: RSAPrivateKey = None, common_name = 'TestCert', valid_seconds=10):
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    if signing_cert != None:
        countryName = get_country_name_from_certificate(signing_cert)
    else:
        countryName = u"DE"

    subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, countryName),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Nowhere"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Someplace"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Fictional Testing Company"),
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),
    ])

    issuer = signing_cert.issuer if signing_cert != None else subject
    keyUsedToSign = signing_key if signing_key != None else key
    cert = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer).public_key(key.public_key()).serial_number(
        x509.random_serial_number()).not_valid_before(datetime.utcnow()).not_valid_after(datetime.utcnow() + timedelta(seconds=valid_seconds)).sign(keyUsedToSign, hashes.SHA256())
    return (cert, key)


def create_dsc(csca_cert: Certificate, csca_key: RSAPrivateKey):
    (cert, key) = create_certificate(csca_cert, csca_key)
    return cert


def create_cms_with_certificate(dsc_cert: Certificate, upload_cert: Certificate, upload_key: RSAPrivateKey):
    return create_cms(dsc_cert.public_bytes(serialization.Encoding.DER), upload_cert, upload_key)


def create_cms(data: bytes, upload_cert: Certificate, upload_key: RSAPrivateKey):
    '''Create a CMS out of <data> using <upload_cert> and <upload_key>
       Return the data in Base64 encoding
    '''

    options = [pkcs7.PKCS7Options.Binary]

    builder = pkcs7.PKCS7SignatureBuilder().set_data(data)
    signed = builder.add_signer(upload_cert, upload_key, hash_algorithm=hashes.SHA256()).sign(
        encoding=serialization.Encoding.DER, options=options)

    return b64encode(signed)