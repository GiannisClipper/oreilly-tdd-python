from django.test import TestCase
from django.urls import reverse, resolve
from django.http import HttpRequest

from lists.views import home_page

class HomePageTest(TestCase):

    def test_root_url_goes_to_home_page_view(self):
        found = resolve(reverse('home'))
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        req = HttpRequest()
        res = home_page(req)
        self.assertTrue(res.content.startswith(b'<html>'))
        self.assertIn(b'<title>ToDo lists</title>', res.content)
        self.assertTrue(res.content.endswith(b'</html>'))