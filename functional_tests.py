from selenium import webdriver
import unittest
 
class NewVisitorTest(unittest.TestCase): #(1)
	
	# setUp和tearDown是在每次测试之前和之后运行的特殊方法。使用它们来启动和停止我们的浏览器 
	# 注意它们有点像try / except，即使在测试期间出现错误，tearDown也会运行。
	def setUp(self):
		self.browser = webdriver.Firefox()
		
	def tearDown(self):
		self.browser.quit()
	
	def test_can_start_a_list_and_retrive_it_later(self):
		# Edith has heard about a cool new online to-do app. She goes 
		# to check out its homepage
		self.browser.get('http://localhost:8000')

		# 使用self.assertIn代替断言。unittest提供了许多像这样的辅助功能来进行测试，
		# 比如assertEqual，assertTrue，assertFalse等等。
		#She notice the page titile and header mention to-do lists
		self.assertIn('To-Do',self.browser.title)
		self.fail('Finish the test!')	#self.fail无论如何都会失败，产生错误信息。 我们用它作为完成测试的提醒。

		# She is invited to enter a to-do item straight away

		# She types "Buy peacock feathers" into a text box(Edith's hobby
		# is tying fly-fishing lures)

		# When she hits enter, the page updates,and now the page lists
		# "1:Buy peacock feathers to make a fly" (Edith is very methodical)

		# There is still a text box inviting her to add anther item. She
		# enters "Use peacock feathers to make a fly" (Edith is very methodical)

		# The page updates again, and now shows both itmes on hre list

		# Edith wonders whether the site will remember her lists ,Then shse sees
		# that the site has generated a unique URL for her -- there is some
		# explanatory text to that effect.

		# She visits that URL - her to -do list is still there

		#Satisfied ,she goes back to sleep

# main function
if __name__=='__main__':
	unittest.main(warnings='ignore')