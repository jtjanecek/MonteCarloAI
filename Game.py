

''' Game object with 2 players. Player -1 and player 1. 0 represents non player.
'''

# Abstract class
class Game():
    def __init__(self):
        ''' Initialize game board etc
        '''
        pass

    def makeMove(self, player: int, move: tuple) -> bool:
        '''
        Parameters:
            player: -1 or 1
            move: tuple for board placement
        Return:
            boolean:
                true - move success
                false - move failed, move could not be placed
        '''
        pass

    def isValidMove(self, board:[list], move: tuple) -> bool:
        '''
        Checks if current board and move are valid
        '''
        pass

    def getAllPossibleMoves(self, currPlayer: int) -> list:
        '''
        Parameters:
            currPlayer: -1 or 1
        Return:
            list of possible moves in tuple form
        '''
        pass

    def hasWinner(self) -> int:
        '''
        Return:
            boolean, -1 if player -1 is winner
                      1 if player 1 is winner
                      0 if no winner
        '''
        pass



    def makeRandomMove(self, currPlayer) -> bool:
        '''
        Parameters:
            currPlayer: -1 or 1
        Returns boolean:
            true - move success
            false - move failed
        '''
        pass

    def printBoad(self) -> None:
        '''
        Prints board to console
        '''






'''
    Checkers
'''
class Checkers(Game):
    def __init__(self):
        ''' Initialize game board etc
        '''
        # 8 by 8 board
        self._board = [
            [0,-1,0,-1,0,-1,0,-1],
            [-1,0,-1,0,-1,0,-1,0],
            [0,-1,0,-1,0,-1,0,-1],
            [0,0,0,0,0,0,0,0,],
            [0,0,0,0,0,0,0,0,],
            [1,0,1,0,1,0,1,0],
            [0,1,0,1,0,1,0,1],
            [1,0,1,0,1,0,1,0]
        ]

    def printBoard(self) -> None:
        '''
        Prints board to console
        '''
        map = {-1:'o',1:'x',0:'-'}
        for row in self._board:
            for col in range(len(row)):
                print(map[row[col]], end = " ")
            print()

    def isValidMove(self, board:[list], move: tuple, currPlayer) -> bool:
        '''
        Checks if current board and move are valid
        '''
        pass

    def makeMove(self, player: int, move: tuple) -> bool:
        '''
        Parameters:
            player: -1 or 1
            move: tuple for board placement
        Return:
            boolean:
                true - move success
                false - move failed, move could not be placed
        '''
        pass

    def getAllPossibleMoves(self, currPlayer: int) -> list:
        '''
        Parameters:
            currPlayer: -1 or 1
        Return:
            list of possible moves in tuple form
        '''
        pass

    def hasWinner(self) -> int:
        '''
        Return:
            boolean, -1 if player -1 is winner
                      1 if player 1 is winner
                      0 if no winner
        '''
        pass

    def makeRandomMove(self, currPlayer) -> bool:
        '''
        Parameters:
            currPlayer: -1 or 1
        Returns boolean:
            true - move success
            false - move failed
        '''
        pass

game = Checkers()
game.printBoard()
