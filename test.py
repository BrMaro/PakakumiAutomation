from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import selenium.common.exceptions
from selenium.webdriver.common.keys import Keys
import time
import openpyxl
from openpyxl import Workbook

options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
url = "https://play.pakakumi.com/"
driver.get(url)
driver.implicitly_wait(10)

# skip the entry dialog box
skip_button = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[1]/div[2]/div/button")
skip_button.click()
driver.implicitly_wait(10)

busts = driver.find_elements(By.TAG_NAME, "tr")
busts.pop(0)

def count_elements(lst, number):
    count = 0
    for element in lst:
        if (element)<number:
            count += 1
    return count

for i, value in enumerate(busts):
    if value.text == "USER @ AMOUNT PROFIT":
        busts = busts[:i]
        busts.pop()
        break

bet_amount = 10
bet_win=15
bet_money =100
red_counter=0
green_counter = 0
sum=0
cleaned_bust_array = []
for bust in busts:
    bust = bust.text
    result = [char for char in bust if char != 'x']
    cleaned_bust = ''.join(result[:bust.index('x')])
    cleaned_bust_array.append(cleaned_bust)
    #print(cleaned_bust)

    if float(cleaned_bust) <= (bet_win/bet_amount+1):
        bet_money = bet_money - bet_amount
        red_counter +=1
    else:
        bet_money += bet_win
        green_counter+=1
    if bet_money <= 0:
        print("all money was lost")
        break
    if float(cleaned_bust)<2:
        sum += cleaned_bust

print(sum/(count_elements(cleaned_bust_array,2)))
print(f"Bet Win {i} == {bet_money}")
print(green_counter,red_counter)


print("sum of last", len(busts), "=", bet_money)



driver.quit()
