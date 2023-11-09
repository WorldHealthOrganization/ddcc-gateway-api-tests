Feature: Trust Anchor

Scenario Outline: All onboarded certificates are signed by the trust anchor
    Given the DCC TLS certificate of country A is used
    And the trust anchor is loaded from the environment config
    When the path "/trustList/certificate?group=<group>" is queried
    Then the response should be OK
    And every CMS should be signed by the trust anchor
  
  Examples:
   | group            | 
   | AUTHENTICATION   |
   | CSCA             |
   | UPLOAD           |