import requests
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.support.wait import WebDriverWait

Run_Web = False
Next_Run = False
Email = "zohar00kogan+1@gmail.com"
Password = "zohar123"
url = "https://web-stg.betayeda.dev/worldofbasketball/login"
# Check the current stage
count = 0
expect_step = 10
def logs(T, SkillName , S ):
    # Receives a string and a double and puts it in a text file
    if (S==1):
        with open('BetaLogs.txt', 'a') as f:
            f.write("step " + str(S) +": " + Email + " is log in!" + " in Taken time: " + "{:.2f} seconds.\n".format(T))
    elif (S==2):
        with open('BetaLogs.txt', 'a') as f:
            f.write("step " + str(S) +": " + " moving to- " + SkillName + "\n")
    else:
        with open('BetaLogs.txt', 'a') as f:
            f.write("step " + str(S) +": " + " complete a " + SkillName + "\n")

Run_Web = True
if Run_Web:
    start_script = time.time()
    service = Service(executable_path="chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.service = service

    # use with the recommendation options to run this program on chrome
    driver = webdriver.Chrome(options=options)

    # Check for 503 error from 22:00 to 07:00
    response = requests.get(url)
    if response.status_code == 503:
        with open('BetaLogs.txt', 'a') as f:
            f.write("Error 503. Please try tomorrow at 07:00 o'clock")
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

    email_field.send_keys(Email)
    password_field.send_keys(Password)

    start_time = time.time()  # Measure the starting time for login

    try:
        # Searches for the element and if it finds it, it records in the file a tex that the user failed to connect
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "mat-error-0"))
        )
        print("The email not contains @ ")
        with open('BetaLogs.txt', 'a') as f:
            f.write("The Login to " + Email + " Fail. \n")
        driver.quit()
        raise SystemExit(1)
    except TimeoutException:
        print("The email contains @")

        # Waits for the login button element to be present for up to 5 seconds
        LogIn_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "login-btn"))
        )

    # Click on this variable
    LogIn_element.click()

    # start to counting time
    start_time = time.time()

    try:
        # Takes 10 seconds and checks if the argument it receives exists
        Skill_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "skill-image-container"))
        )
        # end to counting time
        end_time = time.time()
        # how much time take to login
        taken_time = end_time - start_time
        # Increase the step count by 1
        count+=1

        # move elements to logs function
        logs(taken_time, "Moving from the login to the home page",count)

    except TimeoutException:
        # If not successful it means that the user failed to connect
        with open('BetaLogs.txt', 'a') as f:
            f.write("The Login to " + Email + " Fail. \n")

    # starting counting time
    start_time = time.time()

    # Click on this variable
    Skill_element.click()

    # ending counting time
    end_time = time.time()

    # how much time take to open skill
    taken_time = end_time-start_time

    # take the name of skill
    skill_element = driver.find_element(By.CSS_SELECTOR, ".skill-name")
    skill_name = skill_element.text
    info = "Skill: " + skill_name

    count+=1
    # add the skill name to log
    logs(taken_time, info, count)

    Next_Run = True
    # Run While the Next Button is Clickable
    time.sleep(10)

    while Next_Run:
        try:
            time.sleep(4)
            # Check if you finish skill if you finish its write this to .txt file
            Skill_element = driver.find_element(By.CLASS_NAME, "skill-image-container")
            if Skill_element is not None:
                # Makes a calculation of the running time of the script, some percentages of completion and enters into the log
                finish_script = time.time()
                total_time = finish_script - start_script
                total = count/expect_step
                minutes = total_time//60
                seconds = total_time - (minutes * 60)
                with open('BetaLogs.txt', 'a') as f:
                    f.write(info + " completed by: " + Email + ", in total time: " + str(minutes) +
                            " minutes and {:.2f} second\n".format(seconds))

                driver.quit()
        except NoSuchElementException:
            print(Email + " Couldn't finish the skill")
        try:
            # Checks if the button exists on the page
            next_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                "button.mat-raised-button.mat-button-base.app-button.round.medium.ng-star-inserted"))
            )
        except NoSuchElementException:
            print("The Button dont exsits")
        # If the button is found and clickable, click it
        if next_button.is_enabled():
            time.sleep(1)
            next_button.click()
        else:
            try:
                # Checks if the checkbox is found, if it exists, click it
                CheckBox = driver.find_element(By.CLASS_NAME, "checkbox")
                if CheckBox is not None:
                    # Calculates some percentages and enters the log of the percentage of success so far and also the name of the stage
                    count += 1
                    total = count / expect_step
                    CheckBox.click()
                    logs(total, "Checkbox Question", count)

            except NoSuchElementException:
                print("Checkbox not found")
            try:
                # Checks if the input line exists, if it exists, write in the input line
                Input_fill = driver.find_element(By.XPATH , "//input[@formcontrolname='data']")
                if Input_fill is not None:
                    # Calculates some percentages and enters the log of the percentage of success so far and also the name of the stage
                    count += 1
                    total = count / expect_step
                    Input_fill.send_keys("qwerasd")
                    logs(total, "Text Question", count)
            except NoSuchElementException:
                print("Input field not found")
            try:
                # Checks if there are several questions and if the array is larger than 1, mark the third element in the array
                buttons = driver.find_elements(By.CSS_SELECTOR,
                                       "app-radio-list[formcontrolname='data'] .learner-choose-one-group .learner-item .learner-task-name span")
                if len(buttons) >= 1:
                    # Calculates some percentages and enters the log of the percentage of success so far and also the name of the stage
                    count += 1
                    total = count / expect_step
                    buttons[3].click()
                    logs(total, "Choice question", count)
            except NoSuchElementException:
                print("Buttons not found")
# Take delay
time.sleep(10)
# close the test program
driver.quit()