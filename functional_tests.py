from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
import time
 
class NewVisitorTest(unittest.TestCase): #(1)
	
	# setUp和tearDown是在每次测试之前和之后运行的特殊方法。使用它们来启动和停止我们的浏览器 
	# 注意它们有点像try / except，即使在测试期间出现错误，tearDown也会运行。
	def setUp(self):
		self.browser = webdriver.Firefox()
		
	def tearDown(self):
		self.browser.quit()

	def check_for_row_in_list_table(self,row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text,[row.text for row in rows])
	
	def test_can_start_a_list_and_retrive_it_later(self):
		# Edith has heard about a cool new online to-do app. She goes 
		# to check out its homepage
		self.browser.get('http://localhost:8000')

		# 使用self.assertIn代替断言。unittest提供了许多像这样的辅助功能来进行测试，
		# 比如assertEqual，assertTrue，assertFalse等等。
		#She notice the page titile and header mention to-do lists
		self.assertIn('To-Do',self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do',header_text)

		# She is invited to enter a to-do item straight away
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)

		# She types "Buy peacock feathers" into a text box(Edith's hobby
		# is tying fly-fishing lures)
		inputbox.send_keys('Buy peacock feathers')
		#inputbox.send_keys('Use peacock feathers to make a fly')

		# When she hits enter, the page updates,and now the page lists
		# "1:Buy peacock feathers to make a fly" (Edith is very methodical)
		inputbox.send_keys(Keys.ENTER)
		time.sleep(1)
		self.check_for_row_in_list_table('1:Buy peacock feathers')

		
		#self.assertTrue(
		#	any(row.text == '1:Buy peacock feathers' for row in rows),
		#	f"New to-do item did not appear in table.Contents were:\n{table.text}"
		#)

		# There is still a text box inviting her to add anther item. She
		# enters "Use peacock feathers to make a fly" (Edith is very methodical)
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Use peacock feathers to make a fly')
		inputbox.send_keys(Keys.ENTER)
		time.sleep(1)

		# The page updates again, and now shows both itmes on hre list
		self.check_for_row_in_list_table('1:Buy peacock feathers')
		self.check_for_row_in_list_table('2:Use peacock feathers to make a fly')

		# Edith wonders whether the site will remember her lists ,Then shse sees
		# that the site has generated a unique URL for her -- there is some
		# explanatory text to that effect.

		# She visits that URL - her to -do list is still there

		#Satisfied ,she goes back to sleep
		self.fail('Finish the test!')	#self.fail无论如何都会失败，产生错误信息。 我们用它作为完成测试的提醒。

# main function model
if __name__=='__main__':
	unittest.main(warnings='ignore')