
from MaxConnect4Game import *
import copy

#returns the moves that are possible on a state
def possibleMoves(board):
	possibleMoves = []
	for col, colVal in enumerate(board[0]):
		if colVal == 0:
			possibleMoves.append(col)
	return possibleMoves
		
#calculates the resultant or new state after a particular move
def result(presentGame, column):
	newGame = maxConnect4Game()

	try:
		newGame.nodeDepth = presentGame.nodeDepth + 1
	except AttributeError:
		newGame.nodeDepth = 1

	newGame.pieceCount = presentGame.pieceCount
	newGame.gameBoard = copy.deepcopy(presentGame.gameBoard)
	if not newGame.gameBoard[0][column]:
		for i in range(5, -1, -1):
			if not newGame.gameBoard[i][column]:
				newGame.gameBoard[i][column] = presentGame.currentTurn
				newGame.pieceCount += 1
				break
	if presentGame.currentTurn == 1:
		newGame.currentTurn = 2
	elif presentGame.currentTurn == 2:
		newGame.currentTurn = 1

	newGame.checkPieceCount()
	newGame.countScore()

	return newGame

#performs decision making
class Minimax:
	def __init__(self, game, depth):
		self.currentTurn = game.currentTurn
		self.game = game
		self.maxDepth = int(depth)

	#returns minimax's decision	
	def makeDecision(self):

		# minimumValue = []
		possible_moves = possibleMoves(self.game.gameBoard)
		
		maximum_index = 0
		count = 0
		for move in possible_moves:
			count+=1
			output = result(self.game,move)
		
			x = self.miniValue(output,float('inf'),-float('inf'))
			if possible_moves[maximum_index] < x:
				maximum_index=count
		
		chosen = possible_moves[maximum_index]
		return chosen

	#performs minimizing operations
	def miniValue(self, state, alpha, beta):
		if state.pieceCount == 42 or state.nodeDepth == self.maxDepth:
			return self.utility(state)
		v = float('inf')

		for move in possibleMoves(state.gameBoard):
			newState = result(state,move)

			v = min(v,self.maxiValue(newState,alpha,beta ))
			if v <= alpha:
				return v
			beta = min(beta, v)
		return v

	#performs maximizing operations	
	def maxiValue(self, state, alpha, beta):
		if state.pieceCount == 42 or state.nodeDepth == self.maxDepth:
			return self.utility(state)
		v = -float('inf')

		for move in possibleMoves(state.gameBoard):
			newState = result(state,move)

			v = max(v,self.miniValue( newState,alpha,beta ))
			if v >= beta:
				return v
			alpha = max(alpha, v)
		return v

	#returns the utility that should be maximized or minimized
	def utility(self,state):
		if self.currentTurn == 1:
			utility = int(state.player1Score * 2 - state.player2Score)
		elif self.currentTurn == 2:
			utility = int(state.player2Score * 2 - state.player1Score)

		return utility

