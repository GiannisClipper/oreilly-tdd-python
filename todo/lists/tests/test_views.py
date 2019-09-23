from django.test import TestCase
from django.urls import reverse, resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home
from lists.models import Item, List


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


class ListPageTest(TestCase):

    def test_uses_list_template(self):
        List.objects.create()
        res = self.client.get(f'/lists/{List.objects.first().id}/')
        self.assertTemplateUsed(res, 'lists/list.html')

    def test_displays_all_items_of_a_list(self):
        list1 = List.objects.create()
        Item.objects.create(text='Item 1', list=list1)
        Item.objects.create(text='Item 2', list=list1)

        list2 = List.objects.create()
        Item.objects.create(text='Item 1b', list=list2)
        Item.objects.create(text='Item 2b', list=list2)

        res = self.client.get(f'/lists/{list1.id}/')

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Item 1')
        self.assertContains(res, 'Item 2')
        self.assertNotContains(res, 'Item 1b')
        self.assertNotContains(res, 'Item 2b')
        # Instead of assertIn/response.content.decode()
        # Django provides the assertContains method which knows
        # how to deal with responses and the bytes of their content


class NewListTest(TestCase):

    def send_a_POST_request(self, text):
        #req = HttpRequest()
        #req.method = 'POST'
        #req.POST['add_todo'] = text
        #return home(req)
        # Instead of calling the view function directly
        # use the attribute client of the Django TestCase
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
        list_id = List.objects.last().id

        self.assertEqual(res.status_code, 302)
        self.assertEqual(res['location'], f'/lists/{list_id}/')
        # or similar check:
        self.assertRedirects(res, f'/lists/{list_id}/')

    def test_validation_errors_calls_home_page(self):
        res = self.send_a_POST_request('')
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'lists/home.html')
        self.assertContains(res, 'Empty items not allowed')

class NewItemTest(TestCase):

    def send_a_POST_request(self, text, list_id):
        return self.client.post(
            f'/lists/{list_id}/add_item',
            data={'add_todo': text}
        )

    def test_saves_a_valid_POST_request_to_an_existing_list(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        res = self.send_a_POST_request('A new item', list1.id)

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item')
        self.assertEqual(new_item.list, list1)

    def test_redirects_to_list_view(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        res = self.send_a_POST_request('A new item', list1.id)
        self.assertRedirects(res, f'/lists/{list1.id}/')

    def test_passes_correct_list_to_template(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        res = self.client.get(f'/lists/{list1.id}/')
        self.assertEqual(res.context['list_id'], list1.id)
        # or similar check:
        self.assertContains(res, text=f'/lists/{list1.id}/add_item', status_code=200)