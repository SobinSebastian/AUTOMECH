# from django.test import TestCase

# # Create your tests here.
from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from django.urls import reverse
from selenium import webdriver
# class LoginTest(LiveServerTestCase):
#     def setUp(self):
#         self.driver  = webdriver.Chrome()
#     def tearDown(self):
#         self.driver.quit()
#     def test_login(self):
#         expected_url = 'http://127.0.0.1:8000/' 
#         print('Testing Started')
#         self.driver.get('http://127.0.0.1:8000//accounts/login/')
        
#         self.driver.find_element("id", "id_login")
#         email_field = self.driver.find_element("id", "id_login")
#         password_field = self.driver.find_element("id","id_password")
#         email_field.send_keys('snehajose2024b@mca.ajce.in')
#         password_field.send_keys('!Mynameis22')
#         submit = self.driver.find_element("id","log_sub")
#         submit.click()
#         current_url = self.driver.current_url
#         print(current_url)
#         print(expected_url)
#         self.assertEqual(current_url, expected_url)


class AddtoCartTest(LiveServerTestCase):
    def setUp(self):
        self.driver  = webdriver.Chrome()
    def tearDown(self):
        self.driver.quit()
    def test_login(self):
        expected_url = 'http://127.0.0.1:8000/' 
        print('Testing Started')
        self.driver.get('http://127.0.0.1:8000//accounts/login/')
        
        self.driver.find_element("id", "id_login")
        email_field = self.driver.find_element("id", "id_login")
        password_field = self.driver.find_element("id","id_password")
        email_field.send_keys('snehajose2024b@mca.ajce.in')
        password_field.send_keys('!Mynameis22')
        submit = self.driver.find_element("id","log_sub")
        submit.click()
        cartb = self.driver.find_element("id","basic-service")
        current_url = self.driver.current_url
        print(current_url)
        print(expected_url)
        self.assertEqual(current_url, expected_url)



# class SigninTest(LiveServerTestCase):
#     def setUp(self):
#         self.driver  = webdriver.Chrome()
#     def tearDown(self):
#         self.driver.quit()
#     def test_signin(self):
#         #expected_url = 'http://127.0.0.1:8000//accounts/login/' 
#         print('Testing Started')
#         self.driver.get('http://127.0.0.1:8000/')
#         signup = self.driver.find_element("id","btn-signup")
#         signup.click()
#         current_url = self.driver.current_url
#         print(current_url)
#         user_field = self.driver.find_element("id", "id_username")
#         first_field = self.driver.find_element("id", "id_firstname")
#         last_field = self.driver.find_element("id", "id_lastname")
#         p1_field = self.driver.find_element("id", "id_password1")
#         p2_field = self.driver.find_element("id", "id_password2")
#         user_field.send_keys('sobin1@gmail.com')
#         first_field.send_keys('Sobin')
#         last_field.send_keys('Sebastian')
#         p1_field.send_keys('!Mynameis#44^')
#         p2_field.send_keys('!Mynameis#44^')
#         register = self.driver.find_element("id","signup")
#         register.click()
