# Import the required libraries
from plistlib import UID
from tkinter import *
from pystray import MenuItem as item
import pystray
from PIL import Image, ImageTk
from src.app import Application
from src.service import auth, UserID, getUserBot

isAuth = False
res = auth()

if res.status_code == 200:
  
  authData = res.json()
  UserID().setUID(authData['data']['mac_id'])
  print(authData['data']['mac_id'])
  isAuth = True
  getUserBot()

print(res.json())
app = Application(auth=isAuth)

# Define a function for quit the window

def quit_window(icon, item):
  icon.stop()
  app.destroy()

# Define a function to show the window again

def show_window(icon, item):
  icon.stop()
  app.after(0, app.deiconify())

# Hide the window and show on the system taskbar


def hide_window():
  app.withdraw()
  image = Image.open("image.ico")
  menu = (item('Quit', quit_window), item('Show', show_window))
  icon = pystray.Icon("name", image, "title", menu)
  icon.run()


# app.protocol('WM_DELETE_WINDOW', hide_window)

app.mainloop()
