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
            #time.sleep(2)
            if self._currMove == -1:
                self.doMove(game,player1, self._currMove)
                self._currMove = 1

            elif self._currMove == 1:
                self.doMove(game,player2, self._currMove)
                self._currMove = -1

        game.printBoard()
        print(game.getWinner()," is the winner!")

    def doMove(self, game, player, cursor):
        flag = True
        while flag:
            move = player.getMove(list(game.getBoard()))
            if game.isValidMove(game.getBoard(),move, cursor):
                game.makeMove(cursor, move)
                flag = False;
            else:
                print("INVALID MOVE!")

# First param = -1
# Second param = 1
for i in range(100):
    game = Game(Checkers(), AI.RandomAI(Checkers(), -1), AI.RandomAI(Checkers(), 1))
