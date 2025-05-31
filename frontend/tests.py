from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest.mock import patch
from backend.models import Server, PromQuery
from datetime import datetime

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

    
class MetricViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="pwd",
            email="test@example.com"
        )

        self.server = Server.objects.create(
            name="test",
            user=self.user,
            domain="google.com",
            port=9090,
            is_backup=False
        )
        self.user.active_server = self.server
        self.user.save()

        self.query = PromQuery.objects.create(
            code="cpu_usage",
            title="CPU Usage",
            target_system=PromQuery.TargetSystem.PROMETHEUS
        )

    @patch("frontend.views.api.generic_call")
    def test_get_instantaneous_data_success(self, mock_call):
        self.client.login(username="testuser", password="pwd")
        mock_call.return_value = "42"


        response = self.client.get(
            reverse("frontend:get_instantaneous_data", args=["cpu_usage"]),
            {"source": "server"}
        )


        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "42")

    def test_get_instantaneous_data_invalid_metric(self):
        self.client.login(username="testuser", password="pwd")
        response = self.client.get(
            reverse("frontend:get_instantaneous_data", args=["nonexistent"]),
            {"source": "server"}
        )
        self.assertEqual(response.status_code, 400)

    @patch("frontend.views.api.generic_call")
    def test_get_range_data_success(self, mock_call):
        self.client.login(username="testuser", password="pwd")
        mock_call.return_value = [
            [int(datetime(2025, 5, 1, 10).timestamp()), 5.2],
            [int(datetime(2025, 5, 1, 11).timestamp()), 7.1],
        ]

        self.user.set_active_date_filters("2025-05-01", "2025-05-01")

        response = self.client.get(
            reverse("frontend:get_range_data", args=["cpu_usage"]),
            {"source": "server"}
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("labels", data)
        self.assertIn("values", data)
        self.assertEqual(data["title"], "CPU Usage")