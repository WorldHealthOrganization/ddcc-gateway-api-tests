Feature: Checking connectivity and access to the Gateway

Scenario Outline: Onboarded Countries
    Given that country <country> is onboarded
    When the DCC TLS certificate of <country> is used
    And the path "/trustList" is queried
    Then the response should be OK

    Examples: Onboarded countries
    | country |
    |  XXA    |
    |  XB     |
