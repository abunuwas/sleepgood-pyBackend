from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

	def setUp(self): 
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(5)

	def tearDown(self):
		self.browser.quit()

	def test_can_access_home_page_and_see_products_listed(self):
		##John has a lot of things he doen't use anymore and wish to sell. 
		##He's heard there's a new website which could serve well his purpose. 
		##He goes to check out the hompage of that website.
		self.browser.get('http://localhost:8000/app') 

		##He notices the page title and header mention sell-everything! It looks
		##like he's found what he needs.
		self.assertIn('Sell Everything!', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('Sell Everything!', header_text)

		##First thing in the hompage, he sees a list of products which other users
		##are selling. 
		table = self.browser.find_element_by_id('id_products_table')
		#rows = table.find_elements_by_tag_name('tr')
		#self.assertTrue(
		#	any(row.text == 'My watch' for row in rows)
		#	)

		self.fail('Finish the test!')

	def test_user_registers_and_upload_first_product(self):
		##He decides that he wants to upload his own items to the website, in the
		##hope that he might be able to sell them at a good price. He goes to the
		##register site.
		self.browser.get('http://localhost:8000/register') 

		##He finds a registration form that asks him to enter his first name, 
		##last name, username, address, email, and requests him to confirm 
		##his email address. 
		input_first_name = self.browser.find_element_by_id('id_first_name')
		self.assertEqual(
			input_first_name.get_attribute('placeholder'), 
			'e.g. John'
			)
		input_last_name = self.browser.find_element_by_id('id_last_name')
		input_username = self.browser.find_element_by_id('id_username')
		input_email = self.browser.find_element_by_id('id_email')
		input_confirm_email = self.browser.find_element_by_id('id_confirm_email')
		input_address = self.browser.find_element_by_id('id_address')
		input_password = self.browser.find_element_by_id('id_password')
		input_confirm_password = self.browser.find_element_by_id('id_confirm_password')

		##John is not the kind of person who loves to spend hours registering
		##in a website, and he's not a fan of giving away too much data about him,
		##so he just introduces a username 'john', his address 'Jamaica', and
		##his password 'asdf1234', which the website requires to type a second time
		##to confirm. 		
		input_username.send_keys('john')
		input_password.send_password('asdf1234')
		input_confirm_password('asdf1234')
		#browser.find.submit(Keys.ENTER)

		##The site accepts his requests and redirects him to his account site, which
		##welcomes him with a a personalized message
		welcome_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('Welcome john!', welcome_text)

		##He clicks
		##on the link "Sell something!", which redirects him to a form for uploading
		##items. 
		upload_link = self.browser.find_element_by_id('upload-product')
		#upload_link.click()

		##He uploads a watch for which he provides the following details:
		##title: My watch
		##description: My fancy Swiss watch
		##price: 2000
		##category: watches
		input_title = self.browser.find_element_by_id('id_title')
		input_description = self.browser.find_element_by_id('id_description')
		input_price = self.browser.find_element_by_id('id_price')
		input_category = self.browser.find_element_by_id('id_category')

##After uploading the data, the site validates it and redirects him back to
##his account site,where he sees his watch included in the list of items
##uploaded by him.

##He then navigates back to the homepage to check whether the general list of
##products already includes his.

##He sorts by category - watches, and finds it!

##Happy enough, John decides to leave the site for now, so he logs out and closes
##the browser.

if __name__ == '__main__':
	unittest.main()