from .base import FunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

MAX_WAIT = 5


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_todo_list(self):

        # Edith는 멋진 to-do app을 알게 되었다.
        # 그녀는 홈페이지에 방문한다.
        self.browser.get(self.live_server_url)

        # 그녀는 홈페이지 title과 header이
        # "To-Do"로 시작함을 확인
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        # 그녀는 to-do 항목을 입력할 수 있도록 초대 받음
        # placeholder를 확인(<input placeholder="..">)
        inputbox = self.get_item_input_box()
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        # 그녀는 "Buy peacock feathers"를 텍스트 박스에 입력
        inputbox.send_keys("Buy peacock feathers")
        # 엔터를 누르면, 페이지가 업데이트 되고,
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy peacock feathers")
        # "Use peacock feathers to make a fly" 입력 & 엔터
        inputbox = self.get_item_input_box()
        inputbox.send_keys("Use peacock feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy peacock feathers")
        self.wait_for_row_in_list_table("2: Use peacock feathers to make a fly")

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith starts a new to-do lists
        self.browser.get(self.live_server_url)
        inputbox = self.get_item_input_box()
        inputbox.send_keys("Buy peacock feathers")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy peacock feathers")

        # she notices that her list has a unique URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, "lists/.+")

        # Now a new user, Francis, comes along to the site.

        ## We delete all the browser's cookies
        ## as a way of simulating a brand new user session
        self.browser.delete_all_cookies()

        # Francis visites the home page.
        # There is no sign of Edith's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertNotIn("make a fly", page_text)

        # Francis starts a new list by entering a new item.
        # He is less interesting than Edith...
        inputbox = self.get_item_input_box()
        inputbox.send_keys("Buy milk")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, edith_list_url)

        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertIn("Buy milk", page_text)
