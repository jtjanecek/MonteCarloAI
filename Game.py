import AI
from Checkers import Checkers
import time
# Abstract class
class Game():
    def __init__(self, game, player1, player2):
        ''' Initialize game board etc
        '''
        self.gameLoop(game, player1, player2)

    def gameLoop(self, game, player1, player2):
        self._currMove = -1
        p1CanMove = True
        p2CanMove = True
        while((game.getWinner() == 0) and (p1CanMove or p2CanMove)):
            game.printBoard()
            #time.sleep(2)
            if self._currMove == -1:
                p1CanMove = self.doMove(game,player1, self._currMove)
                self._currMove = 1

            elif self._currMove == 1:
                p2CanMove = self.doMove(game,player2, self._currMove)
                self._currMove = -1

        game.printBoard()
        print(game.getWinner()," is the winner!")
        self._winner = game.getWinner()

    def doMove(self, game, player, cursor) -> bool:
        while True:
            if game.getAllPossibleMoves(game.getBoard(),cursor) == []:
                return False
            move = player.getMove(list(game.getBoard()))
            if game.isValidMove(game.getBoard(),move, cursor):
                game.makeMove(cursor, move)
                return True
            else:
                print("INVALID MOVE!")

# First param = -1
# Second param = 1
d = {-1:0, 1:0, 0:0}
for i in range(100):
    game = Game(Checkers(), AI.RandomAI(Checkers(), -1), AI.RandomAI(Checkers(), 1))
    d[game._winner] += 1
print(d)
