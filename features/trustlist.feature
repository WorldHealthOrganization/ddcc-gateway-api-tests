Feature: Trust List 

As a connected party, I want to be able to read the certificates
of other parties so that I can trust their signatures. 

I want to be able to filter by different criteria, so that I only
need to load relevant information

Scenario Outline: Filter trust list by type
    Given that country A is onboarded
    When the DCC TLS certificate of country A is used
    And the path "/trustList/<cert_type>" is queried
    Then the response should be OK
    And the downloaded list should have more than 0 entries
    And only certificates of type <cert_type> should be in the downloaded list    
    Examples:
    | cert_type |
    |    DSC    |
    |  UPLOAD   |
    |   CSCA    | 

Scenario Outline: Filter trust list by type and country
    Given that country A is onboarded
    When the DCC TLS certificate of country A is used
    And the trust list for <cert_type> and <country> is queried
    Then the response should be OK
    And the downloaded list should have more than 0 entries
    And only certificates of type <cert_type> should be in the downloaded list    
    And only certificates of country <country> should be in the downloaded list    
    Examples:
    | cert_type |  country | 
    |    DSC    |   A      |
    |  UPLOAD   |   B      | 
    |   CSCA    |   B      | 
