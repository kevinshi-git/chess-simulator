import pygame as p
import ChessEngine

width=height=512
dimension=8
sq_size=height//dimension
max_fps=15
images={}

def loadImages():
    pieces=["bR","bN","bB","bQ","bK","bB","bN","bR","bP","wR","wN","wB","wQ","wK","wB","wN","wR","wP"]
    for piece in pieces:
        images[piece]=p.transform.scale(p.image.load("images/"+piece+".png"),(sq_size,sq_size))

def main():
    p.init()
    screen=p.display.set_mode((width,height))
    clock=p.time.Clock()
    screen.fill(p.Color("white"))
    gs=ChessEngine.GameState()

    loadImages()
    running=True
    
    sqSelected=() #keep track where user last clicked (row,col)
    playerClicks=[] #keeps track of last move [(row,col),(newrow,newcol)]
    
    validMoves=gs.getValidMoves() #list of valid moves
    moveMade=False #checks if move has been made

    while running:
        for e in p.event.get():
            if e.type==p.QUIT:
                running=False
            #check mouse clicks
            elif e.type==p.MOUSEBUTTONDOWN:
                location=p.mouse.get_pos()
                col=location[0]//sq_size
                row=location[1]//sq_size
                if (row,col)==sqSelected: #if player clicks square twice, undo move
                    sqSelected=()
                    playerClicks=[]
                else:
                    sqSelected=(row,col)
                    playerClicks.append(sqSelected)
                
                if len(playerClicks)==2: #make moves
                    move=ChessEngine.Move(playerClicks[0],playerClicks[1],gs.board)
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade=True
                        sqSelected=() #resets player clicks so this works
                        playerClicks=[]
                    else:
                        playerClicks=[sqSelected]
            elif e.type==p.KEYDOWN: #reaction when a key is pressed
                if e.key==p.K_z: #undo if z is pressed
                    gs.undoMove()
                    moveMade=True
                    sqSelected=() #resets player clicks so this works
                    playerClicks=[]

        if moveMade:
            validMoves=gs.getValidMoves()
            moveMade=False
        #render 
        drawGameState(screen,gs)
        clock.tick(max_fps)
        p.display.flip()

#visualizes everything
def drawGameState(screen,gs):
    drawBoard(screen)
    drawPieces(screen,gs.board)

def drawBoard(screen):
    colors=[p.Color("white"),p.Color("gray")] 
    for r in range(dimension):
        for c in range(dimension):
            color=colors[(r+c)%2]
            p.draw.rect(screen,color,p.Rect(c*sq_size,r*sq_size,sq_size,sq_size))

def drawPieces(screen,board):
    for r in range(dimension):
        for c in range(dimension):
            piece=board[r][c]
            if piece !="--":
                screen.blit(images[piece],p.Rect(c*sq_size,r*sq_size,sq_size,sq_size))

main()
