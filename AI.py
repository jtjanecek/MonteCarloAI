import random
'''
Abstract class
'''
class AI():
    def __init__(self, game, player):
        self._game = game
        self._player = player

    def getMove(self, gameBoard) -> tuple:
        pass


class RandomAI(AI):
    def getMove(self, gameBoard) -> tuple:
        # l = self._game.getAllPossibleMoves(gameBoard, self._player)
        # return l[int(random.random()*len(l))]
        f1 = input("F1: ")
        f2 = input("F2: ")
        t1 = input("T1: ")
        t2 = input("T2: ")
        return ((f1,f2),(t1,t2))
