from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        # Standard in Selenium tests. Selenium is reasonably good at waiting for
        # pages to complete loading before it tries to do anything, but it’s not perfect.
        # The implicitly_wait tells it to wait a few seconds if it needs to. When asked to find
        # something on the page, Selenium will now wait up to three seconds for it to appear

    def tearDown(self):
        self.browser.quit()

    def test_start_a_new_list_and_retrieve_it_later(self):
        # a user visit todo url
        self.browser.get('http://localhost:8000')

        # verify that is in correct page
        self.assertIn('ToDo lists', self.browser.title)
        headerElem = self.browser.find_element_by_tag_name('h1')
        self.assertIn('ToDo', headerElem.text)

        # invited to enter a new todo text item
        inputElem = self.browser.find_element_by_id('add_todo')
        self.assertEqual(
            inputElem.get_attribute('placeholder'),
            'Add new ToDo item'
        )

        # enter the text "Go for a walk"
        inputElem.send_keys('Go for a walk')
        inputElem.send_keys(Keys.ENTER)

        # page updated and display the text entered
        listElem = self.browser.find_element_by_id('todo_list')
        itemElems = listElem.find_elements_by_tag_name('li')
        self.assertTrue(
            any(x.text == 'Go for a walk' for x in itemElems)
        )

        # still invited to enter a new todo text item
        # and enter "Go another walk"
        inputElem.send_keys('Go another walk')
        inputElem.send_keys(Keys.ENTER)

        # page updated again showing both texts entered
        self.assertTrue(
            any(x.text == 'Go for a walk' for x in itemElems)
        )
        self.assertTrue(
            any(x.text == 'Go another walk' for x in itemElems)
        )

        # user noticed page generated a unique url accessing previous entries

        # visit unique url and access previous entries

        self.fail('Have to finish all tests...')


if __name__ == '__main__':
    unittest.main()