from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.request as url
from time import sleep
import pandas as pd
import os
thisfolder = os.path.dirname(os.path.abspath(__file__))


def props(x):
    return dict((key, getattr(x, key)) for key in dir(x) if key not in dir(x.__class__))


def execScript(script):
  exec(script)



# class window:
#   def openBrowser(url='https://google.com'):
#     driver = webdriver.Chrome(
#         service=Service(ChromeDriverManager().install()))

#     driver.get(url)
#     return (driver, 1)

#   def goToUrl(driver, url):
#     driver.get(url)
# # driver, pageid = window.openBrowser()
# # window.goToUrl(driver, "https://venrena.com")


class Browser:
  def openBrowser(url='https://google.com', options={'browser': 'Chrome', 'maximised': True}):
    driver = None
    if options['browser'] == 'Chrome':
      driver = webdriver.Chrome(
          service=Service(ChromeDriverManager().install()))
    else:
      driver = webdriver.Chrome(
          service=Service(ChromeDriverManager().install()))
    if options['maximised']:
      driver.maximize_window()
    driver.get(url)
    return (driver, 0)

  def goToUrl(driver, pageid, url, options={'time_out': 30, 'same_tab': True}):
    driver.set_page_load_timeout(options['time_out'])
    tabs = driver.window_handles
    driver.switch_to.window(tabs[pageid])
    if options['same_tab']:
      driver.get(url)
      return pageid
    else:
      script = f"window.open('{url}','_blank');"
      driver.execute_script(script)
      return pageid + 1

  def closeBrowser(driver):
    driver.quit()

  def closeTab(driver, tabID):
    tabs = driver.window_handles
    driver.switch_to.window(tabs[tabID])
    driver.close()

  def switchTab(driver, tabID):
    tabs = driver.window_handles
    driver.switch_to.window(tabs[tabID])
    return tabID

  def getDataList(driver, method, element, skipFirst=False):
    dataList = []
    rawdata = []
    print(element)
    rawdata = driver.find_elements(by=method, value=element)

    for d in range(len(rawdata)):
      text = rawdata[d].text
      if text != '':
        dataList.append(rawdata[d].text)

    if skipFirst:
      dataList = dataList[1:]
    return dataList

  def getDataTable(driver, tabID, settings):
    tabs = driver.window_handles
    driver.switch_to.window(tabs[tabID])
    """
    Takes a list of dict of column setting
    e.g
    [{'name': 'AUTO', 'selectortype': 'xpath', 'selector': '//td[@class="name"]' }, {'name': 'AUTO', 'find_by': 'xpath', 'element': '//td[@class="hh-salaries-sorted"]' }]
    

    returns a dict
    e.g
    {
      'columnone': ['item1', 'item2', 'item3'],
      'columntwo': ['item1', 'item2', 'item3']
    }
    
    """
    dataDict = {}
    for i in settings:
      data = Browser.getDataList(
          driver, i['selectortype'], i['selector'], False)
      if i['name'] == 'AUTO':
        colName = data[0]
        dataDict[colName] = data[1:]
      else:
        dataDict[i['name']] = data

    return dataDict


class CSV:
  # def __init__(self):
  #   self.options = {
  #       'seperator': ',',
  #       'index': False,
  #       'encoding': 'utf-8'
  #   }

  def saveDictToCSV(dict, filepath, options=None):
    if not options:
      options = {
          'seperator': ',',
          'index': False,
          'encoding': 'utf-8'
      }
    df = pd.DataFrame(dict)
    df.to_csv(filepath,
              sep=options['seperator'], index=options['index'], encoding=options['encoding'])

  def dataFromCSV(path, filename, options=None):
    if not options:
      options = {
          'seperator': ',',
          'index': False,
          'encoding': 'utf-8'
      }
    df = pd.read_csv(os.path.join(path, filename), sep=options['seperator'])
    return df.to_dict(orient='list')
