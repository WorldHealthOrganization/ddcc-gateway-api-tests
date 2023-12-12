Feature: UPDATE RULES

Tests to update rules

@done
Scenario: Update a Rule created to a new version.
    When create a valid Invalidation Rule for country A
    And the DCC UP certificate of country A is used
    And the created rule is wrapped in a CMS message
    And the DCC TLS certificate of country A is used
    And the rule CMS is uploaded
    Then the response should be OK
    
    When the Version of the rule is changed to 1.0.1
    And the DCC UP certificate of country A is used
    And the created rule is wrapped in a CMS message
    And the DCC TLS certificate of country A is used
    And the rule CMS is uploaded
    Then the response should be OK
    And the response status code should be 201

    When the rules of country A are downloaded
    Then the re-downloaded rule exists in version 1.0.1

@done
Scenario: Two versions of a rule
          Update a Rule created to a new version and ValidFrom value 
          later than old rule. In the end both Versions of the rule 
          should be downloaded.

    When create a valid Invalidation Rule for country A
    And the DCC UP certificate of country A is used
    And the created rule is wrapped in a CMS message
    And the DCC TLS certificate of country A is used
    And the rule CMS is uploaded
    Then the response should be OK
    
    When the Version of the rule is changed to 1.0.1
    And the rule becomes valid 100 seconds in the future
    And the DCC UP certificate of country A is used
    And the created rule is wrapped in a CMS message
    And the DCC TLS certificate of country A is used
    And the rule CMS is uploaded
    Then the response should be OK
    And the response status code should be 201

    When the rules of country A are downloaded
    Then the re-downloaded rule exists in version 1.0.0
    Then the re-downloaded rule exists in version 1.0.1

@done
Scenario: Update a Rule with a Rule lower than the current version. There should be an error.
    When create a valid Invalidation Rule for country A
    And the DCC UP certificate of country A is used
    And the created rule is wrapped in a CMS message
    And the DCC TLS certificate of country A is used
    And the rule CMS is uploaded
    Then the response should be OK
    
    When the Version of the rule is changed to 0.9.0
    And the DCC UP certificate of country A is used
    And the created rule is wrapped in a CMS message
    And the DCC TLS certificate of country A is used
    And the rule CMS is uploaded
    Then the response status code should be 400


@done
Scenario: Update a Rule without following the semantic versioning scheme (e.g. 1.3 instead of 1.3.0)
    When create a valid Invalidation Rule for country A
    And the Version of the rule is changed to 1.3
    And the DCC UP certificate of country A is used
    And the created rule is wrapped in a CMS message
    And the DCC TLS certificate of country A is used
    And the rule CMS is uploaded
    Then the response status code should be 400
    

@done
Scenario: After a rule is updated and valid the old rule should not be in the downloaded list
    When create a valid Invalidation Rule for country A
    And the rule becomes valid 1 seconds in the future
    And the DCC UP certificate of country A is used
    And the created rule is wrapped in a CMS message
    And the DCC TLS certificate of country A is used
    And the rule CMS is uploaded
    Then the response should be OK
    
    When the Version of the rule is changed to 1.0.1
    And the rule becomes valid 3 seconds in the future
    And the DCC UP certificate of country A is used
    And the created rule is wrapped in a CMS message
    And the DCC TLS certificate of country A is used
    And the rule CMS is uploaded
    Then the response should be OK
    And the response status code should be 201

    When the rules of country A are downloaded
    Then the re-downloaded rule exists in version 1.0.0
    Then the re-downloaded rule exists in version 1.0.1

    When we wait for 5 seconds
    And the rules of country A are downloaded
    Then the re-downloaded rule exists in version 1.0.1
    Then the re-downloaded rule does not exist in version 1.0.0

