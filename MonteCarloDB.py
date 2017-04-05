import sqlite3

class MonteCarloDB():
    def __init__(self, playerID):
        db_name = 'monte_carlo_' + str(playerID) + '.db'
        self._db_conn = sqlite3.connect(db_name)
        self._db_cursor = self._db_conn.cursor()

        self._db_cursor.execute("CREATE TABLE IF NOT EXISTS states(state TEXT primary key, num INTEGER, denom INTEGER)")
        self._db_conn.commit()


    def __iter__(self):
        self._db_cursor.execute('SELECT * FROM states')
        for row in self._db_cursor:
            yield row
        return self

    def insert(self, state, num, denom) -> None:
        try:
            self._db_cursor.execute("INSERT INTO states VALUES (?, ?, ?)", (state, num, denom))
            #self._db_conn.commit()
        except:
            self._db_cursor.execute("UPDATE states SET num = ?, denom = ? WHERE state = ?", (num, denom, state))
            #self._db_conn.commit()

    def get(self, state) -> tuple:
        self._db_cursor.execute("SELECT * FROM states WHERE state = ?", (state,))
        results = self._db_cursor.fetchall()
        if results == []:
            return (0,0)
        return (results[0][1],results[0][2])

    def commit(self) -> None:
        self._db_conn.commit()

    def shutdown(self):
        self._db_conn.commit()
        self._db_cursor.close()
        self._db_conn.close()




'''
board = [
            [0,-1,0,-1,0,-1,0,-1],
            [-1,0,-1,0,-1,0,-1,0],
            [0,-1,0,-1,0,-1,0,-1],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [1,0,1,0,1,0,1,0],
            [0,1,0,1,0,1,0,1],
            [1,0,1,0,1,0,1,0]
        ]

b = boardToString(board)
m = MonteCarloDB()
m.insert(b, 1, 2)
m.shutdown()
'''
