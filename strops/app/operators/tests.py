from django.test import TestCase

# Create your tests here.


class OperatorsTestCase(TestCase):
    def test_scales(self):
        for scale, verbose in SCALES:
            self.assertNotIn("_", scale)
