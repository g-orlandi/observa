from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from bs4 import BeautifulSoup

User = get_user_model()


class FrontendTests(TestCase):

    def setUp(self):
        print('\nSetup...')
        self.free_password = 'password'
        self.free_user = User.objects.create_user(username='free_user', password=self.free_password)
        self.assertIsNotNone(self.free_user)

        self.pro_password = 'password'
        self.pro_user = User.objects.create_user(username='pro_user', password=self.pro_password, plan=User.Plan.PRO, email='pro_user@email.com')
        self.assertIsNotNone(self.pro_user)

        from django.conf import settings
        self.assertFalse(settings.DEBUG)

    def tearDown(self):
        return super().tearDown()

    def test_network_page_requires_login(self):

        client = Client()
        network_url = reverse('frontend:network')
        response = client.get(network_url)

        self.assertEqual(response.status_code, 302, "An anonymous user must be redirected to login")
        self.assertTrue('login' in response.url, "Redirection to login page expected")

        client.login(username=self.free_user.username, password=self.free_password)                            
        response2 = client.get(network_url)
        self.assertEqual(response2.status_code, 200, "Every logged user can see /network/ page")

    def test_free_user_sidebar(self):
        client = Client()
        client.login(username=self.free_user.username, password=self.free_password)

        response = client.get(reverse('frontend:network'))

        soup = BeautifulSoup(response.content, 'html.parser')
        sidebar = soup.find('div', class_='sidebar')

        self.assertIsNotNone(sidebar)

        network_link_classes = sidebar.find('li', id='link-network').find('a').get('class', [])
        self.assertNotIn('disabled', network_link_classes)

        resources_link_classes = sidebar.find('li', id='link-resources').find('a').get('class', [])
        self.assertIn('disabled', resources_link_classes)

    def test_pro_user_sidebar(self):
        client = Client()
        client.login(username=self.pro_user.username, password=self.pro_password)

        response = client.get(reverse('frontend:resources'))

        self.assertEqual(200, response.status_code)

        soup = BeautifulSoup(response.content, 'html.parser')
        sidebar = soup.find('div', class_='sidebar')

        self.assertIsNotNone(sidebar)

        network_link_classes = sidebar.find('li', id='link-network').find('a').get('class', [])
        self.assertNotIn('disabled', network_link_classes)

        resources_link_classes = sidebar.find('li', id='link-resources').find('a').get('class', [])
        self.assertNotIn('disabled', resources_link_classes)