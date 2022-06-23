

import tkinter as tk
from tkinter import DISABLED, ttk
from tkinter.font import NORMAL
from turtle import width
from .service import login, UserID, botData, setBotData, getUserBot
# from .bot import execScript
from .script import RunBot

class FirstPage(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    # self.configure(bg='blue')
    emailLabel = tk.Label(self, text="Enter your email E-mail")
    emailLabel.place(x=100, y=100, width=150, height=30)

    emailEntry = tk.Entry(self, text='')
    emailEntry.place(x=280, y=100, width=150, height=30)

    passwordLabel = tk.Label(self, text="Enter your password")
    passwordLabel.place(x=100, y=160, width=150, height=30)

    passwordEntry = tk.Entry(self, text='', show='*')
    passwordEntry.place(x=280, y=160, width=150, height=30)

    workLabel = tk.Label(self, text="Workspace url")
    workLabel.place(x=100, y=220, width=150, height=30)

    workEntry = tk.Entry(self, text='')
    workEntry.place(x=280, y=220, width=150, height=30)
    Button = tk.Button(self, text="Login", font=(
        "Arial", 15), command=lambda: self.login(emailEntry.get(), passwordEntry.get(), workEntry.get(), controller))
    Button.place(x=220, y=280)

  # def reg(self, email, password, macName, controller):
  #   # To do: include validators before calling register function.
  #   res = register(email, password, macName)
  #   print(res.status_code)
  #   if res.status_code == 201:
  #     authData = res.json()
  #     UserID().setUID(authData['data']['mac_id'])
  #     print('setup successful')
  #     controller.show_frame(SecondPage)
  #     controller.updateList()
  #   else:
  #     pass

  def login(self, email, password, workurl, controller):
    # To do: include validators before calling register function.
    res = login(email, password, workurl)
    if res.status_code == 200:
      authData = res.json()
      UserID().setUID(authData['data']['access_token'])
      controller.show_frame(SecondPage)
      controller.updateList()
    else:
      pass


class SecondPage(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    columns = ('num', 'name', 'description','status', 'date_modified')
    self.tree = ttk.Treeview(self, columns=columns, show='headings')
    self.tree.heading('num', text='No.')
    self.tree.heading('name', text='Name')
    self.tree.heading('description', text='Description')
    self.tree.heading('status', text='Status')
    self.tree.heading('date_modified', text='Date Modified')

    self.tree.column('num', width=60)
    self.tree.column('name', width=100)
    self.tree.column('description', width=200)
    self.tree.column('status', width=80)
    self.tree.column('date_modified', width=130)
    self.bots = []
    # self.updateBotList()
    self.tree.grid(row=0, column=0, sticky='nsew')
    self.tree.bind("<<TreeviewSelect>>", self.item_selected)

    # add a scrollbar
    scrollbar = ttk.Scrollbar(
        self, orient=tk.VERTICAL, command=self.tree.yview)
    self.tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')
    self.refreshButton = tk.Button(self, text="Refresh List", font=(
        "Arial", 15), command=lambda: self.updateBotList())
    self.refreshButton.place(x=160, y=280)
    self.execButton = tk.Button(self, text="Run Bot", font=(
        "Arial", 15), command=self.hadleRun)
    self.execButton['state'] = DISABLED
    self.execButton.place(x=320, y=280)
    self.script = ''
  def hadleRun(self):
    botThread = RunBot(1, self.script, False)
    botThread.start()
    self.monitor(botThread)

  def monitor(self, thread):
      if thread.is_alive():
        # check the thread every 100ms
        self.after(100, lambda: self.monitor(thread))
      # else:
      #   print("bot run")
  def updateBotList(self):
    self.bots = getUserBot()
    for i in self.tree.get_children():
      self.tree.delete(i)
    for bot in [(a + 1, b['name'], '', b['status'], b['updated_at']) for a, b in enumerate(self.bots)]:
      self.tree.insert('', tk.END, values=bot)

  def item_selected(self, event):
    for selected_item in self.tree.selection():
      item = self.tree.item(selected_item)
      record = item['values']
      if self.bots[record[0] - 1]['status'] == 'CONNECTED':
        self.execButton['state'] = NORMAL
        self.script = self.bots[record[0] - 1]['script']
      else:
        self.execButton['state'] = DISABLED
      # show a message


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
    self.minsize(600, 350)
    self.maxsize(600, 350)
    self.frames = {}
    for F in self.pageTuple:
      frame = F(window, self)
      self.frames[F] = frame
      frame.grid(row=0, column=0, sticky="nsew")

    if(auth):
      self.updateList()
      self.show_frame(SecondPage)
    else:
      self.show_frame(FirstPage)

  def show_frame(self, page):
    frame = self.frames[page]
    frame.tkraise()

  def refresh_page(self, page):
    self.show_frame(self.pageTuple[page])

  def updateList(self):
    self.frames[SecondPage].updateBotList()
