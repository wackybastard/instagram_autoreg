import string
import random

import config

from random import choice

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from selenium_stealth import stealth
from fake_useragent import UserAgent
from time import sleep

from mail import MailAccount


url = 'https://instagram.com/accounts/emailsignup/'


class InstagramAccount():

    def __init__(self, login, password):
        self.login = login
        self.password = password
        print(f'{login}:{password} has been registered!')

    def write(self, file):
        file.append(f'{self.login}:{self.password}')


def parse_proxy():

    with open('proxy.txt', 'r') as file:
        proxy_list = file.read().split('\n')[0:-1]

    return proxy_list


def set_options(proxy):

    options = webdriver.ChromeOptions()
    options.add_argument('start-maximized')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument(f'--proxy-server={proxy}')
    return options


def init_driver(options, useragent):

    driver = webdriver.Chrome(options=options)
    stealth(driver,
            user_agent=useragent.random,
            languages=['en-US', 'en'],
            vendor='Google Inc.',
            platform='Win32',
            webgl_vendor='Intel Inc.',
            renderer='Intel Iris OpenGL Engine',
            fix_hairline=True
            )
    return driver


def generate_data():

    login = ''.join(random.sample(string.ascii_lowercase, k=20))
    password = ''.join(random.sample(string.printable, k=8))
    return login, password


def accept_cookies(driver):

    button = driver.find_element(by=By.XPATH, value='/html/body/div[4]/div/div/button[1]')
    sleep(2)
    button.click()
    sleep(config.sleep_time)


def fill_form(driver, login, password, mail):

    email_label = driver.find_element(by=By.NAME, value='emailOrPhone')
    email_label.send_keys(mail)

    fullname_label = driver.find_element(by=By.NAME, value='fullName')
    fullname_label.send_keys('Vano')

    username_label = driver.find_element(by=By.NAME, value='username')
    username_label.send_keys(login)

    password_label = driver.find_element(by=By.NAME, value='password')
    password_label.send_keys(password)

    sleep(config.sleep_time)

    button = driver.find_element(by=By.XPATH, value='/html/body/div[1]/section/main/div/div/div[1]/div[2]/form/div[7]/div/button')
    button.click()


def fill_birthdate(driver):

    mounth = driver.find_element(by=By.XPATH, value='/html/body/div[1]/section/main/div/div/div[1]/div/div[4]/div/div/span/span[1]/select')
    mounth_select = Select(mounth)
    mounth_select.select_by_index(random.randrange(1, 12))

    day = driver.find_element(by=By.XPATH, value='/html/body/div[1]/section/main/div/div/div[1]/div/div[4]/div/div/span/span[2]/select')
    day_select = Select(day)
    day_select.select_by_index(random.randrange(1, 28))

    year = driver.find_element(by=By.XPATH, value='/html/body/div[1]/section/main/div/div/div[1]/div/div[4]/div/div/span/span[3]/select')
    year_select = Select(year)
    year_select.select_by_index(random.randrange(21, 29))

    sleep(config.sleep_time)

    button = driver.find_element(by=By.XPATH, value='/html/body/div[1]/section/main/div/div/div[1]/div/div[6]/button')
    button.click()


def fill_code(driver, code):

    code_label = driver.find_element(by=By.NAME, value='email_confirmation_code')
    code_label.send_keys(code)

    button = driver.find_element(by=By.XPATH, value='//*[@id="react-root"]/section/main/div/div/div[1]/div[2]/form/div/div[2]/button')
    button.click()


def register(url, mail_account, driver):

    driver.get(url)

    login, password = generate_data()

    accept_cookies(driver)

    fill_form(driver, login, password, mail_account.address)

    sleep(config.sleep_time)

    fill_birthdate(driver)

    code = mail_account.get_code()

    fill_code(driver, code)

    return login, password


def main():

    proxy_list = parse_proxy()

    options = set_options(choice(proxy_list))

    useragent = UserAgent()

    driver = init_driver(options, useragent)

    mail_account = MailAccount(config.token, config.mail_type)

    login, password = register(url, mail_account, driver)

    account = InstagramAccount(login, password)
    account.write()


if __name__ == '__main__':

    main()
