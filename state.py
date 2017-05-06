
import copy
import math
import random

class State:
	def __init__(self,n,difficulty,board=None):
		'''
		members: 
			ASSUMPTION: max player is X
			2d list - board
		'''
		difficulties = {'easy' : self.easy_eval, 'medium': self.medium_eval,'hard':self.eval, 'Jarvis':self.jarvis_eval}
		self.difficulty = difficulty
		self.eval_f = difficulties[self.difficulty]
		'''
		self.eval_t = eval_f #which eval funtion to use 1 or 2
		if eval_f == '1': #the actual eval function
			self.eval_f = self.eval
		elif eval_f == '2':
			self.eval_f = self.eval2
		else:
			raise Exception('invalid eval function')
		'''
		self.max_util = 1000
		self.min_util = -1000
		self.n = n
		self.last_action = ('*',0,0)
		self.v = None

		if board == None:
			self.board = [['*' for j in range(self.n)] for i in range(self.n)]
			
		else:
			self.board = board
		
		'''
		j
			0  1  2  3
		i=0	*  *  *  *
		i=1 *  *  *  *
		i=2 *  *  *  *
		i=3 *  *  *  *


		j
			0  1  2  3
		i=0	*  *  O  *
		i=1 X  *  *  *
		i=2 *  *  *  O
		i=3 *  *  X  *

		'''
	def print_board(self):
		return '_' * (2 * self.n - 1) + '\n' + '\n'.join([ ' '.join(row) for row in self.board]) + '\n' + '-' * (2 * self.n - 1) + '\n'
	def __str__(self):
		board =  '_' * (2 * self.n - 1) + '\n' + '\n'.join([ ' '.join(row) for row in self.board]) + '\n' + '-' * (2 * self.n - 1) + '\n'
		board += '\n'
		c_t = self.check_terminal()
		if c_t[0] == 'terminal':
			board += 'utility value: ' + str(c_t)
		else:
			board += 'state is not termial, eval value: ' + str(c_t[1])
		return board


	def __repr__(self):
		return str(self)

	def make_move(self,token,row,col):
		if token != 'O' and token != 'X':
			raise Exception('TokenInvalidError')
		'''
			check validity of location
			put token in give location
			output: True if ok, False if move wasn't made
		'''
		if self.board[row][col] == '*':
			self.board[row][col] = token
			self.last_action = (token,row,col)
			return True
		else:
			print('invalid move')
			return False

	def possible_successors(self,token):
		board = copy.deepcopy(self.board)
		for i in range(self.n):
			for j in range(self.n):
				if board[i][j] == '*':
					board[i][j] = token
					successor =  State(self.n,self.difficulty,board)
					successor.last_action = (token,i,j)
					yield successor
					board[i][j] = '*'

	def check_terminal(self):
		'''
			returns a tuple with terminal/not termianl and utility value
			X is the max utility token. This shouldn't matter for the AI because it can choose whether to minimize or maximize
		'''
		star_flag = False

		#check whether there is a row of n of the same token
		for row in self.board:
			if row == ['X'] * self.n:
				return ('terminal',1000)
			elif row == ['O'] * self.n:
				return ('terminal',-1000)
			elif '*' in row:
				star_flag = True

		# check whether there is a column of n of the same token
		flipped_board = [[self.board[i][j] for i in range(self.n) ] for j in range(self.n)] #now columns are grouped together
		for col in flipped_board:
			if col == ['X'] * self.n:
				return ('terminal',1000)
			elif col == ['O'] * self.n:
				return ('terminal',-1000)

		#check diagonals - assumes equal rows and columns
		diag1 = [self.board[i][i] for i in range(self.n)]
		if diag1 == ['X'] * self.n:
			return ('terminal',1000)
		elif diag1 == ['O'] * self.n:
			return ('terminal',-1000)
		diag2 = [self.board[i][self.n-1-i] for i in range(self.n)]
		if diag2 == ['X'] * self.n:
			return ('terminal',1000)
		elif diag2 == ['O'] * self.n:
			return ('terminal',-1000)

		if star_flag == False:
			return ('terminal',0)
		else:
			return ('not terminal',self.eval_f()[0])
	class tokenRef:
		def __init__(self,token):
			self.token = token
		def __eq__(self,rhs):
			return self.token == rhs.token
	def easy_eval(self): #gives same weight to every number of Xs and Os
		return self.eval([1 for i in range(self.n-1,0,-1)])
	def medium_eval(self): #gives different but not substantially different weights
		return self.eval([(i-1)*1 for i in range(self.n-1,0,-1)])
	def eval(self,eval_coefs = None): #weights differ by a factor of 3
		eval_sum = 0
		'''
			input: eval_coefs must be size 2*(n-1)
			assumes there is a tie
			works best for 4x4 - non generic
			count amount of X3s X2s and O3s and O1s
			TODO: test generality
		'''
		if eval_coefs == None:
			 eval_coefs = [(i-1)*3 for i in range(self.n-1,0,-1)]
		eval_coefs[-1] = 1
		var_list = [0] * (self.n-1) * 2 # [X3,X2,X1,O3,O2,O1]
		#[x4,x3,x2,x1,o4,o3,o2,o1]
		#[0.  1. 2. 3. 4. 5. 6. 7]
		#board = [[State.tokenRef(token) for token in row] for row in copy.deepcopy(self.board)] # holds references to a copy of the board
		board = copy.deepcopy(self.board)
		flipped_board = [[board[i][j] for i in range(self.n) ] for j in range(self.n)] #now columns are grouped together
		diag1 = [board[i][i] for i in range(self.n)]
		diag2 = [board[i][(self.n-1)-i] for i in range(self.n)]
		def increment_vars(lst):
			count_X = lst.count('X')
			count_O = lst.count('O')
			if count_X > 0 and count_O == 0:
				var_list[(self.n-1)-count_X] += 1
			if count_X == 0 and count_O > 0:
				var_list[2*(self.n-1)-count_O] += 1

		for row in board:
			increment_vars(row)

		for col in flipped_board:
			increment_vars(col)
		increment_vars(diag1)
		increment_vars(diag2)
		
		
		#print(var_list,eval_coefs,end='\n')
		for i in range(self.n-1): #summing Xs
			eval_sum += (eval_coefs[i] * var_list[i])
		for i in range(self.n-1,self.n*2-2): #subtracting Os
			eval_sum -= (eval_coefs[i-(self.n-1)] * var_list[i])
		return (eval_sum,var_list)
	
	def jarvis_eval(self): 
		'''
		#enhances the value of a close to -win. Avoiding creation of double opportunities
		#intuition: building more options to win is more desireable than having as many in line
		
		#in 4x4: twice X2 should be more valuable than once X3, but X3 should be more valuable than one or 3 X2
		min_tokens  = math.ceil(self.n/2) #this will be the point from which we consider a situation that a player has a chance to win
		eval_sum, var_list = self.eval()
		Xoptions = var_list[self.n - 1 - min_tokens] 
		Ooptions = var_list[2*(self.n - 1) - min_tokens] 
		if Xoptions >= 2:
			eval_sum += Xoptions * 50
		if Ooptions >= 2:
			eval_sum -= Ooptions * 50
		return (eval_sum,var_list)
		'''
		eval_sum, var_list = self.eval()
		#dominate the center
		for row in self.board[1:-1]:
			for cell in row[1:-1]:
				if cell == 'O':
					eval_sum -= 2
				elif cell == 'X':
					eval_sum += 2
		return eval_sum
		#create


def rand_move():
	tokens = ['X','O']
	rand_tok = tokens[random.randint(0,1)]
	rand_row = random.randint(0,self.n-1)
	rand_col = random.randint(0,self.n-1)
	return (rand_tok,rand_row,rand_col)


def test():
	'''
		interactive testing
	'''
	s = State()
	print(s,'\n')
	s.make_move('X',1,0)
	print(s)
	print(s.board)

	for successor in s.possible_successors('O'):
		print(successor)
	
	command = ''
	moves = 0
	while command!='done()':
		print(s)
		print('enter your next move in the following format: <token,row,column>')
		if moves < 14:
			token,row,col = rand_move()
		else:
			command = input('--->')
			token,row,col = command.split(',')
			if command == 'reset()' or command == 'done()':
				s = State()
				moves = 0
				continue
		if not s.make_move(token,int(row),int(col)):
			print('illegal move')
		else:
			moves += 1