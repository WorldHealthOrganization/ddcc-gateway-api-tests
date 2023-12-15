
import requests
from behave import *
from base64 import b64encode, b64decode

@step('the JSON is uploaded via the trustedCertificate API')
def step_impl(context):
    context.response = requests.post(
        url = f'{context.base_url}/trustedCertificate',
        json = context.json_object,
        cert = context.cert
    )

    # Schedule cleanup (delete certificate)
    if context.response.ok:
        context.cleanups.append(
            {'callback': requests.delete,
            'args'    : {
                'url' : f'{context.base_url}/trustedCertificate',
                'cert'    : context.cert,                         
                'headers' : {"Content-Type": "application/cms",
                            "Content-Transfer-Encoding": "base64"},
                'data'    : context.json_object['cms']
            }, 
            'name'    : 'Delete uploaded trusted certificate'}
        )