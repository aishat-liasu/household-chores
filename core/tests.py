from django.contrib.staticfiles import finders
from django.test import TestCase


class HealthCheckTests(TestCase):
    def test_health_endpoint_returns_200(self):
        response = self.client.get("/health/")
        self.assertEqual(response.status_code, 200)


class HomePageTests(TestCase):
    def test_home_returns_200(self):
        self.assertEqual(self.client.get("/").status_code, 200)

    def test_home_shows_header(self):
        self.assertContains(self.client.get("/"), "Household Chores")

    def test_home_references_htmx(self):
        self.assertContains(self.client.get("/"), "htmx.min.js")


class HtmxFragmentTests(TestCase):
    def test_ping_returns_fragment(self):
        response = self.client.get("/ping/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "pong")


class StaticAssetTests(TestCase):
    def test_css_is_findable(self):
        self.assertIsNotNone(finders.find("css/app.css"))

    def test_htmx_is_findable(self):
        self.assertIsNotNone(finders.find("vendor/htmx.min.js"))
