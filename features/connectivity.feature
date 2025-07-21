Feature: Checking connectivity and access to the Gateway

  This feature tests the connectivity and access to the Trust Network Gateway (TNG)
  The connection is mTLS which not only means that the client checks the server integrity,
  but must also present a valid client TLS certificate for the connection to be accepted by the TNG

Scenario Outline: Onboarded Countries
    Given that country <country> is onboarded
    When the DCC TLS certificate of country <country> is used
    And the path "/trustList/certificate" is queried
    Then the response should be OK

    Examples: Onboarded countries
    | country |
    |  A      |
    |  B      |
