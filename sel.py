from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from time import sleep
from selenium.webdriver.support.ui import WebDriverWait

def loginToBluffave(browser):
    browser.get('http://www.bluffave.com/')
    assert 'Play your own private online poker cash games and tournaments! - Bluff Avenue' in browser.title
    bluffaveUser = browser.find_element_by_xpath('//*[@id="loginForm_email"]')
    bluffaveUser.send_keys(creds[0])
    
    bluffavePass = browser.find_element_by_xpath('//*[@id="loginForm_password"]')
    bluffavePass.send_keys(creds[1]+'\n')


if __name__ == '__main__':

    file = open(".creds","r")
    creds=file.read().splitlines()

    chrome_options = Options()
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_extension('uBlock-Origin_v1.20.0.crx')
    browser = webdriver.Chrome('chromedriver.exe',chrome_options=chrome_options)
    try:
        browser.set_window_position(0,0)
        browser.set_window_size(1360,730)
        browser.maximize_window()

        loginToBluffave(browser)
    except AssertionError:
        print("AssertionError, title is wrong")
        browser.quit()
    except:
        print("other browser failure")
        browser.quit()