from django.core import mail
from selenium.webdriver.common.keys import Keys
import re

from .base import FunctionalTest

TEST_EMAIL = 'gagne.danial@gmail.com'
SUBJECT = 'Your login link for Superlists'

class LoginTest(FunctionalTest):
	
	def test_can_get_email_link_to_login(self):
		# I go to the superlists site and notice a "Log In" section 
		# for the first time. It's saying to enter a valid email address
		self.browser.get(self.live_server_url)
		self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
		self.browser.find_element_by_name('email').send_keys(Keys.ENTER)
		
		# A message appears saying a valid email has been sent
		self.wait_for(lambda: self.assertIn(
			"Check your email",
			self.browser.find_element_by_tag_name('body').text
		))
		
		# I check the email and find a message
		email = mail.outbox[0]
		self.assertIn(TEST_EMAIL, email.to)
		self.assertEqual(email.subject, SUBJECT)
		
		# It has a url link in it
		self.assertIn('Use this link to log in', email.body)
		url_search = re.search(r'http://.+/.+$', email.body)
		if not url_search:
			self.fail(f'Could not find url in email body:\n{email.body}')
		url = url_search.group(0)
		self.assertIn(self.live_server_url, url)
		
		# I click it
		self.browser.get(url)
		
		# It logs me in
		self.wait_to_be_logged_in(email=TEST_EMAIL)
		
		# I press Logout
		self.browser.find_element_by_link_text('Log out').click()
		
		# It logs me out
		self.wait_to_be_logged_out(email=TEST_EMAIL)