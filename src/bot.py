from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import pandas as pd
import os
thisfolder = os.path.dirname(os.path.abspath(__file__))


def execScript(script):
  exec(script)


class Window:
  def __init__(self, url='https://google.com'):
    self.driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()))

    self.driver.get(url)

  def getData(self, method, element):
    dataList = []
    rawdata = []
    print(element)
    if method == 'xpath':
      rawdata = self.driver.find_elements(by=By.XPATH, value=element)
    for d in range(len(rawdata)):
      text = rawdata[d].text
      if text != '':
        dataList.append(rawdata[d].text)
    print(len(dataList))
    return dataList

  def goToUrl(self, url):
    self.driver.get(url)

  def openTab(self, url='https://google.com'):
    print('In open tab function')
    script = f"window.open('{url}','_blank');"
    print(script)
    self.driver.execute_script(script)
    tabs = self.driver.window_handles
    self.driver.switch_to.window(tabs[-1])

  def closeTab(self, tabID):
    tabs = self.driver.window_handles
    self.driver.switch_to.window(tabs[tabID])
    self.driver.close()

  def switchTab(self, tabID):
    tabs = self.driver.window_handles
    self.driver.switch_to.window(tabs[tabID])

  def goBackHistory(self):
    self.driver.execute_script("window.history.go(-1)")
    sleep(3)

  def goForwardHistory(self):
    self.driver.execute_script("window.history.go(+1)")
    sleep(3)

  def closeBrowser(self):
    self.driver.quit()


class CSV:
  def __init__(self):
    pass

  def saveDictToCSV(self, dict, path, filename):
    df = pd.DataFrame(dict)
    df.to_csv(os.path.join(path, filename), encoding='utf-8')
