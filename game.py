import players
import state
import gui

class Game:
	def __init__(self):

		self.gui = 
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
		self.state = state.State()
		self.curr_player = self.player1

		root=Tk()
		root.title("n x n Tic Tac Toe")
		self.app=main(root,4,self)
		
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
	def go(self):
		
		while self.state.check_terminal()[0] != 'terminal':
			print(self.state)
			self.curr_player.move(self.state)
			self.next_player()
		print(self.state)
		root.mainloop()
game = Game()
game.go()