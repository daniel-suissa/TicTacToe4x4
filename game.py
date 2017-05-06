import players
import state
#from tkinter import Frame, Canvas, Label, Button, LEFT,RIGHT, ALL, Tk
from tkinter import *
import time

import csv



class Game:
	def __init__(self,master,n,difficulty,params,player2starts):
		self.state = state.State(n,difficulty)
		'''
		----GUI PART
		'''
		self.difficulty =difficulty 
		self.n = n
		self.frame = Frame(master)
		self.frame.pack(fill="both", expand=True)
		self.canvas = Canvas(self.frame, width=100*n, height=100*n)
		self.canvas.pack(fill="both", expand=True)
		self.label=Label(self.frame, text='Tic Tac Toe Game', height=6, bg='black', fg='blue')
		self.label.pack(fill="both", expand=True)
		self.frameb=Frame(self.frame)
		self.frameb.pack(fill="both", expand=True)
		self.Start=Button(self.frameb, text='Click here to start playing', height=4, command=self.start,bg='purple', fg='white')
		self.Start.pack(fill="both", expand=True, side=LEFT) 
		self.AI_TIMES = [] #for performance logging

		if params[1] == 'H':
			self.player1 = players.HumanPlayer(params[0],params[2])
		else:
			self.player1 = players.AIPlayer(parms[2],self.difficulty)
		if params[2] == 'X':
			player2token = 'O'
		else:
			player2token = 'X'
		if params[4] == 'H':
			self.player2 = players.HumanPlayer(params[3],player2token)
		else:
			self.player2 = players.AIPlayer(player2token,self.difficulty)

		self.whostarts = player2starts #if False, player 1 starts. If true - player 2 starts. #need this data for replaying
		if self.whostarts:
			self.curr_player = self.player2
		else:
			self.curr_player = self.player1

	#----GUI METHODS------#
	def _board(self):
		self.canvas.create_rectangle(0,0,100*self.n,100*self.n, outline="black")
		#self.canvas.create_rectangle(100,300,200,0, outline="black") #mid vertical rectangle
		#self.canvas.create_rectangle(0,100,300,200, outline="black")  #mid horizontal rectangle
		for i in range(1,self.n):
			self.canvas.create_rectangle(100*i,self.n*100,100*i+100,0, outline="black") #mid vertical rectangles
			self.canvas.create_rectangle(0,100*i,self.n*100,100*i+100, outline="black")  #mid horizontal rectangle
	
	def start(self):

		#----this part is an extension of __init__ to enable replaying
		if self.whostarts:
			self.curr_player = self.player2
		else:
			self.curr_player = self.player1 #this member is going to tell us whether human made a valid move so AI can go
		if type(self.player2) == players.AIPlayer:
			self.player2.restart()
		#---------
		#Starts the game
		self.Start.config(text = 'Tic Tac Toe Game!')
		self.state = state.State(self.n,self.difficulty)
		print(self.state)
		self.canvas.delete(ALL)
		self.label['text']=('Tic Tac Toe Game')
		self._board()
		self.canvas.bind("<ButtonPress-1>", self.dgplayer)



	def dgplayer(self,event):
		if type(self.curr_player) == players.HumanPlayer:
			for k in range(0,self.n*100,100):
				for j in range(0,self.n*100,100):
					if event.x in range(k,k+100) and event.y in range(j,j+100):
						if self.canvas.find_enclosed(k,j,k+100,j+100)==(): #player1
							X=(2*k+100)/2
							Y=(2*j+100)/2
							X1=int(k/100)
							Y1=int(j/100)
							if self.state.make_move('O',Y1,X1) == False:
								break
							else:
								self.canvas.create_oval( X+25, Y+25, X-25, Y-25, width=4, outline="black")                        
								self.next_player()

		print(self.state)
		self.frame.update_idletasks()
		self.frame.update()
		if type(self.curr_player) == players.AIPlayer and self.state.check_terminal()[0] != 'terminal':
			self.AImove()				
		print(self.state)
		if self.state.check_terminal()[0] == 'terminal':
			self.end()
	def AImove(self):
		'''
		ASSUMPTION: current player is AI player
		ASSUMPTION: AI cannot make an illegal move (no need to re-prompt for move)
		'''
		start = time.clock()
		print('AI thinking...')
		token,row,col = self.curr_player.move(self.state)
		print('AI wants to play at row: ', row, ' and column: ', col)
		Y= 100*row+50
		X= 100*col+50
		self.canvas. create_line( X+20, Y+20, X-20, Y-20, width=4, fill="black")
		self.canvas. create_line( X-20, Y+20, X+20, Y-20, width=4, fill="black")
		self.next_player()
		self.state.make_move(token,row,col)
		self.AI_TIMES.append(time.clock() - start)

		return (token,row,col)
	def end(self):
		self.canvas.unbind("<ButtonPress-1>")
		self.Start.config(text = 'Play Again!')
		AI_avg = sum(self.AI_TIMES)/len(self.AI_TIMES)
		print("AVG AI thinking time: ", AI_avg)
		self.AI_TIMES = []
		#when game ends recordthe result
		#logging only relevant for  4x4 mode
		row=[self.n, self.whostarts,self.difficulty,str(AI_avg)]
		with open(r'AImoves.csv', 'a') as f:
		    writer = csv.writer(f)
		    writer.writerow(row)


    #-----GAME MANAGEMENT METHODS
		
		
	def next_player(self):
		if self.curr_player == self.player1:
			self.curr_player = self.player2
		else:
			self.curr_player = self.player1


def start_game(root, n ,player2starts, player1_name, player1_type,token,player2_name,player2_type, difficulty):
	root.destroy() #close the menu window
	root=Tk() #open a new window
	root.title("n x n Tic Tac Toe")
	params = [player1_name, player1_type,token,player2_name,player2_type] 
	game = Game(root,n,difficulty,params,player2starts)#TODO: have player2starts initialize successful_move in Game
	root.mainloop()
	


def menu():
	#small pre-game menu to choose who starts, players name, difficulty, etc..
	#output: difficulty, n, params
	
	root=Tk()
	root.title("n x n Tic Tac Toe")
	nlabel=Label(root, text='n:')
	nlabel.grid(row = 1,column = 1)
	#nlabel.pack()

	# Variable for the Optionmenu
	n = StringVar()
	# The menu
	noptions = OptionMenu(root, n, "3","4","5","6")
	noptions.grid(row=1, column=2)
	# Set the variable to "a" as default
	n.set("4")

	difficulty_label = Label(root, text = 'Difficulty: ')
	difficulty_label.grid(row = 2, column = 1)
	difficulty = StringVar()
	difficulty_options = OptionMenu(root, difficulty,"easy","medium","hard","Jarvis")
	difficulty_options.grid(row = 2, column = 2)
	difficulty_options.config(width = 8)
	difficulty.set("hard")
	#player 1 is always a human
	player1_name = StringVar()
	player1_name_input = Entry(root)
	player1_label = Label(root, text = "Player1 Name: ")
	player1_label.grid(row = 3,column = 1)
	player1_name_input.grid(row = 3, column = 2)


	player2_name = StringVar()
	player2_name_input = Entry(root)
	player2_label = Label(root, text = "Player2 Name: ")
	player2_label.grid(row = 4,column = 1)
	player2_name_input.grid(row = 4, column = 2)

	player2_type_label = Label(root, text = 'Player2 Type: ')
	player2_type_label.grid(row = 5, column = 1)
	player2_type = StringVar()
	player2_type_options = OptionMenu(root, player2_type, "Human", "AI")
	player2_type_options.grid(row = 5, column = 2)
	player2_type_options.config(width = 8)
	player2_type.set("AI")


	whostarts_label = Label(root, text = 'Who Starts: ')
	whostarts_label.grid(row = 6, column = 1)
	whostarts = StringVar()
	#whostarts.set("Player1") #TODO: set a default
	whostarts_options = OptionMenu(root, whostarts, "Player1", "Player2")
	whostarts_options.grid(row = 6, column = 2)
	whostarts_options.config(width = 8)
	

	if player2_type.get() == 'Human':
		player2_type = 'H'

	def launch(): 
		if whostarts.get() == "Player1":
			player2starts = False
		else:
			player2starts = True
		print(int(n.get()), player2starts, player1_name.get(), 'H','O',player2_name.get(),player2_type.get(), difficulty.get())
		return start_game(root,int(n.get()), player2starts, player1_name.get(), 'H','O',player2_name.get(),player2_type.get(), difficulty.get())
    
	start_button = Button(root, text='Click here to start playing',command = launch)
	start_button.grid(row = 7)
	root.mainloop()

menu()

