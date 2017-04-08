
class AIPlayer:
	def __init__(self, token,difficulty = 'medium'):
		'''
		difficulty determines cutoff
		'''
		diff = {'easy': 3, 'medium' : 4, 'hard' : 5}
		self.cutoff = diff[difficulty]
		self.token = token
		self.name = 'AI PLayer'
		self.num_moves = 0
	def adjust_cutoff(self):
		if self.num_moves > 1:
			self.cutoff += 1
		if self.num_moves > 3:
			self.cutoff += 2
		if self.num_moves > 5:
			self.cutoff += 2
	def move(self,state):
		'''
		'''
		v,move = self.max(state,state.min_util,state.max_util,0)
		state.make_move(*move)
		self.num_moves += 1
	def max(self,state,alpha,beta,depth):
		'''
			max
		'''
		c_t = state.check_terminal()
		if c_t[0] == 'terminal' or depth >= self.cutoff:
			return (c_t[1],state.last_action) #the utility value / eval value
		v = state.min_util
		best_action = None
		for successor in state.possible_successors(self.token):
			new_v = max(v,self.min(successor,alpha,beta,depth+1)[0])
			if new_v != v or best_action == None:
				best_action = successor.last_action
				v = new_v
			if v >= beta:
				return (v,best_action)
			alpha = max(alpha,v)
		return (v,best_action)
	def min(self,state,alpha,beta,depth):
		'''
			min
		'''
		c_t = state.check_terminal()
		if c_t[0] == 'terminal' or depth >= self.cutoff:
			return (c_t[1],state.last_action) #the utility value / eval value
		v = state.max_util
		best_action = None
		for successor in state.possible_successors(self.token):
			new_v = min(v,self.max(successor,alpha,beta,depth+1)[0])
			if new_v != v or best_action == None:
				best_action = successor.last_action
				v = new_v
			if v <= alpha:
				return (v,best_action)
			beta = max(beta,v)
		return (v,best_action)
class HumanPlayer:
	def __init__(self,name="Player1",token='X'):
		self.name = name
		self.token = token
	def move(self, state):
		'''
		console version
		'''
		token,row,col = input("It\'s " + self.name + '\'s move: ').split(',')

		while(not state.make_move(token,int(row),int(col))):
			input("Oops, invalid move. Go again: ")
		return (token,int(row),int(col))
