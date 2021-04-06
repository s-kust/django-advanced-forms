from django.test import LiveServerTestCase
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import unittest

# This test is only partial, just to demonstrate my skills
# The main thing it does is add a new column 
# to the existing schema. The parameters of the new column 
# (name, type, order) differ from the default parameters. 
# After adding, the results are checked, 
# and then the newly added column is removed.
# TODO: Test new schema addition and removal.

class FunctionalTests(LiveServerTestCase):
    fixtures = ['fixtures/initial_data.json']
    
    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(10)

    @classmethod
    def tearDownClass(self):
        self.browser.quit()
        super().tearDownClass()
        
    def test_all_pages_functions(self):   
        
        # start from homepage
        
        self.browser.get('%s%s' % (self.live_server_url, '/'))
        delay = 10 # seconds
        try:
            myElem = WebDriverWait(self.browser, delay).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'schemas list')))
            # print ("Home Page is ready!")
        except TimeoutException:
            print ("Home Page loading took too much time!")
        self.assertIn ('Django People', self.browser.title)
        self.assertIn ('Create new schema', self.browser.page_source)
        self.assertIn ('Modified', self.browser.page_source)
        
        # go to "Create new schema" page
        # TODO: tests for new schema addition and deletion fuctionality
        
        self.browser.find_element_by_xpath('//input[@value="Create new schema"]').click()        
        try:
            myElem = WebDriverWait(self.browser, delay).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'schemas list')))
        except TimeoutException:
            print ("Create New Schema Page loading took too much time!")
        self.assertIn ('Django People', self.browser.title)
        self.assertIn ('<legend>New Schema</legend>', self.browser.page_source)        
        time.sleep(3)
        
        # go back to the list of all schemas
        
        self.browser.find_element_by_xpath("//a[@href='/']").click();
        self.assertIn ('Django People', self.browser.title)
        self.assertIn ('Create new schema', self.browser.page_source)
        self.assertIn ('Modified', self.browser.page_source)
        time.sleep(3)
        
        # go to the specific schema (id=5) page
        
        self.browser.find_element_by_xpath("//form[@action='/schema/5/' and @method='post']//input[@type='submit' and @value='Edit']").click()
        try:
            myElem = WebDriverWait(self.browser, delay).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'schemas list')))
        except TimeoutException:
            print ("Edit Schema Page loading took too much time!")
        
        self.assertIn ('Int First Column 5', self.browser.page_source) 
        # self.assertIn ('I want to add a new column', self.browser.page_source)
        
        # add a new column to the schema with parameters 
        # that differ from the default parameters
        
        self.browser.find_element_by_xpath("//input[@type='text' and @name='add_column_name']").send_keys(Keys.CONTROL + "a")
        self.browser.find_element_by_xpath("//input[@type='text' and @name='add_column_name']").send_keys(Keys.DELETE)
        self.browser.find_element_by_xpath("//input[@type='text' and @name='add_column_name']").send_keys("New column in Selenium Integration Test")
        
        self.browser.find_element_by_xpath("//select[@name='add_column_type']/option[text()='Full Name']").click()
        
        self.browser.find_element_by_xpath("//input[@type='number' and @name='add_column_order']").send_keys(Keys.CONTROL + "a")
        self.browser.find_element_by_xpath("//input[@type='number' and @name='add_column_order']").send_keys(Keys.DELETE)
        self.browser.find_element_by_xpath("//input[@type='number' and @name='add_column_order']").send_keys("54")        
        time.sleep(4)
        
        self.browser.find_element_by_xpath("//input[@type='submit' and @value='Add New Column']").click()
        try:
            myElem = WebDriverWait(self.browser, delay).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'schemas list')))
            # print ("Home Page is ready!")
        except TimeoutException:
            print ("Edit Schema Page loading took too much time!")
            
        # check the results of adding a new column
        
        self.assertIn ('New column in Selenium Integration Test', self.browser.page_source)
        self.assertIn ('value="54" min="0" class="numberinput form-control"', self.browser.page_source)
        self.assertNotIn ('Hello World', self.browser.page_source)
        time.sleep(8)
        
        # remove the newly added column and check the results 
        
        self.browser.find_element_by_xpath("//input[@type='text' and @value='New column in Selenium Integration Test']//following::input[@type='submit' \
        and @value='Delete']").click()
        try:
            myElem = WebDriverWait(self.browser, delay).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'schemas list')))
            # print ("Home Page is ready!")
        except TimeoutException:
            print ("Edit Column Details Page loading took too much time!")
        self.assertNotIn ('New column in Selenium Integration Test', self.browser.page_source)
        self.assertNotIn ('value="54" min="0" class="numberinput form-control"', self.browser.page_source)
        self.assertNotIn ('Hello World', self.browser.page_source)
        time.sleep(4)

if __name__ == '__main__':
    # unittest.main(warnings='ignore')
    unittest.main()