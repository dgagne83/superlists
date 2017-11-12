from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):
	
	def test_cannot_add_empty_list_items(self):
		# I go to the home page and accidentally try to submit
		# an empty list item. I hit Enter on the empty input box
		self.browser.get(self.live_server_url)
		self.get_item_input_box().send_keys(Keys.ENTER)
		
		# The browser intercepts the request
		self.wait_for(lambda: self.browser.find_element_by_css_selector(
			'#id_text:invalid'
		))

		# I try again with some text for the item, the error disappears
		self.get_item_input_box().send_keys('Buy milk')
		self.wait_for(lambda: self.browser.find_element_by_css_selector(
			'#id_text:valid'
		))
		
		# the item submits successfully
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')
		
		# Perversely, I now decide to submit a second blank list item
		self.get_item_input_box().send_keys(Keys.ENTER)
		
		# I receive a similar warning on the list page
		self.wait_for_row_in_list_table('1: Buy milk')
		self.wait_for(lambda: self.browser.find_element_by_css_selector(
			'#id_text:invalid'
		))

		# And I can correct it by filling some text in
		self.get_item_input_box().send_keys('Make tea')
		self.wait_for(lambda: self.browser.find_element_by_css_selector(
			'#id_text:valid'
		))
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')
		self.wait_for_row_in_list_table('2: Make tea')
		
	def test_cannot_add_duplicate_items(self):
		# I go to the homepage and start a new list
		self.browser.get(self.live_server_url)
		self.get_item_input_box().send_keys('Buy sugar')
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy sugar')
		
		# I accidentally try and enter a duplicate item
		self.get_item_input_box().send_keys('Buy sugar')
		self.get_item_input_box().send_keys(Keys.ENTER)
		
		# I see a helpful error message
		self.wait_for(lambda: self.assertEqual(
			self.browser.find_element_by_css_selector('.has-error').text,
			"You've already got this in your list"
		))