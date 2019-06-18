from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
chrome_options.add_extension(r'C:\Users\tarn\workspace\uBlock-Origin_v1.20.0.crx')
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get('http://bluffave.com/')