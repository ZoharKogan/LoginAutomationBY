# First demo version

import requests
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def login_process(email, password, url):
    options = Options()
    options.add_experimental_option("detach", True)

    ser_obj = Service("C:/Users/zohar/PycharmProjects/pythonProject/driver/chromedriver.exe")
    driver = webdriver.Chrome(service=ser_obj, options=options)

    try:
        # Check for 503 error from 22:00 to 07:00
        response = requests.get(url)
        if response.status_code == 503:
            logger.error("Error 503. Please try tomorrow at 07:00 o'clock")
            return

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

        start_time = time.time()  # Measure the starting time for login

        try:
            login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//app-button[@class='login-btn']//button")))
            login_button.click()

            # waiting for a change in the URL
            WebDriverWait(driver, 10).until(EC.url_changes(driver.current_url))
            end_time = time.time()  # Measure the ending time for login
            login_time = end_time - start_time  # Calculate the time taken for login
            with open('BetaLogs.txt', 'a') as f:
             f.write(f"Step 1: {email} is Login! Time taken: {login_time:.2f} seconds\n")


            # Click on all 'Continue' buttons
            continue_buttons = wait.until(EC.presence_of_all_elements_located(
                (By.XPATH, "//app-typography/span[@class='xs regular' and contains(text(), 'Continue')]")))
            for button in continue_buttons:
                button.click()

            with open('BetaLogs.txt', 'a') as f:
             f.write("Step 2: Skill entry success!\n.")

            # Loop to handle questions
            while True:
                try:
                    # Check if there are questions
                    time.sleep(5)  # Adjust delay as needed
                    skill_element = driver.find_element(By.CLASS_NAME, "skill-image-container")
                    if skill_element is not None:
                        logger.info("Skill completed!")
                        with open('BetaLogs.txt', 'a') as f:
                            f.write(f"Step 3: {email} completed the skill.\n")
                            end_time = time.time()  # Measure the ending time for login
                            login_time = end_time - start_time  # Calculate the time taken for login
                            with open('BetaLogs.txt', 'a') as f:
                                f.write(f"Skill completed! Time taken: {login_time / 60 :.2f} mintues")

                        # Closing the browser as the skill is completed
                        driver.quit()
                        return  # Exit the function if the skill is completed
                except NoSuchElementException:
                    logger.error("Couldn't finish the skill")

                    # Check if the browser is on the home page
                    if driver.current_url == url:
                        logger.info("Returning to homepage...")
                        # Closing the browser if back to homepage without completing the skill
                        driver.quit()
                        with open('BetaLogs.txt', 'a') as f:
                            f.write("Returned to homepage without completing the skill.\n")
                            f.write(f"Total time taken: {login_time:.2f} seconds\n")
                        return  # Exit the function if back to homepage
                except Exception as e:
                    logger.error(f"An error occurred: {str(e)}")

                # Check if the button exists on the page
                try:
                    next_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR,
                                                         "button.mat-raised-button.mat-button-base.app-button.round.medium.ng-star-inserted"))
                    )
                    # If the button is found and clickable, click it
                    if next_button.is_enabled():
                        time.sleep(4)
                        next_button.click()
                    else:
                        # Checks if the checkbox is found, if it exists, click it
                        try:
                            CheckBox = driver.find_element(By.CLASS_NAME, "checkbox")
                            if CheckBox is not None:
                                time.sleep(4)
                                CheckBox.click()
                                time.sleep(2)
                        except NoSuchElementException:
                            logger.error("Checkbox not found")

                        # Checks if the input line exists, if it exists, write in the input line
                        try:
                            Input_fill = driver.find_element(By.XPATH, "//input[@formcontrolname='data']")
                            if Input_fill is not None:
                                time.sleep(4)
                                Input_fill.send_keys("qweerr")
                                time.sleep(2)
                        except NoSuchElementException:
                            logger.error("Input field not found")

                        # Checks if there are several questions and if the array is larger than 1, mark the third element in the array
                        try:
                            buttons = driver.find_elements(By.CSS_SELECTOR,
                                                           "app-radio-list[formcontrolname='data'] .learner-choose-one-group .learner-item .learner-task-name span")
                            if len(buttons) >= 1:
                                time.sleep(4)
                                buttons[2].click()
                                time.sleep(2)
                        except NoSuchElementException:
                            logger.error("Buttons not found")

                except NoSuchElementException:
                    logger.error("The Button doesn't exist")

        except TimeoutException:
            end_time = time.time()  # Measure the ending time for login
            login_time = end_time - start_time  # Calculate the time taken for login
            with open('BetaLogs.txt', 'a') as f:
                f.write(f"Skill completed! Time taken: {login_time/ 60 :.2f} seconds")
        except NoSuchElementException:
            end_time = time.time()  # Measure the ending time for login
            login_time = end_time - start_time  # Calculate the time taken for login
            error_message = driver.find_element(By.ID, "mat-error-2").text
            logger.error(f"Login failed. Error: {error_message}. Time taken: {login_time:.2f} seconds")
    finally:
        # Commented out the automatic closing of the browser
        # driver.quit()
        pass

if __name__ == "__main__":
    email = "zohar00kogan+1@gmail.com"
    password = "zohar123"
    url = "https://web-stg.betayeda.dev/worldofbasketball/login"
    login_process(email, password, url)
