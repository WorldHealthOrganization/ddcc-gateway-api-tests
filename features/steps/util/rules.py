import json
from base64 import b64decode
from os import path
from typing import List

import requests
from asn1crypto.cms import ContentInfo
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.x509 import Certificate
from requests import Response
from steps.util import eu_gateway_url, certificateFolder, verify
from steps.util.certificates import create_cms


def download_rule_of_country(country: str, cert_location: str, key_location: str) -> Response:
    return requests.get(url=eu_gateway_url + f"/rules/{country}", verify=verify, cert=(
        cert_location, key_location))


def get_rule_id_list(ruleList) -> List[str]:
    return ruleList.keys()


def get_rule_from_cms(cms: bytes):
    signedData = ContentInfo.load(cms)
    ruleJson = signedData['content']['encap_content_info']['content'].native
    return json.loads(ruleJson)


def get_rules_from_rulelist(rulelist):
    rulesCms = [rule[-1]["cms"] for rule in rulelist.values()]
    return [get_rule_from_cms(b64decode(cms)) for cms in rulesCms]


def delete_rule_by_id(ruleId: str, upload_cert: Certificate, upload_key: RSAPrivateKey, tls_cert_location: str, tls_key_location: str) -> Response:
    data = create_cms(ruleId.encode("utf-8"), upload_cert, upload_key)
    headers = {"Content-Type": "application/cms-text",
               "Content-Transfer-Encoding": "base64"}
    response = requests.delete(url=eu_gateway_url + "/rules", verify=verify,
                               data=data, headers=headers, cert=(tls_cert_location, tls_key_location))
    return response


def delete_rule_by_id_with_base_data(ruleId: str) -> Response:
    upload_cert = x509.load_pem_x509_certificate(
        open(path.join(certificateFolder, "upload.pem"), "rb").read())
    upload_key = serialization.load_pem_private_key(
        open(path.join(certificateFolder, "key_upload.pem"), "rb").read(), None)
    tls_cert_location = path.join(certificateFolder, "auth.pem")
    tls_key_location = path.join(certificateFolder, "key_auth.pem")
    data = create_cms(ruleId.encode('utf-8'), upload_cert, upload_key)
    headers = {"Content-Type": "application/cms-text",
               "Content-Transfer-Encoding": "base64"}
    response = requests.delete(url=eu_gateway_url + "/rules", verify=verify,
                               data=data, headers=headers, cert=(tls_cert_location, tls_key_location))
    return response
