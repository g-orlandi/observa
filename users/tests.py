from django.test import TestCase
from users.models import User
from datetime import date
from backend.models import Server, Endpoint

class UserModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test", email="test@example.com", password="pwd")
        self.server = Server.objects.create(name="server", user=self.user, domain="google.com", port="8000", is_backup=False)
        self.backup = Server.objects.create(name="backup", user=self.user, domain="facebook.com", port="8000", is_backup=True)
        self.endpoint = Endpoint.objects.create(name="endpoint", user=self.user, url="https://unimore.it")

    def test_set_active_date_filters_valid(self):
        self.user.set_active_date_filters("2025-05-01", "2025-05-10")
        self.assertEqual(self.user.filter_date_from, date(2025, 5, 1))
        self.assertEqual(self.user.filter_date_to, date(2025, 5, 10))

    def test_set_active_date_filters_invalid(self):
        with self.assertRaises(Exception) as context:
            self.user.set_active_date_filters("2025-05-10", "2025-05-01")
        self.assertEqual(str(context.exception), "Start date cannot be after the end date.")

    def test_get_accessible_backup_servers(self):
        backups_servers = self.user.get_accessible_backup_servers()
        self.assertIn(self.backup, backups_servers)
        self.assertNotIn(self.server, backups_servers)
        self.assertNotIn(self.endpoint, backups_servers)