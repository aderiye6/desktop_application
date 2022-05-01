from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import os
thisfolder = os.path.dirname(os.path.abspath(__file__))
driverPath = os.path.join(thisfolder, 'chromedriver.exe')

def execScript(script):
  exec(script)


def openBrowser(url='google.com'):
  driver = webdriver.Chrome(driverPath)
  driver.get(url)
  return driver


def getData(driver, method, element):
  dataList = []
  rawdata=[]
  print(element)
  if method == 'xpath':
    rawdata = driver.find_elements(by=By.XPATH, value=element)
  for d in range(len(rawdata)):
    text = rawdata[d].text
    dataList.append(rawdata[d].text)
  print(len(dataList))
  return dataList


def genDataTable(obj):
  print(obj)
  return pd.DataFrame(obj)

def saveDataTableCSV(dataTable, path, filename):
  dataTable.to_csv(os.path.join(path, filename), encoding='utf-8')

def closeBrowser(driver):
  driver.close()


