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
            Possible values are defined in "testing_environments.json"
                         ''')
    
    testenv = json.load(open(os.path.join('features','testing_environments.json'))).get(cfg.userdata.get('testenv'))
    context.base_url = testenv.get('base_url')
    context.testenv = testenv
    
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

 

def before_scenario(context, scenario): 
    '''Reset the following attributes of the context: 
        - cleanups
    '''
    context.cleanups = []

def after_scenario(context, scenario):
    for cleanup_job in context.cleanups: 
        try: 
            cleanup_job['callback'](**cleanup_job['args'])
            print(f'Completed cleanup: {cleanup_job["name"]}')
        except Exception as ex: 
            warnings.warn(f'Error during cleanup of "{cleanup_job.get("name")}": {ex}')