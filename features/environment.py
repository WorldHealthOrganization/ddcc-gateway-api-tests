from behave import * 
import pycountry
import json
import warnings
import os

def before_all(context):    
    cfg = context.config

    # Require a testing environment
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
    
    # Patch testing countries into pycountry: 
    try:
        test_countries = json.load(open(os.path.join('features','testing_countries.json')))
        for country_def in test_countries.get('countries'):
            _add_country(pycountry.countries, **country_def)
    except Exception as ex:
        message = f"Testing countries could not be loaded ({str(ex)})"
        warnings.warn(message)   
    

def _add_country(db, **params):
    '''Add a country to a pycountry database for the duration of this session.
       This is useful to patch testing countries into a list of countries.'''
    if not db._is_loaded:
        db._load()
    # Create an instance of the virtual country
    obj = db.data_class(**params)
    # Add it to the database
    db.objects.append(obj)
    # Update the indices
    for key, value in params.items():
        value = value.lower()
        if key in db.no_index:
            continue
        index = db.indices.setdefault(key, {})
        index[value] = obj

 

def before_scenario(scenario, context): 
    '''Reset the following attributes of the context: 
        - client_headers 
        - cleanups
    '''
    context.client_headers = {}
    context.cleanups = []

def after_scenario(scenario, context):
    for cleanup_job in context.cleanups: 
        try: 
            cleanup_job['callback'](**cleanup_job['args'])
        except Exception as ex: 
            warnings.warn(f'Error during cleanup of "{cleanup_job.get("name")}": {ex}')