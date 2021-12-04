import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Book


class BookTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "bookshelf_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "ezugworie", "E2u8w0r1e", "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        self.new_book = {
            "title": "A Day In Chicago",
            "author": "Ezugworie Eucharia",
            "rating": "4"
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass


# DONE: Write at least two tests for each endpoint - one each for success and error behavior.
#        You can feel free to write additional tests for nuanced functionality,
#        Such as adding a book without a rating, etc.
#        Since there are four routes currently, you should have at least eight tests.
# Optional: Update the book information in setUp to make the test database your own!


#__________________Define Route Tests_________________#

    def test_add_new_book(self):
        '''Testing to see if books are added as expected'''
        resp = self.client().post("/books", json=self.new_book)
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(len(data["books"]))

    def test_list_books(self):
        '''Testing to see if all books are listed as expected'''
        resp = self.client().get("/books")
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_books"])
        self.assertTrue(len(data["books"]))

    def test_edit_book_rating(self):
        '''Testing to see if book rating is edited as expected'''
        resp = self.client().patch("/books/17", json={"rating": "5"})
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])

    def test_delete_book(self):
        '''Testing to see if books are deleted as expected'''
        resp = self.client().delete('/books/16')
        data = json.loads(resp.data)

        book = Book.query.filter(Book.id == 16).one_or_none()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data["deleted"])
        self.assertEqual(data['deleted'], 16)
        self.assertTrue(data["total_books"])
        self.assertTrue(len(data["books"]))

#__________________Define Error Tests_________________#

    def test_failed_edit_rating(self):
        '''Testing to see if error 400 handler works as expected'''
        resp = self.client().patch('/books/15')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], "The server could not understand the request due to invalid syntax")

    def test_list_books_beyond_valid_page(self):
        '''Testing to see if error 404 handler works as expected'''
        resp = self.client().get('/books?page=500')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "The server can not find the requested resource")

    def test_not_allowed_method(self):
        '''Testing to see if error 405 handler works as expected'''
        resp = self.client().get('/books/6')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "This method is not allowed for the requested URL")

    def test_delete_nonexisting_book(self):
        '''Testing to see if error 422 handler works as expecrted'''
        resp = self.client().delete('/books/4')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "The request was unable to be followed due to semantic errors")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
