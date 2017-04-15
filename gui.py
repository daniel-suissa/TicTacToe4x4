#this code is creditted to http://forum.codecall.net/topic/76094-tkinter-tic-tac-toe-tutorial/
#The board was customized. Note that the structure was changed to interact properly with the other classes

from tkinter import Frame, Canvas, Label, Button, LEFT,RIGHT, ALL, Tk
from random import randint
import state


class main:
    def __init__(self,master,n,state):
        self.state = state
        self.n = n
        self.frame = Frame(master)
        self.frame.pack(fill="both", expand=True)
        self.canvas = Canvas(self.frame, width=100*n, height=100*n)
        self.canvas.pack(fill="both", expand=True)
        self.label=Label(self.frame, text='Tic Tac Toe Game', height=6, bg='black', fg='blue')
        self.label.pack(fill="both", expand=True)
        self.frameb=Frame(self.frame)
        self.frameb.pack(fill="both", expand=True)
        self.Start2=Button(self.frameb, text='Click here to start playing', height=4, command=self.start2,bg='purple', fg='white')
        self.Start2.pack(fill="both", expand=True, side=LEFT)  
        self.move_maid = False
    def _board(self):
        self.canvas.create_rectangle(0,0,100*self.n,100*self.n, outline="black")
        #self.canvas.create_rectangle(100,300,200,0, outline="black") #mid vertical rectangle
        #self.canvas.create_rectangle(0,100,300,200, outline="black")  #mid horizontal rectangle
        for i in range(1,self.n):
            self.canvas.create_rectangle(100*i,self.n*100,100*i+100,0, outline="black") #mid vertical rectangles
            self.canvas.create_rectangle(0,100*i,self.n*100,100*i+100, outline="black")  #mid horizontal rectangle
    def start2(self):
        #Starts the game
        self.canvas.delete(ALL)
        self.label['text']=('Tic Tac Toe Game')
        self._board()
    def play(self):
        self.canvas.bind("<ButtonPress-1>", self.dgplayer)
        #TODO: make so that play makes only one move using dgplayer
        #Fix players.py so that play_on_gui calls Game's play on gui which needs to return a MOVE TUPLE
    def dgplayer(self,event):
        for k in range(0,300,100):
            for j in range(0,300,100):
                if event.x in range(k,k+100) and event.y in range(j,j+100):
                    if self.canvas.find_enclosed(k,j,k+100,j+100)==():
                        X=(2*k+100)/2
                        Y=(2*j+100)/2
                        X1=int(k/100)
                        Y1=int(j/100)
                        if self.state.make_move('O',X1,Y1) == False:
                            break
                        else:
                            self.canvas.create_oval( X+25, Y+25, X-25, Y-25, width=4, outline="black")
                            self.trigger=False                         
                            self.canvas.unbind("<ButtonPress-1>")  
                            self.move_maid = True
    def autoplayer(self,token,row,col):
        X=(2*row+100)/2
        Y=(2*col+100)/2
        X1=int(row/100)
        Y1=int(col/100)
        if self.state.make_move('O',X1,Y1) == False:
            return
        else:
            self.canvas. create_line( X+20, Y+20, X-20, Y-20, width=4, fill="black")
            self.canvas. create_line( X-20, Y+20, X+20, Y-20, width=4, fill="black")
    def end(self):
        self.canvas.unbind("<ButtonPress-1>")
        self.j=True
