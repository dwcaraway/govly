from behave import *

@given('I am on the homepage')
def step_impl(context):
    context.browser.get("http://%s:%s/" % (context.app.host, context.app.port) )
        
@then('the tenet3 logo is displayed')
def step_impl(context):
    elem = context.browser.find_element_by_css_selector(".tenet3-logo img")
    assert 'Tenet 3, LLC' == elem.get_attribute("alt")
    assert "logo-transparent.png" in elem.get_attribute("src")

@then('the metra logo is displayed')
def step_impl(context):
    elem = context.browser.find_element_by_css_selector(".metra-logo img")
    assert 'Tenet 3, LLC' == elem.get_attribute("alt")
    assert "MeTRA-small.png" in elem.get_attribute("src")

@then('the "{tab}" tab is selected')
def step_impl(context, tab):
	tab_text = tab.lower()
	elem = context.browser.find_element_by_css_selector("li.active a")
	assert tab_text in elem.get_attribute("href")
