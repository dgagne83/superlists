from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		
	def tearDown(self):
		self.browser.quit()
		
	def test_can_start_a_list_and_retrieve_it_later(self):
		# During the course of the day, I need to generate
		# to-do lists. To facilitate the process, I would like 
		# to access a web page
		self.browser.get('http://localhost:8000')

		# I notice the tab says "To-Do" as the header and title
		self.assertIn('To-Do', self.browser.title)
		self.fail('Finish the test!')

		# I'm invited to enter a to-do item right away

		# I type "buy peacock feathers" into a text box
		# so i can start to make my fishing lures

		# I hit enter and the page updates with
		# "1: Buy peacock feathers" as a to-do list item

		# there is still a text box inviting to add another item
		# I enter "Use peacock feathers to make a fly"

		# the page updates again with both items

		# I wonder whether the site will remember my list
		# then I notice the site generated a unique url --
		# there is some explanatory text

		# I visit the url and the text is still there

		# satisfied, I close my computer

if __name__ == '__main__':
	unittest.main(warnings='ignore')

