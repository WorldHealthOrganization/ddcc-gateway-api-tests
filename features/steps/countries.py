from behave import given
import os

@given('that country {country} is onboarded')
def step_impl(context, country):
    assert os.path.isdir(os.path.join('certificates',country)), f'Country directory not found for {country}'