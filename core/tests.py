from django.test import TestCase


class HealthCheckTests(TestCase):
    def test_health_endpoint_returns_200(self):
        response = self.client.get("/health/")
        self.assertEqual(response.status_code, 200)
