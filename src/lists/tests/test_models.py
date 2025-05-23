from django.test import TestCase
from lists.models import Item, List


class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        mylist = List()
        mylist.save()

        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.list = mylist
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.list = mylist
        second_item.save()

        saved_lists = List.objects.get()
        self.assertEqual(saved_lists, mylist)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_item = saved_items[0]
        second_item = saved_items[1]
        self.assertEqual(first_item.text, "The first (ever) list item")
        self.assertEqual(first_item.list, mylist)
        self.assertEqual(second_item.text, "Item the second")
        self.assertEqual(second_item.list, mylist)
