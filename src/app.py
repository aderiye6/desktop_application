

import tkinter as tk
from tkinter import DISABLED, ttk
from tkinter.font import NORMAL
from turtle import width
from .service import register, UserID, botData, setBotData, getUserBot
from .bot import execScript


class FirstPage(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    # self.configure(bg='blue')
    emailLabel = tk.Label(self, text="Enter your email E-mail")
    emailLabel.place(x=100, y= 100, width= 150, height= 30)
    
    emailEntry = tk.Entry(self, text='')
    emailEntry.place(x=280, y=100, width=150, height=30)


    passwordLabel = tk.Label(self, text="Enter your email password")
    passwordLabel.place(x=100, y=160, width=150, height=30)

    passwordEntry = tk.Entry(self, text='')
    passwordEntry.place(x=280, y=160, width=150, height=30)

    macLabel = tk.Label(self, text="Enter your PC name")
    macLabel.place(x=100, y=220, width=150, height=30)

    macEntry = tk.Entry(self, text='')
    macEntry.place(x=280, y=220, width=150, height=30)
    Button = tk.Button(self, text="Register PC", font=(
        "Arial", 15), command=lambda: self.reg(emailEntry.get(), passwordEntry.get(), macEntry.get(), controller))
    Button.place(x=220, y=280)

  def reg(self, email, password, macName, controller):
    # To do: include validators before calling register function.
    res = register(email, password, macName)
    print(res.status_code)
    if res.status_code == 201:
      authData = res.json()
      UserID().setUID(authData['data']['mac_id'])
      print('setup successful')
      getUserBot()
      controller.show_frame(SecondPage)
    else: 
      pass

class SecondPage(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    columns = ('num','name', 'description', 'date_modified')
    self.tree = ttk.Treeview(self, columns=columns, show='headings')
    self.tree.heading('num', text='No.')
    self.tree.heading('name', text='Name')
    self.tree.heading('description', text='Description')
    self.tree.heading('date_modified', text='Date Modified')

    self.tree.column('num', width=60)
    self.tree.column('name', width=140)
    self.tree.column('description', width=250)
    self.tree.column('date_modified', width=130)
    self.bots = []
    self.updateBotList()
    self.tree.grid(row=0, column=0, sticky='nsew')
    self.tree.bind("<<TreeviewSelect>>", self.item_selected)

    # add a scrollbar
    scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
    self.tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')
    self.refreshButton = tk.Button(self, text="Refresh List", font=(
        "Arial", 15), command=lambda: refreshList(''))
    self.refreshButton.place(x=160, y=280)
    self.execButton = tk.Button(self, text="Run Bot", font=(
        "Arial", 15), command=lambda: execScript(self.script))
    self.execButton['state'] = DISABLED
    self.execButton.place(x=320, y=280)
    self.script = ''

  def refreshList(self):
    pass
  def updateBotList(self):
    self.bots = getUserBot()
    for bot in [(a + 1, b['bot_name'], b['bot_desc'], b['updated_at']) for a, b in enumerate(self.bots)]:
      self.tree.insert('', tk.END, values=bot)

  def item_selected(self, event):
    for selected_item in self.tree.selection():
      item = self.tree.item(selected_item)
      record = item['values']
      self.execButton['state'] = NORMAL
      self.script= self.bots[record[0] - 1]['script']
      # show a message
      print(record)

class PopUp(tk.Toplevel):
  def __init__(self, parent):
    #To do: Add pop up window for warning and error mesages
    pass

class Application(tk.Tk):
  def __init__(self, auth, *args, **kwargs):
    tk.Tk.__init__(self, *args, **kwargs)
    auth = auth

    self.title("Awesome RPA")
    self.iconbitmap("./image.ico")
    self.pageTuple = (FirstPage, SecondPage)
    # creating a window
    window = tk.Frame(self)
    window.pack()

    window.grid_rowconfigure(0, minsize=350)
    window.grid_columnconfigure(0, minsize=700)
    self.minsize(600,350)
    self.maxsize(600, 350)
    self.frames = {}
    for F in self.pageTuple:
      frame = F(window, self)
      self.frames[F] = frame
      frame.grid(row=0, column=0, sticky="nsew")

    if(auth):
      self.show_frame(SecondPage)
    else:
      self.show_frame(FirstPage)

  def show_frame(self, page):
    frame = self.frames[page]
    frame.tkraise()

  def refresh_page(self, page):
    self.show_frame(self.pageTurple[page])

