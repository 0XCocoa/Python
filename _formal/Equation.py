class Equation:
    def __init__(self, items=None):
        self.items = self.create(items)
    
    def create(self, items):
        if items: return items

        print('请按项依次输入一元多次方程的系数和指数')
        item = input().split()
        try: 
            items = [list(map(eval,[item[i-1],item[i]])) for i in range(len(item)) if i%2]
        except:
            items = []
            temp = ''
            for elem in item:
                if elem in ['y', '=', '+']:
                    continue
                elif elem == '-':
                    temp = elem
                else:
                    if temp:
                        elem = temp + elem
                        temp = ''
                    items.append(elem)

            for i,elem in enumerate(items):
                item = elem.replace('^','').split('x')
                items[i] = [float(item[0]), (float(item[1]) if item[1] else 1) if len(item) != 1 else 0]
            
        return items

    def print(self):
        print('方程为：', end='\n  ')
        for i,item in enumerate(self.items):
            if item[1] == 1:
                elem2 = 'x'
            elif not item[1]:
                elem2 = ''
            else:
                elem2 = f'x^{item[1]}'
            elem1 = '' if not item[0]-1 and elem2 else f'{item[0]}'
            if i != len(self.items)-1:
                print(elem1 + elem2 + ' + ',end='')
            else:
                print(elem1 + elem2)
    
    def change(self, index, data):
        for i,item in enumerate(self.items):
            if item[1] == index:
                self.items[i][0] += data
                if not self.items[i][0]:
                    self.items.pop(i)
                break

    def calculate(self, x) -> float:
        res = 0
        for item in self.items:
            res += item[0] * (x ** item[1])
        print(f'当 x = {x} 时， y = {res}')
        return res

    def r_calculate(self, y, x0) -> float:
        self.change(0, -y)
        ee = self.derive()
        step = 0

        zero = self.calculate(x0)
        while step < 20 and abs(zero) > 1e-10:
            x0 = x0 - (zero / ee.calculate(x0))
            zero = self.calculate(x0)
            step += 1

        print(f'当 y = {y} 时， x = {x0}')
        return x0

    def derive(self):
        items = [[item[0]*item[1], item[1]-1] for item in self.items]
        if not items[-1][0]:
            items.pop(-1)
        return Equation(items)

    def extremum(self, x0):
        ee = self.derive()
        eee = ee.derive()
        step = 0

        one = ee.calculate(x0)
        while step < 20 and abs(one) > 1e-10:
            x0 = x0 - (one / eee.calculate(x0))
            one = ee.calculate(x0)
            step += 1

        if step == 20:
            print(f'函数在 x = {x0} 附近无极值')
        else:
            y0 = self.calculate(x0)
            print(f'函数在 x = {x0} 处有极值 y = {y0}')
            return y0

    def line(self, x=None, y=None, x0=None):
        if not y:
            if not x0: x0 = 1
            y = self.calculate(x,x0)
        else:
            x = self.r_calculate(y)
        
        k = self.derive().calculate(x)
        b = y - k*x

        b = '+ ' + str(b) if b > 0 else '- ' + str(-b)
        print(f'所求直线为 y = {k}x {b}')
