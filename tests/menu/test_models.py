from django.test import TestCase
from menu.models import Menu


class AnimalTestCase(TestCase):
    def setUp(self):
        Menu.objects.create(name="lion", sound="roar")
        Menu.objects.create(name="cat", sound="meow")

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        lion = Menu.objects.get(name="lion")
        cat = Menu.objects.get(name="cat")
        self.assertEqual(lion.speak(), 'The lion says "roar"')
        self.assertEqual(cat.speak(), 'The cat says "meow"')
