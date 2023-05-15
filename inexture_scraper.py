import time

from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()
import os
import datetime

# driver = webdriver.Chrome()

# MODIFIED INITIAL DRIVER BCZ ITS CONFLICTS WITH SELENIUM VERSION
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("https://portal.inexture.com/auth")

wait = WebDriverWait(driver, 10)
email_field = wait.until(EC.visibility_of_element_located((By.NAME, "username")))
password_field = driver.find_element(By.NAME, "password")

email_field.send_keys(os.getenv("USER_NAME"))
password_field.send_keys(os.getenv("PASSWORD"))

password_field.send_keys(Keys.RETURN)

time.sleep(5)

if "https://portal.inexture.com/" in driver.current_url:
    print("Login successful!")
    page_source = driver.page_source
    driver.implicitly_wait(5)
    wait = WebDriverWait(driver, 20)
    time.sleep(5)
    dashboard = driver.find_elements(By.CLASS_NAME, "text-base")
    driver.implicitly_wait(10)
    main_contain = [i.text for i in dashboard]

    leave_today = dashboard[0].text
    full_day_leave = dashboard[1].text
    half_day_leave = dashboard[2].text
    upcoming_leave = dashboard[3].text
    upcoming_full_leave = dashboard[4].text
    upcoming_half_leave = dashboard[5].text
    wfh_today = dashboard[6].text
    early_exit_today = dashboard[9].text
    my_leaves = dashboard[12].text
    time_log_prev_day = dashboard[15].text
    today_birthday = dashboard[18].text
    upcoming_birthday = dashboard[19].text
    today_work_anniversary = dashboard[20].text
    current_month_holiday = dashboard[21].text
    upcoming_holiday = dashboard[22].text

    dashboard_data = {
        "date": f"{datetime.datetime.now()}",
        leave_today: {
            'full_day': {full_day_leave: []},
            'half_day': {half_day_leave: []}
        },
        upcoming_leave: {
            'full_day': {upcoming_full_leave: []},
            'half_day': {upcoming_half_leave: []},
        },
        wfh_today: {
            'full_day': {dashboard[7].text: []},
            'half_day': {dashboard[8].text: []}
        },
        early_exit_today: {
            'full_day': dashboard[10].text,
            'half_day': dashboard[11].text
        },
        my_leaves: {
            'used_leaves': dashboard[13].text,
            'remaining': dashboard[14].text,
            'detailed_leaves': {}
        },
        time_log_prev_day: {
            'this_week': dashboard[16].text,
            'this_month': dashboard[17].text,
            'my_time_log_details': {}
        },
        today_birthday: [],
        upcoming_birthday: [],
        today_work_anniversary: [],
        current_month_holiday: [],
        upcoming_holiday: []
    }


    # Extract the text content of the element
    elements = driver.find_elements(By.CLASS_NAME, "cursor-pointer")
    time.sleep(3)
    # TODAY LEAVE DATA
    today_leave_persons = elements[1]
    time.sleep(3)
    today_leave_persons.click()
    time.sleep(3)
    names = today_leave_persons.find_elements(By.XPATH, "//span[@class='capitalize ml-2']")
    time.sleep(3)
    today_leave_each_data = today_leave_persons.find_elements(By.XPATH, "//tr[@class='mantine-1avyp1d']")
    time.sleep(3)
    for row in today_leave_each_data:
        if len((row.text.splitlines())) == 4:
            leave_type = (row.text.splitlines())[2]
            if leave_type == "Full":
                dashboard_data[leave_today]["full_day"][full_day_leave].append((row.text.splitlines())[0])
            else:
                dashboard_data[leave_today]["half_day"][half_day_leave].append((row.text.splitlines())[0])
        else:
            leave_type = (row.text.splitlines())[3]
            if leave_type == "Full":

                dashboard_data[leave_today]["full_day"][full_day_leave].append((row.text.splitlines())[1])

            else:

                print(row.text.splitlines()[1])
                dashboard_data[leave_today]["half_day"][half_day_leave].append((row.text.splitlines())[1])

    # CLICK BACK OR CLOSE TO GO BACk
    time.sleep(2)
    today_leave_cursor = driver.find_element(By.XPATH,
                                             "//button[@class='mantine-UnstyledButton-root mantine-ActionIcon-root mantine-Modal-close mantine-4ywiu8']")
    today_leave_cursor.click()

    # UPCOMING LEAVE
    time.sleep(2)
    upcoming_leave_persons = elements[2]
    upcoming_leave_persons.click()
    time.sleep(2)
    today_upcoming_leave_each_data = upcoming_leave_persons.find_elements(By.XPATH, "//tr[@class='mantine-1avyp1d']")
    time.sleep(3)
    for row in today_upcoming_leave_each_data:
        if len((row.text.splitlines())) == 4:
            leave_type = (row.text.splitlines())[2]
            if leave_type == "Full":
                dashboard_data[upcoming_leave]["full_day"][upcoming_full_leave].append((row.text.splitlines())[0])
            else:
                dashboard_data[upcoming_leave]["full_day"][upcoming_half_leave].append((row.text.splitlines())[0])
        else:
            # print(row.text.splitlines())
            leave_type = (row.text.splitlines())[3]
            if leave_type == "Full":

                dashboard_data[upcoming_leave]["full_day"][upcoming_full_leave].append((row.text.splitlines())[1])


            else:

                dashboard_data[upcoming_leave]["full_day"][upcoming_half_leave].append((row.text.splitlines())[1])

    # CLICK BACK OR CLOSE TO GO BACK
    time.sleep(3)
    upcoming_leave_cursor = driver.find_element(By.XPATH,
                                                "//button[@class='mantine-UnstyledButton-root mantine-ActionIcon-root mantine-Modal-close mantine-4ywiu8']")
    upcoming_leave_cursor.click()
    time.sleep(3)
    # WORK FROM HOME
    wfh_persons = elements[3]
    wfh_persons.click()
    time.sleep(3)
    wfh_each_data = wfh_persons.find_elements(By.XPATH, "//tr[@class='mantine-1avyp1d']")
    time.sleep(3)
    for row in wfh_each_data:
        if len((row.text.splitlines())) == 3:
            dashboard_data[wfh_today]["full_day"][f"{dashboard[7].text}"].append((row.text.splitlines())[0])
        else:
            dashboard_data[wfh_today]["full_day"][f"{dashboard[7].text}"].append((row.text.splitlines())[1])

    # CLICK BACK OR CLOSE TO GO BACK
    wfh_cursor = driver.find_element(By.XPATH,
                                     "//button[@class='mantine-UnstyledButton-root mantine-ActionIcon-root mantine-Modal-close mantine-4ywiu8']")
    wfh_cursor.click()

    # MY LEAVES
    my_leave_card = elements[5]
    my_leave_card.click()
    my_leave_internal = my_leave_card.find_elements(By.XPATH, "//tr[@class='mantine-1avyp1d']")
    for row in my_leave_internal:
        if len((row.text.splitlines())) == 3:
            dashboard_data[my_leaves]["detailed_leaves"][f"{(row.text.splitlines())[1]}"] = {
                "total_leave": row.text.splitlines()[2]}
        else:
            dashboard_data[my_leaves]["detailed_leaves"][f"{(row.text.splitlines())[2]}"] = {
                "total_leave": row.text.splitlines()[3]}

    # CLICK BACK OR CLOSE TO GO BACK
    my_leave_cursor = driver.find_element(By.XPATH,
                                          "//button[@class='mantine-UnstyledButton-root mantine-ActionIcon-root mantine-Modal-close mantine-4ywiu8']")
    my_leave_cursor.click()

    # MY LEAVES
    time_log_card = elements[6]
    time_log_card.click()
    time_log_internal = time_log_card.find_elements(By.XPATH, "//tr[@class='mantine-1avyp1d']")
    for row in time_log_internal:
        if len((row.text.splitlines())) == 3:
            dashboard_data[time_log_prev_day]["my_time_log_details"][f"{(row.text.splitlines())[1].split()[1]}"] = {
                "total_duration": row.text.splitlines()[2]}
        else:
            dashboard_data[time_log_prev_day]["my_time_log_details"][f"{(row.text.splitlines())[2].split()[1]}"] = {
                "total_duration": row.text.splitlines()[3]}

    # ADD DATA INTO JSON FILE
    # from datetime import date
    #
    # today_date = date.today()


    today_date = datetime.datetime.now()
    filename = f'{today_date}_dashboard_data.json'
    import json

    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            try:
                json_data = json.load(f)
            except ValueError:
                json_data = []
    else:
        json_data = []

    json_data.append(dashboard_data)

    with open(filename, 'w') as f:
        json.dump(json_data, f, indent=4)

else:
    print("Login failed.")

driver.quit()
