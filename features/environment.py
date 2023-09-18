from behave import * 

def before_all(context):    
    cfg = context.config

    if not cfg.userdata.get('testenv'): 
        raise ValueError('''
            ERROR: Testing environment not set. 
            Please use -D testenv=<testenv> to define the target.
            Possible values are: LOCAL, DEV, UAT, or a custom URL
                         ''')
    
    if cfg.userdata.get('testenv').upper() == 'LOCAL':
        context.base_url = 'https://localhost:8443'
    elif cfg.userdata.get('testenv').upper() == 'DEV':
        context.base_url = 'https://tng-dev.who.int'
    elif cfg.userdata.get('testenv').upper() == 'UAT':
        context.base_url = 'https://tng-uat.who.int'
    elif cfg.userdata.get('testenv').startswith('http'):
        context.base_url = cfg.userdata.get('testenv')
    else:
        raise ValueError('Invalid testenv')
