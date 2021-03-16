from tkinter import *
from tkinter import ttk
import tk_tools as tools
import webbrowser
import numpy as np

window = Tk()
window.title("일정관리자")
window.geometry('900x400')

rowheader = []
colheader = []
board = []
palette = {}

with open("일정관리자\\palette.txt") as data :
    temp = data.read().splitlines()
    for i in temp :
        p = i.split(" | ")
        palette[p[0]] = p[1]

with open("일정관리자\\board.txt") as data :
    temp = data.read().splitlines()
    colheader = temp[0].split(" | ")
    temp = temp[1:]
    for i in range(len(temp)) :
        temp[i] = temp[i].split(" | ")
        rowheader.append(temp[i][0])
        board.append(temp[i][1:])

gateways = []
headerentrys = []

class GateWay() :
    def __init__(self,i,j) :
        self.i = i
        self.j = j
        gateways[i].append(ttk.Combobox(window,values=list(palette.keys()),validate="focus"))
        gateways[i][j].config(validatecommand=lambda:gateways[i+0][j+0].get() in np.transpose(np.array(paletteboard.get()))[0])
        gateways[i][j].config(invalidcommand=lambda:gateways[i+0][j+0].current(0))
        gateways[i][j].set(board[j][i])
        gateways[i][j].bind('<Button-3>',lambda event : webbrowser.open_new_tab(palette[gateways[i][j].get()]))
        gateways[i][j].place(x=i*90+60,y=j*30+30,width=90,height=30)


for i in range(len(board[0])) :
    gateways.append([])
    Label(window,text=colheader[i],relief="groove").place(x=i*90+60,y=0,width=90,height=30)
    for j in range(len(rowheader)) :
        GateWay(i,j)

for j in range(len(rowheader)) :
    headerentrys.append(ttk.Entry(window))
    headerentrys[j].insert(0,rowheader[j])
    headerentrys[j].place(x=0,y=j*30+30,width=60,height=30)

paletteboard = tools.MultiSlotFrame(window,2)
paletteboard.place(x=i*90+150,y=0)
Button(window,text="AddOption",command=lambda:paletteboard.add(["",""])).place(x=i*90+465,y=0)
for i in palette.keys() :
    paletteboard.add([i,palette[i]])



window.mainloop()