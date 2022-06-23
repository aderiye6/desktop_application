from email import parser
import requests
from getmac import get_mac_address as gma
from configparser import ConfigParser
import os
thisfolder = os.path.dirname(os.path.abspath(__file__))
inifile = os.path.join(thisfolder, 'config.ini')
# baseURL = 'http://localhost:5000/api/v1'
baseURL = 'https://kophy-rpa.herokuapp.com/api/v1'
userid  = ''
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

def login(email, password, workspace_url):
  mac = gma()
  regURL = '/auth/login/machine'
  url = baseURL + regURL
  data = {
    # 'mac': str(mac),
    'email': email,
    'password': password,
    'workspace_url': workspace_url,
    'mac_id': gma()
  }
  res = requests.post(url, json=data)
  return res 

def getUserBot():
  mac = gma()
  botURL = f'/bots/{mac}'
  url = baseURL + botURL
  # data = {
  #     'mac_id': gma()
  # }
  headers = {"Authorization": f"Bearer {UserID().getUID()}"}
  res = requests.get(url, headers=headers)
  if res.status_code == 200:
    return res.json()['data']
  return []

def setBotData(data):
  global botData
  botData = data
# class UserID:
#   def __init__(self) -> None:
#     self.parser =  ConfigParser()
#     print(inifile)
#     self.parser.read(inifile)

#   def getUID(self):
#     return self.parser.get('user', 'uid')

#   def setUID(self, uid):
#     self.parser.set('user', 'uid', uid)
#     with open(inifile, 'w') as configFile:
#       self.parser.write(configFile)

class UserID:
  def __init__(self):
    self.uid = userid
  def getUID(self):
    return self.uid

  def setUID(self, uid):
    global userid
    userid = uid