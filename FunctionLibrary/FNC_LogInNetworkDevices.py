import time
from selenium.webdriver.common.by import By
import serial
import subprocess
import socket

def FNC_LogIn5GODUSRT853L(driver, URLAddress):
    ### Accessing WebGUI via Selenium Webdriver
    driver.get(URLAddress)
    ### Inputing WebGUI with Username & Password
    username = driver.find_element(By.ID, "username")
    username.send_keys("")
    password = driver.find_element(By.ID, "password")
    password.send_keys("")
    ### Clicking LOGIN button
    driver.find_element(By.ID, "login").click()
    ### (1) - Firstly Accessing 5G-ODU's Tab: Mobile Network
    driver.find_element(By.ID, "label-mobilenetwork").click()
    time.sleep(1)
    ### (2) - Secondly Accessing 5G-ODU's Inner-Tab: RF Parameters
    driver.find_element(By.ID, 'rfparamters').click()
    time.sleep(1)
    ### (3) - Thirdly Clicking the right hand side content of RF Parameters
    driver.find_element(By.ID, 'rfparam').click()
    time.sleep(1)
    return driver

def FNC_LogIn5GODUGMOD513(driver, URLAddress):
    ### Accessing WebGUI via Selenium Webdriver
    driver.get(URLAddress)
    time.sleep(1)
    ### (0) - Proceed to unsafe website
    try:
        driver.find_element(By.XPATH, "// *[ @ id = 'details-button']").click()
        driver.find_element(By.XPATH, "//*[@id='proceed-link']").click()
        time.sleep(1)

        driver.find_element(By.XPATH, "// *[ @ id = 'MainLogOut']").click()
        time.sleep(1)
    except:
        driver.find_element(By.XPATH, "// *[ @ id = 'MainLogOut']").click()
        time.sleep(1)

    ### Inputing WebGUI with Password
    password = driver.find_element(By.ID, "IndexLoginPwd")
    password.send_keys("")
    ### Clicking LOGIN button
    driver.find_element(By.XPATH, "//*[@id='btLoginForm']").click()

    ### (1) - Firstly Accessing 5G-ODU's Tab: Mobile Network
    driver.switch_to.frame("MainMenu")
    driver.find_element(By.XPATH, "//*[@id='mainNewMenuLoginNetwork']").click()

    driver.switch_to.default_content()
    driver.switch_to.frame("content")
    driver.switch_to.frame("networkContent")
    time.sleep(1)
    return driver

def FNC_SerialConnect5GODUSRT853L(port, baudrate=115200):
    ### Function to initialize serial connection
    ser = serial.Serial(port, baudrate, timeout=1)
    if ser.is_open:
        print(f"Connected to {port} at {baudrate} baud.")
    return ser


def FNC_SerialConnectAccuver():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    sock.connect(("127.0.0.1", int(7890)))
    return sock