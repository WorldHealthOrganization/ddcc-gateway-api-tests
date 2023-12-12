from behave import * 
import requests
from time import sleep

@step('the path "{path}" is queried')
def step_impl(context, path):
    context.response = requests.get(f'{context.base_url}{path}', cert=context.cert)

@step('the response should be OK')
def step_impl(context):
    if not context.response.ok: 
        print(context.response.status_code, context.response.text)
    assert context.response.ok, 'The response was not OK'

@step('the response status code should be {status_code}')
def step_impl(context, status_code):
    if 'x' in status_code.lower():
        # partial match
        partial_code = status_code.lower().replace('x','')
        assert str(context.response.status_code).startswith(partial_code),\
            f"Got status code {context.response.status_code} but expected {status_code}"
    else:
        # full match
        assert context.response.status_code == int(status_code), \
            f"Got status code {context.response.status_code} but expected {status_code}"

@step('the result list should contain {lookup_string}')
def step_impl(context, lookup_string):
    assert lookup_string in context.response.json()

@step('the result list should have at least {number} entries')
def step_impl(context, number):
    assert len(context.response.json()) > int(number)

@step('we wait for {seconds} seconds')
def step_impl(context, seconds):
    sleep(float(seconds))