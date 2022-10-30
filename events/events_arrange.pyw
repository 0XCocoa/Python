from tkinter import *
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
from tkinter import scrolledtext
from  operator  import  itemgetter

import sys
sys.path.append('D:\Tools\VS Code\Python')
from _formal.Tkinter import Tkinter
from _formal.Method import interval_time, dele, dataIn, dataOut

now_time = str(datetime.now()).split(' ')[0]
path_ori = Path('D:\Tools\VS Code\Python\__pycache__')
path_event = path_ori/'events.txt'
path_account = path_ori/'account.txt'



def F(txt):
    po = txt.find(' ')
    if txt.count(' ')-1:
        po2 = txt.find(' ',po+1)
        return [txt[:po], datetime.now().year, int(txt[po+1:po2]), int(txt[po2+1:])]
    else:
        return [txt[:po], 0, 0, 0]


@dele
def list_delete(item: list, elem=None) -> list:
    return True if elem[-1]==0 else False

def arranging():
    if not (items := dataOut(path_event)): return
    items, deleted = list_delete(items)

    items.sort(key=lambda x: itemgetter(1,2,3)(x))
    
    items.extend(deleted)
    dataIn(items, path_event)


# 调整返回值为颜色
def get_color(time_list):
    res = interval_time(time_list)
    if res < 2:
        color = 'red'
    elif res < 4:
        color = 'orange'
    elif res > 7:
        color = 'grey'
    else:
        color = 'black'
    return color


def Account(append):
    items = dataOut(path_account)
    if items[-1][0] != now_time:
        items.append([now_time,0])
    money = float(items[-1][1]) + float(append.replace('+','.'))
    items[-1] = [now_time,round(money,2)]
    dataIn(items,path_account)


def account_show():
    items = dataOut(path_account)
    
    x_data = [x[0][5:] for x in items]
    y_data = [x[1] for x in items]
    for x, y in zip(x_data, y_data):
        plt.text(x, y, '%.00f' % y, ha='center', va='bottom', fontsize=7.5)
    
    plt.plot(x_data, y_data, 'bo--', alpha=0.5, linewidth=1, label='cost')

    plt.legend()
    plt.xlabel('date')
    plt.ylabel('costs')
    
    plt.show()



# 
# 1 添加
# 

def Input():
    tk = Tkinter('Input',480,280)
    tk.frame()
    tk.scrolledtext()

    def click_1():
        if not (txt := tk.t_get()): return
        for x in txt.split('\n'):
            if x.count(' '):
                with open(path_event,'a',encoding='utf-8') as f:
                    f.write(f'{F(x)}\n')
            else:
                Account(x)
        arranging()
        tk.window.destroy()
    tk.button(text="Save", bg="orange", fg="red", command=click_1)

    tk.after(tk._texts[0].focus)
    tk.bind("<Shift-KeyPress-Return>", click_1)
    tk._end()

    Open()



# 
# 2 显示事项
# 

def Open():
    global items,rank
    if not (items := dataOut(path_event)): return 1
    rank = [x for x in range(len(items))]

    tk = Tkinter(f'Today is :  {now_time}', 640,520)
    window = tk.window
    tk.frame(width=360, height=480, labelframe=1)
    tk.frame(0, 1, labelframe=1)
    

    tk.label(1, 10, text="event".rjust(12), note=1, side='left')
    tk.label(1, 11, text="deadline".rjust(16), note=1, side='right')

    for i in range(len(items)):
        tk.frame(0, 20+i, labelframe=1)
        state = BooleanVar()
        def clean(i):
            global rank, items
            tk._frames[20+i].destroy()
            index = rank.index(i)
            items.pop(index)
            rank.pop(index)
            dataIn(items, path_event)
        color = get_color(items[i][1:])
        Checkbutton(tk._frames[20+i], text=f"{i+1}. {items[i][0]}", var=state, font=("Arial Bold", 14), command=lambda: clean(i), fg=color).pack(side='left')
        text = '——' if not items[i][-1] else f"{items[i][2]}.{str(items[i][3]).rjust(2,'0')}"
        tk.label(20+i, text=text.rjust(12), font=("Arial Bold", 14), fg=color, side='right')

    def to_input():
        window.destroy()
        Input()
    
    tk.button(text="Append", bg="orange", fg="red", command=to_input, side='bottom')
    tk.button(tk.window, text="Account", bg="orange", fg="red", command=account_show, anchor='se')

    tk.bind("<Alt-a>", account_show)
    tk.bind("<KeyPress-Return>", to_input)
    tk._end()



if Open():
    Input()
