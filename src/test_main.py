#! /usr/bin/env python3

import unittest

from main import index


class TestHelloWorld(unittest.TestCase):

    def test1(self) -> None:
        self.assertEqual(index(), "<h1>Web App with Python Flask!</h1>")


if __name__ == "__main__":

    unittest.main(verbosity=2)
