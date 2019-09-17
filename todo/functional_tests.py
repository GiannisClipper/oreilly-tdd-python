from selenium import webdriver
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

        # verify through title that is in correct page
        self.assertIn('ToDo lists', self.browser.title)

        # invited to enter a new todo text item

        # enter the text "Go for a walk"

        # page updated and display the text entered

        # still invited to enter a new todo text item

        # enter "Go another walk"

        # page updated again showing both texts entered

        # user noticed page generated a unique url accessing previous entries

        # visit unique url and access previous entries

        self.fail('Have to finish all tests...')


if __name__ == '__main__':
    unittest.main()