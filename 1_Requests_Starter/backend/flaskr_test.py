
#_____________IMPORTING DEPENDENCIES_____________#

import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import *

#____________DEFINE TESTCASE CLASS______________#

class BookTestCase(unittest.TestCase):
    '''This is the test case class for the bookshelf API'''

    def setUp(self):
        '''This defines test variables and initializes the test app'''
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "bookshelf_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "student", "student", "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        self.new_book = {
            "title": "The Article",
            "author": "Uche M. N",
            "rating": "5"
        }

        # binds the app to the current context

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()                #create all tables

    def tearDown(self):
        '''This is executed after each test'''
        pass
    
#__________________Define Route Tests_________________#

    def test_add_new_book(self):
        '''Testing to see if books are added as expected'''
        resp = self.client().post("/books", json = self.new_book)
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

    def test_successful_search_found_book(self):
        '''Creating a successful book-search test before implementing search feature'''
        resp = self.client().post('/books', json = {"search": "Code"})
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_books'])
        self.assertTrue(len(data['books']))
        self.assertEqual(len(data['books']), 3)

    def test_successful_search_no_book(self):
        '''Creating a book_not_found search test before implementing search feature'''
        resp = self.client().post('/books', json={"search": "Ezechitoke"})
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["total_books"], 0)
        self.assertEqual(len(data["books"]), 0)

    def test_edit_book_rating(self):
        '''Testing to see if book rating is edited as expected'''
        resp = self.client().patch("/books/34", json = {"rating": "5"})
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])

    def test_delete_book(self):
        '''Testing to see if books are deleted as expected'''
        resp = self.client().delete('/books/39')
        data = json.loads(resp.data)

        book = Book.query.filter(Book.id == 39).one_or_none()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data["deleted"])
        self.assertEqual(data['deleted'], 39)
        self.assertTrue(data["total_books"])
        self.assertTrue(len(data["books"]))

#__________________Define Error Tests_________________#


    def test_failed_edit_rating(self):
        '''Testing to see if error 400 handler works as expected'''
        resp = self.client().patch('/books/15')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "The server could not understand the request due to invalid syntax")


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



#_____________EXECUTE THE TEST__________________#
if __name__ == '__main__':
    unittest.main()