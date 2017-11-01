from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):
	
	def test_cannot_add_empty_list_items(self):
		# I go to the home page and accidentally try to submit
		# an empty list item. I hit Enter on the empty input box

		# The home page refreshes, and there is an error message saying
		# that list items cannot be blank

		# I try again with some text for the item, which now works

		# Perversely, I now decide to submit a second blank list item

		# I receive a similar warning on the list page

		# And I can correct it by filling some text in
		self.fail('write me!')