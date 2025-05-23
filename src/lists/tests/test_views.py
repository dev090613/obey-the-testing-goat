from django.test import TestCase
from django.http import HttpRequest
from lists.views import home_page
from lists.models import Item, List


class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):

        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        mylist = List.objects.create()
        response = self.client.get(f"/lists/{mylist.id}/")
        self.assertTemplateUsed(response, "list.html")

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text="itemey 1", list=correct_list)
        Item.objects.create(text="itemey 2", list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text="other list item", list=other_list)

        response = self.client.get(f"/lists/{correct_list.id}/")

        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")
        self.assertNotContains(response, "other list item")

    def test_passes_correct_list_to_template(self):
        correct_list = List.objects.create()
        other_list = List.objects.create()

        response = self.client.get(f"/lists/{correct_list.id}/")
        self.assertEqual(response.context["list"], correct_list)


class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f"/lists/{correct_list.id}/add_item",
            data={"item_text": "A new item for an existing list"},
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.get()
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_after_POST(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f"/lists/{correct_list.id}/add_item",
            data={"item_text": "A new list item"},
        )
        self.assertRedirects(response, f"/lists/{correct_list.id}/")
