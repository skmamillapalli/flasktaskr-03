import unittest
from views import db, app
from models import User
from _config import basedir
import os

# This test is to verify the dunctionality of db -> Insertion/Deletion
DATABASE_NAME = 'test.db'
class AllAppTests(unittest.TestCase):
  def setUp(self):
      # Reset the values in original config app
      app.config['TESTING'] = True
      app.config['WTF_CSRF_ENABLED'] = False
      app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(basedir, DATABASE_NAME)
      app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
      # Mock the app Object to provide fake attributes/methods.
      self.app = app.test_client()
      db.create_all()
  
  def test_create_user(self):
      #db.session.query(User).filter_by(name='sunil').delete()
      db.session.add(User("sunil","sunilmsk@sunil.in", 3))
      db.session.commit()

  def tearDown(self):
      db.session.remove()
      db.drop_all()


if __name__ == '__main__':
    unittest.main()
