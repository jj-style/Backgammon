class MyGame():
    def __init__(self,pc,ac):
        self.turn = None
        self.PlayerColor = pc
        self.AIColor = ac
        self.black_moves = 0
        self.white_moves = 0
        self.inGame = False
        
    def setChangeTurn(self):
        if self.turn == self.PlayerColor: self.turn = self.AIColor
        else: self.turn = self.PlayerColor

    def setTurn(self,newTurn):
        self.turn = newTurn

    def getTurn(self):
        return self.turn

    def getInGame(self):
        return self.inGame

    def setInGame(self,in_game):
        self.inGame = in_game

    def getColorOpposite(self):
        if self.turn == self.PlayerColor:
            return self.PlayerColor,self.AIColor
        else:
            return self.AIColor,self.PlayerColor

    def getGameOver(self,Board,Bar):
        remaining = 0
        for i in range(2):
            for k in range(12):
                if Board[i][k].getContainsColor() == self.getTurn():
                    remaining += Board[i][k].getNumberOfPieces()
        remaining += Bar.getNoPieces(self.getTurn())
        return remaining == 0
    
    def setIncreaseMove(self):
        if self.turn == self.PlayerColor:
            self.black_moves+=1
        else:
            self.white_moves+=1
    def getMoves(self):
        if self.turn == self.PlayerColor:
            return self.black_moves
        else:
            return self.white_moves
    def getBothMoves(self):
        return [self.black_moves,self.white_moves]
    def setBothMoves(self,b,w):
        self.black_moves = b
        self.white_moves = w
