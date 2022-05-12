from .bot import *
from threading import Thread
import os
thisfolder = os.path.dirname(os.path.abspath(__file__))
testfile = os.path.join(thisfolder, 'testscript.txt')


class RunBot(Thread):
  def __init__(self, botid, script, test):
    super().__init__()
    self.botID = botid
    if test:
      self.script = open(testfile, 'r').read()
    else:
      self.script = script

  def run(self):
    execScript(self.script)


