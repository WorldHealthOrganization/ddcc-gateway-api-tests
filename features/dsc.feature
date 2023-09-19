Feature: DSC

Certificate hich the member states are using to sign documents.
As a participant in the smart trust network, I want to manage my DSCs:
To upload and download them and delete them if necessary. 
I expect unauthorized access to be prevented and basic checks to be 
performed against my uploads. 

@wip
Scenario: Upload an RSA DSC
    When an RSA key with 4092 bits is created
    Then country XA is set in the certificate subject
    And the DCC SCA certificate of XA is used
    And the created key and subject are being signed
    Then the DCC UP certificate of XA is used
    And the created cert is wrapped in a CMS message

@wip
Scenario: Upload an ECDSA DSC
    When an ec key from curve SECP256R1 is created
    Then country XA is set in the certificate subject
    And the DCC SCA certificate of XA is used
    And the created key and subject are being signed
    Then the DCC UP certificate of XA is used
    And the created cert is wrapped in a CMS message

