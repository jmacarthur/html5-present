Feature: Creating web pages

  Scenario: Create a basic presentation
    Given we have the example presentation
    and the output directory is empty
    When we run convert on it
    Then the output directory contains the first slide