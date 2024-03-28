# from django.test import TestCase

# # Create your tests here.
from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
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
        print('Testing Started Add to Cart')
        self.driver.get('http://127.0.0.1:8000//accounts/login/')
        
        self.driver.find_element("id", "id_login")
        email_field = self.driver.find_element("id", "id_login")
        password_field = self.driver.find_element("id","id_password")
        email_field.send_keys('snehajose2024b@mca.ajce.in')
        password_field.send_keys('!Mynameis22')
        submit = self.driver.find_element("id","log_sub")
        submit.click()
        time.sleep(5)
        cartbutton = self.driver.find_element("id","standard-service")
        cartbutton.click()
        wait = WebDriverWait(self.driver, 10)  

        try:
            toast_message = wait.until(EC.presence_of_element_located((By.ID, "swal2-title")))
            toast_text = toast_message.text
            if toast_text == "Item added to the cart":
                print("Toast message verified: 'Item added to the cart'")
                print('Item add to Cart')
            else:
                print("Unexpected toast message:", toast_text)
        except TimeoutException:
            print("Toast message not found within 10 seconds")


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
