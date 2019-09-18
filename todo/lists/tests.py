from django.test import TestCase
from django.urls import reverse, resolve
from django.http import HttpRequest

from django.template.loader import render_to_string
from lists.views import home_page

class HomePageTest(TestCase):

    def test_root_url_goes_to_home_page_view(self):
        found = resolve(reverse('home'))
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        req = HttpRequest()
        res = home_page(req)
        expected_html = render_to_string('lists/home.html')
        self.assertEqual(res.content.decode(), expected_html)
