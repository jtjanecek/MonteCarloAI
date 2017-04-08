import AI
from Checkers import Checkers
import time
from copy import deepcopy
# Abstract class
class Game():
    def __init__(self, game, player1, player2):
        ''' Initialize game board etc
        '''
        self.gameLoop(game, player1, player2)

    def gameLoop(self, game, player1, player2):
        # player1 = -1
        # player2 = 1
        board = game.getNewBoard()
        currentMove = game.getplayer1ID()
        self._p1CanMove = True
        self._p2CanMove = True
        counter = 0
        while((game.getWinner(board) == 0) and (self._p1CanMove or self._p2CanMove)):
            game.printBoard(board)
            counter += 1
            if counter > 500:
                #game.printBoard()
                self.winner = game.getWinner(board)
                print("TOO MANY MOVES")
                break
            if currentMove == game.getplayer1ID():
                board = self.doMove(game, player1, currentMove, board)
                currentMove = game.getplayer2ID()

            elif currentMove == game.getplayer2ID():
                board = self.doMove(game, player2, currentMove, board)
                currentMove = game.getplayer1ID()

        #game.printBoard()
        self.winner = game.getWinner(board)

    def doMove(self, game, player, playerID, board) -> bool:
        while True:
            if game.getAllPossibleMoves(board, playerID) == []:
                if playerID == game.getplayer1ID():
                    self._p1CanMove = False
                else:
                    self._p2Canmove = False
                return board
            move = player.getMove(deepcopy(board))
            if game.isValidMove(board,move, playerID):
                if playerID == game.getplayer1ID():
                    self._p1CanMove = True
                else:
                    self._p2Canmove = True
                board = game.makeMove(playerID, move, board)
                return board
            else:
                print("INVALID MOVE!")




# First param = -1
# Second param = 1
tryhard = 'y' == input('Tryhard (y/n): ')
p2 = input("Random (r) or Console (c): ")
num_games = int(input("Number of games: "))

d = {-1:0, 1:0, 0:0}
agent1 = AI.MonteCarloAI(Checkers(), -1, tryhard)
agent2 = AI.RandomAI(Checkers(), 1)

if p2 == 'r':
    agent2 = AI.RandomAI(Checkers(), 1)
elif p2 == 'c':
    agent2 = AI.ConsoleAI(Checkers(), 1)


for i in range(num_games):
    print("Playing game:",i+1)
    game = Game(Checkers(), agent1, agent2)
    agent1.gameOver(game.winner)
    agent2.gameOver(game.winner)
    print("                 Winner:",game.winner)
    d[game.winner] += 1
print(d)
