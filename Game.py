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

        self._currMove = -1
        p1CanMove = True
        p2CanMove = True
        while((game.getWinner() == 0) and (p1CanMove or p2CanMove)):
            #game.printBoard()
            print(".", end = "")
            #time.sleep(2)
            if self._currMove == -1:
                p1CanMove = self.doMove(game,player1, self._currMove)
                self._currMove = 1

            elif self._currMove == 1:
                p2CanMove = self.doMove(game,player2, self._currMove)
                self._currMove = -1

        #game.printBoard()
        self._winner = game.getWinner()

    def doMove(self, game, player, cursor) -> bool:
        while True:
            if game.getAllPossibleMoves(game.getBoard(),cursor) == []:
                return False
            move = player.getMove(deepcopy(game.getBoard()))
            if game.isValidMove(game.getBoard(),move, cursor):
                game.makeMove(cursor, move)
                return True
            else:
                print("INVALID MOVE!")

# First param = -1
# Second param = 1
d = {-1:0, 1:0, 0:0}
r = AI.RandomAI(Checkers(), 1)
#m = AI.RandomAI(Checkers(), 1)
m = AI.MonteCarloAI(Checkers(), -1)
for i in range(100):
    print("Playing game:",i+1)
    game = Game(Checkers(), m, r)
    if game._winner == 1:
       m.backPropagate(True)
    else:
       m.backPropagate(False)
    print("                 Winner:",game._winner)
    d[game._winner] += 1
print(d)
