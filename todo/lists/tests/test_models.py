from django.test import TestCase
from django.core.exceptions import ValidationError

from lists.models import Item, List


class ModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list1 = List()
        list1.save()

        item1 = Item()
        item1.text = 'A first item'
        item1.list = list1
        item1.save()

        item2 = Item()
        item2.text = 'A second one'
        item2.list = list1
        item2.save()

        saved_lists = List.objects.all()
        self.assertEqual(saved_lists[0], list1)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        self.assertEqual(saved_items[0].text, item1.text)
        self.assertEqual(saved_items[0].list, list1)
        self.assertEqual(saved_items[1].text, item2.text)
        self.assertEqual(saved_items[1].list, list1)

    def test_not_save_empty_item(self):
        list1 = List.objects.create()
        item = Item(list=list1, text='')
        with self.assertRaises(ValidationError):
            # Django does have full_clean method to manually run 
            # full validation if DB not support some constraints
            item.full_clean()
            item.save()

    def test_get_absolute_url(self):
        list1 = List.objects.create()
        self.assertEqual(list1.get_absolute_url(), f'/lists/{list1.id}/')
