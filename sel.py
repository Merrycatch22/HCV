from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

def isBluffaveHomepage(browser):
    return browser.title=='Home Page - Bluff Avenue'

def loginToBluffave(browser):
    browser.get('http://www.bluffave.com/')
    assert 'Play your own private online poker cash games and tournaments! - Bluff Avenue' in browser.title
    bluffaveUser = browser.find_element_by_xpath('//*[@id="loginForm_email"]')
    bluffaveUser.send_keys(creds[0])
    
    bluffavePass = browser.find_element_by_xpath('//*[@id="loginForm_password"]')
    bluffavePass.send_keys(creds[1]+'\n')
    
    WebDriverWait(browser, 10).until(isBluffaveHomepage)
    
def openGames(browser):
    i=2
    bluffaveGames = browser.find_elements_by_xpath('//*[@id="homePlayingFriendsBox"]/div/div[2]/div/div[2]/table/tbody/tr['+str(i)+']/td[4]/a')
    
    while len(bluffaveGames)>0:
        bluffaveGames[0].click()
        print(browser.current_url)
        
        tablesPlayingThisGame = WebDriverWait(browser,10).until(lambda x : x.find_element_by_xpath('//*[@id="cashLobby"]/embed'))
        clickFlash = ActionChains(browser)
        clickFlash.move_to_element_with_offset(tablesPlayingThisGame,190,228)
        clickFlash.pause(3)
        clickFlash.click()
        clickFlash.pause(3)
        clickFlash.click()
        clickFlash.perform()
        
        browser.get('http://www.bluffave.com/')
        WebDriverWait(browser, 10).until(isBluffaveHomepage)
        i+=1
        bluffaveGames = browser.find_elements_by_xpath('//*[@id="homePlayingFriendsBox"]/div/div[2]/div/div[2]/table/tbody/tr['+str(i)+']/td[4]/a')

if __name__ == '__main__':

    file = open(".creds","r")
    creds=file.read().splitlines()

    chrome_options = Options()
    chrome_options.add_argument('--always-authorized-plugins=true')
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_extension('uBlock-Origin_v1.20.0.crx')
    browser = webdriver.Chrome('chromedriver.exe',chrome_options=chrome_options)
        
    try:
        browser.set_window_position(0,0)
        browser.set_window_size(1360,730)
        browser.maximize_window()

        loginToBluffave(browser)
        openGames(browser)
    except AssertionError:
        print("AssertionError, title is wrong")
        browser.quit()
    except:
        print("other browser failure")
        browser.quit()