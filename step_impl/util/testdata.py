from os import path, environ
from step_impl.util import certificateFolder


def get_country_code(country):
    """TODO: Load country code from certificates"""
    if country.lower() == 'countrya':
        return 'XA'
    elif country.lower() == 'countryb':
        return 'XB'
    elif country.lower() == 'countryc':
        return 'XC'
    else:
        return 'XX'


def get_country_gateway_url(country):
    """TODO: Keep config in environment or file"""
    return {
        'CountryA': environ.get('first_gateway_url'),
        'CountryB': environ.get('first_gateway_url'),
        'CountryC': environ.get('second_gateway_url'),
    }.get(country)


def get_gateway_url_by_name(gateway):
    return {
        'firstgateway': environ.get('first_gateway_url'),
        'secondgateway': environ.get('first_gateway_url'),
        'thirdgateway': environ.get('second_gateway_url'),
    }.get(gateway.lower().replace(' ', '').replace('_', ''))


def get_country_cert_files(country, cert_type):
    """Return a tuple with paths to the country's certificate file and private key"""

    assert cert_type in ('csca', 'auth', 'upload'), "Unknown certificate type: Must be one of csca|auth|upload"

    # for compatibility: no country or "firstCountry" means old EU case
    if country == 'firstCountry' or country is None:
        return path.join(certificateFolder, f"{cert_type}.pem"), path.join(certificateFolder, f"key_{cert_type}.pem")

    return (path.join(certificateFolder, country, f"{cert_type}.pem"),
            path.join(certificateFolder, country, f"key_{cert_type}.pem"))


def get_ssl_public_key(country):
    """TODO: Load public key from certificates"""

    # Placeholder public key
    return '''
    MIIBNDCB3KADAgECAgRhJeHLMAoGCCqGSM49BAMCMCMxITAfBgNVBAMMGFZhbGlkYXRpb25TZXJ2
    aWNlU2lnbktleTAeFw0yMTA4MjUwNjIzMDdaFw0yMjA4MjUwNjIzMDdaMCMxITAfBgNVBAMMGFZh
    bGlkYXRpb25TZXJ2aWNlU2lnbktleTBZMBMGByqGSM49AgEGCCqGSM49AwEHA0IABIMdlvwpEPWm
    brhAZLOZm6NGyCQofFbpE1EfYK9i+kLpmwDgAtc99zoZg9d2oZtpC9zNLs71cncpJSkqpST1HKEw
    CgYIKoZIzj0EAwIDRwAwRAIgct73rVroQYuxpZS/Y/awVrceBjAOvFqmxDr07Y8BBqsCIBjH9085
    RqVzFfZsdO9Y9YazZ1q0+oqmwl7ypT2xWEoU'''
