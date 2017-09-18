from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()
		
	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])

	def test_can_start_a_list_and_retrieve_it_later(self):
		# During the course of the day, I need to generate
		# to-do lists. To facilitate the process, I would like
		# to access a web page
		self.browser.get('http://localhost:8000')

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
		time.sleep(1)

		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn('1: Buy peacock feathers', [row.text for row in rows])

		# there is still a text box inviting to add another item
		# I enter "Use peacock feathers to make a fly"
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)
		inputbox.send_keys('Use peacock feathers to make a fly')
		inputbox.send_keys(Keys.ENTER)
		time.sleep(1)

		# the page updates again with both items
		self.check_for_row_in_list_table('1: Buy peacock feathers')
		self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
		
		# I wonder whether the site will remember my list
		# then I notice the site generated a unique url --
		# there is some explanatory text
		self.fail('Finish the test!')

		# I visit the url and the text is still there

		# satisfied, I close my computer

if __name__ == '__main__':
	unittest.main(warnings='ignore')

