import json
from base64 import b64encode
from datetime import datetime, timedelta
from os import getcwd, path
from typing import List

import requests
from asn1crypto import cms
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.x509.oid import NameOID
from behave import *
from requests.exceptions import SSLError
from steps.util.json import DateTimeEncoder
from steps.util.rules import delete_rule_by_id_with_base_data

def add_rule_to_store(context, rule):
    try:
        rules = context.created_rules
    except KeyError:
        rules = []
        context.created_rules = rules
    rules.append(rule)

@step('the rule {rule_id} is deleted')
def step_impl(context, rule_id):
    return delete_rule_by_id_with_base_data(context, rule_id)

@step("the rule CMS is uploaded as cms-text")
def step_impl(context):
    return upload_rule(context, content_type="application/cms-text")

@step("the rule CMS is uploaded")
def upload_rule(context, content_type="application/cms"):
    data = context.created_cms

    context.response = requests.post(url=f'{context.base_url}/rules',
                                     headers={"Content-Type": content_type,
                                            "Content-Transfer-Encoding": "base64"},
                                     data=str(b64encode(data),'utf-8'),
                                     cert=context.cert,
                                     )

    if context.response.ok:
        # Schedule a deletion of the created rule for after the scenario
        args = {'context':context, 'rule_id':context.rule.get('Identifier')}
        context.cleanups.append(
            {'callback': delete_rule_by_id_with_base_data,
            'args'    : args, 
            'name'    : f'Delete uploaded rule {context.rule.get("Identifier")}'}
        )

# @step("delete all created rules")
# def delete_all_created_rules(context):
#     try:
#         rules: List[Certificate] = context.created_rules
#         for rule in rules:
#             ruleId = rule["Identifier"]
#             delete_rule_by_id_with_base_data(ruleId)
#     except KeyError:
#         return
