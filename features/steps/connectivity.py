from behave import * 
import requests


@step('the path "{path}" is queried')
def step_impl(context, path):
    context.response = requests.get(f'{context.base_url}{path}', cert=context.cert)


@step('the response should be OK')
def step_impl(context):
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

