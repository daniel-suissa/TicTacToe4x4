
class AIPlayer:
	diff = {'easy': 1, 'medium' : 2, 'hard' : 3}
	increments = {'easy': 0, 'medium' : 0, 'hard' : 2}
	#easy   1 2 3
	#medium 2 3 4 5 6 7
	#hard   3 5 7 9
	def __init__(self, token,difficulty):
		'''
		difficulty determines cutoff
		'''
		self.increment = AIPlayer.increments[difficulty]
		self.cutoff = AIPlayer.diff[difficulty]
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
		#note that depth will contain the current depth and depth_reached is the max depth reached in the current subtree
		v,move,did_cutoff,depth_reached,nodes_count,pruning_max,pruning_min = self.max(state,state.min_util,state.max_util,0,did_cutoff,depth_reached,nodes_count,pruning_max,pruning_min)
		#state.make_move(*move) #to make move directly through console
		print('cutoff_level: ', self.cutoff, 'did_cutoff?: ', did_cutoff, ' depth_reached: ', depth_reached, '#nodes: ', nodes_count, ' max pruning: ', pruning_max, ' min_pruning: ', pruning_min)
		self.num_moves += 2
		self.cutoff += self.increment
		return move
	def max(self,state,alpha,beta,depth,did_cutoff,depth_reached,nodes_count,pruning_max,pruning_min):
		'''
			max
		'''
		c_t = state.check_terminal()
		if c_t[0] == 'terminal' or depth >= self.cutoff:
			if depth >= self.cutoff:
				did_cutoff = True
			return (c_t[1],state.last_action,did_cutoff,depth_reached,nodes_count,pruning_max,pruning_min) #the utility value / eval value
		v = state.min_util
		best_action = None
		non_incremented_depth_reached = depth_reached
		for successor in state.possible_successors(self.token):
			nodes_count += 1
			new_v,move,did_cutoff,new_depth_reached,nodes_count,pruning_max,pruning_min = self.min(successor,alpha,beta,depth+1,did_cutoff,non_incremented_depth_reached+1,nodes_count,pruning_max,pruning_min)
			depth_reached = max(new_depth_reached,depth_reached)
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
		c_t = state.check_terminal()
		if c_t[0] == 'terminal' or depth >= self.cutoff:
			#print('reached end. eval is: ', c_t[1])
			if depth >= self.cutoff:
				did_cutoff = True
			return (c_t[1],state.last_action,did_cutoff,depth_reached,nodes_count,pruning_max,pruning_min) #the utility value / eval value
		v = state.max_util
		best_action = None
		non_incremented_depth_reached = depth_reached
		for successor in state.possible_successors(self.opponent):
			nodes_count += 1
			new_v,move,did_cutoff,new_depth_reached,nodes_count,pruning_max,pruning_min = self.max(successor,alpha,beta,depth+1,did_cutoff,non_incremented_depth_reached+1,nodes_count,pruning_max,pruning_min)
			depth_reached = max(new_depth_reached,depth_reached)
			new_v = min(v,new_v)
			best_action = successor.last_action
			v = new_v
			if v <= alpha:
				pruning_min += 1
				return (v,best_action,did_cutoff,depth_reached,nodes_count,pruning_max,pruning_min)
			beta = max(beta,v)
		return (v,best_action,did_cutoff,depth_reached,nodes_count,pruning_max,pruning_min)

#clean this up an cleanup
class HumanPlayer:
	def __init__(self,name,token):
		self.name = name
		self.token = token
	def move_on_console(self, state):
		'''
		console version
		'''
		token,row,col = input("It\'s " + self.name + '\'s move: ').split(',')

		while(not state.make_move(token,int(row),int(col))):
			input("Oops, invalid move. Go again: ")
		return (token,int(row),int(col))

