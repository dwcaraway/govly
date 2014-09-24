from selenium import webdriver
from flask import Flask
import liveandletdie
import sure
import logging
import unittest


class FunctionalTest(unittest.TestCase):

    def setup(self):
        """Setup servers and selenium web drivers prior to tests"""
        #Create the test server for browser testing
        self.app = liveandletdie.Flask('../../run.py', port=5555, timeout=10.0)
        self.app.live(kill=True)    
        self.browser = webdriver.PhantomJS() 

    def teardown(self):
        """Close the running test server and webdrivers"""
        self.app.die()
        self.browser.quit()

    def test_homepage(self):
        """The sum should equal the combination of the two parts"""
        (2+2).should.equal(4)
