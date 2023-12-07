from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from faker import Faker
import re
import csv

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

driver.get("https://worklenz.com/auth")
driver.maximize_window()
faker = Faker()

statues = []
status_names = ["Backlog", "Ongoing", "Development work", "Testing & Review", "Resolved"]
before_statues_details = []
after_statues_details = []


def main():
    login()
    project_tab()


def login():
    wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Email']"))).send_keys(
        "coyonic318@hupoi.com")
    wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Password']"))).send_keys(
        "Test@12345")
    wait.until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Log in']"))).click()
    time.sleep(10)


def project_tab():
    wait.until(
        EC.visibility_of_element_located((By.XPATH, "//strong[normalize-space()='Projects']"))).click()
    time.sleep(10)


def check_project_segment():
    segments = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "ant-segmented-group")))
    all_segment = segments.find_elements(By.TAG_NAME, "label")[0]
    all_segment_class_name = all_segment.get_attribute("class")
    if "item-selected" not in all_segment_class_name:
        all_segment.click()


def go_to_need_project_inside():
    t_body = driver.find_element(By.TAG_NAME, "tbody")
    t_body.find_elements(By.TAG_NAME, "tr")[0].click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//a[normalize-space()='Board']"))).click()


def add_new_statues():
    new_status_column = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "new-column-sec")))
    new_status_column.find_element(By.TAG_NAME, "button").click()
    status_name = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Name']")))
    status_name.send_keys(status_names[faker.random_int(min=0, max=4)])
    driver.find_element(By.XPATH, "//span[normalize-space()='Create']").click()
    time.sleep(3)


def get_each_statues_tasks_count_before_adding_tasks():
    board_wrapper = driver.find_element(By.CLASS_NAME, "board-wrapper")
    columns = board_wrapper.find_elements(By.CLASS_NAME, "board-column")
    for column in columns:
        status_details = {
            "status_title": "",
            "tasks_count": ""
        }
        status_label = column.find_element(By.CLASS_NAME, "kanban-status-label").text
        status_name = re.sub(r'\(\d+\)', '', status_label)
        tasks = column.find_elements(By.CLASS_NAME, "task")
        tasks_count = (len(tasks))
        status_details["status_title"] = status_name
        status_details["tasks_count"] = tasks_count
        before_statues_details.append(status_details)
    print(before_statues_details)
    return


def get_all_statues():
    wrapper = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "board-wrapper")))
    statues_columns = wrapper.find_elements(By.CLASS_NAME, "board-column")
    for statues_column in statues_columns:
        statues.append(statues_column)
    time.sleep(3)


def add_tasks_to_boards():
    i = 1
    while i <= len(statues):
        wait.until(
            EC.visibility_of_element_located((By.XPATH, "(//div[@class='column-footer'])[" + str(i) + "]"))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Enter task name']"))).send_keys(
            faker.name(), "'s task" + Keys.ENTER)
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//button[@class='ant-btn add-task-btn-card me-2']"))).click()
        i += 1


def get_each_statues_tasks_count_after_adding_tasks():
    board_wrapper = driver.find_element(By.CLASS_NAME, "board-wrapper")
    columns = board_wrapper.find_elements(By.CLASS_NAME, "board-column")
    for column in columns:
        status_details = {
            "status_title": "",
            "tasks_count": ""
        }
        status_label = column.find_element(By.CLASS_NAME, "kanban-status-label").text
        status_name = re.sub(r'\(\d+\)', '', status_label)
        tasks = column.find_elements(By.CLASS_NAME, "task")
        tasks_count = (len(tasks))
        status_details["status_title"] = status_name
        status_details["tasks_count"] = tasks_count
        after_statues_details.append(status_details)
    print(after_statues_details)
    return


def write_csv_file():
    file_path = 'check_tasks_count.csv'
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=before_statues_details[0].keys())
        writer.writeheader()
        writer.writerows(before_statues_details)
        writer.writerow({})
        writer.writerows(after_statues_details)


main()
check_project_segment()
go_to_need_project_inside()
add_new_statues()
get_each_statues_tasks_count_before_adding_tasks()
get_all_statues()
add_tasks_to_boards()
get_each_statues_tasks_count_after_adding_tasks()
write_csv_file()
