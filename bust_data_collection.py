from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions
from selenium.webdriver.common.keys import Keys
import time
import os
import re
from dotenv import load_dotenv

load_dotenv()

phone_number = os.getenv('PHONE_NUMBER')
password = os.getenv('PASSWORD')

print("\nPAKAKUMI AUTOMATION\n\n")

options = Options()
driver_path = 'C:\\Users\\Techron\\PycharmProjects\\chromedriver.exe'
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(options=options, service=service)
url = "https://play.pakakumi.com/"
driver.get(url)
driver.implicitly_wait(30)
time.sleep(10)


def save_csv_to_file(arr, file_name):
    arr = pd.DataFrame(arr)

    # Specify the file path for the CSV file
    csv_file_path = f'C:\\Users\\Techron\\PycharmProjects\\AeroBet\{file_name}'

    # Check if the CSV file already exists
    if not os.path.exists(csv_file_path):
        # If the file doesn't exist, create a new CSV file
        arr.to_csv(csv_file_path)
    else:
        # If the file already exists, append the new data to the end
        arr.to_csv(csv_file_path, mode='a', header=False)

    print("Saved to csv file")


def skip_entry_dialog_box():
    skip_button = driver.find_element(By.XPATH, "(//button[@role='button'])[1]")
    driver.implicitly_wait(10)
    print("Tutorial skipped.")
    skip_button.click()


def split_date_time(date_time_str):
    # Example date-time string from the Selenium output

    # Extracting the date and time using regular expressions
    # This pattern assumes the format "Sat, 24 August 2024 at 18:54:00"
    date_pattern = r"(\d{1,2} \w+ \d{4})"
    time_pattern = r"(\d{2}:\d{2}:\d{2})"

    # Find the date and time using the regex pattern
    date_match = re.search(date_pattern, date_time_str)
    time_match = re.search(time_pattern, date_time_str)

    if date_match and time_match:
        date_str = date_match.group(1)
        time_str = time_match.group(1)
        return date_str, time_str


bust_data = []


def main():
    skip_entry_dialog_box()

    # Latest bust
    latest_bust = driver.find_element(By.XPATH, "(//a[@class='css-19toqs6'])[1]")
    latest_bust.click()
    driver.implicitly_wait(10)

    while True:
        # Transtition to the Div with data
        div = driver.find_element(By.XPATH, "//div[@class='css-18aotig']")
        round_no = driver.find_element(By.XPATH, "(//div[@class='css-et0ovv'])[1]").text
        bust = driver.find_element(By.XPATH, "(//div[@class='css-et0ovv'])[2]").text
        date_and_time = driver.find_element(By.XPATH, "(//div[@class='css-et0ovv'])[3]").text
        date_str, time_str = split_date_time(date_and_time)

        print(f"Round No.: {round_no} Time: {time_str} Bust: {bust}")

        bust_data.append({
            "Round No.": round_no,
            "date": date_str,
            "time": time_str,
            "Bust": bust,
        })

        driver.find_element(By.XPATH,"(//a[@class='css-15qmqf7'])[1]").click()  # Previous Button
        driver.implicitly_wait(10)


save_csv_to_file(bust_data,"bust_data.csv")

main()





