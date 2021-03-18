from tkinter import *
from tkinter import ttk
import tk_tools as tools
import webbrowser
import numpy as np

def rowsave() :
  with open("palette.dat",'w') as data :
    for i in paletteboard.get()[:-1] :
      data.write(i[0]+" | "+i[1]+"\n")
    data.write(paletteboard.get()[-1][0]+" | "+paletteboard.get()[-1][1])
  with open("board.dat","w") as data :
    for i in colheaderentrys[:-1] :
      data.write(i.get()+" | ")
    data.write(colheaderentrys[-1].get())
    temp = np.transpose(np.array(gateways))
    for i in enumerate(temp) :
      data.write("\n"+rowheaderentrys[i[0]].get())
      for j in i[1] :
        data.write(" | "+j.get())

def save(event=None) :
  if event == None :
    rowsave()
  elif event.state == 12 :
    rowsave()

Chrome_Path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"

window = Tk()
window.title("schedule_manager")
window.geometry('900x500')

rowheader = []
colheader = []
board = []
palette = {}

with open("palette.txt") as data :
  temp = data.read().splitlines()
  for i in temp :
    p = i.split(" | ")
    palette[p[0]] = p[1]

with open("board.txt") as data :
  temp = data.read().splitlines()
  colheader = temp[0].split(" | ")
  temp = temp[1:]
  for i in range(len(temp)) :
    temp[i] = temp[i].split(" | ")
    rowheader.append(temp[i][0])
    board.append(temp[i][1:])

gateways = []
rowheaderentrys = []
colheaderentrys = []

class GateWay() :
  def __init__(self,i,j) :
    self.i = i
    self.j = j
    gateways[i].append(ttk.Combobox(window,values=list(palette.keys()),validate="focus"))
    gateways[i][j].config(validatecommand=self.validating)
    gateways[i][j].config(invalidcommand=lambda:gateways[i+0][j+0].current(0))
    gateways[i][j].set(board[j][i])
    gateways[i][j].bind('<Button-1>',self.validating)
    gateways[i][j].bind('<Button-3>',self.openweb)
    gateways[i][j].place(x=i*90+60,y=j*30+30,width=90,height=30)

  def validating(self,event=None) :
    gateways[self.i][self.j]["values"] = list(np.transpose(np.array(paletteboard.get()))[0])
    return gateways[self.i][self.j].get() in np.transpose(np.array(paletteboard.get()))[0]

  def openweb(self,event=None) :
    palette = {}
    for i in paletteboard.get() :
      palette[i[0]] = i[1]
    if not self.validating() :
      gateways[self.i][self.j].current(0)
    webbrowser.get(Chrome_Path).open_new_tab(palette[gateways[self.i][self.j].get()])

for i in range(len(board[0])) :
  gateways.append([])
  colheaderentrys.append(Entry(window,text=colheader[i],relief="groove"))
  colheaderentrys[i].insert(0,colheader[i])
  colheaderentrys[i].place(x=i*90+60,y=0,width=90,height=30)
  for j in range(len(rowheader)) :
    GateWay(i,j)

for j in range(len(rowheader)) :
  rowheaderentrys.append(ttk.Entry(window))
  rowheaderentrys[j].insert(0,rowheader[j])
  rowheaderentrys[j].place(x=0,y=j*30+30,width=60,height=30)

def addoption() :
  paletteboard.add(["",""])
  for gates in gateways :
    for gate in gates :
      gate["values"] = list(np.transpose(np.array(paletteboard.get()))[0])

paletteboard = tools.MultiSlotFrame(window,2)
paletteboard.place(x=i*90+150,y=0)
Button(window,text="AddOption",command=addoption).place(x=i*90+465,y=0)
for i in palette.keys() :
  paletteboard.add([i,palette[i]])

Button(window,text="Save",command=save).place(width=60,height=30)
window.bind("<s>",save)


window.mainloop()