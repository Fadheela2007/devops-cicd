import unittest

from app import app


class AppTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_accueil(self):
        self.assertEqual(self.client.get("/").status_code, 200)

    def test_sante(self):
        self.assertEqual(self.client.get("/health").get_json()["status"], "ok")

    def test_metriques(self):
        self.client.get("/")
        self.assertIn(b"http_requests_total", self.client.get("/metrics").data)


if __name__ == "__main__":
    unittest.main()
