from robot import*

class Screen:
    def __init__(self, hub: hub, menuRow = 4):
        self.menuRow = menuRow
        self.hub = hub
        self.width = 5
        self.height = 5
        self.currPage = 0
        self.pages = []
        self.hub.color(Color.CYAN)
        self.hub.setOffButton(Button.LEFT_MINUS)
        

    def __str__(self):
        return f"Screen(width={self.width}, height={self.height})"

    def __repr__(self):
        return self.__str__()
    
    def addPage(self, page):
        page.hub = self.hub
        self.pages.append(page)
    
    
    def start(self):
        self.renderPage()
    
    def update(self):
        
        if self.hub.isButtonPressed(Button.LEFT):
            self.currPage = (self.currPage - 1) % len(self.pages)
            self.renderPage()
            self.release(Button.LEFT)
        if self.hub.isButtonPressed(Button.RIGHT):
            self.currPage = (self.currPage + 1) % len(self.pages)
            self.renderPage()
            self.release(Button.RIGHT)
            
        if self.hub.isButtonPressed(Button.BLUETOOTH):
            self.battery()
            
            self.renderPage()
        
        if self.hub.isButtonPressed(Button.CENTER):
            self.hub.color(Color.RED)
            self.hub.clear()
            self.loading()
            while self.hub.isButtonPressed(Button.CENTER):
                pass
            self.pages[self.currPage].renderImage()
            self.hub.color(Color.MAGENTA)
            self.hub.setOffButton(Button.BLUETOOTH)
            self.pages[self.currPage].func()
            raise SystemExit("Exiting screen")
    
    def battery(self):
        max = 8400
        min = 6000
        voltage = self.hub.m_hub.battery.voltage()
        per = int(100 * (voltage - min) / (max - min))
        print(per)
        a = maxV( minV(per - 80, 0) * 5, 100) 
        b = maxV( minV(per - 60, 0) * 5, 100) 
        c = maxV( minV(per - 40, 0) * 5, 100) 
        d = maxV( minV(per - 20, 0) * 5, 100) 
        e = maxV( minV(per     , 0) * 5, 100)
        
        time = 0
        dur = 3000
        delta = 10
        t = [0,0,0,0,0]
        k = 0
        while self.hub.isButtonPressed(Button.BLUETOOTH):
            t[k] = (time) // (dur//500) - k * 100
            if t[k] >= 100:
                k += 1
            i = 15
            bat = Matrix([
                [t[4], 0, 0, a, i],
                [t[3], 0, 0, b, 0],
                [t[2], 0, 0, c, 0],
                [t[1], 0, 0, d, 0],
                [t[0], 0, 0, e, i]
            ])
            self.hub.image(bat)
            time += delta
            if time > dur:
                raise SystemExit("Exiting screen")
            wait(delta)
            
    def release(self, button: Button):
        a = 0
        while self.hub.isButtonPressed(button) and a < 200:
            wait(10)
            a += 10
    def renderPage(self):
        self.render()
        self.pages[self.currPage].renderIcon()
    
    def loading(self):
        self.hub.animate(loading, 80)
    def render(self):
        for i in range(self.width):
            if len(self.pages) == 0:
                return
            bright = 0
            if i == self.currPage:
                bright = 100
            elif i < len(self.pages):
                bright = 30
            self.hub.pixel(i,self.menuRow, bright)
class Page:
    def __init__(self,func, hub = None, icon = None, image = None, delta = 0):
        self.func = func
        self.icon = icon
        self.image = image
        self.hub = hub
        self.delta = delta
    
    def renderIcon(self):
        if self.icon is None:
            for i in range(5):
                for o in range(4):
                    self.hub.pixel(i, o, 0)
            return
        for i in range(maxV(self.icon.shape[0],4)):
            for o in range(self.icon.shape[1]):
                self.hub.pixel(o, i, self.icon[i, o])
    def renderImage(self):
        if self.image is None:
            return
        if  self.delta == 0:
            self.hub.image(self.image)
        else:
            self.hub.animate(self.image,self.delta)
            

l1 = Matrix([
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [30, 60, 100, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
])
l2 = Matrix([
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 30, 60, 100, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
])

l3 = Matrix([
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 30, 60, 100],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
])

l31 = Matrix([
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 30, 100],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
])

l4 = Matrix([
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 100, 60],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
])

l5 = Matrix([
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0,0, 100, 60, 30],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
])

l6 = Matrix([
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 100, 60, 30, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
])
l7 = Matrix([
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [100, 60, 30,0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
])

l71 = Matrix([
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [100, 30, 0,0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
])

l8 = Matrix([
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [60, 100, 0,0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
])

loading = [l1, l2, l3, l31, l4, l5, l6, l7, l71, l8]