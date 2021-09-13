from selenium import webdriver
from random import randint
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import Select

driver = webdriver.Firefox()

with open('wordlist.txt', 'r') as words:
    wordlist = [line.strip() for line in words]
unclaimed = []


def is_unclaimed(word):
    driver.get(f'https://www.twitter.com/{word}')
    time.sleep(3)
    body = driver.find_element_by_tag_name('body')
    if "This account doesn’t exist" in body.text and word not in 'paper':
        return word


def switchTabs():
    p = driver.current_window_handle
    tabs = driver.window_handles
    for tab in tabs:
        if tab != p:
            driver.switch_to.window(tab)
            time.sleep(1)


driver.get("https://mail.protonmail.com/login")
time.sleep(2)
emailbox = driver.find_element_by_id("username")
emailbox.send_keys('infinime')
passwordbox = driver.find_element_by_id("password")
passwordbox.send_keys('thisisme')
passwordbox.send_keys((Keys.ENTER))
time.sleep(3)
driver.execute_script('window.open("https://mail.protonmail.com/inbox", "_blank");')  # noqa: E501
switchTabs()

for word in wordlist:
    unclaimed += [is_unclaimed(word)]
print(unclaimed)

for name in set(unclaimed):
    if name is not None:
        driver.get('https://twitter.com/i/flow/signup')
        time.sleep(3)
        namebox = driver.find_element_by_name('name')
        spans = driver.find_elements_by_class_name('css-16my406')
        for x in spans:
            if "use email instead" in x.text.lower():
                useemailbtn = x
        useemailbtn.click()
        time.sleep(1)
        emailbox = driver.find_element_by_name('email')
        namebox.send_keys(name)
        emailbox.send_keys(f'infinime+{name}@protonmail.com')
        monthbox = Select(driver.find_element_by_id("Month"))
        daybox = Select(driver.find_element_by_id("Day"))
        yearbox = Select(driver.find_element_by_id('Year'))
        monthbox.select_by_index(randint(1, 12))
        daybox.select_by_index(randint(1, 31))
        yearbox.select_by_index(randint(19, 56))
        nextbtn = driver.find_element_by_class_name('r-urgr8i')
        nextbtn.click()
        time.sleep(2)
        nextbtn = driver.find_elements_by_class_name('css-18t94o4')[1]
        nextbtn.click()
        potentialSignUps = driver.find_elements_by_class_name('r-1awozwy')
        for x in potentialSignUps:
            if x.text == 'Sign up':
                signup = x
                break
        signup.click()
        switchTabs()
        time.sleep(20)
        driver.find_element_by_class_name('navigationItem-item').click()
        time.sleep(5)
        subjectText = driver.find_element_by_class_name("subject-text").text
        if "is your twitter verification code" in subjectText.lower():
            vCode = subjectText.split(" ")[0]
        switchTabs()
        vCodebox = driver.find_element_by_class_name("r-30o5oe")
        vCodebox.send_keys(vCode)
        nextbtn = driver.find_elements_by_class_name('css-18t94o4')[1]
        nextbtn.click()
        time.sleep(3)
        passwordbox = driver.find_element_by_class_name("r-30o5oe")
        passwordbox.send_keys("cl4!m3d247")
        nextbtn = driver.find_elements_by_class_name('css-18t94o4')[0]
        nextbtn.click()
