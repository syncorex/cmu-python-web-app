#! /usr/bin/env python3

import unittest

from app import app


class TestTriviaApp(unittest.TestCase):

    def setUp(self) -> None:
        app.testing = True

    def test_home_ok(self) -> None:
        client = app.test_client()
        res = client.get("/")
        self.assertEqual(res.status_code, 200)

    def test_home_res(self) -> None:
        client = app.test_client()
        res = client.get("/")
        self.assertIn("Trivia", str(res.data),
                      "HTML Response invalid (no 'Trivia'")

    def test_question_get(self) -> None:
        client = app.test_client()
        res = client.get("/question/0")
        self.assertEqual(res.status_code, 200)

    def test_question_correct(self) -> None:
        client = app.test_client()
        res = client.post("/question/0", data={
            "answer": "test"
        })
        self.assertIn("<p>Correct!", str(res.data),
                      "Question processing failed or \
                      'Correct' element missing from HTML response")

    def test_question_wrong(self) -> None:
        client = app.test_client()
        res = client.post("/question/0", data={
            "answer": "incorrect"
        })
        self.assertIn("<p>Wrong!", str(res.data),
                      "Question processing failed or \
                      'Wrong' element missing from HTML response")


if __name__ == "__main__":

    unittest.main(verbosity=2)
