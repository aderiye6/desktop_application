from email import parser
import requests
from getmac import get_mac_address as gma
from configparser import ConfigParser
import os
thisfolder = os.path.dirname(os.path.abspath(__file__))
inifile = os.path.join(thisfolder, 'config.ini')
baseURL = 'http://localhost:5000/api/v1'

botData = []

def auth():
  mac = gma()
  authURL = '/user/machine/login'
  url = baseURL + authURL
  data = {
    'mac': str(mac)
  }
  res = requests.post(url, json=data)

  return res

def register(email, password, macName):
  mac = gma()
  regURL = '/user/machine/register'
  url = baseURL + regURL
  data = {
    'mac': str(mac),
    'email': email,
    'password': password,
    'mac_name': macName
  }
  res = requests.post(url, json=data)
  return res 

def getUserBot():
  authURL = '/bots/'
  url = baseURL + authURL
  data = {
    'mac_id': UserID().getUID()
  }
  res = requests.get(url, params=data)
  print(res.json())
  if res.status_code == 200:
    return res.json()['data']
  return []

def setBotData(data):
  global botData
  botData = data
class UserID:
  def __init__(self) -> None:
    self.parser =  ConfigParser()
    self.parser.read(inifile)

  def getUID(self):
    return self.parser.get('user', 'uid')

  def setUID(self, uid):
    print(self.getUID())
    print('called uid', uid)
    self.parser.set('user', 'uid', uid)
    with open(inifile, 'w') as configFile:
      self.parser.write(configFile)
