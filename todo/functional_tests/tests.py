from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        # Standard in Selenium tests. Selenium is reasonably good at waiting for
        # pages to complete loading before it tries to do anything, but it’s not perfect.
        # The implicitly_wait tells it to wait a few seconds if it needs to. When asked to find
        # something on the page, Selenium will now wait up to three seconds for it to appear

    def tearDown(self):
        self.browser.quit()

    def find_item_in_list(self, text):
        import time
        time.sleep(3)
        listElem = self.browser.find_element_by_id('todo_list')
        itemElems = listElem.find_elements_by_tag_name('li')
        #print([x.text for x in itemElems])
        #self.assertTrue(
        #    any(x.text == text for x in itemElems)
        #)
        self.assertIn(text, [x.text for x in itemElems])

    def test_edit_a_new_list_and_retrieve_it_later(self):
        # call home page and
        # check that is the proper home page
        #self.browser.get('http://localhost:8000')
        self.browser.get(self.live_server_url)
        headerElem = self.browser.find_element_by_tag_name('h1')

        self.assertIn('ToDo lists', self.browser.title)
        self.assertIn('Your ToDo list', headerElem.text)

        # can enter a new todo item
        inputElem = self.browser.find_element_by_id('add_todo')

        self.assertEqual(
            inputElem.get_attribute('placeholder'),
            'Add new ToDo item'
        )

        # enter a first item and
        # updated page should display the text entered
        inputElem.send_keys('Go for a walk')
        inputElem.send_keys(Keys.ENTER)

        self.find_item_in_list('1: Go for a walk')

        # enter a second item and
        # updated page should display both texts entered
        inputElem = self.browser.find_element_by_id('add_todo')
        inputElem.send_keys('Go another walk')
        inputElem.send_keys(Keys.ENTER)

        self.find_item_in_list('1: Go for a walk')
        self.find_item_in_list('2: Go another walk')

        # page provides a unique url to access previous entries

        # call unique url with previous entries

        self.fail('Have to finish all tests...')
