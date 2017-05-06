# 4x4 Tic Tac Toe



Terminal Execution:
	1. Open terminal on a Mac OS X
	2. cd into the Tic Tac Toe folder
	3. run 'python game.py'

	To exit the program, simply terminate the GUI process by clicking on the 'X' of the window
	Note that Python 3 or above is needed along with the Tkinter module to run the program

Executable Run:


Menu:
	The menu was design to allow different versions of Tic Tac Toe. You should choose a difficulty level, the size of the board n (4x4 works the fastest), and decide whether player1 or player2 (usually the AI) plays first.
	Difficulties:
		The 'easy' difficulty uses a minimax cutoff of only 1 level, meaning that the AI sees only 1 move forward. Additionaly, it uses easy_eval to prioritize moves, which gives the same importance to every number of token placed on a clear row/column/diagonal.

		The 'medium' difficulty sees 2 steps into the future, and uses medium_eval, which does differetiates between different number of token placed, but not substantially.

		The 'hard' difficulty sees a growing amount of steps into the future, starting with 3 and growing by 2 with every move. It uses the eval function 6*Xthree + 3*Xtwo + Xone - (6*Othree + 3*Otwo + Oone)

		The Jarvis difficulty resembles the 'hard' difficulty, but uses a jarvis_eval method which its proof of concept will be explained later.

	Click the button and start playing!

The Classes
	Game Class:
		This is where the GUI and game management come together. Game manages the following:
		1. Tkinter GUI
		2. game State (separate type)
		3. game Players (seperate types)
		4. Ongoing game data and metrics such as who is the first player, the difficulty, current player and size of the board (this code is design for a generalize nxn that can be run as 4x4)

		The main function to notice in this class is dgplayer(self,event).
		This function is bound to the canvas button press. Every time the event MouseClick occurs, the location will be translated to the correct cell and place an 'O' token in it. Right after the human player has placed the token, the AIPlayer's 'move' method will be called to execute the opponent's move. Note that if you chose that the AI plays first, the first MouseClick will initiate the AI 'move'

	State Class: