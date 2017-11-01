from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

class NewVisitorTest(FunctionalTest):				

	def test_can_start_a_list_for_one_user(self):
		# During the course of the day, I need to generate
		# to-do lists. To facilitate the process, I would like
		# to access a web page
		self.browser.get(self.live_server_url)

		# I notice the tab says "To-Do" as the header and title
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		# I'm invited to enter a to-do item right away
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)

		# I type "buy peacock feathers" into a text box
		# so i can start to make my fishing lures
		inputbox.send_keys('Buy peacock feathers')

		# I hit enter and the page updates with
		# "1: Buy peacock feathers" as a to-do list item
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy peacock feathers')

		# there is still a text box inviting to add another item
		# I enter "Use peacock feathers to make a fly"
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Use peacock feathers to make a fly')
		inputbox.send_keys(Keys.ENTER)

		# the page updates again with both items
		self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
		self.wait_for_row_in_list_table('1: Buy peacock feathers')
	
	def test_multiple_users_can_start_lists_at_different_urls(self):
		# I start a new to-do list
		self.browser.get(self.live_server_url)
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy peacock feathers')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy peacock feathers')
		
		# I notice the list has a unique url
		danial_list_url = self.browser.current_url
		self.assertRegex(danial_list_url, '/lists/.+')
		
		# a new user, francis comes to the site
		
		## we use a new browser session to make sure no information
		## from danial's list is coming through from cookies, etc
		self.browser.quit()
		self.browser = webdriver.Firefox()
		
		# francis visits the home home page and there is no
		# sign of danials list
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertNotIn('make a fly', page_text)
		
		# francis begins to enter list items
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')
		
		# francis gets his own unique url
		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url, '/lists/.+')
		self.assertNotEqual(francis_list_url, danial_list_url)
		
		# still no sign of danials url
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertIn('Buy milk', page_text)
		
		# satisfied, francis closes his computer
