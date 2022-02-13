from random import randint, random
from tkinter import *
import win32api,win32con,time

#start,playing,stop,restart
winx=win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
winy=win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
START,PLAYING,STOP,RESTART='start','playing','stop','restart'
RIGHT,LEFT,UP,DOWN='right','left','up','down'
# SMALL,MID,BIG='Small','Mid','Big'
gamex,gamey=800,600
map_size={1:[50,'Small'],2:[40,'Mid'],3:[20,'Big']}
default_size=1
gamestate=START
direction=RIGHT
rec_size=map_size[default_size][0]
tick_time=16
score=0
restart=False
infor=''
ffff=True

class Root:
    def __init__(self,winx,winy,gamex,gamey,title=None) -> None:
        self.winx,self.winy,self.gamex,self.gamey,self.title=winx,winy,gamex,gamey,title
        self.root = Tk()
        if not title:
            self.root.title('Test')
        else:
            self.root.title(title)
        self.root.resizable(height=False,width=False)
        self.root.geometry(str(gamex)+'x'+str(gamey)+'+'+str(int((winx-gamex)//2))+'+'+str(int((winy-gamey)//2)))
        self.root.bind_all('<KeyPress-a>',self.left)
        self.root.bind_all('<KeyPress-d>',self.right)
        self.root.bind_all('<KeyPress-w>',self.up)
        self.root.bind_all('<KeyPress-s>',self.down)
        self.root.protocol('WM_DELETE_WINDOW',self.onclosing)
        self.canvas_game=Canvas(self.root,height=gamey,width=gamex-200,background='green')
        self.canvas_state=Canvas(self.root,height=gamey,width=200,background='blue')
        self.canvas_state.bind_all('<Button-1>',self.click_statefield)
        self.canvas_game.place(x=0,y=0)
        self.canvas_state.place(x=600,y=0)
    def click_statefield(self,event):
        global gamestate,ffff,default_size,rec_size
        x,y=event.x,event.y
        if gamestate==START:
            if x>=40 and x<=160 and y>=100 and y<=140:
                None
            elif x>=40 and x<=80 and y>=200 and y<=240:
                default_size-=1
                if default_size==0:
                    default_size=3
                rec_size=map_size[default_size][0]
            elif x>=self.gamex-680 and x<=self.gamex-640 and y>=200 and y<=240:
                default_size+=1
                if default_size==4:
                    default_size=1
                rec_size=map_size[default_size][0]
            elif x>=40 and x<=160 and y>=300 and y<=340:
                gamestate=PLAYING
            elif x>=40 and x<=160 and y>=400 and y<=440:
                ffff=False
        elif gamestate==PLAYING:
            if x>=40 and x<=160 and y>=100 and y<=140:
                None
            elif x>=40 and x<=160 and y>=200 and y<=240:
                gamestate=STOP
            elif x>=40 and x<=160 and y>=300 and y<=340:
                ffff=False
        elif gamestate==STOP:
            if x>=40 and x<=160 and y>=100 and y<=140:
                None
            elif x>=40 and x<=160 and y>=200 and y<=240:
                gamestate=PLAYING
            elif x>=40 and x<=160 and y>=300 and y<=340:
                ffff=False
        elif gamestate==RESTART:
            if x>=40 and x<=160 and y>=100 and y<=140:
                None
            elif x>=40 and x<=160 and y>=200 and y<=240:
                global restart
                restart=True
            elif x>=40 and x<=160 and y>=300 and y<=340:
                ffff=False
    def update_all(self):
        self.root.update()
    def draw_game(self,snack,apple):
        global tick_time,score,gamestate
        # self.clear_gamefiled()
        # self.draw_game_line()
        if gamestate==PLAYING:
            tick_time+=1
            if tick_time>=16:
                #opert
                if direction==RIGHT:
                    next_head=(snack.head[0]+1,snack.head[1])
                elif direction==LEFT:
                    next_head=(snack.head[0]-1,snack.head[1])
                elif direction==UP:
                    next_head=(snack.head[0],snack.head[1]-1)
                elif direction==DOWN:
                    next_head=(snack.head[0],snack.head[1]+1)
                if snack.eatself(next_head) or snack.hitwall(next_head):
                    gamestate=RESTART
                else:
                    if snack.eat_apple(apple,next_head):
                        snack.head=next_head
                        snack.body.insert(0,next_head)
                        apple.setxy(snack)
                        score+=1
                    else:
                        snack.head=next_head
                        snack.body.insert(0,next_head)
                        snack.body.pop()
                self.clear_gamefiled()
                self.draw_game_snack(snack)
                self.draw_game_apple(apple)
                # print(str(apple.x)+':'+str(apple.y))
                tick_time=0
    def draw_state(self):
        self.clear_statefield()
        if gamestate==START:
            self.draw_state_start()
        elif gamestate==PLAYING:
            self.draw_state_playing()
        elif gamestate==STOP:
            self.draw_state_stop()
        elif gamestate==RESTART:
            self.draw_state_restart()
    def clear_gamefiled(self):
        self.canvas_game.delete('all')
    def clear_statefield(self):
        self.canvas_state.delete('all')
    def draw_game_line(self):
        for i in range(0,(self.gamex-200)//rec_size):
            self.canvas_game.create_line(i*rec_size,0,i*rec_size,self.gamey)
        for i in range(0,gamey//rec_size):
            self.canvas_game.create_line(0,i*rec_size,self.gamex,i*rec_size)
    def draw_state_start(self):
        self.canvas_state.create_rectangle(40,100,self.gamex-640,140,fill='white')
        self.canvas_state.create_rectangle(40,200,80,240,fill='white')
        self.canvas_state.create_rectangle(self.gamex-680,200,self.gamex-640,240,fill='white')
        self.canvas_state.create_rectangle(40,300,self.gamex-640,340,fill='white')
        self.canvas_state.create_rectangle(40,400,self.gamex-640,440,fill='white')
        self.canvas_state.create_text(100,120,text='map:'+map_size[default_size][1])
        self.canvas_state.create_text(100,220,text='←                 →')
        self.canvas_state.create_text(100,320,text='Start')
        self.canvas_state.create_text(100,420,text='Exit')
    def draw_state_playing(self):
        self.canvas_state.create_rectangle(40,100,self.gamex-640,140,fill='white')
        self.canvas_state.create_rectangle(40,200,self.gamex-640,240,fill='white')
        self.canvas_state.create_rectangle(40,300,self.gamex-640,340,fill='white')
        self.canvas_state.create_text(100,120,text='score='+str(score))
        self.canvas_state.create_text(100,220,text='stop')
        self.canvas_state.create_text(100,320,text='Exit')
    def draw_state_stop(self):
        self.canvas_state.create_rectangle(40,100,self.gamex-640,140,fill='white')
        self.canvas_state.create_rectangle(40,200,self.gamex-640,240,fill='white')
        self.canvas_state.create_rectangle(40,300,self.gamex-640,340,fill='white')
        self.canvas_state.create_text(100,120,text='score='+str(score))
        self.canvas_state.create_text(100,220,text='contine')
        self.canvas_state.create_text(100,320,text='Exit')
    def draw_state_restart(self):
        self.canvas_state.create_rectangle(0,100,self.gamex-600,140,fill='white')
        self.canvas_state.create_rectangle(40,200,self.gamex-640,240,fill='white')
        self.canvas_state.create_rectangle(40,300,self.gamex-640,340,fill='white')
        self.canvas_state.create_text(100,120,text=infor)
        self.canvas_state.create_text(100,220,text='restart')
        self.canvas_state.create_text(100,320,text='Exit')
    def left(self,event):
        global direction
        if direction!=LEFT and direction!=RIGHT:
            direction=LEFT
    def right(self,event):
        global direction
        if direction!=LEFT and direction!=RIGHT:
            direction=RIGHT
    def up(self,event):
        global direction
        if direction!=UP and direction!=DOWN:
            direction=UP
    def down(self,event):
        global direction
        if direction!=UP and direction!=DOWN:
            direction=DOWN
    def draw_game_snack(self,snack):
        t=0
        for i in snack.body:
            if t==0:
               self.canvas_game.create_oval(i[0]*rec_size,i[1]*rec_size,(i[0]+1)*rec_size,(i[1]+1)*rec_size,fill='red')
            else:
                self.canvas_game.create_oval(i[0]*rec_size,i[1]*rec_size,(i[0]+1)*rec_size,(i[1]+1)*rec_size,fill='white')
            t+=1
    def draw_game_apple(self,apple):
        self.canvas_game.create_oval(apple.x*rec_size,apple.y*rec_size,(apple.x+1)*rec_size,(apple.y+1)*rec_size,fill='yellow')
    def onclosing(self):
        global ffff
        ffff=False

class Snack:
    def __init__(self) -> None:
        self.head=(1,1)
        self.body=[self.head,(0,1)]
    def reset_snack(self):
        global direction,score,infor
        direction=RIGHT
        self.head=(1,1)
        self.body=[self.head,(0,1)]
        score=0
        infor=''
    def hitwall(self,next_head):
        global infor
        if next_head[0]<0 or next_head[0]>((gamex-200)//rec_size-1) or next_head[1]<0 or next_head[1]>(gamey//rec_size-1):
            infor='you have hitten the wall!\nand yoru score is '+str(score)
            return True
        return False
    def eatself(self,next_head):
        global infor
        for i in range(0,self.body.__len__()-1):
            if self.body[i][0]==next_head[0] and self.body[i][1]==next_head[1]:
                global infor
                infor='you have eatten yourself!\nand yoru score is '+str(score)
                return True
        return False
    def eat_apple(self,apple,next_head):
        if apple.x==next_head[0] and apple.y==next_head[1]:
            return True
        return False

class Apple:
    def __init__(self) -> None:
        self.x,self.y=0,0
        self.setbeginxy()
    def setxy(self,snack):
        self.x=randint(0,(gamex-200)//rec_size-1)
        self.y=randint(0,gamey//rec_size-1)
        for i in snack.body:
            if i[0]==self.x and i[1]==self.y:
                self.setxy(snack)
                break
    def setbeginxy(self):
        self.x=randint(0,(gamex-200)//rec_size-1)
        self.y=randint(0,gamey//rec_size-1)
        if (self.x==0 and self.y==1) or (self.x==1 and self.y==1):
            self.setbeginxy()

if __name__ == '__main__':
    root = Root(winx,winy,gamex,gamey,'SnackGame2.0')
    snack=Snack()
    apple=Apple()
    while ffff:
        if restart==True:
            snack.reset_snack()
            apple.setxy(snack)
            gamestate=PLAYING
            restart=False
        root.draw_game(snack,apple)
        root.draw_state()
        root.update_all()
        time.sleep(0.02)