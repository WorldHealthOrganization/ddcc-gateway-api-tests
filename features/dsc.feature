Feature: DSC

This feature describes the DSC interface for uploading, downloading,
DSCs to TNG.

A DSC is a certificate, which a member state uses to sign documents.
As a participant in the smart trust network, I want to manage my DSCs:
To upload and download them and delete them if necessary. 
I expect unauthorized access to be prevented and basic checks to be 
performed against my uploads. 

The scenarios assume that countries A and B are onboarded and allowed to 
use the gateway while country XC is NOT onboarded and has no permission.

Background: The default DSC for most tests is a EC SECP384R1 from A
    When an EC key from curve SECP384R1 is created
    And country A is set in the certificate subject
    And the DCC SCA certificate of country A is used
    And the created key and subject are being signed
    Then set the created certificate as the default

Scenario: Upload an RSA DSC
    When an RSA key with 4092 bits is created
    And country A is set in the certificate subject
    And the DCC SCA certificate of country A is used
    And the created key and subject are being signed
    And the DCC UP certificate of country A is used
    And the created cert is wrapped in a CMS message
    And the DCC TLS certificate of country A is used
    And the CMS is uploaded via the signerCertificate API
    Then the response should be OK

    When the path "/trustList/certificate" is queried
    Then the created cert is found in the trust list

Scenario: Upload an ECDSA DSC
    When an EC key from curve SECP256R1 is created
    And country A is set in the certificate subject
    And the DCC SCA certificate of country A is used
    And the created key and subject are being signed
    And the DCC UP certificate of country A is used
    And the created cert is wrapped in a CMS message
    And the DCC TLS certificate of country A is used
    And the CMS is uploaded via the signerCertificate API
    Then the response should be OK

    When the path "/trustList/certificate" is queried
    Then the created cert is found in the trust list

Scenario: Country B can see DSCs uploaded by Country A
    Given the default certificate is used
    And the DCC UP certificate of country A is used
    And the created cert is wrapped in a CMS message
    And the DCC TLS certificate of country A is used
    And the CMS is uploaded via the signerCertificate API
    And the response should be OK

    When the DCC TLS certificate of country B is used
    And the path "/trustList/certificate" is queried
    Then the created cert is found in the trust list

Scenario: Country B CANNOT upload DSCs created by Country A, signed by B
    Given the default certificate is used
    And the DCC UP certificate of country B is used
    And the created cert is wrapped in a CMS message
    And the DCC TLS certificate of country B is used
    And the CMS is uploaded via the signerCertificate API
    Then the response status code should be 4xx

Scenario: Country B CANNOT upload DSCs created and signed by Country A
    Given the default certificate is used
    And the DCC UP certificate of country A is used
    And the created cert is wrapped in a CMS message
    And the DCC TLS certificate of country B is used
    And the CMS is uploaded via the signerCertificate API
    Then the response status code should be 4xx

Scenario: Country A can delete a DSC using the standard endpoint
    Given the default certificate is used
    And the DCC UP certificate of country A is used
    And the created cert is wrapped in a CMS message
    And the DCC TLS certificate of country A is used
    And the CMS is uploaded via the signerCertificate API
    And the response should be OK

    When the DCC TLS certificate of country A is used
    And the CMS is deleted via the signerCertificate API
    Then the response should be OK

    When the path "/trustList" is queried
    Then the created cert is NOT found in the trust list

Scenario: Country A can delete a DSC using the alternate endpoint
    Given the default certificate is used
    And the DCC UP certificate of country A is used
    And the created cert is wrapped in a CMS message
    And the DCC TLS certificate of country A is used
    And the CMS is uploaded via the signerCertificate API
    And the response should be OK

    When the DCC TLS certificate of country A is used
    And the CMS is deleted via the alternate signerCertificate API
    Then the response should be OK

    When the path "/trustList" is queried
    Then the created cert is NOT found in the trust list

