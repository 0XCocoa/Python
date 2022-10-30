import ctypes
from tkinter import *

from pathlib import Path
from tkinter import scrolledtext

class Tkinter:
    # 
    # 创建类
    def __init__(self, title: str='', width: int=None, height: int=None, **kwargs):
        window=Tk()
        self.window = window
        vg = lambda key: kwargs.get(key)

        # 调整分辨率
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        ScaleFactor=ctypes.windll.shcore.GetScaleFactorForDevice(0)
        window.tk.call('tk', 'scaling', ScaleFactor/75)

        if width and height:
            w_distance=(window.winfo_screenwidth()-width)//2
            h_distance=(window.winfo_screenheight()-height)//2
            window.geometry(f"{width}x{height}+{w_distance}+{h_distance}")
        window.title(title)
        if vg('expand'):
            window.state("zoomed")
        if vg('top'):
            window.attributes("-topmost", True)

        self._frames = {}
        self._labels = {}
        self._texts = {}

    def frame(self, root=None, tag=0, **kwargs):
        vg = lambda key: kwargs.get(key)
        root = self.window if root == None else self._frames[root]
        frame = LabelFrame(root, width=vg('width'), height=vg('height')) \
            if vg('labelframe') else Frame(root, width=vg('width'), height=vg('height'))
        if not (expand := vg('expand')): expand = 'yes'
        frame.pack(expand=expand, side=vg('side'), anchor=vg('anchor'), fill=vg('fill'))
        self._frames[tag] = frame

    def label(self, frame=0, tag=0, **kwargs):
        vg = lambda key: kwargs.get(key)
        if isinstance(frame, int):
            frame = self._frames[frame]
        if vg('type') == 1:
            kwargs['font'] = ("Arial Bold", 12)
            kwargs['fg'] = 'grey'
            tag = 100
        label = Label(
            frame, 
            text = vg('text'), 
            font = vg('font'), 
            fg = vg('fg'),
            textvariable = vg('textvariable')
        )
        label.pack(expand=vg('expand'), side=vg('side'), anchor=vg('anchor'))
        self._labels[tag] = label

    def text(self, frame=0, tag=0, **kwargs):
        vg = lambda key: kwargs.get(key)
        if isinstance(frame, int):
            frame = self._frames[frame]
        if not vg('width'):
            kwargs['width'] = 12
        txt = Entry(
            frame, 
            width = vg('width')
        )
        txt.pack(expand=vg('expand'), side=vg('side'), anchor=vg('anchor'))
        txt.focus()
        self._texts[tag] = txt

    def button(self, frame=0, **kwargs):
        vg = lambda key: kwargs.get(key)
        if isinstance(frame, int):
            frame = self._frames[frame]
        Button(
            frame, 
            text = vg('text'), 
            bg = vg('bg'), 
            fg = vg('fg'), 
            command = vg('command')
        ).pack(expand=vg('expand'), side=vg('side'), anchor=vg('anchor'))

    def checkbutton(self, frame=0, **kwargs):
        vg = lambda key: kwargs.get(key)
        if isinstance(frame, int):
            frame = self._frames[frame]
        state = BooleanVar()
        Checkbutton(
            frame, 
            var = state, 
            text = vg('text'), 
            font = vg('font'), 
            bg = vg('bg'), 
            fg = vg('fg'), 
            command = vg('command')
        ).pack(expand=vg('expand'), side=vg('side'), anchor=vg('anchor'))
        
    def scrolledtext(self, frame=0, tag=0, **kwargs):
        vg = lambda key: kwargs.get(key)
        if isinstance(frame, int):
            frame = self._frames[frame]
        text = scrolledtext.ScrolledText(
            frame, 
            width=vg('width') if vg('width') else 40, 
            height=vg('height') if vg('height') else 10,
        )
        text.pack(expand=vg('expand'), side=vg('side'), anchor=vg('anchor'))
        self._texts[tag] = text


    # 
    # 方法类
    def t_get(self, tag=0):
        txt = self._texts[tag]
        if isinstance(txt, Entry):
            text = txt.get().strip()
            txt.delete(0,END)
        else:
            text = txt.get(1.0, END).strip()
            txt.delete(1.0, END)
        return text
    
    def l_config(self, tag=0, **kwargs):
        self._labels[tag].configure(**kwargs)

    def clearTk(self):
        self._frames = {}
        self._labels = {}
        self._texts = {}
        for child in self.window.winfo_children():
            child.destroy()
    
        
    # 
    # 结束
    def after(self, func, time=200):
        self.window.after(time, func)
    
    def bind(self, button, func, item=None):
        target = item if item else self.window
        if not isinstance(button, list): button = [button]
        for x in button:
            target.bind(x, lambda self: func())

    def _end(self, loop=True):
        window = self.window
        window.lift()
        window.focus_force()
        window.bind("<KeyPress-Escape>", lambda self: window.destroy())
        window.mainloop()


# 
# 集成类方法
def choose_path() -> str:
        global path
        path = Path('D:/')
        tk = Tkinter('$$ get your file_path $$', 640, 480, expand=1)

        def get_in(change):
            global path
            tk.clearTk()
            path = change
            show()

        def get_back():
            global path
            tk.clearTk()
            path = path.parent
            show()

        def show():
            tk.frame(labelframe=1)
            item = [elem for elem in path.glob('*')]
            if not item:
                tk.window.destroy()
            for i,elem in enumerate(item):
                exec(f"""
def click_i():
    get_in(elem)
if (place := 1 + i//20) == len(tk._frames):
    tk.frame(0, place, side='left')
txt = elem.name if elem.is_file() else elem.name + ' /'
color = 'orange' if elem.is_file() else 'green'
tk.button(place, text=txt.center(40), fg=color, command=click_i)""", 
{'i':i, 'elem':elem, 'tk':tk, 'get_in':get_in})
                        
        show()
        tk.bind(['<BackSpace>', '<Button-4>'], get_back)
        tk._end()
        return str(path)