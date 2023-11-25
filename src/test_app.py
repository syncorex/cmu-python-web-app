#! /usr/bin/env python3

import unittest

# from app import index


class TestHelloWorld(unittest.TestCase):

    def test1(self) -> None:
        self.assertNotEqual("Testing needs work!", " ")


if __name__ == "__main__":

    unittest.main(verbosity=2)
