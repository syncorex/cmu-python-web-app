#! /usr/bin/env python3

import unittest

from main import hello_world


class TestHelloWorld(unittest.TestCase):

    def test1(self) -> None:
        self.assertEqual(hello_world(), "<p>Hello, World!</p>")


if __name__ == "__main__":

    unittest.main(verbosity=2)
