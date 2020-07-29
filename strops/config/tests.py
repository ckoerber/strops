"""Imports all the EspressoDB tests."""
from espressodb.base.tests.apps import AppTest  # noqa
from espressodb.base.tests.views.urls import URLViewTest as URLVT  # noqa


class URLViewTest(URLVT):
    exclude_urls = ["notifications", "populate"]

    strops_urls = ["/operators/", "/schemes/", "/schemes/operator-mapping/from/"]

    def test_strops_urls(self):
        """Tests the HTTP status of urls provided by strops.
        """
        for url in self.strops_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
