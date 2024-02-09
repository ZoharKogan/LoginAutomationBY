import requests # need to install
import time  # for adding delays
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException  # Import TimeoutException

# email & password for checking
email = "zohar00kogan+1@gmail.com"
password = "zohar123"

options = Options()
options.add_experimental_option("detach", True)

ser_obj = Service("C:/Users/zohar/PycharmProjects/pythonProject/driver/chromedriver.exe")
driver = webdriver.Chrome(service=ser_obj, options=options)

url = "https://web-stg.betayeda.dev/worldofbasketball/login"

# Check for 503 error from 22:00 to 07:00
response = requests.get(url)
if response.status_code == 503:
    print("Error 503. Please try tomorrow at 07:00 o'clock")
    driver.quit()
    exit()

driver.get(url)
driver.maximize_window()

# waiting button to be clickable
wait = WebDriverWait(driver, 10)
login_with_email_button = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//div[contains(@class, 'login-via-btn')]//span[contains(text(), 'Login via email')]")))

login_with_email_button.click()

# Find and input email and password
email_field = driver.find_element(By.ID, "mat-input-0")
password_field = driver.find_element(By.ID, "mat-input-1")

email_field.send_keys(email)
password_field.send_keys(password)

login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//app-button[@class='login-btn']//button")))
login_button.click()

# waiting for a change in the URL
try:
    WebDriverWait(driver, 10).until(EC.url_changes(driver.current_url))
    print("Login successful!")

    continue_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[contains(@class, 'action-chip continue')]//span[contains(text(), 'Continue')]")))
    continue_button.click()

except:  # closing browser if login is failed
    print("Login failed, please check your email or password!")
    driver.quit()

time.sleep(10)  # Adjust the delay time as needed

# driver.quit()
