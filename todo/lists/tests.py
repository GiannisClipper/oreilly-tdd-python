from django.test import TestCase
from django.urls import reverse, resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item

class HomePageTest(TestCase):

    def test_root_url_calls_home_page_view(self):
        found = resolve(reverse('home'))

        self.assertEqual(found.func, home_page)

    def test_home_page_view_returns_correct_html(self):
        req = HttpRequest()
        res = home_page(req)

        self.assertTrue(res.content.strip().startswith(b'<html>'))
        self.assertIn(b'<title>ToDo lists</title>', res.content)
        self.assertTrue(res.content.strip().endswith(b'</html>'))
        #expected_html = render_to_string('lists/home.html')
        #self.assertEqual(res.content.decode(), expected_html)

    def test_home_page_can_handle_a_POST_request(self):
        req = HttpRequest()
        req.method = 'POST'
        req.POST['add_todo'] = 'A new todo item'
        res = home_page(req)
        self.assertIn('A new todo item', res.content.decode())


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        item1 = Item()
        item1.text = 'The first item'
        item1.save()
        item2 = Item()
        item2.text = 'The second one'
        item2.save()
        saved_items = Item.objects.all()
        saved_item1 = saved_items[0]
        saved_item2 = saved_items[1]

        self.assertEqual(saved_items.count(), 2)
        self.assertEqual(saved_item1.text, 'The first item')
        self.assertEqual(saved_item2.text, 'The second one')