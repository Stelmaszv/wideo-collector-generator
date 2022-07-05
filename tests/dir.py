from unittest import TestCase

from core.dir import FaindStar


class TestFaindStarGood(TestCase):

    def setUp(self) -> None:
        self.FS = FaindStar("Name (Star and Star2)")

    def test_argumants(self):
        self.assertEqual(type(self.FS.start), int)
        self.assertEqual(self.FS.start, 5)
        self.assertEqual(type(self.FS.end), int)
        self.assertEqual(self.FS.end, 20)

    def test_return_stars_in_string(self):
        self.assertEqual(self.FS.return_stars_in_string(), 'Star and Star2')

    def test_star_list(self):
        self.assertEqual(self.FS.create_star_list(), ['Star', 'Star2'])
        self.assertEqual(len(self.FS.create_star_list()), 2)

class TestFaindStarWrong(TestCase):

    def setUp(self) -> None:
        self.FS = FaindStar("Name (Star)")

    def test_argumants(self):
        self.assertEqual(type(self.FS.start), int)
        self.assertEqual(self.FS.start, 5)
        self.assertEqual(type(self.FS.end), int)
        self.assertEqual(self.FS.end, 10)

    def test_return_stars_in_string(self):
        self.assertEqual(self.FS.return_stars_in_string(), 'Star')

    def test_star_list(self):
        self.assertEqual(self.FS.create_star_list(), ['Star'])
        self.assertEqual(len(self.FS.create_star_list()), 1)

class TestFaindStarNoStars(TestCase):

    def setUp(self) -> None:
        self.FS = FaindStar("Name")

    def test_argumants(self):
        self.assertEqual(type(self.FS.start), int)
        self.assertEqual(self.FS.start, -1)
        self.assertEqual(type(self.FS.end), int)
        self.assertEqual(self.FS.end, -1)

    def test_return_stars_in_string(self):
        self.assertEqual(self.FS.return_stars_in_string(), '')

    def test_star_list(self):
        self.assertEqual(self.FS.create_star_list(), [''])
        self.assertEqual(len(self.FS.create_star_list()), 1)