from selenium import webdriver
from flask import Flask
import liveandletdie

def before_all(context):
	"""Setup servers and selenium web drivers prior to BDD tests"""
	#Create the test server for browser testing
	context.app = liveandletdie.Flask('../run.py', port=5555, timeout=10.0)
	context.app.live(kill=True)    
	context.browser = webdriver.PhantomJS() 

def after_all(context):
	"""Close the running test server and webdrivers"""
	context.app.die()
	context.browser.quit()
