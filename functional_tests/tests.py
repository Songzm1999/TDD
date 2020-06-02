from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from django.test import LiveServerTestCase
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10
 
class NewVisitorTest(LiveServerTestCase): #(1)
	
	# setUp和tearDown是在每次测试之前和之后运行的特殊方法。使用它们来启动和停止我们的浏览器 
	# 注意它们有点像try / except，即使在测试期间出现错误，tearDown也会运行。
	def setUp(self):
		self.browser = webdriver.Firefox()
		
	def tearDown(self):
		self.browser.quit()

	def wait_for_row_in_list_table(self,row_text):
		start_time = time.time()
		while True:
			try:
				table = self.browser.find_element_by_id('id_list_table')
				rows = table.find_elements_by_tag_name('tr')
				self.assertIn(row_text,[row.text for row in rows])
				return
			except (AssertionError,WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)

	def check_for_row_in_list_table(self,row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text,[row.text for row in rows])
	
	def test_can_start_a_list_for_one_user(self):
		# Edith has heard about a cool new online to-do app. She goes 
		# to check out its homepage
		self.browser.get(self.live_server_url)

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
		self.wait_for_row_in_list_table('1:Buy peacock feathers')

		
		#self.assertTrue(
		#	any(row.text == '1:Buy peacock feathers' for row in rows),
		#	f"New to-do item did not appear in table.Contents were:\n{table.text}"
		#)

		# There is still a text box inviting her to add anther item. She
		# enters "Use peacock feathers to make a fly" (Edith is very methodical)
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Use peacock feathers to make a fly')
		inputbox.send_keys(Keys.ENTER)

		# The page updates again, and now shows both itmes on hre list
		self.wait_for_row_in_list_table('1:Buy peacock feathers')
		self.wait_for_row_in_list_table('2:Use peacock feathers to make a fly')

		# Edith wonders whether the site will remember her lists ,Then shse sees
		# that the site has generated a unique URL for her -- there is some
		# explanatory text to that effect.

		# She visits that URL - her to -do list is still there

		#Satisfied ,she goes back to sleep
		# self.fail('Finish the test!')	#self.fail无论如何都会失败，产生错误信息。 我们用它作为完成测试的提醒。
	
	def test_multiple_users_can_start_lists_at_different_urls(self):
        # 乔伊新建一个待办事项清单
		self.browser.get(self.live_server_url)
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy peacock feathers')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1:Buy peacock feathers')

		# 她注意到清单有个唯一的URL
		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/.+')

		# 现在一名焦作弗朗西斯的新用户访问了网站

		## 我们使用了一个新浏览器会话
		## 确保乔伊的信息不会从cookie中泄露出去
		self.browser.quit()
		self.browser = webdriver.Firefox()

		# 弗朗西斯访问首页
		# 页面中看不到乔伊的清单
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertNotIn('make a fly', page_text)

		# 弗朗西斯输入一个新待办事项，新建一个清单
		# 他不像乔伊那样兴趣盎然
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1:Buy milk')

		# 弗朗西斯获得了他的唯一URL
		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url, '/lists/.+')
		self.assertNotEqual(francis_list_url, edith_list_url)

		# 这个页面还是没有乔伊的清单
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertIn('Buy milk', page_text)

		#两个人都很满意，然后去休息了

	def test_layout_and_styling(self):
		# 乔伊访问首页
		self.browser.get(self.live_server_url)
		self.browser.set_window_size(1024, 768)
		# 她看到输入框完美地居中显示
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta=10
		)
		# 她新建了一个清单，看到输入框仍完美地居中显示
		inputbox.send_keys('testing')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1:testing')
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta=10
		)