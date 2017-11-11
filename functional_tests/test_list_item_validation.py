from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):
	
	def test_cannot_add_empty_list_items(self):
		# I go to the home page and accidentally try to submit
		# an empty list item. I hit Enter on the empty input box
		self.browser.get(self.live_server_url)
		self.get_item_input_box().send_keys(Keys.ENTER)
		
		# The home page refreshes, and there is an error message saying
		# that list items cannot be blank
		self.wait_for(lambda: self.assertEqual(
			self.browser.find_element_by_css_selector('.has-error').text,
			"You can't have an empty list item"
		))

		# I try again with some text for the item, which now works
		self.get_item_input_box().send_keys('Buy milk')
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')
		
		# Perversely, I now decide to submit a second blank list item
		self.get_item_input_box().send_keys(Keys.ENTER)
		
		# I receive a similar warning on the list page
		self.wait_for(lambda: self.assertEqual(
			self.browser.find_element_by_css_selector('.has-error').text,
			"You can't have an empty list item"
		))

		# And I can correct it by filling some text in
		self.get_item_input_box().send_keys('Make tea')
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')
		self.wait_for_row_in_list_table('2: Make tea')