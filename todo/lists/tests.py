from django.test import TestCase
from django.urls import reverse, resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home
from lists.models import Item


class HomePageTest(TestCase):

    def test_calls_home_view(self):
        found = resolve(reverse('home'))
        self.assertEqual(found.func, home)

    def test_returns_correct_html(self):
        req = HttpRequest()
        res = home(req)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.content.strip().startswith(b'<html>'))
        self.assertIn(b'<title>ToDo lists</title>', res.content)
        self.assertTrue(res.content.strip().endswith(b'</html>'))
        #expected_html = render_to_string('lists/home.html')
        #self.assertEqual(res.content.decode(), expected_html)

    #def test_home_page_displays_saved_list_items(self):
    #    Item.objects.create(text='Item 1')
    #    Item.objects.create(text='Item 2')
    #    req = HttpRequest()
    #    res = home(req)

    #    self.assertIn('Item 1', res.content.decode())
    #    self.assertIn('Item 2', res.content.decode())


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        item1 = Item()
        item1.text = 'A first item'
        item1.save()
        item2 = Item()
        item2.text = 'A second one'
        item2.save()
        saved_items = Item.objects.all()
        saved_item1 = saved_items[0]
        saved_item2 = saved_items[1]

        self.assertEqual(saved_items.count(), 2)
        self.assertEqual(saved_item1.text, 'A first item')
        self.assertEqual(saved_item2.text, 'A second one')


class ListPageTest(TestCase):

    def test_uses_list_template(self):
        res = self.client.get('/lists/unique-name/')
        self.assertTemplateUsed(res, 'lists/list.html')

    def test_displays_all_items(self):
        Item.objects.create(text='Item 1')
        Item.objects.create(text='Item 2')
        res = self.client.get('/lists/unique-name/')
        # Instead of calling the view function directly
        # we use the attribute client of the Django TestCase
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Item 1')
        self.assertContains(res, 'Item 2')
        # Instead of assertIn/response.content.decode()
        # Django provides the assertContains method which knows
        # how to deal with responses and the bytes of their content


class NewListTest(TestCase):

    def send_a_POST_request(self, text):
        #req = HttpRequest()
        #req.method = 'POST'
        #req.POST['add_todo'] = text
        #return home(req)
        return self.client.post(
            '/lists/new',
            data={'add_todo': text}
        )

    def test_saves_a_valid_POST_request(self):
        res = self.send_a_POST_request('A new item')
        self.assertIn('A new item', [x.text for x in Item.objects.all()])

    def test_not_saves_a_blank_POST_request(self):
        res = self.send_a_POST_request('')
        self.assertNotIn('', [x.text for x in Item.objects.all()])

    def test_redirects_after_a_POST_request(self):
        res = self.send_a_POST_request('A new item')

        self.assertEqual(res.status_code, 302)
        self.assertEqual(res['location'], '/lists/unique-name/')
        # or similar check:
        self.assertRedirects(res, '/lists/unique-name/')