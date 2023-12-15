Feature: Trusted certificate API    

As a non-EU participant, I will be using the /trustedCertificate API
instead of the /signerCertificate API

Background: The default DSC for most tests is a EC SECP384R1 from A
    When an EC key from curve SECP384R1 is created
    And country A is set in the certificate subject
    And the DCC SCA certificate of country A is used
    And the created key and subject are being signed
    Then set the created certificate as the default

Scenario: A DSC uploaded via trustedCertificate API is the old and the new trust list
    Given the default certificate is used
    And the DCC UP certificate of country A is used
    And the created cert is wrapped in a CMS message
        And the CMS is wrapped in a JSON object
        And the JSON kid attribute is set to ABCDEFGH
        And the JSON group attribute is set to DSC
        And the JSON domain attribute is set to DCC
    And the DCC TLS certificate of country A is used
    And the JSON is uploaded via the trustedCertificate API
    And the response should be OK

    When the path "/trustList" is queried
    Then the created cert is found in the trust list

    When the path "/trustList/certificate?group=DSC" is queried
    Then the created cert is found in the trust list

Scenario: Only DSCs of domain DCC appear in the EU trust list
    Given the default certificate is used
    And the DCC UP certificate of country A is used
    And the created cert is wrapped in a CMS message
        And the CMS is wrapped in a JSON object
        And the JSON kid attribute is set to ABCDEFGH
        And the JSON group attribute is set to DSC
        And the JSON domain attribute is set to ICAO
    And the DCC TLS certificate of country A is used
    And the JSON is uploaded via the trustedCertificate API
    And the response should be OK

    When the path "/trustList" is queried
    Then the created cert is NOT found in the trust list

    When the path "/trustList/certificate?group=DSC" is queried
    Then the created cert is found in the trust list

Scenario: The default domain is DCC
    Given the default certificate is used
    And the DCC UP certificate of country A is used
    And the created cert is wrapped in a CMS message
        And the CMS is wrapped in a JSON object
        And the JSON kid attribute is derived from the cert hash
        And the JSON group attribute is set to DSC
    And the DCC TLS certificate of country A is used
    And the JSON is uploaded via the trustedCertificate API
    And the response should be OK

    When the path "/trustList" is queried
    Then the created cert is found in the trust list

    When the path "/trustList/certificate?group=DSC&domain=DCC" is queried
    Then the created cert is found in the trust list

Scenario: By default, the KID is derived from the first 8 bytes of the  SHA-256 fingerprint
    Given the default certificate is used
    And the DCC UP certificate of country A is used
    And the created cert is wrapped in a CMS message
        And the CMS is wrapped in a JSON object
        And the JSON group attribute is set to DSC
    And the DCC TLS certificate of country A is used
    And the JSON is uploaded via the trustedCertificate API
    And the response should be OK

    When the path "/trustList" is queried
    Then the created cert is found in the trust list
    And the re-downloaded cert's KID is the first 8 bytes of the thumbprint

Scenario: Country B CANNOT upload DSCs created by Country A
    Given the default certificate is used
    And the DCC UP certificate of country B is used
    And the created cert is wrapped in a CMS message
        And the CMS is wrapped in a JSON object
        And the JSON kid attribute is derived from the cert hash
        And the JSON group attribute is set to DSC
        And the JSON domain attribute is set to DCC
    And the DCC TLS certificate of country B is used
    And the JSON is uploaded via the trustedCertificate API
    Then the response status code should be 4xx


Scenario: A country cannot sideload TLS certificates
    Given the default certificate is used
    And the DCC UP certificate of country A is used
    And the created cert is wrapped in a CMS message
        And the CMS is wrapped in a JSON object
        And the JSON kid attribute is derived from the cert hash
        And the JSON group attribute is set to AUTHENTICATION
        And the JSON domain attribute is set to DCC
    And the DCC TLS certificate of country A is used
    And the JSON is uploaded via the trustedCertificate API
    Then the response status code should be 4xx

@wip
Scenario Outline: Other certificate types than DCC are not visible in the EU trust list
    Given the default certificate is used
    And the DCC UP certificate of country A is used
    And the created cert is wrapped in a CMS message
        And the CMS is wrapped in a JSON object
        And the JSON kid attribute is derived from the cert hash
        And the JSON group attribute is set to <group>
        And the JSON domain attribute is set to DCC
    And the DCC TLS certificate of country A is used
    And the JSON is uploaded via the trustedCertificate API
    And the response should be OK

    When the path "/trustList" is queried
    Then the response should be OK
    And the created cert is NOT found in the trust list

    When the path "/trustList/certificate?group=<group>" is queried
    Then the response should be OK
    And the created cert is found in the trust list
  
  Examples:
   | group  | 
   | SIGN   |
   | AUTH   |
   | CUSTOM |

