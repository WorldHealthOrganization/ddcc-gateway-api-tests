import json
import requests
from jsonschema import validate, ValidationError
from behave import given, when, then

def github_to_raw(url: str) -> str:
    """
    Convert a GitHub URL like:
    https://github.com/<org>/<repo>/blob/<branch>

    Into a raw URL like:
    https://raw.githubusercontent.com/<org>/<repo>/<branch>
    """
    if "github.com" not in url or "/blob/" not in url:
        raise ValueError("Invalid GitHub blob URL")

    parts = url.split("github.com/")[1].split("/blob/")
    repo_part = parts[0]                # org/repo
    branch_and_path = parts[1]         # branch/path/to/file

    # Some URLs include `refs/heads/main` instead of `main`
    branch_and_path = branch_and_path.replace("refs/heads/", "")

    raw_url = f"https://raw.githubusercontent.com/{repo_part}/{branch_and_path}"
    return raw_url

@given('the schema file "{schema_file}" is fetched from GitHub cdn repository')
def fetch_schema(context, schema_file):
    raw_repo_url = github_to_raw(context.repo_url)
    url = f"{raw_repo_url}{schema_file}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch schema from {url}")
    context.schema = response.json()

@given('the instance file "{instance_file}" is fetched from GitHub cdn repository')
def fetch_instance(context, instance_file):
    raw_repo_url = github_to_raw(context.repo_url)
    url = f"{raw_repo_url}{instance_file}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch instance from {url}")
    context.instance = response.json()

@when('validate the instance against the schema')
def validate_instance(context):
    try:
        validate(instance=context.instance, schema=context.schema)
        context.validation_passed = True
        context.validation_error = None
    except ValidationError as e:
        context.validation_passed = False
        context.validation_error = str(e)

@then('the instance should be valid according to the schema')
def check_validation(context):
    if not context.validation_passed:
        raise AssertionError(f"Validation failed: {context.validation_error}")