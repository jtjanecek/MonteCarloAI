class Checkers():
    def __init__(self):
        # 8 by 8 board
        self._board = [
            [0,-1,0,-1,0,-1,0,-1],
            [-1,0,-1,0,-1,0,-1,0],
            [0,-1,0,-1,0,-1,0,-1],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [1,0,1,0,1,0,1,0],
            [0,1,0,1,0,1,0,1],
            [1,0,1,0,1,0,1,0]
        ]

    def printBoard(self) -> None:
        '''
        Prints board to console
        '''
        map = {-1:'o', -2:'O', 1:'x', 2:'X', 0:'-'}
        for row in self._board:
            for col in range(len(row)):
                print(map[row[col]], end = " ")
            print()
        print()

    def isValidMove(self, board: [list], move: tuple, currPlayer: int) -> bool:
        '''
        Checks if current board and move are valid
        ex: move = ((1,2),(3,4))
        '''

        # Check if out of bounds
        if len(move) != 2 or len(move[0]) != 2 or len(move[1]) != 2:
            return False
        if move[0][0] > 7 or move[0][0] < 0 or move[0][1] > 7 or move[0][1] < 0:
            return False
        if move[1][0] > 7 or move[1][0] < 0 or move[1][1] > 7 or move[1][1] < 0:
            return False

        if board[move[1][0]][move[1][1]] != 0:
            return False

        if currPlayer == -1:
            king = -2
        elif currPlayer == 1:
            king = 2

        # Check if move from is current player
        if (board[move[0][0]][move[0][1]] != currPlayer) and (board[move[0][0]][move[0][1]] != king):
            return False

        # Check if move is king
        if board[move[0][0]][move[0][1]] == king:
            isKing = True
        else:
            isKing = False

        # Check if its a simple move
        if abs(move[0][1] - move[1][1]) == 1 and board[move[1][0]][move[1][1]] == 0:
            if isKing and abs(move[0][0] - move[1][0]) == 1:
                return True
            if currPlayer == -1 and (move[0][0] - move[1][0]) == -1:
                return True
            elif currPlayer == 1 and (move[0][0] - move[1][0]) == 1:
                return True

        # Check if its a jump
        elif abs(move[0][1] - move[1][1]) == 2:
            if ((move[0][0] + move[1][0]) % 2 != 0) or ((move[0][1] + move[1][1]) % 2 != 0):
                return False
            if currPlayer == -1 and (move[0][0] - move[1][0]) == -2 and board[int((move[0][0] + move[1][0])/2)][int((move[0][1] + move[1][1])/2)] > 0:
                return True
            elif currPlayer == 1 and (move[0][0] - move[1][0]) == 2 and board[int((move[0][0] + move[1][0])/2)][int((move[0][1] + move[1][1])/2)] < 0:
                return True
        return False;

    def getAllPossibleMoves(self, board: [list], currPlayer: int) -> list:
        '''
        Parameters:
            currPlayer: -1 or 1
        Return:
            list of possible moves in tuple form
        '''
        resultList = []
        positions = []

        if currPlayer == -1:
            for i in range(len(board)):
                for j in range(len(board[i])):
                    if board[i][j] < 0:
                        positions.append((i,j))



        elif currPlayer == 1:
            for i in range(len(board)):
                for j in range(len(board[i])):
                    if board[i][j] > 0:
                        positions.append((i,j))


        for i in range(len(board)):
            for j in range(len(board[i])):
                for move in positions:
                    if self.isValidMove(board,(move,(i,j)),currPlayer):
                        resultList.append((move,(i,j)))

        return resultList

    def getWinner(self) -> int:
        '''
        Return:
            boolean, -1 if player -1 is winner
                      1 if player 1 is winner
                      0 if no winner
        '''
        c1 = 0
        c2 = 0
        for i in range(len(self._board)):
            for j in range(len(self._board[i])):
                if self._board[i][j] < 0:
                    c1 += 1
                elif self._board[i][j] > 0:
                    c2 += 1
        if c1 == 0:
            return 1
        if c2 == 0:
            return -1
        return 0


    def makeMove(self, player: int, move: tuple) -> None:
        '''
        Parameters:
            player: -1 or 1
            move: tuple for board placement
        '''
        # Have to delete old move, especially if jump
        self._board[move[0][0]][move[0][1]] = 0
        self._board[move[1][0]][move[1][1]] = player

    def getBoard(self) -> [list]:
        return list(self._board)



'''
Test Cases



board = [
    [0,-1,0,-1,0,-1,0,-1],
    [-1,0,-1,0,-1,0,-1,0],
    [0,-1,0,-1,0,-1,0,-1],
    [0,0,0,0,0,0,0,0],
    [0,0,0,2,0,0,0,0],
    [1,0,0,0,1,0,1,0],
    [0,1,0,1,0,1,0,1],
    [1,0,1,0,1,0,1,0]
]
c = Checkers()
l = c.getAllPossibleMoves(board,-1)
print(l)
print(len(l))
'''
