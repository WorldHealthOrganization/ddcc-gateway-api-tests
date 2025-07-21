Feature: Valuesets 

As a participant, I want to download valuesets from the gateway

Scenario: Get valueset IDs 
    Given that country A is onboarded
    When the DCC TLS certificate of country A is used
    And the path "/valuesets" is queried
    Then the response should be OK
    And the result list should contain country-2-codes
    And the result list should contain covid-19-lab-result
    And the result list should contain covid-19-lab-test-type
    And the result list should contain disease-agent-targeted
    And the result list should contain sct-vaccines-covid-19
    And the result list should contain vaccines-covid-19-auth-holders
    And the result list should contain vaccines-covid-19-encoding-instructions
    And the result list should contain vaccines-covid-19-names
    And the result list should contain covid-19-lab-test-manufacturer-and-name

Scenario Outline: Get Valuesets
    Given that country A is onboarded
    When the DCC TLS certificate of country A is used
    And the path "/valuesets/<valueset_id>" is queried
    Then the response should be OK
    And the result list should have at least 1 entries
  Examples:
      | valueset_id                             |
      | country-2-codes                         |
      | covid-19-lab-result                     |
      | covid-19-lab-test-type                  |
      | disease-agent-targeted                  |
      | sct-vaccines-covid-19                   |
      | vaccines-covid-19-auth-holders          | 
      | vaccines-covid-19-encoding-instructions |
      | vaccines-covid-19-names                 |
      | covid-19-lab-test-manufacturer-and-name |


Scenario: Unauthorized client cannot download valuesets
    When the DCC TLS certificate of country C is used
    And the path "/valuesets" is queried
    Then the response status code should be 4xx