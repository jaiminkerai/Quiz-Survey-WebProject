from datetime import datetime, timedelta
import unittest, os, time
from app import app, db
from app.models import User, Post
from selenium import webdriver
basedir = os.path.abspath(os.path.dirname(__file__))

class SystemTest(unittest.TestCase):
    #assume no driver yet
    driver = None

    def setUp(self):
        self.driver = webdriver.Firefox(executable_path = os.path.join(basedir, 'geckodriver'))
        #If self driver is not found do not run test
        if not self.driver:
            self.skipTest
        else:
            #initiate database and create user jaimin
            db.init_app(app)
            db.create_all()
            db.session.query(User).delete()
            db.session.query(Post).delete()
            u = User(id=1, username= "jaimin", email="jaimin@kerai.com")
            u.set_password("pw")
            db.session.add(u)
            db.session.commit()
            self.driver.maximize_window()
            self.driver.get('http://localhost:5000/')

    def tearDown(self):
        #if self.driver is running, then run teardown function
        if self.driver:
            self.driver.close()
            db.session.query(User).delete()
            db.session.query(Post).delete()
            db.session.commit()
            db.session.remove()
    
    def test_login(self):
        #go to local host (app)
        self.driver.get('http://localhost:5000/')
        #provides operating system time to load
        time.sleep(1)
        #finds username, password and submit field by id
        user_field = self.driver.find_element_by_id('username')
        password_field = self.driver.find_element_by_id('password')
        submit = self.driver.find_element_by_id('submit')

        #submits jaimin and pw in the userfield and password
        user_field.send_keys('jaimin')
        password_field.send_keys('pw')
        submit.click()
        time.sleep(1)

        #finds element by id equal to greeting and matches it to html of 'Quizzes'
        greeting = self.driver.find_element_by_id('greeting').get_attribute('innerHTML')
        self.assertEqual(greeting, 'Quizzes')

if __name__ == '__main__':
    unittest.main(verbosity=2)