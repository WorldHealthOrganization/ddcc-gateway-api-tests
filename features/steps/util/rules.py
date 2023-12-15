import json
from base64 import b64decode
from os import path
from typing import List
import requests
from countries import Country

from asn1crypto.cms import ContentInfo
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from requests import Response
from steps.util.certificates import create_cms



def get_rule_id_list(ruleList) -> List[str]:
    return ruleList.keys()


def get_rule_from_cms(cms: bytes):
    signedData = ContentInfo.load(cms)
    ruleJson = signedData['content']['encap_content_info']['content'].native
    return json.loads(ruleJson)


def get_rules_from_rulelist(rulelist):
    '''rulelist is the JSON structure that comes from the gateway. 
       it is organized as follows: 
       { 'RULE-ID-1' : [  { versioned rule object},
                          { versioned rule object},
                          ...
                        ],
         'RULE-ID-2 :  ...
       }
     
       Returns: flattened list of all versions of all rules,
         CMS decoded
    '''
    flat_rule_list = []
    for rule_sub_list in rulelist.values(): 
        for rule_obj in rule_sub_list:
            flat_rule_list.append(get_rule_from_cms(b64decode(rule_obj['cms'])))
    
    return flat_rule_list
    #rulesCms = [rule[-1]["cms"] for rule in rulelist.values()]
    #return [get_rule_from_cms(b64decode(cms)) for cms in rulesCms]

def delete_rule_by_id_with_base_data(context, rule_id) -> Response:
    """ Send a delete request by Rule ID. 
        Country code is taken from rule ID (second segment TT-CC-NNNN)
         T = Type, C = Country, N = Number
        Upload and TLS certificate are selected to match the country,
        regardless of what certificates have been used earlier. 
    """
    country = Country(context, rule_id.split('-')[1])
    # Rules only exist in domain DCC, therefore hard coded domain DCC
    up_cert_path = path.join('certificates', country.alpha_3, 'DCC', f'UP.pem')
    up_key_path = path.join('certificates', country.alpha_3, 'DCC', f'UP.key')
    upload_cert = x509.load_pem_x509_certificate(open(up_cert_path,'rb').read())
    upload_key = serialization.load_pem_private_key(open(up_key_path,'rb').read(), None)
    
    tls_cert_location = path.join('certificates', country.alpha_3, 'DCC', f'TLS.pem')
    tls_key_location = path.join('certificates', country.alpha_3, 'DCC', f'TLS.key')
    data = create_cms(rule_id.encode('utf-8'), upload_cert, upload_key)
    headers = {"Content-Type": "application/cms-text",
               "Content-Transfer-Encoding": "base64"}
    response = requests.delete(url=context.base_url + "/rules", 
                               data=data, headers=headers, cert=(tls_cert_location, tls_key_location))
    return response
