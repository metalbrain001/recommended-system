""" 
Test cases for the app module. 
"""

from django.test import SimpleTestCase
from app import calc


class CalcTests(SimpleTestCase):
    """Test cases for the calc module."""

    def test_add(self):
        """Test the add function."""

        res = calc.add(3, 8)
        self.assertEqual(res, 11)

    def test_subtract(self):
        """Test the subtract function."""

        res = calc.subtract(6, 11)
        self.assertEqual(res, 5)
