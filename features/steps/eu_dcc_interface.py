import requests
from behave import *
from base64 import b64encode, b64decode

@step('the CMS is uploaded via the signerCertificate API')
def step_impl(context):
    args = {
        'url'     : f'{context.base_url}/signerCertificate',
        'headers' : {"Content-Type": "application/cms",
                     "Content-Transfer-Encoding": "base64"},
        'data'    : str(b64encode(context.created_cms),'utf-8'),
        'cert'    : context.cert,         
    }

    context.response = requests.post(**args)

    if context.response.ok:
        context.cleanups.append(
            {'callback': requests.delete,
            'args'    : args, 
            'name'    : 'Delete uploaded signer certificate'}
        )

@step('the CMS is deleted via the signerCertificate API')
def step_impl(context):
    args = {
        'url'     : f'{context.base_url}/signerCertificate',
        'headers' : {"Content-Type": "application/cms",
                     "Content-Transfer-Encoding": "base64"},
        'data'    : str(b64encode(context.created_cms),'utf-8'),
        'cert'    : context.cert,         
    }

    context.response = requests.delete(**args)

@step('the CMS is deleted via the alternate signerCertificate API')
def step_impl(context):
    args = {
        'url'     : f'{context.base_url}/signerCertificate/delete',
        'headers' : {"Content-Type": "application/cms",
                     "Content-Transfer-Encoding": "base64"},
        'data'    : str(b64encode(context.created_cms),'utf-8'),
        'cert'    : context.cert,         
    }

    context.response = requests.post(**args)
