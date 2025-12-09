Feature: Validate did json trustlist instance against a JSON schema from tng-cdn repo

  Scenario Outline: Validate DID Document instance against schema
    Given the schema file "<schema_file>" is fetched from GitHub cdn repository
    And the instance file "<instance_file>" is fetched from GitHub cdn repository
    When validate the instance against the schema
    Then the instance should be valid according to the schema

    Examples:
      | schema_file                      | instance_file         |  |
      | schema/did-trustlist-schema.json | v2/trustlist/did.json |  |