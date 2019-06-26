from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.common.keys import Keys
import pyperclip
from collections import defaultdict

# TODO: copy hands from the browsers that are running games.
def copyHands(browser,handle):
    if not windowInitd[handle]:
        handLog=ActionChains(browser)
        handLog.move_to_element_with_offset(browser.find_element_by_tag_name('body'),116,540)
        handLog.click()
        handLog.perform()

        ffwd=ActionChains(browser)
        ffwd.pause(1)
        ffwd.move_to_element_with_offset(browser.find_element_by_tag_name('body'),116,650)
        ffwd.click()
        ffwd.perform()

        for i in range(20):
            clearDisc=ActionChains(browser)
            clearDisc.pause(0.25)
            
            clearDisc.move_to_element_with_offset(browser.find_element_by_tag_name('body'),358,385)
            clearDisc.click()
            clearDisc.perform()
        
        print (browser.current_url)
    # copyAll.send_keys(Keys.CONTROL,'A')
    
# returns true iff the title of the browser is the (logged in) Home Page of Bluff Avenue.
def isBluffaveHomepage(browser):
    return browser.title=='Home Page - Bluff Avenue'

# log into Bluffave with the .creds
def loginToBluffave(browser):
    browser.get('http://www.bluffave.com/')
    # wait until the title of the login screen shows up
    WebDriverWait(browser,10).until(lambda x: 'Play your own private online poker cash games and tournaments! - Bluff Avenue' in browser.title)
    bluffaveUser = browser.find_element_by_xpath('//*[@id="loginForm_email"]')
    bluffaveUser.send_keys(creds[0])
    
    bluffavePass = browser.find_element_by_xpath('//*[@id="loginForm_password"]')
    bluffavePass.send_keys(creds[1]+'\n')
    #wait until we are logged in.
    WebDriverWait(browser, 10).until(isBluffaveHomepage)

# for each game, open it if the URL has not been seen by doing some jank clicks and waits on the Flash. 
def openGames(browser,urls):
    i=2
    bluffaveGames = browser.find_elements_by_xpath('//*[@id="homePlayingFriendsBox"]/div/div[2]/div/div[2]/table/tbody/tr['+str(i)+']/td[4]/a')
    
    while len(bluffaveGames)>0:
        bluffaveGames[0].click()
        currNumWindows=len(browser.window_handles)
        # if we have not visited this url and opened the site
        if browser.current_url not in urls:
            
            #click on the flash application with some pauses, because cannot grab by html
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
            # have we added a new window?
            if len(browser.window_handles)-currNumWindows>=1:
                #if so, add it to urls so we don't try again.
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
    # chrome_options.add_extension('uBlock-Origin_v1.20.0.crx')
    # may need to generalize for OS compatibility
    browser = webdriver.Chrome(chrome_options=chrome_options)
    
    # we expect mainHandles[0] to be the main handle.
    mainHandles=browser.window_handles
    assert len(mainHandles)==1

    windowInitd=defaultdict(bool)
    handLists=defaultdict(list)
    
    try:
        # browser.minimize_window()
        # browser.set_window_position(0,0)
        # browser.set_window_size(1360,730)
        
        urls=[]
        loginToBluffave(browser)
        # urls = openGames(browser,urls)
        # print(urls)
        while True:
            browser.switch_to.window(mainHandles[0])
            urls = openGames(browser,urls)
            # print(browser.window_handles)

            for handle in browser.window_handles:
                if not handle == mainHandles[0]:
                    # TODO: grab data!
                    browser.switch_to.window(handle)
                    copyHands(browser,handle)
            #try every 60 seconds.
            sleep(6)
    except AssertionError:
        print("AssertionError, title is wrong")
        browser.quit()
    except NoSuchWindowException:
        #we've closed a window or it crashed!
        print("window has been closed")
        # browser.quit()