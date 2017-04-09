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
        if self._playerID == game.getplayer1ID():
            self._player1 = True

    def getMove(self, gameBoard) -> tuple:
        pass

    def gameOver(self, winner) -> None:
        pass


class RandomAI(AI):
    def getMove(self, gameBoard) -> tuple:
        #print("GENERATING MVOE FOR RANDOM")
        random.seed()
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
    def __init__(self, game, playerID, tryhard):
        AI.__init__(self, game, playerID)
        self._history = []
        self._db = MonteCarloDB(playerID)
        self._tryhard = tryhard
        self._num_simulations = 100
        self._max_depth = 10

        # board1 = [
        #     [0,-1,0,-1,0,-1,0,-1],
        #     [-1,0,-1,0,-1,0,-1,0],
        #     [0,-1,0,-1,0,-1,0,-1],
        #     [0,0,0,0,0,0,0,0],
        #     [0,0,0,0,0,0,0,0],
        #     [1,0,1,0,1,0,1,0],
        #     [0,1,0,1,0,1,0,1],
        #     [1,0,1,0,1,0,1,0]
        # ]
        #
        # board2 = [
        #     [0,-1,0,-1,0,-1,0,-1],
        #     [-1,0,-1,0,-1,0,-1,0],
        #     [0,0,0,-1,0,-1,0,-1],
        #     [-1,0,0,0,0,0,0,0],
        #     [0,1,0,0,0,0,0,0],
        #     [0,0,0,0,1,0,1,0],
        #     [0,1,0,1,0,1,0,1],
        #     [1,0,1,0,1,0,1,0]
        # ]
        #
        # move = ((3,0),(5,2))
        #
        # assert(self.evaluateBoard(board1, board2) == -1)
        # print(self.simulate(board2,move))

    def getMove(self, gameBoard) -> tuple:
        # query database for the stats on each possible move.
        possibleMoves = self._game.getAllPossibleMoves(gameBoard, self._playerID)
        stats = self.getMovesStats(deepcopy(possibleMoves), deepcopy(gameBoard))
        move = self.pickMove(deepcopy(gameBoard), possibleMoves, stats)
        self.addToHistory(move, gameBoard)
        return move

    def getMovesStats(self, possibleMoves, gameBoard):
        stats = []
        for move in possibleMoves:
            moveRepr = self.getMoveRepr(move, gameBoard)
            stats.append(self._db.get(moveRepr))
        return stats


    def pickMove(self, board, possibleMoves, stats):
        '''
        if stats are empty:
            for each move:
                simulate random simulations from that move
                update stats list
            get avg of stats list
            back propagate
        pick move from policy
        '''
        if self.areLeaves(stats):
            stats = []
            for move in possibleMoves:
                stat = self.simulate(deepcopy(board),move)
                stats.append(stat)
            # TODO: back propagagte
        print('Possible Moves:',possibleMoves)
        print('Stats:',stats)
        move = self.policy(possibleMoves, stats)
        print('Move chosen:',move)
        return move



    def simulate(self, board, move) -> tuple:
        boardBefore = deepcopy(board)
        boardAfter = self._game.makeMove(self._playerID, move, board)
        num = 0
        denom = 0
        for i in range(self._num_simulations):
            outcome = self.randomPlayout(deepcopy(boardBefore), deepcopy(boardAfter))
            if outcome == self._playerID:
                num += 1
            denom += 1
        return (num, denom)

    def randomPlayout(self, boardBefore, boardAfter):
        if self._player1:
            currentID = self._game.getplayer2ID()
        else:
            currentID = self._game.getplayer1ID()
        for i in range(self._max_depth):
            move = self.getRandomMove(deepcopy(boardAfter), currentID)
            boardAfter = self._game.makeMove(currentID, move, boardAfter)
            if currentID == self._game.getplayer1ID():
                currentID = self._game.getplayer2ID()
            else:
                currentID = self._game.getplayer1ID()
        return self.evaluateBoard(boardBefore, boardAfter)

    def evaluateBoard(self, boardBefore, gameBoard):
        # Specific to checkers
        # TODO: fix evaluate baord to compate boardBefore and gameBoard
        BME = 0
        BOPP = 0
        AME = 0
        AOPP = 0

        for i in boardBefore:
            for j in i:
                if j < 0:
                    BME += 1
                elif j > 0:
                    BOPP += 1
        for k in gameBoard:
            for y in k:
                if y < 0:
                    AME += 1
                elif y > 0:
                    AOPP += 1
        result = (BME - AME) < (BOPP - AOPP)
        if result:
            return -1
        else:
            return 1

    def getRandomMove(self, board, playerID):
        random.seed()
        l = self._game.getAllPossibleMoves(board, playerID)
        return l[int(random.random() * len(l))]

    def policy(self, possibleMoves, stats) -> tuple:
        c = 1.41421356237
        c = .5
        t = self.getNumSims(stats)
        base = .7
        currentMax = -999
        currentMaxIndex = 0

        for i in range(len(possibleMoves)):
            weight = stats[i][0] / stats[i][1]
            if weight > currentMax:
                currentMax = weight
                currentMaxIndex = i
        return possibleMoves[currentMaxIndex]

        '''
        for i in range(len(possibleMoves)):
            if stats[i][1] == 0:
                if self._tryhard:
                    weight = 0
                else:
                    weight = 9999
            else:
                if self._tryhard:
                    weight = stats[i][0] / stats[i][1]
                else:
                    weight = (stats[i][0] / stats[i][1]) + c * math.sqrt(math.log(t) / stats[i][1])
            if weight > currentMin:
                currentMin = weight
                currentMinIndex = i


        if currentMin == base:
            #print("No stats... returning random move")
            random.seed()
            return possibleMoves[int(random.random() * len(possibleMoves))]
        print(stats)
        print("Highest move: ", stats[currentMinIndex])
        return possibleMoves[currentMinIndex]
        '''



    def addToHistory(self, move, gameBoard):
        self._history.append(self.getMoveRepr(move,gameBoard))

    def getMoveRepr(self, move, gameBoard) -> str:
        board = self._game.makeMove(self._playerID, move, deepcopy(gameBoard))
        return self.boardToString(board)

    def getNumSims(self, stats):
        total = 0
        for num, denom in stats:
            total += denom
        return total

    def gameOver(self, winner):
        self.backPropagate(winner == self._playerID)

    def backPropagate(self, win: bool):
        '''
        win = True for win
        win = False for loss
        '''
        print("Len of back prop: ",len(self._history))
        for move in self._history:
            stats = self._db.get(move)
            num = stats[0]
            denom = stats[1] + 1
            if win:
                num += 1
            self._db.insert(move,num,denom)
        self._db.commit()
        self._history = []
        print("Back prop complete")

    def areLeaves(self, stats):
        for num, denom in stats:
            if num != 0 and denom != 0:
                return False
        return True


    def boardToString(self, board) -> str:
        s = ''
        for i in board:
            for j in i:
                s += str(j) + ' '
        return s
