from behave import given
import pycountry
import os

def Country(code):
    """Return a Country object for a country's 2-letter or 3-letter code
       or None if the country was not found"""
    code = code.upper()
    if len(code) == 2: 
        return pycountry.countries.get(alpha_2=code)
    elif len(code) == 3:
        return pycountry.countries.get(alpha_3=code)
    else:
        return None

@given('that country {country_code} is onboarded')
def step_impl(context, country_code):
    country = Country(country_code)
    assert os.path.isdir(os.path.join('certificates',country.alpha_3)), f'Country directory not found for {country_code}'
