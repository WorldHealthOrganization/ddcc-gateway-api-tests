from behave import *
from datetime import datetime, timedelta

@step("the {attributename} of the rule is changed to {attributevalue}")
def change_rule_to_new_version(context, attributename, attributevalue):
    ''' e.g. "When the Version of the rule is changed to 1.0.1" '''
    context.rule[attributename] = attributevalue
    #context.new_version = context.rule['Version']

@step("the rule becomes valid {seconds} seconds in the future")
def step_impl(context, seconds):
    context.rule['ValidFrom'] = datetime.now()+timedelta(seconds=int(seconds))