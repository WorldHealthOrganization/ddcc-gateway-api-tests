from behave import given
import pycountry
import os

def Country(context, code_or_alias):
    """Return a Country object for a country's 2-letter or 3-letter code
       or None if the country was not found"""
    
    if len(code_or_alias) == 1:  # assume that we have an alias
        code = context.testenv.get(f'country_{code_or_alias.upper()}')
    else:
        code = code_or_alias
    
    code = code.upper()
    if len(code) == 2: 
        return pycountry.countries.get(alpha_2=code)
    elif len(code) == 3:
        return pycountry.countries.get(alpha_3=code)
    else:
        return None

@given('that country {country_code} is onboarded')
def step_impl(context, country_code):
    country = Country(context, country_code)
    assert os.path.isdir(os.path.join('certificates',country.alpha_3)), f'Country directory not found for {country_code}'
