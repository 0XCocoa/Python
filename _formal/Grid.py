from tkinter import *
from _formal.Tkinter import Tkinter

class Grid:
    def __init__(self, size=45, line=14, left=20, tag=True, load=False):
        self.size = size
        self.line = line
        self.left = left
        self.po_line = [size*i+left for i in range(line+1)]

        round = size*line+left*2
        tk = Tkinter('',round,round)
        cv = Canvas(tk.window,bg='white',height=round,width=round)
        cv.pack(expand='yes')

        self.tk = tk
        self.cv = cv

        for y in range(line):
            for x in range(line):
                tag = f'{x}_{y}' if tag else ''
                self.elem_create(x,y,x+1,y+1,tag=tag)
        tk._end(False)
        cv.bind('<Button-1>', self.put)
        tk.window.bind('<Control-s>', self.save)
        tk.window.bind('<Control-z>', self.back)

        if load: self.load()

    def elem_create(self,x1,y1,x2=None,y2=None,kind='rectangle',offset=0,fill='white',tag=''):
        size = self.size
        po_line = self.po_line
        if not x2: x2 = x1
        if not y2: y2 = y1
        exec(f'self.cv.create_{kind}(po_line[x1]-size*offset,po_line[y1]-size*offset,po_line[x2]+size*offset,po_line[y2]+size*offset,fill=fill,tags=("{tag}"))')

    def put(self, event):
        size = self.size
        left = self.left
        cv = self.cv
        if not isinstance(event, tuple):
            x = (event.x - left)//size
            y = (event.y - left)//size
            self.temp = (x,y)
            print(f'po: {(event.x, event.y)}, elem: {(x, y)}')
        else:
            x,y = event
            print(f'elem: {(x, y)}')
        c_color = cv.itemcget(f'{x}_{y}', 'fill')
        if c_color == 'white':
            cv.itemconfig(f'{x}_{y}', fill='black')
        else:
            cv.itemconfig(f'{x}_{y}', fill='white')

    def back(self, event):
        self.put(self.temp)

    def tract(self, x, y, end, state=1):
        if not state:
            self.save()
            self.layout[y*self.line+x] = 'brown'
            if not self.tract(x,y,end):
                print('not found...')
            return
        print(f'now: ({x},{y})')
        line = self.line
        layout = self.layout
        max = len(layout)
        if (x,y) == end:
            layout[y*line+x] = 'brown'
            self.load(layout)
            return 1
        if (po := y*line+x+1)<max and layout[po] == 'white':
            layout[po] = 'red'
            if self.tract(x+1, y, end):
                return 1
        if (po := (y+1)*line+x) and layout[po] == 'white':
            layout[po] = 'red'
            if self.tract(x, y+1, end):
                return 1
        if (po := y*line+x-1) and layout[po] == 'white':
            layout[po] = 'red'
            if self.tract(x-1, y, end):
                return 1
        if (po := (y-1)*line+x) and layout[po] == 'white':
            layout[po] = 'red'
            if self.tract(x, y-1, end):
                return 1
        layout[y*line+x] = 'white'
        return 0
        
    def after(self, func):
        self.tk.window.after(200,func)

    def change_bind(self, button, func):
        self.tk.window.unbind(button)
        self.tk.window.bind(button, func)

    def save(self, event=None):
        line = self.line
        cv = self.cv
        layout = [cv.itemcget(f'{x}_{y}', 'fill') for y in range(line) for x in range(line)]
        self.layout = layout

        with open('D:/Tools/VS code/Python/__pycache__/Grid.txt', 'w', encoding='utf-8') as f:
            f.write(f'{layout}\n')
        print('Saved..')
    
    def load(self, layout=None):
        line = self.line
        cv = self.cv
        if not layout:
            with open('D:/Tools/VS code/Python/__pycache__/Grid.txt', 'r', encoding='utf-8') as f:
                if not (layout := f.read()): return
                layout = eval(layout)

        for y in range(line):
            for x in range(line):
                cv.itemconfig(f'{x}_{y}', fill=layout[y*line+x])
    
    def show(self):
        mainloop()
