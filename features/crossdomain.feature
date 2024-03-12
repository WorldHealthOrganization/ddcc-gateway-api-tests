Feature: Cross domain DSC upload

A country should be able to upload DSCs for a domain
using UP or SCA certificates from a different domain

Scenario Outline: Use one domain for signing and upload, another in payload
    When an EC key from curve SECP256R1 is created
    And country A is set in the certificate subject
    And the <source_domain> SCA certificate of country A is used
    And the created key and subject are being signed
    And the <source_domain> UP certificate of country A is used
    And the created cert is wrapped in a CMS message
        And the CMS is wrapped in a JSON object
        And the JSON kid attribute is set to ABCDEFGH
        And the JSON group attribute is set to DSC
        And the JSON domain attribute is set to <target_domain>
    And the <source_domain> TLS certificate of country A is used
    And the JSON is uploaded via the trustedCertificate API
    Then the response should be OK

    When the path "/trustList/certificate?domain=<target_domain>" is queried
    Then the created cert is found in the trust list

Examples:
    | source_domain | target_domain |
    |  DCC          |   ICAO        | 
    |  DCC          |  RACSEL-DDVC  |
    |  DCC          |   IPS         |
