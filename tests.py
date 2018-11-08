import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
import sqlalchemy
from EVMS import app, db

# import all models to be tested

class UserTest(unittest.TestCase):
    def setUp(self):
        db_username = app.config['DB_USER_NAME']
        db_password = app.config['DB_PASSWORD']
        db_host = app.config['DB_HOST']
        self.db_name = 'test_evms'
        self.db_uri ="mysql+pymysql://%s:%s@%s/" %(db_username, db_password, db_host)
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED']= False
        app.config['DB_NAME'] = 'test_evms'
        app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri + self.db_name
        engine = sqlalchemy.create_engine(self.db_uri)
        conn = engine.connect()
        conn.execute('commit')
        conn.execute('CREATE DATABASE ' + self.db_name)
        db.create_all()
        conn.close()
        self.app = app.test_client()
        
    def tearDown(self):
        db.session.remove()
        engine = sqlalchemy.create_engine(self.db_uri)
        conn = engine.connect()
        conn.execute('commit')
        conn.execute('DROP DATABASE ' + self.db_name)
        conn.close()
    
    def create_user(self):
        return self.app.post('/register', data= dict(
            firstname='Hassan',
            lastname='Emam',
            username= 'hemam',
            email ='hassan.emam@hotmail.com',
            password ='hassan',
            confirm='hassan',
            organisation =None), follow_redirects=True)

    def test_create_user(self):
        rv = self.create_user()
        print(rv.data)
        assert 'User Registered' in str(rv.data)
        
if __name__ == '__main__':
    unittest.main()