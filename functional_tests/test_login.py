from django.core import mail
from selenium.webdriver.common.keys import Keys
import re
import os
import poplib
import time

from .base import FunctionalTest

SUBJECT = 'Your login link for Superlists'


class LoginTest(FunctionalTest):

	def wait_for_email(self, test_email, subject):
		if not self.staging_server:
			email = mail.outbox[0]
			self.assertIn(test_email, email.to)
			self.assertEqual(email.subject, subject)
			return email.body
		
		email_id = None
		start = time.time()
		inbox = poplib.POP3_SSL('pop.gmail.com')
		try:
			inbox.user(test_email)
			inbox.pass_(os.environ['GMAIL_PASSWORD'])
			while time.time() - start < 60:
				# get 10 newest messages
				count, _ = inbox.stat()
				for i in reversed(range(max(1, count - 10), count + 1)):
					print('getting msg', i)
					_, lines, __ = inbox.retr(i)
					lines = [l.decode('utf8') for l in lines]
					if f'Subject: {subject}' in lines:
						email_id = i
						body = '\n'.join(lines)
						return body
				time.sleep(5)
		finally:
			if email_id:
				inbox.dele(email_id)
			inbox.quit()
	
	def test_can_get_email_link_to_login(self):
		# I go to the superlists site and notice a "Log In" section 
		# for the first time. It's saying to enter a valid email address
		if self.staging_server:
			test_email = 'gagne.danial@gmail.com'
		else:
			test_email = 'danial@example.com'
		
		self.browser.get(self.live_server_url)
		self.browser.find_element_by_name('email').send_keys(test_email)
		self.browser.find_element_by_name('email').send_keys(Keys.ENTER)
		
		# A message appears saying a valid email has been sent
		self.wait_for(lambda: self.assertIn(
			'Check your email',
			self.browser.find_element_by_tag_name('body').text
		))
		
		# I check the email and find a message
		body = self.wait_for_email(test_email, SUBJECT)
		
		# It has a url link in it
		self.assertIn('Use this link to log in', body)
		url_search = re.search(r'http://.+/.+$', body)
		if not url_search:
			self.fail(f'Could not find url in email body:\n{body}')
		url = url_search.group(0)
		self.assertIn(self.live_server_url, url)
		
		# I click it
		self.browser.get(url)
		
		# It logs me in
		self.wait_to_be_logged_in(email=test_email)
		
		# I press Logout
		self.browser.find_element_by_link_text('Log out').click()
		
		# It logs me out
		self.wait_to_be_logged_out(email=test_email)