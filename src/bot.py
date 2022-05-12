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


key = dict(props(Keys))


class Window:
  def __init__(self, url='https://google.com'):
    self.driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()))

    self.driver.get(url)

  def getDataList(self, method, element, skipFirst=False):
    dataList = []
    rawdata = []
    print(element)
    rawdata = self.driver.find_elements(by=method, value=element)

    for d in range(len(rawdata)):
      text = rawdata[d].text
      if text != '':
        dataList.append(rawdata[d].text)

    if skipFirst:
      dataList = dataList[1:]
    return dataList

  def getDataTable(self, settings):
    """
    Takes a list of dict of column setting
    e.g
    [{'name': 'AUTO', 'find_by': 'xpath', 'element': '//td[@class="name"]' }, {'name': 'AUTO', 'find_by': 'xpath', 'element': '//td[@class="hh-salaries-sorted"]' }]
    

    returns a dict
    e.g
    {
      'columnone': ['item1', 'item2', 'item3'],
      'columntwo': ['item1', 'item2', 'item3']
    }
    
    """
    dataDict = {}
    for i in settings:
      data = self.getDataList(i['find_by'], i['element'], False)
      if i['name'] == 'AUTO':
        colName = data[0]
        dataDict[colName] = data[1:]
      else:
        dataDict[i['name']] = data

    return dataDict

  def getData(self, method, element):
    self.driver.find_element(method, element).text

  def goToUrl(self, url):
    self.driver.get(url)

  def openTab(self, url='https://google.com'):
    script = f"window.open('{url}','_blank');"
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

  def elementClick(self, method, element):
    self.driver.find_element(method, element).click()

  def elementInput(self, method, element, keysList):
    self.driver.find_element(method, element).send_keys(*keysList)

  def refreshPage(self, tabID):
    self.switchTab(tabID)
    self.driver.refresh()

  def saveImage(self, method, element, path, filename):
    img = self.driver.find_element(method, element)
    src = img.get_attribute('src')
    url.urlretrieve(src, os.path.join(path, filename))

  def screenShot(self, tabID, path, filename):
    self.switchTab(tabID)
    el = self.driver.find_element_by_tag_name('body')
    el.screenshot(os.path.join(path, filename))
  
  def waitElement(self, method, element, timeout):
    try:
      element_present = EC.presence_of_element_located((method, element))
      WebDriverWait(self.driver, timeout).until(element_present)
    except TimeoutException:
      print("Timed out waiting for element")

  def handleAlert(self, action, text=None):
    obj = self.driver.switch_to.alert
    msg = obj.text
    if action == 'accept':
      obj.accept()
    elif action == 'cancel':
      obj.dismiss()
    elif action == 'input':
      obj.send_keys(text)

    return msg

  def closeBrowser(self):
    self.driver.quit()
    

class CSV:
  def __init__(self):
    self.options = {
        'seperator': ',',
        'index': False,
        'encoding': 'utf-8'
    }

  def saveDictToCSV(self, dict, path, filename):
    df = pd.DataFrame(dict)
    df.to_csv(os.path.join(path, filename), encoding='utf-8', index=False)

  def dataFromCSV(self, path, filename):
    df = pd.read_csv(os.path.join(path, filename))
    return df.to_dict(orient='list')

  def mergeCSV(self, allFilePath, outputFilePath, options= None):
    if not options:
      options = self.options
    #combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f, sep=options['seperator'], engine='python') for f in allFilePath])
    #export to csv
    combined_csv.to_csv(outputFilePath, index=options['index'], encoding=options['encoding'])

  def splitCSV(self, filePath, outputDir, outputName, splitOptions, options=None):
    if not options:
      options = self.options
    # To do: remove duplicate values
    data = pd.read_csv(filePath, sep=options['seperator'], engine='python')
    if splitOptions['by'] == 'row':
      size = len(data) 
      length = splitOptions['length']
      count = 0
      
      start = count*length
      end = length*(count + 1)
      while start< size:

        if end > size:
          end = size
        df = data[start: end]
        df.to_csv(os.path.join(outputDir, f'{outputName}_{count+1}.csv'))
        count +=1
        start = count*length
        end = length*(count + 1)
    elif splitOptions['by'] == 'column':
      # To do: split CSV by column, split csv by value on a column
      pass



