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


key = dict(props(Keys))

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
  def openBrowser(url='https://google.com', options={'browser': 'Chrome', 'maximized': True}):
    driver = None
    if options['browser'] == 'Chrome':
      driver = webdriver.Chrome(
          service=Service(ChromeDriverManager().install()))
    else:
      driver = webdriver.Chrome(
          service=Service(ChromeDriverManager().install()))
    if options['maximized']:
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
  def goBackHistory(driver, tabID, times):
    tabs = driver.window_handles
    driver.switch_to.window(tabs[tabID])
    driver.execute_script(f"window.history.go({-1 * times})")
    sleep(3)

  def goForwardHistory(driver, tabID, times):
    tabs = driver.window_handles
    driver.switch_to.window(tabs[tabID])
    driver.execute_script(f"window.history.go({times})")
    sleep(3)

  def elementClick(driver, tabID, method, element, options={"clicktype": "Single Click"}):
    tabs = driver.window_handles
    driver.switch_to.window(tabs[tabID])
    driver.find_element(by=method, value=element).click()

  def elementInput(driver, tabID, method, element, keysList):
    tabs = driver.window_handles
    driver.switch_to.window(tabs[tabID])
    driver.find_element(by=method, value=element).send_keys(*keysList)


  def refreshPage(driver, tabID):
    tabs = driver.window_handles
    driver.switch_to.window(tabs[tabID])
    driver.refresh()

  def saveImage(driver, tabID, method, element, filePath):
    tabs = driver.window_handles
    driver.switch_to.window(tabs[tabID])
    img = driver.find_element(by=method, value=element)
    src = img.get_attribute('src')
    url.urlretrieve(src,filePath)
    return filePath

  def screenShot(driver, tabID, filePath):
    tabs = driver.window_handles
    driver.switch_to.window(tabs[tabID])
    el = driver.find_element_by_tag_name('body')
    el.screenshot(filePath)
    return filePath

  def waitElement(driver, tabID, method, element, options = {"condition": "To appear", "timeout": 30}):
    tabs = driver.window_handles
    driver.switch_to.window(tabs[tabID])
    try:
      if options["condition"] == "To appear":
        element_present = EC.presence_of_element_located((method, element))
        WebDriverWait(driver, options["timeout"]).until(element_present)
    except TimeoutException:
      pass
      # print("Timed out waiting for element")

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

  def dataFromCSV(filePath, options=None):
    if not options:
      options = {
          'seperator': ',',
          'index': False,
          'encoding': 'utf-8'
      }
    df = pd.read_csv(filePath, sep=options['seperator'])
    return df.to_dict(orient='list')

  def mergeCSV(allFilePath, outputFilePath, options=None):
    if not options:
      options = {
          'seperator': ',',
          'index': False,
          'encoding': 'utf-8'
      }
    #combine all files in the list
    combined_csv = pd.concat(
        [pd.read_csv(f, sep=options['seperator'], engine='python') for f in allFilePath])
    #export to csv
    combined_csv.to_csv(
        outputFilePath, index=options['index'], encoding=options['encoding'])

  def splitCSV(filePath, outputDir, outputName, maxRows, options=None):
    if not options:
      options = {
          'seperator': ',',
          'index': False,
          'encoding': 'utf-8'
      }
    # To do: remove duplicate values
    data = pd.read_csv(filePath, sep=options['seperator'], engine='python')
    size = len(data)
    length = maxRows
    count = 0

    start = count*length
    end = length*(count + 1)
    while start < size:

      if end > size:
        end = size
      df = data[start: end]
      df.to_csv(os.path.join(outputDir, f'{outputName}_{count+1}.csv'))
      count += 1
      start = count*length
      end = length*(count + 1)

    return outputDir
    # if splitOptions['by'] == 'row':
    #   size = len(data)
    #   length = splitOptions['length']
    #   count = 0

    #   start = count*length
    #   end = length*(count + 1)
    #   while start < size:

    #     if end > size:
    #       end = size
    #     df = data[start: end]
    #     df.to_csv(os.path.join(outputDir, f'{outputName}_{count+1}.csv'))
    #     count += 1
    #     start = count*length
    #     end = length*(count + 1)
    # elif splitOptions['by'] == 'column':
    #   # To do: split CSV by column, split csv by value on a column
    #   pass
