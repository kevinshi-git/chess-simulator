#saves game state and determines moves
class GameState():
    def __init__(self) -> None:
        #starting game state, "--" is empty tile
        self.board=[
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"],]
        self.whiteToMove=True
        self.moveLog=[]
        self.moveFunctions={"P":self.getPawnMoves,"R":self.getRookMoves,"N":self.getKnightMoves,
                            "B":self.getBishopMoves, "Q":self.getQueenMoves,"K":self.getKingMoves}
    
    def makeMove(self,move): #runs basic moves, can't work for special cases like castling
        self.board[move.startRow][move.startCol]="--"
        self.board[move.endRow][move.endCol]=move.pieceMoved
        self.moveLog.append(move) #log moves
        self.whiteToMove=not self.whiteToMove #switch turns

    def undoMove(self):
        if not self.moveLog:
            return
        move=self.moveLog.pop()
        self.board[move.startRow][move.startCol]=move.pieceMoved
        self.board[move.endRow][move.endCol]=move.pieceCaptured
        self.whiteToMove=not self.whiteToMove #switch turns

    def getValidMoves(self):
        return self.getAllPossibleMoves()
    
    def getAllPossibleMoves(self):
        moves=[]
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn=self.board[r][c][0]
                if (turn=="w" and self.whiteToMove) or (turn=="b" and not self.whiteToMove):
                    piece=self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves)
                    
        return moves

    def getPawnMoves(self,r,c,moves):
        if self.whiteToMove and r>0: #white pawn moves
            if self.board[r-1][c]=="--": #move one forward
                moves.append(Move((r,c),(r-1,c),self.board))
                if r==6 and self.board[r-2][c]=="--": #move 2 forward
                    moves.append(Move((r,c),(r-2,c),self.board))
            if c-1>=0 and self.board[r-1][c-1][0]=="b": #capture diagnal left
                    moves.append(Move((r,c),(r-1,c-1),self.board))
            if c+1<=7 and self.board[r-1][c+1][0]=="b": #capture diagnal right
                    moves.append(Move((r,c),(r-1,c+1),self.board))
        elif r<7: #black pawn moves
            if self.board[r+1][c]=="--": #move 1 forward
                moves.append(Move((r,c),(r+1,c),self.board))
                if r==1 and self.board[r+2][c]=="--": #move 2 forward
                    moves.append(Move((r,c),(r+2,c),self.board))
            if c-1>=0 and self.board[r+1][c-1][0]=="w": #diagnal left
                moves.append(Move((r,c),(r+1,c-1),self.board))
            if c+1<=7 and self.board[r+1][c+1][0]=="w": #diagnal right
                moves.append(Move((r,c),(r+1,c+1),self.board))



    def checkDirections(self,r,c,moves,directions,tile_limit): #helper to find non pawn moves
        enemy_color="b" if self.whiteToMove else "w"
        for x,y in directions:
            new_r=r+x
            new_c=c+y
            tiles_traversed=0
            while 0<=new_r<=7 and 0<=new_c<=7 and tiles_traversed<tile_limit:
                if self.board[new_r][new_c]!="--":
                    if self.board[new_r][new_c][0]==enemy_color:
                        moves.append(Move((r,c),(new_r,new_c),self.board))
                    break
                else:
                    moves.append(Move((r,c),(new_r,new_c),self.board))
                new_r+=x
                new_c+=y
                tiles_traversed+=1


    def getRookMoves(self,r,c,moves):
        directions=[(0,1),(0,-1),(1,0),(-1,0)]
        self.checkDirections(r,c,moves,directions,float("inf"))
    def getKingMoves(self,r,c,moves):
        directions=[(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,-1),(-1,1)]
        self.checkDirections(r,c,moves,directions,1)
    def getQueenMoves(self,r,c,moves):
        directions=[(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,-1),(-1,1)]
        self.checkDirections(r,c,moves,directions,float("inf"))
    def getBishopMoves(self,r,c,moves):
        directions=[(1,1),(1,-1),(-1,-1),(-1,1)]
        self.checkDirections(r,c,moves,directions,float("inf"))
    def getKnightMoves(self,r,c,moves):
        directions = [(1, 2), (1, -2), (-1, 2), (-1, -2),
                      (2, 1), (2, -1), (-2, 1), (-2, -1)]
        self.checkDirections(r,c,moves,directions,1)



class Move():
    ranksToRows={"1":7,"2":6,"3":5,"4":4,
                 "5":3,"6":2,"7":1,"8":0}
    rowsToRanks={v:k for k,v in ranksToRows.items()}

    filesToCols={"a":0,"b":1,"c":2,"d":3,
                 "e":4,"f":5,"g":6,"h":7}
    colsToFiles={v:k for k,v in filesToCols.items()}

    def __init__(self,startSq,endSq,board) -> None:
        self.startRow=startSq[0]
        self.startCol=startSq[1]
        self.endRow=endSq[0]
        self.endCol=endSq[1]

        self.pieceMoved=board[self.startRow][self.startCol]
        self.pieceCaptured=board[self.endRow][self.endCol]
    def __eq__(self,other) -> bool:
        if isinstance(other,Move):
            return self.getChessNotation()==other.getChessNotation()
        return False

    def getChessNotation(self):# "real" chess notation
        return self.getRankFile(self.startRow,self.startCol)+self.getRankFile(self.endRow,self.endCol)
    def getRankFile(self,r,c):#basically prints row and col
        return self.colsToFiles[c]+self.rowsToRanks[r]