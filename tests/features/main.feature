Feature: Security Dashboard 

    Scenario: The Tenet3 and Metra logos display on home page and Edit tab is default 
        Given I am on the homepage
        Then the tenet3 logo is displayed
        And the metra logo is displayed
        And the "Edit" tab is selected

        #    Scenario: The edit view displays Tools and Properties areas 
        #Given I am on the homepage
        # When the edit view is selected
        #Then the "Tools" area is displayed
        #And the "Properties" area is displayed
