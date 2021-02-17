import unittest
from ConnectGetFilterXML_S3 import *


class TestConnectXML(unittest.TestCase):

    def test_search_findall(self):
        string  = "work in progress"
        self.assertEqual(string,string)

if __name__ == "__main__":
    unittest.main()