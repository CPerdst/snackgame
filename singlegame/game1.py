from tkinter import *
from tkinter import messagebox
import win32api,win32con,time,random,sys

window_x=win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
window_y=win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
gamewin_x,gamewin_y=800,600
rec_size=20
flush_time = 0.1
direction='right'
score=0
gamestate=True
infor=''
restart=False

class Root:
    def __init__(self,winx,winy,gamex,gamey,rec_size,flush_time) -> None:
        self.winx=winx
        self.winy=winy
        self.gamex=gamex
        self.gamey=gamey                
        self.rec_size=rec_size
        self.flush_time=flush_time
        self.root = Tk()
        self.root.geometry(str(self.gamex)+'x'+str(self.gamey)+'+'+str(int((self.winx-self.gamex)//2))+'+'+str(int((self.winy-self.gamey)//2)))
        self.root.resizable(height=False,width=False)
        self.canvas=Canvas(self.root,height=self.gamey,width=self.gamex)
        self.canvas.bind_all('<KeyPress-a>',self.left)
        self.canvas.bind_all('<KeyPress-d>',self.right)
        self.canvas.bind_all('<KeyPress-w>',self.up)
        self.canvas.bind_all('<KeyPress-s>',self.down)
        self.canvas.grid()
    def draw_line(self):
        for i in range(0,self.gamex//self.rec_size+1):
            self.canvas.create_line(i*self.rec_size,0,i*self.rec_size,self.gamey)
        for i in range(0,self.gamey//self.rec_size+1):
            self.canvas.create_line(0,i*self.rec_size,self.gamex,i*self.rec_size)
    def update(self):
        self.root.update()
    def left(self,event):
        global direction
        if direction!='right' and direction!='left':
            direction='left'
    def right(self,event):
        global direction
        if direction!='right' and direction!='left':
            direction='right'
    def up(self,event):
        global direction
        if direction!='up' and direction!='down':
            direction='up'
    def down(self,event):
        global direction
        if direction!='up' and direction!='down':
            direction='down'
    def draw(self,snack,apple):
        self.canvas.delete('all')
        # self.draw_line()
        t=1
        for i in snack.body:
            if t==1:
                self.canvas.create_oval(i[0]*rec_size,i[1]*rec_size,i[0]*rec_size+rec_size,i[1]*rec_size+rec_size,fill='red')
            # self.canvas.create_rectangle(i[0]*rec_size,i[1]*rec_size,(i[0]+1)*rec_size,(i[1]+1)*rec_size,fill='green')
            else:
                self.canvas.create_oval(i[0]*rec_size,i[1]*rec_size,i[0]*rec_size+rec_size,i[1]*rec_size+rec_size,fill='green')
            t+=1
        self.canvas.create_rectangle(apple.x*rec_size,apple.y*rec_size,(apple.x+1)*rec_size,(apple.y+1)*rec_size,fill='yellow')
        self.canvas.create_text(200,gamewin_y//2,text=infor,fill='red')
        self.canvas.create_text(20,20,text=str(score),fill='purple')
    def on_closing(self):
        self.root.destroy()
    def set_restart(self):
        self.canvas.create_oval(gamewin_x//2-10,gamewin_y//2-10,gamewin_x//2+10,gamewin_y//2+10)
        self.canvas.create_text(gamewin_x//2,gamewin_y//2-50,text=infor)
        self.canvas.create_text(gamewin_x//2,gamewin_y//2-30,text='press this for contine')
        self.canvas.bind_all('<Button-1>',self.restart)
    def restart(self,event):
        # print(type(event))
        global gamestate,restart
        if event.x>=gamewin_x//2-10 and event.x<=gamewin_x//2+10 and event.y>=gamewin_y//2-10 and event.y<=gamewin_y//2+10:
            self.canvas.delete('all')
            gamestate=True
            restart=True

class Snack:
    def __init__(self) -> None:
        self.head=(2,1)
        self.body=[self.head,(1,1),(0,1)]
    def ifendgame(self,root):
        if self.hitwall(root) or self.eatself(root):
            return True
        return False
    def hitwall(self,root):
        global infor
        if self.head[0]<0 or self.head[0]>(gamewin_x//rec_size-1) or self.head[1]<0 or self.head[1]>(gamewin_y//rec_size-1):
            infor = 'you have hittne the wall!'
            return True
        return False
    def eatself(self,root):
        global infor
        for i in range(0,self.body.__len__()-1):
            if self.body[i][0]==self.head[0] and self.body[i][1]==self.head[1]:
                infor='you have eatten yourself!'
                return True
        return False
    def eatapple(self,apple):
        if self.head[0]==apple.x and self.head[1]==apple.y:
            return True
        return False
    def restart(self):
        self.head=(2,1)
        self.body.clear()
        self.body.append(self.head)
        self.body.append((1,1))
        self.body.append((0,1))
        global direction,score,infor
        direction='right'
        score=0
        infor=''

class Apple:
    def __init__(self) -> None:
        self.x,self.y=0,0
    def setxy(self,snack):
        self.x=random.randint(0,gamewin_x//rec_size-1)
        self.y=random.randint(0,gamewin_y//rec_size-1)
        for i in snack.body:
            if i[0]==self.x and i[1]==self.y:
                self.setxy(snack)
                break

if __name__ == '__main__':
    root = Root(window_x,window_y,gamewin_x,gamewin_y,rec_size,flush_time)
    snack=Snack()
    apple=Apple()
    apple.setxy(snack=snack)
    root.draw(snack=snack,apple=apple)
    root.root.protocol('WM_DELETE_WINDOW',root.on_closing)
    flag=0
    while True:
        if restart:
            snack.restart()
            apple.setxy(snack)
            restart=False
        if flag>=16 and gamestate==True:
            if direction=='right':
                snack.head=(snack.head[0]+1,snack.head[1])
                if snack.ifendgame(root):
                    gamestate=False
                if snack.eatapple(apple):
                    snack.body.insert(0,snack.head)
                    apple.setxy(snack)
                    score+=1
                else:
                    snack.body.pop()
                    snack.body.insert(0,snack.head)
            elif direction=='down':
                snack.head=(snack.head[0],snack.head[1]+1)
                if snack.ifendgame(root):
                    gamestate=False
                if snack.eatapple(apple):
                    snack.body.insert(0,snack.head)
                    apple.setxy(snack)
                    score+=1
                else:
                    snack.body.pop()
                    snack.body.insert(0,snack.head)
            elif direction=='left':
                snack.head=(snack.head[0]-1,snack.head[1])
                if snack.ifendgame(root):
                    gamestate=False
                if snack.eatapple(apple):
                    snack.body.insert(0,snack.head)
                    apple.setxy(snack)
                    score+=1
                else:
                    snack.body.pop()
                    snack.body.insert(0,snack.head)
            elif direction=='up':
                snack.head=(snack.head[0],snack.head[1]-1)
                if snack.ifendgame(root):
                    gamestate=False
                if snack.eatapple(apple):
                    snack.body.insert(0,snack.head)
                    apple.setxy(snack)
                    score+=1
                else:
                    snack.body.pop()
                    snack.body.insert(0,snack.head)
            root.draw(snack,apple)
            if not gamestate:
                root.canvas.delete('all')
                root.set_restart()
            # print(str(snack.body)+':'+str((apple.x,apple.y)))
            flag=0
        flag+=1
        time.sleep(0.02)
        root.update()