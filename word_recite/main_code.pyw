import sys
import random
import pyautogui
from tkinter import *
from pathlib import Path
from datetime import datetime
from finding import looking_up

import sys
sys.path.append('D:\Tools\VS Code\Python')
from _formal.Tkinter import Tkinter
from _formal.Method import dataOut, dataIn, center_window, interval_time, list_duplicate, day_reduce

now_name   = str(datetime.now()).split(' ')[0] + '.txt'
path_ori   = Path('D:\Tools\VS Code\Python\word_recite')
path_state = path_ori/'__pycache__'/'state.txt'
word_dir   = path_ori/'words'


def Temp():
    if dataOut(path_state)[0][0] == now_name: return True
    with open(path_state,'w',encoding='utf-8') as f:
        f.write(f'{[now_name]}\n')
    
    file_list = list(word_dir.glob('*'))
    for x in file_list:
        if x.is_file() and str(x).split('\\')[-1] != 'beyond.txt' and str(x).split('\\')[-1] != 'temp.txt':
            with open(x,'r',encoding='utf-8') as f:
                txt = f.read()
            if not txt:
                x.unlink()
                continue
            file_modify = datetime.fromtimestamp(x.stat().st_ctime)
            days = interval_time(file_modify)
            if days in [4, 8, 16, 30]:
                with open(word_dir/'temp.txt','a',encoding='utf-8') as f:
                    f.write(txt)
            elif days == 49:
                with open(word_dir/'beyond.txt','a',encoding='utf-8') as f:
                    f.write(txt)
            if days > 90:
                x.unlink()

    for x in ['temp.txt','beyond.txt']:
        if not (items := dataOut(word_dir/x)): continue
        dataIn(list_duplicate(items), word_dir/x)



# 
# 1 录入
# 

def Section_1():
    window = center_window("今天背没背心里有点数好吗，别玩了一天",640,270)
    frame = LabelFrame(window)
    frame.pack(expand='yes')
    Label(frame, text="Word", fg='grey', font=("Arial Bold", 10)).pack()
    txt_1 = Entry(frame, width=12)
    txt_1.pack()
    txt_1.focus()
    lbl_2 = Label(frame, text="(state)", font=("Arial Bold", 10))
    lbl_2.pack()

    def click_1(self=None, path=now_name):
        target_word = txt_1.get()
        txt_1.delete(0,END)

        if looking_up(path,target_word):
            lbl_2.configure(text='请检查!', fg="red")
        else:
            lbl_2.configure(text='stored!', fg="green")

    def click_2():
        yesterday_name = day_reduce(now_name)
        click_1(path=yesterday_name)

    Button(frame,text="Next", bg="orange", fg="red", command=click_1).pack()
    Button(window,text="yesterday's", bg="orange", fg="red", command=click_2).pack(anchor='se')

    window.lift()
    window.after(200, lambda: pyautogui.press('shift'))
    window.bind("<KeyPress-Return>", click_1)
    window.bind("<KeyPress-Escape>", lambda self: window.destroy())

    mainloop()



# 
# 2 背单词
# 

def Section_2():
    saved = []
    window = center_window(f'搞快点给我背知道吗，还有 {interval_time([2022,12,10])} 天就要六级了还搁这儿玩呢',640,270)
    frame = LabelFrame(window)
    frame.pack(expand='yes')
    frame_top = Frame(frame)
    frame_top.pack(fill='x')
    frame_bottom = Frame(frame)
    frame_bottom.pack(fill='x')
    frame_1 = LabelFrame(frame_top)
    frame_1.pack(side='left')
    frame_2 = LabelFrame(frame_top)
    frame_2.pack(side='left')
    frame_3 = LabelFrame(frame_top)
    frame_3.pack(side='left')
    frame_4 = Frame(frame_bottom)
    frame_4.pack(side='left')
    frame_5 = Frame(frame_bottom)
    frame_5.pack(side='right')

    w1=StringVar()
    w2=StringVar()
    w3=StringVar()
    w4=StringVar()

    def w_destroy(self=None):
        window.destroy()

    def One():
        nonlocal saved
        if not (items := dataOut(word_dir/'temp.txt')): 
            saved = []
            w_destroy()
            return True

        left = len(items)
        w4.set(f'剩余单词：{left-1}')
        rd=random.randint(0, left-1)
        saved = [items[rd][0],items[rd][1],items[rd][2]]
        w1.set(saved[0])
        w2.set(saved[1])
        items.pop(rd)

        dataIn(items, word_dir/'temp.txt')

    def check():
        while True:
            w3.set(' '*40)
            if One(): yield True
            yield
            w3.set(saved[2])
            yield

    func = check()
    def generator(self=None):
        if next(func): return True
    
    if generator(): return True

    Label(frame_1, text="Word", fg='grey').pack()
    Label(frame_1, textvariable=w1).pack()
    Label(frame_2, text="Accent", fg='grey').pack()
    Label(frame_2, textvariable=w2).pack()
    Label(frame_3, text="Meaning", fg='grey').pack()
    Label(frame_3, textvariable=w3).pack()
    Label(frame_4, textvariable=w4, fg='grey').pack()
    Button(frame_5, text="Next", bg="orange", fg="red", width=6, command=generator).pack(side='left')

    window.focus_force()
    window.bind("<Return>", generator)
    window.bind("<Button-4>", generator)
    window.bind("<KeyPress-Escape>", w_destroy)

    mainloop()

    if saved:
        with open(word_dir/'temp.txt', 'a', encoding='utf-8') as f:
            f.write(f'{saved}\n')



# 
# 3 测试
# 

def Section_3():
    saved = []
    window = center_window('来嘛，看哈你到底背到没把之前的单词',640,270)
    frame_1 = LabelFrame(window).pack()
    frame_2 = LabelFrame(window).pack()
    frame_3 = LabelFrame(window).pack()
    frame_4 = Frame(window)
    frame_4.pack(side='right')

    w1=StringVar()
    w2=StringVar()
    w3=StringVar()
    w4=StringVar()

    def w_destroy(self=None):
        window.destroy()

    def One():
        nonlocal saved
        if not (items := dataOut(word_dir/'beyond.txt')): 
            saved = []
            w_destroy()
            return True

        left = len(items)
        w4.set(f'剩余单词：{left-1}')
        rd=random.randint(0, left-1)
        saved = [items[rd][0],items[rd][1],items[rd][2]]
        w1.set(saved[0])
        w2.set(saved[1])
        w3.set(saved[2])
        items.pop(rd)

        dataIn(items, word_dir/'beyond.txt')

    def check():
        while True:
            if One(): yield True
            yield
            answer = txt_1.get()
            txt_1.delete(0,END)
            w1_v = w1.get()
            w2_v = w2.get()
            if w1_v!=answer:
                lbl_5.configure(text="Wrong!", fg="red")
                yield
                answer = txt_1.get()
                txt_1.delete(0,END)
                w1_v = w1.get()
                w2_v = w2.get()
                if w1_v==answer:
                    lbl_5.configure(text="(state)", fg="grey")
                    continue
                lbl_4.configure(text=f"正确答案是：{w1_v}, 读音为：{w2_v}")
                with open(word_dir/now_name, 'a', encoding='utf-8') as f:
                    f.write(f'{[w1_v,w2_v,w3.get()]}\n')
                yield
                txt_1.delete(0,END)
                lbl_4.configure(text="")
                lbl_5.configure(text="(state)", fg="grey")

    func = check()
    def generator(self=None):
        if next(func): return True

    if generator(): return True

    Label(frame_1, text="(meaning)", fg='grey').pack(side='top')
    Label(frame_1, textvariable=w3).pack(expand='yes')
    Label(frame_1, textvariable=w4, fg='grey').pack(expand='yes')
    Label(frame_2, text="请填写对应单词", fg='grey', font=("Arial Bold", 10)).pack(side='top')
    txt_1 = Entry(frame_2, width=12)
    txt_1.pack(expand='yes')
    lbl_4 = Label(frame_3, text="", fg='green')
    lbl_4.pack(side='top')
    lbl_5 = Label(frame_3, text="(state)", font=("Arial Bold", 10), fg='grey')
    lbl_5.pack(side='bottom')
    btn_1 = Button(frame_3, text="Next", bg="orange", fg="red", command=generator)
    btn_1.pack(expand='yes')

    txt_1.bind("<Return>", generator)
    window.lift()
    window.focus_force()
    txt_1.focus()
    window.after(200, lambda: pyautogui.press('shift'))
    window.bind("<Button-4>", generator)
    window.bind("<KeyPress-Escape>", w_destroy)

    mainloop()

    if saved:
        with open(word_dir/'beyond.txt', 'a', encoding='utf-8') as f:
            f.write(f'{saved}\n')



if not Temp():
    sys.exit(0)
Section_1()
Section_2()
Section_3()
