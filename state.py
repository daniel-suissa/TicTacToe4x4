
import copy



class State:
	def __init__(self):
		'''
		members: 
			ASSUMPTION: max player is X
			2d list - board
		'''
		self.rows = 4
		self.cols = 4
		self.board = [['*' for j in range(self.cols)] for i in range(self.rows)]
		self.max_util = 1000
		self.min_util = -1000
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
	def p_init(self,board):
		'''
		return a new State with board as member
		'''
	def print_board(self):
		return '_' * (2 * self.cols - 1) + '\n' + '\n'.join([ ' '.join(row) for row in self.board]) + '\n' + '-' * (2 * self.cols - 1) + '\n'
	def __str__(self):
		board =  '_' * (2 * self.cols - 1) + '\n' + '\n'.join([ ' '.join(row) for row in self.board]) + '\n' + '-' * (2 * self.cols - 1) + '\n'
		board += '\n'
		c_t = self.check_terminal()
		if c_t != None:
			board += 'utility value: ' + str(c_t)
		else:
			board += 'state is not termial'
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
			return True
		else:
			print('invalid move')
			return False

	def possible_successors(self,token):
		if token == 'X':
			#generate successor states
			'''
			'''
		elif token == 'O':
			#generate successor states
			'''
			'''
	def check_terminal(self):
		'''
			return 'O' / 'X' / 'Tie' / None (not terminal)
		'''
		star_flag = False

		#check whether there is a row of 4 of the same token
		for row in self.board:
			if row == ['X'] * 4:
				return 1000
			elif row == ['O'] * 4:
				return -1000
			elif '*' in row:
				star_flag = True

		# check whether there is a column of 4 of the same token
		flipped_board = [[self.board[i][j] for i in range(self.cols) ] for j in range(self.rows)] #now columns are grouped together
		for col in flipped_board:
			if col == ['X'] * 4:
				return 1000
			elif col == ['O'] * 4:
				return 'O'

		#check diagonals - assumes equal rows and columns
		diag1 = [self.board[i][i] for i in range(self.cols)]
		if diag1 == ['X'] * 4:
			return 1000
		elif diag1 == ['O'] * 4:
			return -1000
		diag2 = [self.board[i][self.cols-1-i] for i in range(self.cols)]
		if diag1 == ['X'] * 4:
			return 1000
		elif diag1 == ['O'] * 4:
			return -1000

		if star_flag == False:
			return self.eval()
		else:
			return None
	def eval(self):
		'''
			assumes there is a tie
			works best for 4x4 - non generic
			count amount of X3s X2s and O3s and O1s
		'''
		var_list = [0] * 6 # [X3,X2,X1,O3,O2,O1]
		board = copy.deepcopy(self.board)
		#TODO: modify this to disregard already-counted tokens
		def increment_vars(lst):
			str_lst = ''.join(lst)
			if 3*'X' in str_lst:
				var_list[0] += 1
			elif 2*'X' in str_lst:
				var_list[1] += 1
			var_list[2] += lst.count('X')
			if 3*'O' in str_lst:
				var_list[3] += 1
			elif 2*'O' in str_lst:
				var_list[4] += 1
			var_list[5] += lst.count('O')

		flipped_board = [[board[i][j] for i in range(self.cols) ] for j in range(self.rows)] #now columns are grouped together
		diag1 = [board[i][i] for i in range(self.cols)]
		diag2 = [board[i][self.cols-1-i] for i in range(self.cols)]
		
		for row in board:
			increment_vars(row)
		for col in flipped_board:
			increment_vars(col)
		increment_vars(diag1)
		increment_vars(diag2)
		X3 = var_list[0]
		X2 = var_list[1]
		X1 = var_list[2]
		O3 = var_list[3]
		O2 = var_list[4]
		O1 = var_list[5]
		return (6*X3+3*X2+X1)-(6*O3+3*O2+O1)
		
import random	
def rand_move():
	tokens = ['X','O']
	rand_tok = tokens[random.randint(0,1)]
	rand_row = random.randint(0,3)
	rand_col = random.randint(0,3)
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
test()