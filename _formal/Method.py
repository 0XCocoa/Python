import functools



# 
# 键鼠操作
# 

import pyautogui
from pynput import mouse, keyboard

global ctrl1, ctrl2
ctrl1=mouse.Controller()
ctrl2=keyboard.Controller()

def mouse_click(position_x, position_y, count=1):
    global ctrl1
    ctrl1.position = (position_x, position_y)
    ctrl1.click(mouse.Button.left, count)

def key_click(key, count=1):
    global ctrl2
    for i in range(count):
        ctrl2.press(key)
        ctrl2.release(key)



# 
# 时间模块
# 

import time
from datetime import datetime

def time_cost(func):
    @functools.wraps(func)
    def wrapper(*args, **kargs):
        start_time = time.time()
        f = func(*args,**kargs)
        exec_time = time.time() - start_time
        print(f'程序: {func.__name__} 用时：{round(exec_time,3)}秒')
        return f
    return wrapper

def interval_time(*args: list) -> int:
    # 使args可以被修改
    args = list(args)

    for i in range(len(args)):
        # 是否为datetime类型数据
        if not isinstance(args[i],list):
            args[i] = [args[i].year,args[i].month,args[i].day]

        # 里面是否为字符串
        if not isinstance(args[i][0],int) \
        or not isinstance(args[i][1],int) \
        or not isinstance(args[i][2],int):
            args[i] = list(map(int,args[i]))
    
    # 是否只传入一个
    if len(args) == 1:
        args.append([datetime.now().year,datetime.now().month,datetime.now().day])

    if [0,0,0] in args:
        return 9999

    res = 0
    months = [31,28,31,30,31,30,31,31,30,31,30,31]
    def adjust(year):
        return bool((year%4==0 and year%100) or year%400==0)
     
    for i in range(args[0][0],args[1][0]):
        res+=adjust(i)+365
    
    months[1] = adjust(args[0][0])+28
    for i in range(1,args[0][1]):
        res-=months[i]
    months[1] = adjust(args[1][0])+28
    for i in range(1,args[1][1]):
        res+=months[i]
    
    res-=args[0][2]
    res+=args[1][2]

    return abs(res)

def day_reduce(ori: str, reduce: int=1) -> str:
    ori_1,ori_2 = ori[:10],ori[10:]
    months = [31,28,31,30,31,30,31,31,30,31,30,31]
    def adjust(year):
        return bool((year%4==0 and year%100) or year%400==0)
    item = ori_1.split('-')
    if item[2] == '01':
        if item[1] == '01':
            item[0] = str(int(item[0])-1)
            item[1] = '12'
            item[2] = '31'
        else:
            months[1] = adjust(int(item[0]))+28
            item[1] = str(int(item[1])-1).rjust(2,'0')
            item[2] = str(months[int(item[1])-1])
    else:
        item[2] = str(int(item[2])-1).rjust(2,'0')
    return '-'.join(item) + ori_2



# 
# clipboard操作
# 

import win32con
import win32clipboard as cp

def copy_to(text):
    state = None
    try:
        cp.OpenClipboard() 
        cp.EmptyClipboard() 
        cp.SetClipboardData(win32con.CF_UNICODETEXT, text)
    except:
        state = True
    finally:
        cp.CloseClipboard()
        return state



# 
# 数学方法
# 

# from  operator  import  itemgetter
# items  =  [( '2' ,  '3' ,  '10' ), ( '1' ,  '2' ,  '3' ), ( '5' ,  '6' ,  '7' ), ( '2' ,  '5' ,  '10' ), ( '2' ,  '4' ,  '10' )]
# res = sorted(items, key = lambda x: list(map(eval,itemgetter(2, 1)(x))))


# 
# tkinter方法
# 

from tkinter import *

def center_window(title: str, width: int, height: int) -> Tk:
    window=Tk()
    w_distance=(window.winfo_screenwidth()-width)//2
    h_distance=(window.winfo_screenheight()-height)//2
    window.title(title)
    window.geometry(f"{width}x{height}+{w_distance}+{h_distance}")
    return window



# 
# 文件操作
# 

def dataOut(path: str) -> list:
    with open(path, 'r', encoding='utf-8') as f:
        items = f.readlines()
    if not items:
        return []

    try:
        # 还原双重列表原始数据类型
        items = list(map(eval,items))
        for i,item in enumerate(items):
            for j,elem in enumerate(item):
                try:
                    temp = eval(elem)
                    if str(temp) == elem:
                        items[i][j] = temp
                    else:
                        print(f'未将元素：{elem} 转换为：{temp}')
                except Exception:
                    pass
    except:
        raise TypeError('dataOut的对象要求是双重列表')

    return items

def dataIn(items: list, path: str):
    with open(path,'w',encoding='utf-8') as f:  
        res = '\n'.join(map(str,items))
        res += '\n' if res else ''
        f.write(res)



# 
# 列表操作
# 

def dele(func):
    @functools.wraps(func)
    def wrapper(*args):
        deleted = []
        to_delete = []
        for i,x in enumerate(*args):
            if func(*args, x):
                to_delete.append(i)
                deleted.append(x)
        for i in reversed(to_delete):
            args[0].pop(i)
        return args[0], deleted
    return wrapper

@dele
def list_delete(item: list, elem=None) -> list:
    return True if elem else False


def list_duplicate(items: list) -> list:
    return [x for i, x in enumerate(items) if x not in items[:i]] 



# 
# 线程操作
# 

from threading import Thread

def add_to_thread(func) -> None:
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        Thread(target=func, args=args, kwargs=kwargs).start()
        return
    return wrapper