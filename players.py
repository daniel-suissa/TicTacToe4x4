
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
		if self.token == 'X':
			self.opponent = 'O'
		else:
			self.opponent = 'X'
	def move(self,state):
		'''
		'''
		did_cutoff = False
		depth_reached = 0
		nodes_count = 0
		pruning_max = 0
		pruning_min = 0
		v,move,did_cutoff,depth_reached,nodes_count,pruning_max,pruning_min = self.max(state,state.min_util,state.max_util,0,did_cutoff,depth_reached,nodes_count,pruning_max,pruning_min)
		state.make_move(*move)
		print('cutoff: ', did_cutoff, ' depth_reached: ', depth_reached, '#nodes: ', nodes_count, ' max pruning: ', pruning_max, ' min_pruning: ', pruning_min)
		self.num_moves += 2
		self.cutoff+= 1
	def max(self,state,alpha,beta,depth,did_cutoff,depth_reached,nodes_count,pruning_max,pruning_min):
		'''
			max
		'''
		depth_reached += 1
		c_t = state.check_terminal()
		if c_t[0] == 'terminal' or depth >= self.cutoff:
			if depth >= self.cutoff:
				did_cutoff = True
			return (c_t[1],state.last_action,did_cutoff,depth_reached,nodes_count,pruning_max,pruning_min) #the utility value / eval value
		v = state.min_util
		best_action = None
		depth_reached_temp = depth_reached #remember depth reached to not overincrement
		for successor in state.possible_successors(self.token):
			depth_reached = depth_reached_temp
			nodes_count += 1
			new_v,move,did_cutoff,depth_reached,nodes_count,pruning_max,pruning_min = self.min(successor,alpha,beta,depth+1,did_cutoff,depth_reached,nodes_count,pruning_max,pruning_min)
			new_v = max(v,new_v)
			if new_v != v or best_action == None:
				best_action = successor.last_action
				v = new_v
			if v >= beta:
				pruning_max += 1
				return (v,best_action,did_cutoff,depth_reached,nodes_count,pruning_max,pruning_min)
			alpha = max(alpha,v)
		return (v,best_action,did_cutoff,depth_reached,nodes_count,pruning_max,pruning_min)
	def min(self,state,alpha,beta,depth,did_cutoff,depth_reached,nodes_count,pruning_max,pruning_min):
		'''
			min
		'''
		depth_reached += 1
		c_t = state.check_terminal()
		if c_t[0] == 'terminal' or depth >= self.cutoff:
			#print('reached end. eval is: ', c_t[1])
			if depth >= self.cutoff:
				did_cutoff = True
			return (c_t[1],state.last_action,did_cutoff,depth_reached,nodes_count,pruning_max,pruning_min) #the utility value / eval value
		v = state.max_util
		best_action = None
		depth_reached_temp = depth_reached
		for successor in state.possible_successors(self.opponent):
			depth_reached = depth_reached_temp
			nodes_count += 1
			new_v,move,did_cutoff,depth_reached,nodes_count,pruning_max,pruning_min = self.max(successor,alpha,beta,depth+1,did_cutoff,depth_reached,nodes_count,pruning_max,pruning_min)
			new_v = min(v,new_v)
			best_action = successor.last_action
			v = new_v
			if v <= alpha:
				pruning_min += 1
				return (v,best_action,did_cutoff,depth_reached,nodes_count,pruning_max,pruning_min)
			beta = max(beta,v)
		return (v,best_action,did_cutoff,depth_reached,nodes_count,pruning_max,pruning_min)
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
