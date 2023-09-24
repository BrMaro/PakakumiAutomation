from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions
from selenium.webdriver.common.keys import Keys
import time
import random
import pywhatkit
from openpyxl import Workbook, load_workbook
import openpyxl
import os
import subprocess


phone = input("Enter your phone number: ")
password = input("Enter your password: ")

options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome()
url = "https://play.pakakumi.com/"
driver.get(url)
driver.implicitly_wait(30)
time.sleep(10)

# skip the entry dialog box
wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div/div[1]/div[2]/div/button")))
skip_button = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[1]/div[2]/div/button")
driver.implicitly_wait(10)
skip_button.click()


# enter login details
def login_details(phone, password):
    login = driver.find_element(By.XPATH, "/html/body/div/div[2]/div[1]/div/div[4]/div/a[1]")
    login.click()
    phone_number = driver.find_element(By.XPATH, "html/body/div/div[3]/div/div/div/div/div[1]/div/input")
    phone_number.send_keys(phone)
    pas = driver.find_element(By.XPATH, "/html/body/div/div[3]/div/div/div/div/div[2]/div/input")
    pas.send_keys(password)
    time.sleep(2)
    button = driver.find_element(By.CLASS_NAME, "css-d5jaaj")
    button.click()
    driver.implicitly_wait(10)
    time.sleep(5)
    skip_button = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[1]/div[2]/div/button")
    skip_button.click()
    print("Signed in")


def previous_bets_calculation(bet_money):
    initial_money = bet_money
    busts = driver.find_elements(By.TAG_NAME, "tr")
    busts.pop(0)

    for i, value in enumerate(busts):
        if value.text == "USER @ AMOUNT PROFIT":
            busts = busts[:i]
            busts.pop()
            break

    bet_amount = 100
    bet_win = 0.5 * bet_amount
    for bust in busts:
        bust = bust.text
        result = [char for char in bust if char != 'x']
        cleaned_bust = ''.join(result[:bust.index('x')])

        if float(cleaned_bust) < 1.5:
            bet_money = bet_money - bet_amount
        else:
            bet_money += bet_win
        if bet_money == 0:
            print("all money was lost")
            break
    print("Average of last", len(busts), "=", bet_money)
    if bet_money > initial_money:
        print("profitable")
    else:
        print("Non-profitable")
    print(bet_money)


def bet_placement(bet_amount, auto_cashout):
    bet_amount_input = driver.find_element(By.XPATH,
                                           "(//input[@class='css-10zyika'])[1]")
    driver.implicitly_wait(1)
    bet_amount_input.send_keys(Keys.CONTROL + "a")
    bet_amount_input.send_keys(Keys.DELETE)
    bet_amount_input.send_keys(bet_amount)

    auto_cashout_input = driver.find_element(By.XPATH, "(//input[@class='css-10zyika'])[2]")
    driver.implicitly_wait(1)
    auto_cashout_input.send_keys(Keys.CONTROL + "a")
    auto_cashout_input.send_keys(Keys.DELETE)
    auto_cashout_input.send_keys(auto_cashout)
    driver.implicitly_wait(1)
    bet_button = driver.find_element(By.XPATH,
                                     "//span[text()='Bet']")

    bet_button.click()


def green_counter(cleaned_bust_array):
    # maintain a red vs green counter to evade the occurrences of red
    red_counter = 0
    green_counter = 0
    for i in cleaned_bust_array:
        if float(i) > auto_cashout:
            green_counter += 1
        else:
            red_counter += 1
    # print(green_counter,red_counter)
    return green_counter


def bet_money_calculation(account_money, green_counter):
    if account_money > 100 and green_counter >= 4:
        bet_money = 0.1 * account_money
    else:
        bet_money = 10
    return bet_money


def cleaned_busts():
    busts = driver.find_elements(By.TAG_NAME, "tr")
    busts.pop(0)
    cleaned_bust_array = []

    # isolate the busts and clean them to remain with floats
    for i, value in enumerate(busts):
        if value.text == "USER @ AMOUNT PROFIT":
            busts = busts[:i]
            busts.pop()
            break

    for bust in busts:
        bust = bust.text
        result = [char for char in bust if char != 'x']
        cleaned_bust = ''.join(result[:bust.index('x')])
        cleaned_bust_array.append(cleaned_bust)
    return cleaned_bust_array

def is_clickable(element):
    try:
        return element.is_enabled() and element.is_displayed()
    except:
        return False

login_details(phone,password)
driver.implicitly_wait(10)

initial_balance = driver.find_element(By.XPATH, "//*[@id='root']/div[2]/div[1]/div/div[4]/div/div[1]/a")
initial_balance = float(initial_balance.text.replace('KES ', ''))
print(f"Intial money in account = {initial_balance}")
max_profit = 0
account_money = 1000

while True:
    auto_cashout = 1.5
    losses = 0
    try:
        bet_button = driver.find_element(By.XPATH,"//span[text()='Bet']")
        bet_money = 10
        while bet_button.is_enabled() and bet_button.is_enabled():
            cleaned_bust_array = cleaned_busts()
            new_balance = initial_balance
            current_balance = driver.find_element(By.XPATH, "//*[@id='root']/div[2]/div[1]/div/div[4]/div/div[1]/a")
           # profit = float(current_balance.text.replace('KES ', '')) - initial_balance
            driver.implicitly_wait(10)


            if float(cleaned_bust_array[0]) <= 2:
                #bet_placement(bet_money, auto_cashout)
                account_money -= bet_money
                bet_money *=2

            else:
                account_money += bet_money
                bet_money = 10

                driver.implicitly_wait(2)
                print(cleaned_bust_array[0])
                print("Bet Value:",bet_money)
                print("Account:",account_money)
                # print(f"Current Balance:{current_balance.text}")
                # print(f"Profits:{round(profit, 3)}")
                # print(f"Max profit:{round(max_profit, 3)}")
                # print(f"Disparity with Max profit:{round(max_profit - profit, 3)}")
            while not bet_button.is_enabled():
                time.sleep(1)


    except selenium.common.exceptions.ElementClickInterceptedException:
        pass
    except selenium.common.exceptions.NoSuchWindowException:
        pass
    except KeyboardInterrupt:
        pass
    except selenium.common.exceptions.StaleElementReferenceException:
        pass
    except ValueError:
        pass
    except selenium.common.exceptions.NoSuchElementException:
        pass
    except ConnectionRefusedError:
        pass
driver.quit()
"""

documents_path = 'C:\\Users\\Techron\\Documents'
excel_path = "C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\EXCEL.EXE"
wb.save(os.path.join(documents_path, "odds.xlsx"))
subprocess.run([excel_path, "odds.xlsx"])



MOre parameters to add later
if the current bust goes above 2, then there is a high chance that the next one will definitely go above 2
if the current bust is above 20 then the next one is less that 1
if i make 3 or 4 losses in a row wait for 30 secs

            # if cleaned_bust_array[0]==1.03:
            #    auto_cashout = 2

"""
