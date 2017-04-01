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
        while(game.getWinner() == 0):
            game.printBoard()
            time.sleep(2)
            if self._currMove == -1:
                self._currMove = 1
                flag = True
                while flag:
                    move = player1.getMove(list(game.getBoard()))
                    if game.isValidMove(game.getBoard(),move, -1):
                        game.makeMove(-1, move)
                        flag = False;
            elif self._currMove == 1:
                self._currMove = -1
                flag = True
                while flag:
                    move = player2.getMove(list(game.getBoard()))
                    if game.isValidMove(game.getBoard(),move, 1):
                        game.makeMove(1, move)
                        flag = False;
        print(game.getWinner()," is the winner!")


# First param = -1
# Second param = 1
game = Game(Checkers(), AI.RandomAI(Checkers(), -1), AI.RandomAI(Checkers(), 1))
