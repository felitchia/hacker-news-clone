import unittest
import os
from models import Article, User
from app import db, app

TEST_DB = 'test.db'

class InitialTestCase(unittest.TestCase):


    def test_database_existance(self):
        tester = os.path.exists('hacker_news.db')
        self.assertTrue(tester)

    def setUp(self):
        """Set up a blank temp database before each test"""
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        """Destroy blank temp database after each test"""
        db.drop_all()


    def tearDown(self):
        db.drop_all()

    def test_article_db_insert(self):
        fake_article = Article(title='Fake Title', text=None, link='fake_link', upvotes=5, downvotes=-4, date=db.func.current_timestamp())
        db.session.add(fake_article)
        db.session.commit()
        article =  db.session.query(Article).filter_by(title='Fake Title').first()
        self.assertEquals('Fake Title', article.title)
        self.assertEquals(None, article.text)
        self.assertEquals('fake_link', article.link)
        self.assertEquals(5, article.upvotes)
        self.assertEquals(-4, article.downvotes)
        self.assertEquals(1, article.votes)
        self.assertIsNotNone(article.date)
        #print(article.date)

    def test_user_db_insert_link(self):
        fake_user = User(username='user', password='pass', email='email@email')
        db.session.add(fake_user)
        db.session.commit()
        user =  db.session.query(User).filter_by(username='user').first()
        self.assertEquals('user', user.username)
        self.assertEquals('pass', user.password)
        self.assertEquals('email@email', user.email)

if __name__ == '__main__':
    unittest.main()

