
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def FNC_OpeningChromeViaSelenium(executablePath):

    service = Service(executable_path=executablePath)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    ###driver = webdriver.Chrome(executable_path=executablePath)
    ####driver = webdriver.Chrome(ChromeDriverManager().install())

    return driver
