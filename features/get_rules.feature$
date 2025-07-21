Feature: GET RULES

This feature downloads all rules from the gateway.

Scenario: Get all onboarded countries. Should have at least the own country in the list.
    When the DCC TLS certificate of country A is used
    And the path "/countrylist" is queried
    And the response should be OK
    And the response status code should be 200
    Then check that country A is in onboared countries list
    Then check that country B is in onboared countries list
    Then check that country C is not in onboared countries list

Scenario: Get all onboarded countries with unauthenticated NBTLS. Should lead to an error.
    When the DCC TLS certificate of country C is used
    And the path "/countrylist" is queried
    Then the response status code should be 4xx

Scenario: Download Rules of all Countries.
    When the DCC TLS certificate of country A is used
    And the path "/countrylist" is queried
    And the rules of country A are downloaded
    And the response should be OK
    Then the response status code should be 200

Scenario: Get Rules from any country with an unauthenticated NBTLS. Should lead to an error.
    When the DCC TLS certificate of country C is used
    And the path "/countrylist" is queried
    And the rules of country C are downloaded
    Then the response status code should be 4xx