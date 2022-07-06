import ast
import os
from unittest import TestCase
from core.dir import FaindStar, BasseScan, StarElment
from tests.collector_test_hellper import CollectorEnvConfig, CollectorInnit, CollectorDist

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
        self.assertEqual(self.FS.start, -1)
        self.assertEqual(self.FS.end, -1)

    def test_return_stars_in_string(self):
        self.assertEqual(self.FS.return_stars_in_string(), '')

    def test_star_list(self):
        self.assertEqual(self.FS.create_star_list(), [''])
        self.assertEqual(len(self.FS.create_star_list()), 1)

class TestBasseScan(TestCase):

    test_dir='A-D\Dual\\1'

    def setUp(self) -> None:
        self.BS = BasseScan()
        self.CI = CollectorInnit()
        self.CDC= CollectorEnvConfig()
        self.BS.base_init("Name", self.test_dir)

    def test_argumants(self):
        self.assertEqual(self.BS.name, "Name")
        self.assertEqual(self.BS.dir, self.test_dir+"\\Name")
        self.assertEqual(self.BS.shema_url, "")

    def test_clear_name(self):
        self.assertEqual(self.BS.clear_name("Name (Star).avi"), "Name")

    def test_set_dir(self):
        self.CDC.data_config()
        self.CDC.dist_create()
        self.assertEqual(self.BS.set_dir("Name",'movies'), "C:\\Work\\VP\\movies\\M-P\\Name")
        self.CDC.remove_config()
        self.CDC.remove_dist()

    def test_init_dir(self):
        dir = self.CI.add_star_dir(self.test_dir + "\\Name")
        self.BS.dir=dir
        self.BS.base_dir = ['photo','movies']
        self.BS.init_dir()
        self.assertEqual(len(os.listdir(self.BS.dir)), 2)
        self.assertEqual(os.path.isdir(self.BS.dir+'/movies'), True)
        self.assertEqual(os.path.isdir(self.BS.dir+'/photo'), True)
        self.CI.delete_collector_dir()

class TestAbstractAddElment(TestCase):
    test_dir = 'A-D\Dual\\1'

    def setUp(self):

        self.CI = CollectorInnit()
        self.CDC = CollectorEnvConfig()
        self.CDC.data_config()
        self.CDC.dist_create()
        with open('dist.json') as f:
            data = f.read()
            db = ast.literal_eval(data)
        self.BS = StarElment("Name", self.test_dir,db)

    def test_create_json_config_not_create(self):
        self.CI.add_star_dir(self.test_dir + "\\Name")
        self.assertEqual(self.BS.create_json_config(), False)
        self.CI.delete_collector_dir()
























    """
    def test_create_json_config_not_create(self):
        self.CI.init_dirs()
        dir = self.CI.add_movie_dir(self.test_dir + "\\Name")
        self.BS.base_init("Name",dir)
        self.BS.dir=dir
        self.CI.add_config(dir)
        self.assertEqual(self.BS.create_json_config(),False)
        self.CI.delete_collector_dir()
    """