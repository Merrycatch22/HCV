from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.common.keys import Keys
import pyperclip

# TODO: copy hands from the browsers that are running games.
def copyHands(browser):
    copyAll=ActionChains(browser)
    copyAll.move_by_offset(0,0)
    copyAll.click()

    copyAll.send_keys(Keys.CONTROL,'A')

# returns true iff the title of the browser is the (logged in) Home Page of Bluff Avenue.
def isBluffaveHomepage(browser):
    return browser.title=='Home Page - Bluff Avenue'

# log into Bluffave with the .creds
def loginToBluffave(browser):
    browser.get('http://www.bluffave.com/')
    assert 'Play your own private online poker cash games and tournaments! - Bluff Avenue' in browser.title
    bluffaveUser = browser.find_element_by_xpath('//*[@id="loginForm_email"]')
    bluffaveUser.send_keys(creds[0])
    
    bluffavePass = browser.find_element_by_xpath('//*[@id="loginForm_password"]')
    bluffavePass.send_keys(creds[1]+'\n')
    
    WebDriverWait(browser, 10).until(isBluffaveHomepage)

# for each game, open it if the URL has not been seen by doing some jank clicks and waits on the Flash. 
def openGames(browser,urls):
    i=2
    bluffaveGames = browser.find_elements_by_xpath('//*[@id="homePlayingFriendsBox"]/div/div[2]/div/div[2]/table/tbody/tr['+str(i)+']/td[4]/a')
    
    while len(bluffaveGames)>0:
        bluffaveGames[0].click()
        currNumWindows=len(browser.window_handles)
        # print(browser.current_url)
        if browser.current_url not in urls:
            
            tablesPlayingThisGame = WebDriverWait(browser,10).until(lambda x : x.find_element_by_xpath('//*[@id="cashLobby"]/embed'))
            clickFlash = ActionChains(browser)
            clickFlash.move_to_element_with_offset(tablesPlayingThisGame,190,228)
            clickFlash.pause(3)
            clickFlash.click()
            clickFlash.pause(3)
            clickFlash.click()
            clickFlash.perform()
        
        #sad sleeping
        sleep(3)
        print(len(browser.window_handles)-currNumWindows)
        if len(browser.window_handles)-currNumWindows>=1:
            urls.append(browser.current_url)
            print(browser.current_url)

        browser.get('http://www.bluffave.com/')
        WebDriverWait(browser, 10).until(isBluffaveHomepage)
        i+=1
        bluffaveGames = browser.find_elements_by_xpath('//*[@id="homePlayingFriendsBox"]/div/div[2]/div/div[2]/table/tbody/tr['+str(i)+']/td[4]/a')

    return urls
if __name__ == '__main__':

    file = open(".creds","r")
    creds=file.read().splitlines()

    chrome_options = Options()
    chrome_options.add_argument('--always-authorized-plugins=true')
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_extension('uBlock-Origin_v1.20.0.crx')
    browser = webdriver.Chrome('chromedriver.exe',chrome_options=chrome_options)
    
    mainHandles=browser.window_handles
    assert len(mainHandles)==1

    try:
        # browser.minimize_window()
        # browser.set_window_position(0,0)
        # browser.set_window_size(1360,730)
        
        urls=[]
        loginToBluffave(browser)
        # urls = openGames(browser,urls)
        # print(urls)
        while True:
            urls = openGames(browser,urls)
            # print(browser.window_handles)
            sleep(60)
    except AssertionError:
        print("AssertionError, title is wrong")
        browser.quit()
    except NoSuchWindowException:
        print("window has been closed")
        print(set(browser.window_handles)-mainHandles)
        # browser.quit()