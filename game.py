import players
import state
from tkinter import Frame, Canvas, Label, Button, LEFT,RIGHT, ALL, Tk

class Game:
	def __init__(self,master,n):
		self.state = state.State(n)

		'''
		----GUI PART
		'''
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
		self.i = 0 #number of moves
		self.successful_move = False #this member is going to tell us whether human made a valid move so AI can go

		params = self.init_from_console()
		if params[1] == 'H':
			self.player1 = players.HumanPlayer(params[0],params[2])
		else:
			self.player1 = players.AIPlayer(parms[2],params[5])
		if params[2] == 'X':
			player2token = 'O'
		else:
			player2token = 'X'
		if params[4] == 'H':
			self.player2 = players.HumanPlayer(params[3],player2token)
		else:
			self.player2 = players.AIPlayer(player2token,params[5])
		self.curr_player = self.player1


	#----GUI METHODS------#
	def _board(self):
		self.canvas.create_rectangle(0,0,100*self.n,100*self.n, outline="black")
		#self.canvas.create_rectangle(100,300,200,0, outline="black") #mid vertical rectangle
		#self.canvas.create_rectangle(0,100,300,200, outline="black")  #mid horizontal rectangle
		for i in range(1,self.n):
			self.canvas.create_rectangle(100*i,self.n*100,100*i+100,0, outline="black") #mid vertical rectangles
			self.canvas.create_rectangle(0,100*i,self.n*100,100*i+100, outline="black")  #mid horizontal rectangle
	def start2(self):
		#Starts the game
		self.Start2.config(text = 'Tic Tac Toe Game!')
		self.state = state.State(self.n)
		print(self.state)
		self.canvas.delete(ALL)
		self.label['text']=('Tic Tac Toe Game')
		self._board()
		self.canvas.bind("<ButtonPress-1>", self.dgplayer)
	def human_move(self,k,j):
		'''
		input: 
			(int) k - 
		'''

	def dgplayer(self,event):
		for k in range(0,self.n*100,100):
			for j in range(0,self.n*100,100):
				if event.x in range(k,k+100) and event.y in range(j,j+100):
					if self.canvas.find_enclosed(k,j,k+100,j+100)==():
						if self.i % 2 == 0: #human player
							X=(2*k+100)/2
							Y=(2*j+100)/2
							X1=int(k/100)
							Y1=int(j/100)
							if self.state.make_move('O',Y1,X1) == False:
								break
							else:
								self.canvas.create_oval( X+25, Y+25, X-25, Y-25, width=4, outline="black")                        
								self.i += 1
								self.next_player()
								self.successful_move = True
						else:
							#second player can be either human or AI
							if type(self.curr_player) == players.HumanPlayer:
								X=(2*k+100)/2
								Y=(2*j+100)/2
								X1=int(k/100)
								Y1=int(j/100)
								if self.state.make_move('X',Y1,X1) == False:
									break
								else:
									self.canvas.create_oval( X+25, Y+25, X-25, Y-25, width=4, outline="black")                       
									self.i += 1
									self.next_player()
									self.successful_move = True
		print(self.state)
		self.frame.update_idletasks()
		self.frame.update()
		if self.successful_move:
			self.AImove()
		self.successful_move = False				
		print(self.state)
		if self.state.check_terminal()[0] == 'terminal':
			self.end()
	def AImove(self):
		'''
		ASSUMPTION: current player is AI player
		ASSUMPTION: AI cannot make an illegal move (no need to re-prompt for move)
		'''
		print('AI thinking...')
		token,row,col = self.curr_player.move(self.state)
		print('AI wants to play at row: ', row, ' and column: ', col)
		Y= 100*row+50
		X= 100*col+50
		self.canvas. create_line( X+20, Y+20, X-20, Y-20, width=4, fill="black")
		self.canvas. create_line( X-20, Y+20, X+20, Y-20, width=4, fill="black")
		self.i += 1
		self.next_player()
		self.state.make_move(token,row,col)
		return (token,row,col)
	def end(self):
		self.canvas.unbind("<ButtonPress-1>")
		self.Start2.config(text = 'Play Again!')



    #-----GAME MANAGEMENT METHODS
		
		
	def next_player(self):
		if self.curr_player == self.player1:
			self.curr_player = self.player2
		else:
			self.curr_player = self.player1
	def init_from_console(self):
		'''
		output: tuple (player1_name,player1_type,player1_token,player2_name,player2_type,difficulty)
		'''
		#TODO: write this
		return ('Player1','H','O','Player2','AI','hard')

	#clean the method at cleanup
	def go(self):
		while self.state.check_terminal()[0] != 'terminal':
			print(self.state)
			self.curr_player.move(self.state)
			#it pains me to add this block, but in the essence of time I need a quick solution to control player switch
			#TODO: change players in callback
			while self.app.move_maid == False:
				continue
			self.app.move_maid = True
			self.next_player()
		print(self.state)
		
root=Tk()
root.title("n x n Tic Tac Toe")
game = Game(root,4)
root.mainloop()