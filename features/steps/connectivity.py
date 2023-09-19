from behave import * 
import requests


@when('the path "{path}" is queried')
def step_impl(context, path):
    context.response = requests.get(f'{context.base_url}{path}', cert=context.cert)


@then('the response should be OK')
def step_impl(context):
    assert context.response.ok, 'The response was not OK'
