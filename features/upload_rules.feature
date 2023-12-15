Feature: Upload Rules

Tests to upload new rules

Scenario Outline: Upload a valid invalidation Rule. 
    (Invalidation Rule is used because it can be deleted automatically)

    When create a valid <ruletype> Rule for country A
    And the DCC UP certificate of country A is used
    And the created rule is wrapped in a CMS message
    And the DCC TLS certificate of country A is used
    And the rule CMS is uploaded
    Then the response should be OK

    When the rules of country A are downloaded
    Then the re-downloaded rule exists in version 1.0.0

    Examples:
        | ruletype     | 
        | Acceptance   | 
        | Invalidation |

Scenario Outline: Content-type headers
    The content type header of rules normally in the test 
    is "application/cms-text" but it can also be "application/cms" 
    like for the certificates

    When create a valid <ruletype> Rule for country A
    And the DCC UP certificate of country A is used
    And the created rule is wrapped in a CMS message
    And the DCC TLS certificate of country A is used
    And the rule CMS is uploaded as cms-text
    Then the response should be OK

    When the rules of country A are downloaded
    Then the re-downloaded rule exists in version 1.0.0

    Examples:
        | ruletype     | 
        | Acceptance   | 
        | Invalidation |

Scenario Outline: Unauthenticated user
    Upload a Rule with an unauthenticated certificate. 
    There should be an error and the Response Code should be 401.

    When create a valid <ruletype> Rule for country C
    And the DCC UP certificate of country C is used
    And the created rule is wrapped in a CMS message
    And the DCC TLS certificate of country C is used
    And the rule CMS is uploaded
    Then the response status code should be 4xx

    When the DCC TLS certificate of country A is used
    And the rules of country C are downloaded
    Then the re-downloaded rule does not exist in version 1.0.0

    Examples:
        | ruletype     | 
        | Acceptance   | 
        | Invalidation |

Scenario Outline: Wrong country authentication
    Upload a Rule with a TLS certificate of another country. 
    There should be an error and the status code should be 400.

    When create a valid <ruletype> Rule for country A
    And the DCC UP certificate of country B is used
    And the created rule is wrapped in a CMS message
    And the DCC TLS certificate of country B is used
    And the rule CMS is uploaded
    Then the response status code should be 4xx

    When the rules of country A are downloaded
    Then the re-downloaded rule does not exist in version 1.0.0

    Examples:
        | ruletype     | 
        | Acceptance   | 
        | Invalidation |

Scenario Outline: Trailing data
    Upload a Rule with trailing data after the main payload. 
    The API should reject the rule. 
    
    When create a valid <ruletype> Rule for country A
    And the DCC UP certificate of country A is used
    And the created rule is wrapped in a CMS message with extra data
    And the DCC TLS certificate of country A is used
    And the rule CMS is uploaded
    Then the response status code should be 4xx

    When the rules of country A are downloaded
    Then the re-downloaded rule does not exist in version 1.0.0

    Examples:
        | ruletype     | 
        | Acceptance   | 
        | Invalidation |