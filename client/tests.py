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

'''
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
'''

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

'''
class Addnewcat(LiveServerTestCase):
    def setUp(self):
        self.driver  = webdriver.Chrome()
    def tearDown(self):
        self.driver.quit()
    def test_Add_Category(self):
        self.driver.get('http://127.0.0.1:8000//accounts/login/')
        
        self.driver.find_element("id", "id_login")
        email_field = self.driver.find_element("id", "id_login")
        password_field = self.driver.find_element("id","id_password")
        email_field.send_keys('admin@gmail.com')
        password_field.send_keys('1234')
        self.driver.find_element("id","log_sub").click()
        time.sleep(5) 
        self.driver.find_element("id","service_category_nav").click()
        time.sleep(5) 
        self.driver.find_element("id","Category_Modal").click()
        time.sleep(2)
        self.driver.find_element("id", "id_category_name").send_keys('Periodic Service')
        self.driver.find_element("id","sub_category_name").click()
        wait = WebDriverWait(self.driver, 10)  

        try:
            toast_message = wait.until(EC.presence_of_element_located((By.ID, "swal2-title")))
            toast_text = toast_message.text
            if toast_text == "New ServiceCategory Is Added":
                print("Toast message verified: 'New ServiceCategory Is Added'")
                print('Item add to Cart')
            else:
                print("Unexpected toast message:", toast_text)
        except TimeoutException:
            print("Toast message not found within 10 seconds")
'''
'''
# Test For add NEW MECHANIC
class AddnewMech(LiveServerTestCase):
    def setUp(self):
        self.driver  = webdriver.Chrome()
    def tearDown(self):
        self.driver.quit()
    def test_Add_Category(self):
        self.driver.get('http://127.0.0.1:8000//accounts/login/')
        
        self.driver.find_element("id", "id_login")
        email_field = self.driver.find_element("id", "id_login")
        password_field = self.driver.find_element("id","id_password")
        email_field.send_keys('sebastiansobin43@gmail.com')
        password_field.send_keys('!Mynameis22')
        self.driver.find_element("id","log_sub").click()
        time.sleep(2) 
        self.driver.find_element("id","mech_add").click()
        time.sleep(2) 
        self.driver.find_element("id","bt_add_mech").click()
        time.sleep(2) 
        self.driver.find_element("id", "id_email").send_keys('Ram2196@gmail.com')
        self.driver.find_element("id", "id_first_name").send_keys('Ram')
        self.driver.find_element("id", "id_last_name").send_keys('Raj')
        self.driver.find_element("id","new_mech").click()
        wait = WebDriverWait(self.driver, 10)  

        try:
            toast_message = wait.until(EC.presence_of_element_located((By.ID, "swal2-title")))
            toast_text = toast_message.text
            if toast_text == "New Mechanic is Added":
                print("Toast message verified: 'New Mechanic is Added'")
            else:
                print("Unexpected toast message:", toast_text)
        except TimeoutException:
            print("Toast message not found within 10 seconds") '''
'''
class addnewcar(LiveServerTestCase):
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
        time.sleep(2) 
        self.driver.get('http://127.0.0.1:8000/Vehicles')
        time.sleep(2)
        self.driver.find_element("id","c_new_add").click()
        time.sleep(2)
        vregno = self.driver.find_element("id","id_vehicle_Regno")
        vregno.send_keys('KL05AE3019')
        make_company= self.driver.find_element("id","id_make_company")
        model_name = self.driver.find_element("id","id_model_name")
        model_variant = self.driver.find_element("id","id_model_variant")
        make_company.send_keys('Maruti Suzuki')
        model_name.send_keys('WagonR')
        model_variant.send_keys('LXI')
        self.driver.find_element("id","Add_v").click()
        wait = WebDriverWait(self.driver, 10)  
        try:
            toast_message = wait.until(EC.presence_of_element_located((By.ID, "swal2-title")))
            toast_text = toast_message.text
            if toast_text == "New Vehicle is Added":
                print("Toast message verified: 'New Vehicle is Added'")
            else:
                print("Unexpected toast message:", toast_text)
        except TimeoutException:
            print("Toast message not found within 10 seconds")
'''