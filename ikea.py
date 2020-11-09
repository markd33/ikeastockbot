from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json

#set up webdriver in headless and URL
options = Options()
options.add_argument('--headless')
browser = webdriver.Chrome(executable_path = 'chromedriver.exe',options=options)
browser.implicitly_wait(5)   #wait for page to load

#get URL
URL = 'https://www.ikea.com/ca/en/p/markus-office-chair-vissle-dark-gray-90289172/'
browser.get(URL)

#If located, check stock
if len(browser.find_elements_by_class_name('range-revamp-stockcheck__item-link')) != 0:
    result = browser.find_element_by_class_name('range-revamp-stockcheck__item-link')

    if 'Out of stock' in result.text:
        newstatus = 'Out of stock'
    else:
        newstatus = 'In stock'

#else select location then check stock
else:
    browser.find_element_by_id('webcaLocationButton').click()
    browser.find_element_by_id('webcaLocationUIButtonChange').click()
    browser.find_element_by_xpath('//button[text()=" IKEA Coquitlam "]').click()
    browser.find_element_by_id('webcaLocationUIButtonClose').click()
    result = browser.find_element_by_class_name('range-revamp-stockcheck__item-link')

    if 'Out of stock' in result.text:
        newstatus = 'Out of stock'
    else:
        newstatus = 'In stock'

#overwrite status in JSON
with open('ikeainfo.json', 'r+') as f:
    json_data = json.load(f)
    json_data['oldstatus'] = json_data['newstatus']
    json_data['newstatus'] = newstatus
    f.seek(0)
    f.write(json.dumps(json_data))
    f.truncate()

#email alert if status has changed
if json_data['newstatus'] != json_data['oldstatus']:
    finalstatus = 'Product is now ' + json_data['newstatus'].lower()
    print(finalstatus)

#exit the browser/webdriver
browser.quit()