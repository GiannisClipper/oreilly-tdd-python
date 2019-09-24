from .base import FunctionalTest
from unittest import skip

class ItemValidationTest(FunctionalTest):

    #@skip
    def test_not_add_empty_items(self): 
        # user calls home page 
        self.browser.get(self.live_server_url)

        # user enters empty item and
        # page refreshes with an error message
        self.enter_item_in_list('')
        error = self.browser.find_element_by_css_selector('.error')
        self.assertEqual(error.text, 'Empty items not allowed')

        # user enter some text and now works
        self.enter_item_in_list('Go for shopping')
        self.find_item_in_list('1: Go for shopping')

        # user enters empty item again and
        # page refreshes with an error message
        self.enter_item_in_list('')
        self.find_item_in_list('1: Go for shopping')
        error = self.browser.find_element_by_css_selector('.error')
        self.assertEqual(error.text, 'Empty items not allowed')

        # user enters some text again and works
        self.enter_item_in_list('Go for a coffee')
        self.find_item_in_list('1: Go for shopping')
        self.find_item_in_list('2: Go for a coffee')

        #self.fail('Have to finish all tests...')
