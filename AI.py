import random
from MonteCarloDB import MonteCarloDB
from copy import deepcopy
import math
'''
Abstract class
'''
class AI():
    def __init__(self, game, playerID):
        self._game = game
        self._playerID = playerID

    def getMove(self, gameBoard) -> tuple:
        pass


class RandomAI(AI):
    def getMove(self, gameBoard) -> tuple:
        #print("GENERATING MVOE FOR RANDOM")
        l = self._game.getAllPossibleMoves(gameBoard, self._playerID)
        return l[int(random.random() * len(l))]


class ConsoleAI(AI):
    def getMove(self, gameBoard) -> tuple:
        f1 = input("F1: ")
        f2 = input("F2: ")
        t1 = input("T1: ")
        t2 = input("T2: ")
        return ((int(f1) - 1,int(f2) - 1),(int(t1) - 1,int(t2) - 1))


class MonteCarloAI(AI):
    def __init__(self, game, playerID):
        AI.__init__(self, game, playerID)
        self._history = []
        self._db = MonteCarloDB(playerID)

    def getMove(self, gameBoard) -> tuple:
        # query database for the stats on each possible move.
        possibleMoves = self._game.getAllPossibleMoves(gameBoard, self._playerID)
        stats = self.getMovesStats(deepcopy(possibleMoves), deepcopy(gameBoard))
        # pick move based on exploration vs exploitation
        move = self.pickMove(possibleMoves, stats)
        # add move to stack
        self.addToHistory(move, gameBoard)

        # return move
        return move

    def getMovesStats(self, possibleMoves, gameBoard):
        stats = []
        for move in possibleMoves:
            self._game.setBoard(gameBoard)
            self._game.makeMove(self._playerID, move)
            board = self._game.getBoard()
            stats.append(self._db.get(self.boardToString(board)))
        return stats

    def addToHistory(self, move, gameBoard):
        self._game.setBoard(gameBoard)
        self._game.makeMove(self._playerID, move)
        board = self._game.getBoard()
        self._history.append(self.boardToString(board))

    def pickMove(self, possibleMoves, stats):
        c = 1.41421356237
        t = self.getNumSims(stats)
        currentMin = -999
        currentMinIndex = 0
        for i in range(len(possibleMoves)):
            if stats[i][1] == 0:
                weight = 0
            else:
                #weight = (stats[i][0] / stats[i][1]) + c * math.sqrt(math.log(t) / stats[i][1])
                weight = stats[i][0] / stats[i][1]
            if weight > currentMin:
                currentMin = weight
                currentMinIndex = i
        return possibleMoves[int(random.random() * len(possibleMoves))]
        return possibleMoves[currentMinIndex]

    def getNumSims(self, stats):
        total = 0
        for num, denom in stats:
            total += denom
        return total

    def backPropagate(self, win: bool):
        '''
        win = True for win
        win = False for loss
        '''
        print("Len of back prop: ",len(self._history))
        for move in self._history:
            stats = self._db.get(move)
            num = stats[0]
            denom = stats[0] + 1
            if win:
                num += 1
            self._db.insert(move,num,denom)
        self._db.commit()
        self._history = []
        print("Back prop complete")



    def boardToString(self, board) -> str:
        s = ''
        for i in board:
            for j in i:
                s += str(j) + ' '
        return s
