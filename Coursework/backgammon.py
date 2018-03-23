import pygame,time,random,csv,tkinter,os
import tkinter.messagebox as mb
from classUndoStack import MyStack
from classButton import MyButton
from classGame import MyGame
from classLeaderboard import MyLeaderboard
from classToggle import MyToggleSwitch,MyToggleSwitchColor
import keyboard_input
import hard_ai

#Image loading
current_directory = os.getcwd()
RollButtonImg = pygame.image.load("{}//Images//button_roll.png".format(current_directory))
RollButtonHoverImg = pygame.image.load("{}//Images//button_roll_hover.png".format(current_directory))
undoButtonImg = pygame.image.load("{}//Images//undo.png".format(current_directory))

menu_img = pygame.image.load("{}//Images//Menu//menuImg.png".format(current_directory))
newGameImg = pygame.image.load("{}//Images//Menu//new_game.png".format(current_directory))
newGameHoverImg = pygame.image.load("{}//Images//Menu//new_game_hover.png".format(current_directory))
loadGameImg = pygame.image.load("{}//Images//Menu//load_game.png".format(current_directory))
loadGameHoverImg = pygame.image.load("{}//Images//Menu//load_game_hover.png".format(current_directory))
quitImg = pygame.image.load("{}//Images//Menu//quit.png".format(current_directory))
quitHoverImg = pygame.image.load("{}//Images//Menu//quit_hover.png".format(current_directory))

settingsBackground = pygame.image.load("{}//Images//Menu//settings_background.png".format(current_directory))
settingsImgMenu = pygame.image.load("{}//Images//Menu//settings.png".format(current_directory))
settingsImgInGame = pygame.image.load("{}//Images//settings_in_game.png".format(current_directory))
sliderOnImg = pygame.image.load("{}//Images//slider_on.png".format(current_directory))
sliderOffImg = pygame.image.load("{}//Images//slider_off.png".format(current_directory))

leaderboardImg = pygame.image.load("{}//Images//Menu//leaderboard.png".format(current_directory))
leaderboardBackground = pygame.image.load("{}//Images//Menu//leaderboard_background.png".format(current_directory))
instructionsImgMenu = pygame.image.load("{}//Images//Menu//instructions.png".format(current_directory))
instructionsImgInGame = pygame.image.load("{}//Images//instructions_in_game.png".format(current_directory))
gameOverBackground = pygame.image.load("{}//Images//Menu//game_over_screen.png".format(current_directory))

window_icon = pygame.image.load("{}//Images//icon.png".format(current_directory))

#global color variable definitions
maroonBrown = (165,42,42)
beige = (228,228,161)
background = (200,161,101)
borderBrown = (82,21,21)
validGreen = (0,205,0,0.01)
brightRed = (255,0,0)

black = (0,0,0)
white = (255,255,255)
yellow = (255,255,0)
grey = (211,211,211)

#Global variable definitions
PlayerColor = "Black"
AIColor = "White"
SAVEDGAME = "saved_game.csv" #name of csv file to load
AIPAUSE = 1   #length to pause between ai moves
size = width,height = 700,500

#Classes
rollButton = MyButton((size[0]/4)*2.25,size[1]/2,RollButtonImg)
Quit = MyButton((size[0]/2-int(quitImg.get_width()/2)),400,quitImg)
new = MyButton((size[0]/2-int(newGameImg.get_width()/2)),250,newGameImg)
load = MyButton((size[0]/2-int(loadGameImg.get_width()/2)),325,loadGameImg)
leaderboardButton = MyButton(size[0]-100,size[1]-75,leaderboardImg)
instructionsButtonMenu = MyButton(size[0]-75,size[1]-125,instructionsImgMenu)
instructionsButtonInGame = MyButton(size[0]-25,size[1]/2+25,instructionsImgInGame)
undoButton = MyButton(size[0]-25,size[1]/2,undoButtonImg)
settingsButtonMenu = MyButton(size[0]-75,size[1]-185,settingsImgMenu)
settingsButtonInGame = MyButton(size[0]-25,size[1]/2-25,settingsImgInGame)

#toggle switches
toggleHighlightMoves = MyToggleSwitch(sliderOnImg,sliderOffImg,170,150,'Highlight Moves On','Highlight Moves Off')
toggleAIDifficulty = MyToggleSwitch(sliderOnImg,sliderOffImg,170,250,'Hard AI','Easy AI')
togglePieceColor = MyToggleSwitchColor(sliderOnImg,sliderOffImg,450,150,'Black vs White','Blue vs Red')
toggleDiceAnimation = MyToggleSwitch(sliderOnImg,sliderOffImg,450,250,'Dice Animation On','Dice Animation Off')
toggle12Player = MyToggleSwitch(sliderOnImg,sliderOffImg,310,350,'1 Player','2 Player')

toggleAIDifficulty = MyToggleSwitch(sliderOnImg,sliderOffImg,170,150,'Hard AI','Easy AI')
toggle12Player = MyToggleSwitch(sliderOnImg,sliderOffImg,450,150,'1 Player','2 Player')
toggleHighlightMoves = MyToggleSwitch(sliderOnImg,sliderOffImg,170,250,'Highlight Moves On','Highlight Moves Off')
toggleDiceAnimation = MyToggleSwitch(sliderOnImg,sliderOffImg,450,250,'Dice Animation On','Dice Animation Off')
togglePieceColor = MyToggleSwitchColor(sliderOnImg,sliderOffImg,170,350,'Black vs White','Blue vs Red')
toggleAIPause = MyToggleSwitch(sliderOnImg,sliderOffImg,450,350,'AI Pause On','AI Pause Off')

class Spike(): #class spike for each spike on board
    def __init__(self):
        self.color = None
        self.containsColor = None
        self.NumberOfPieces = 0
        self.image = None
        self.spikeNo = None
        self.baseX = None
        self.baseY = None
        self.lcoord = None
        self.rcoord = None
        self.centercoord = None

    def setColor(self, color):
        self.color = color

    def setContainsColor(self, color):
        self.containsColor = color	

    def setImage(self,left,right,center):
        self.image = pygame.draw.polygon(screen, self.getColor(), ((left),(right),(center)), 0)

    def setNumberOfPieces(self,n):
        self.NumberOfPieces += n
        if self.NumberOfPieces == 0:
            self.setContainsColor(None)

    def setSpikeNo(self,i):
        i = int(i)
        self.spikeNo = i

    def setBaseX(self,x):
        self.baseX = x

    def setBaseY(self,y):
        self.baseY = y

    def setLeftCoord(self,coord):
        self.lcoord = coord

    def setRightCoord(self,coord):
        self.rcoord = coord
        
    def setCenterCoord(self,coord):
        self.centercoord = coord
        
    def getColor(self):
        return (self.color[0],self.color[1],self.color[2])
    def getContainsColor(self):
        return self.containsColor
    def getImage(self):
        return self.image
    def getNumberOfPieces(self):
        return self.NumberOfPieces
    def getSpikeNo(self):
        return self.spikeNo
    def getBaseX(self):
        return self.baseX
    def getBaseY(self):
        return self.baseY
    def getLeftCoord(self):
        return self.lcoord
    def getRightCoord(self):
        return self.rcoord
    def getCenterCoord(self):
        return self.centercoord

class MyBar():
    def __init__(self):
        self.pieces = []
        self.x = 25+(50*6)
        self.y = 25
        self.width = 50
        self.height = size[1]-(25*2)
        self.img = pygame.draw.rect(screen,borderBrown,(self.x,self.y,self.width,self.height),0)

    def set_piece(self,color):
        self.pieces.append(color)

    def remove_piece(self,color):
        self.pieces.remove(color)

    def displayBarRect(self):
        pygame.draw.rect(screen,borderBrown,(self.x,self.y,self.width,self.height),0)

    def getNoPieces(self,color):
        n = 0
        for piece in self.pieces:
            if piece == color:
                n+=1
        return n

    def getPieceList(self):
        return self.pieces

    def getBarImg(self):
        return self.img

class MyDice():
    def __init__(self):
        self.rollList = []
        self.diceImages = self.loadDiceImages()
    def loadDiceImages(self):
        dice = [0,0,0,0,0,0]
        for i in range(6):
            n = pygame.image.load("{}//Images//dice-{}.png".format(current_directory,i+1)) #load image of each dice from directory
            n = pygame.transform.scale(n,(50,50))       #transform the image smaller
            dice[i] = n                                 #place dice image into list
        return dice
    
    def roll_dice_effect(self):
        for i in range(10):             #10 times
            num1 = random.randint(1,6)  #get a random number
            pos1 = num1 - 1             # get the dice image position in the list
            screen.blit(self.diceImages[pos1],((size[0]/4)*2.8,size[1]/2))  #display the dice

            num2 = random.randint(1,6) #same as above for the other dice
            pos2 = num2 - 1
            screen.blit(self.diceImages[pos2],((size[0]/4)*3.2,size[1]/2))
            pygame.display.update()
            time.sleep(.1)

    def roll_dice(self):
        if toggleDiceAnimation.getStatus() == True: #if dice animation is on
            self.roll_dice_effect()         #show rolling dice effect
        num1 = random.randint(1,6)      #pick random number between 1 and 6
        num2 = random.randint(1,6)
        pos1 = num1 - 1                 #position is for the dice image to display since index starts at 0
        pos2 = num2 - 1
        if num1 == num2:                #if the numbers are the same
            self.rollList = [num1,num1,num1,num1]   #add 4 of the number to the roll list
        else:
            self.rollList = [num1,num2]
    
    def displayDice(self):
        if len(self.rollList) == 0:             #if there are no numbers in the roll list
            screen.blit(rollButton.getImage(),(rollButton.getX(),rollButton.getY()))
        else:
            distance = 0
            for i in range(len(self.rollList)): #for each number in the roll list
                screen.blit(self.diceImages[self.rollList[i]-1],(((size[0]/4)*2.4)+distance,size[1]/2)) #display the dice image 
                distance+=50
    def setRollList(self,myList):
        self.rollList = myList       
    def getRollList(self):
        return self.rollList
    def removeNumber(self,n):
        self.rollList.remove(n)
#____________________________________________________SPIKES___________________________________________________________________#

def setSpikes(): #set every item in 2d array board as a spike class
    for i in range(2):
        for k in range(12):
            Board[i][k] = Spike()
            
def setSpikeNumber():   #set a number for each spike from 1 to 24 going round the board clockwise
    for i in range(0,12):
        Board[0][i].setSpikeNo(i+1)
        Board[1][i].setSpikeNo(24-i)

def setSpikeColors(): #set alternate colors for each spike
    for i in range(0,12,2):         #every other spike to set colour on both rows
        Board[0][i].setColor(beige)
        Board[1][i].setColor(maroonBrown)

    for i in range(1,13,2):         #every other spike to set colour on both rows
        Board[0][i].setColor(maroonBrown)
        Board[1][i].setColor(beige)

def setSpikeImage():    #set each spikes triangle image
    y1 = 25
    x1 = 25
    for i in range(12):         #every other spike to set colour on both rows
        if i == 6:
            x1+=50
        Board[0][i].setImage((x1,y1),(x1+50,y1),(x1+25,y1+150)) #draws spike
        Board[0][i].setBaseX(x1+25)                                    #spikes center x coordinate for moving piece to spike
        Board[0][i].setBaseY(y1+12)                                       #spikes y coordinate at base for stacking pieces
        Board[0][i].setLeftCoord((x1,y1))                                   #this and next 2 lines set coordinates for drawing green triangle over it for valid moves
        Board[0][i].setRightCoord((x1+50,y1))
        Board[0][i].setCenterCoord((x1+25,y1+150))
        
        Board[1][i].setImage((x1,size[1]-y1),(x1+50,size[1]-y1),(x1+25,size[1]-y1-150))
        Board[1][i].setBaseX(x1+25)
        Board[1][i].setBaseY(size[1]-y1-12)
        Board[1][i].setLeftCoord((x1,size[1]-y1))
        Board[1][i].setRightCoord((x1+50,size[1]-y1))
        Board[1][i].setCenterCoord((x1+25,size[1]-y1-150))
        
        x1+=50

def getSpikeFromNumber(target_no):
    i = 0
    k = 0
    while i < 2: #iterate through all spikes on the board
        while k < 12:
            if Board[i][k].getSpikeNo() == target_no: #if the spikes number is the number you want to find
                return Board[i][k]      #return the spike class
            k+=1
        i+=1
        k=0

def getHighestSpike(color): #find the spike with the highest number containing pieces of a colour
    if color == Game.PlayerColor:
        boardNumber = 1
    else:
        boardNumber = 0
    count = 5
    while count > -1:
        piece = Board[boardNumber][count]
        if piece.getNumberOfPieces() > 0 and piece.getContainsColor()==color:
            return piece
        count -=1
#____________________________________________PIECES______________________________________________________#

def setInitialPiecePosition():
    #black pieces moving clockwise
    Board[0][0].setNumberOfPieces(2)
    Board[0][11].setNumberOfPieces(5)
    Board[1][7].setNumberOfPieces(3)
    Board[1][5].setNumberOfPieces(5)

    #set spike contain colour to black
    Board[0][0].setContainsColor(Game.PlayerColor)
    Board[0][11].setContainsColor(Game.PlayerColor)
    Board[1][7].setContainsColor(Game.PlayerColor)
    Board[1][5].setContainsColor(Game.PlayerColor)

    #white pieces moving anit-clockwise
    Board[1][0].setNumberOfPieces(2)
    Board[1][11].setNumberOfPieces(5)
    Board[0][7].setNumberOfPieces(3)
    Board[0][5].setNumberOfPieces(5)

    #set spike contain colour to white
    Board[1][0].setContainsColor(Game.AIColor)
    Board[1][11].setContainsColor(Game.AIColor)
    Board[0][7].setContainsColor(Game.AIColor)
    Board[0][5].setContainsColor(Game.AIColor)

def displayPieces():
    for i in range(12):
        if Board[0][i].getNumberOfPieces() != 0: #if the spike has pieces on
            number_of_pieces = Board[0][i].getNumberOfPieces()  #get the number of pieces it has
            pieceDistance = 0
            count = 0
            while count < number_of_pieces and count < 6: #draw up to 6 pieces
                if Board[0][i].getContainsColor() == Game.PlayerColor: #determine the color of piece to draw
                    color = togglePieceColor.getPieceColor()[0] 
                else: color = togglePieceColor.getPieceColor()[1]
                pygame.draw.circle(screen,color,(Board[0][i].getBaseX(),Board[0][i].getBaseY()+pieceDistance),10,0) #draw the piece
                pieceDistance+=22   #increase height
                count+=1

            number_of_pieces -= count
            if number_of_pieces != 0: #if there are more than 6 pieces
                if color == togglePieceColor.getPieceColor()[0]: text_color = togglePieceColor.getPieceColor()[1] #get opposite color to piece color for text
                else: text_color = togglePieceColor.getPieceColor()[0]
                renderText(str(number_of_pieces),15,text_color,Board[0][i].getBaseX()-3,Board[0][i].getBaseY()+pieceDistance-29) #text showing number of additional pieces
            
                
        if Board[1][i].getNumberOfPieces() != 0:
            number_of_pieces = Board[1][i].getNumberOfPieces()
            pieceDistance = 0
            count = 0
            while count < number_of_pieces and count < 6:
                if Board[1][i].getContainsColor() == Game.PlayerColor:
                   color = togglePieceColor.getPieceColor()[0]
                else: color = togglePieceColor.getPieceColor()[1]
                pygame.draw.circle(screen,color,(Board[1][i].getBaseX(),Board[1][i].getBaseY()-pieceDistance),10,0)
                pieceDistance+=22
                count+=1

            number_of_pieces -= count
            if number_of_pieces != 0:
                if color == togglePieceColor.getPieceColor()[0]: text_color = togglePieceColor.getPieceColor()[1]
                else: text_color = togglePieceColor.getPieceColor()[0]
                renderText(str(number_of_pieces),15,text_color,Board[1][i].getBaseX()-3,Board[1][i].getBaseY()-pieceDistance+15)
    #bar piece displaying
    pieceDistance = 0
    for piece in Bar.getPieceList():
        if piece == Game.PlayerColor:
            color = togglePieceColor.getPieceColor()[0]
        else:
            color = togglePieceColor.getPieceColor()[1]
        pygame.draw.circle(screen,color,(int(round(size[0]/2)),int(round(size[1]/2 + pieceDistance))),10,0)
        pieceDistance += 22
#________________________________________________BOARD_______________________________________________________#

def addBorders(): #adds boarders around board
    topHorz = pygame.draw.rect(screen,borderBrown,(0,0,size[0],25),0)
    bottomHorz = pygame.draw.rect(screen,borderBrown,(0,size[1]-25,size[0],25),0)
    rightVert = pygame.draw.rect(screen,borderBrown,(size[0]-25,25,25,size[1]-50),0)
    leftVert = pygame.draw.rect(screen,borderBrown,(0,25,25,size[1]-50),0)
    buttonsBar = pygame.draw.rect(screen,white,(size[0]-25,(size[1]/2),25,50),0)

    #adding background square for in game buttons to show hovering
    mx, my = pygame.mouse.get_pos()
    if undoButton.getWithin(mx,my): undo_bg_color = grey    #if the mouse coordinates are over the button, make square grey to show hover
    else: undo_bg_color = white                             #otherwise show white to show no hover
    if instructionsButtonInGame.getWithin(mx,my): instructions_bg_color = grey
    else: instructions_bg_color = white
    if settingsButtonInGame.getWithin(mx,my): settings_bg_color = grey
    else: settings_bg_color = white
    undoBg = pygame.draw.rect(screen,undo_bg_color,(size[0]-25,(size[1]/2),25,25),0) #draw the background square
    instructionBg = pygame.draw.rect(screen,instructions_bg_color,(size[0]-25,(size[1]/2)+25,25,25),0)
    settingsBg = pygame.draw.rect(screen,settings_bg_color,(size[0]-25,(size[1]/2)-25,25,25),0)

def RollDiceButton(mx,my):
    if rollButton.getWithin(mx,my): #if mouse coordiantes are over the roll dice button
        if rollButton.getImage() != RollButtonHoverImg: #if the roll button image isn't the hover image (to prevent unnecessary assignment of new image)
            rollButton.setImage(RollButtonHoverImg)         #set the image to the hover image
    else:
        if rollButton.getImage() != RollButtonImg: rollButton.setImage(RollButtonImg) #if the image isn't normal image set to normal image
    screen.blit(rollButton.getImage(),(rollButton.getX(),rollButton.getY()))        #show the image

def getRollButtonEvents():
    for event in pygame.event.get(): #event to allow player to quit
        if event.type == pygame.QUIT:
            askSave() #save game

        mx, my = pygame.mouse.get_pos()
        RollDiceButton(mx,my)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rollButton.getWithin(mx,my): #if click on roll button
                Dice.roll_dice() #roll the dice
                return True
            elif undoButton.getWithin(mx,my): #if click the undo button
                undoLoad() #perform an undo
                return True
            elif instructionsButtonInGame.getWithin(mx,my): showInstructions() #if click instructions, show the instructions
            elif settingsButtonInGame.getWithin(mx,my): settingsEvents() #if click settings, show the settings screen
    return False
#____________________________________________________INITIALISE______________________________________________________#

def initialiseBoard(game_type):
    setSpikes()
    setSpikeNumber()
    setSpikeColors()

    if game_type == 'new':
        setInitialPiecePosition()
        Game.setTurn(Game.PlayerColor)
    elif game_type == 'load':
        color = setSavedPosition(SAVEDGAME)
    elif game_type == 'empty':
        Game.setTurn(None)    

def initPygame():
    pygame.init()
    pygame.display.set_caption('Backgammon')
    pygame.display.set_icon(window_icon)
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    return screen,clock

def setSavedPosition(file_name):
    try:
        saved_file = open("{}//CSV//{}".format(current_directory,file_name))
        saved = csv.reader(saved_file,delimiter=',')
        save_list = []
        for row in saved:
            save_list.append(row)

        count = 0
        for i in range(2):
            for k in range(12):
                Board[i][k].setNumberOfPieces(int(save_list[count][0]))
                if save_list[count][1] == 'b': set_color = Game.PlayerColor
                elif save_list[count][1] == 'w': set_color = Game.AIColor
                else: set_color = None
                Board[i][k].setContainsColor(set_color)
                count+=1
        for black in range(int(save_list[24][0])):
            Bar.set_piece(Game.PlayerColor)
        for white in range(int(save_list[24][1])):
            Bar.set_piece(Game.AIColor)

        while "" in save_list[26] == True:
            save_list[26].remove("")
        colorGo = "".join(save_list[26])
        Game.setBothMoves(int(save_list[27][0]),int(save_list[27][1]))

        try:
            tempRollList = save_list[25]
            new_dice_list = []
            for number in tempRollList:
                if number != '':
                    new_dice_list.append(int(number))
            Dice.setRollList(new_dice_list)
        except:
            Dice.setRollList([])
        finally:
            Game.setTurn(colorGo)
    except:
        tkinterMessageBox(1,"Error","Unable to load game. Starting new one.")
        initialiseBoard('new')
        Game.setTurn(Game.PlayerColor)
#_________________________________________________SAVING GAME______________________________________________________________#

def saveGame(file_name): #save game to csv file
    try:
        save_file = open("{}//CSV//{}".format(current_directory,file_name),'w',newline='')
        csvwriter = csv.writer(save_file,delimiter =',')
        for i in range(2):
            for k in range(12):
                number_of_pieces = Board[i][k].getNumberOfPieces()
                color = Board[i][k].getContainsColor()
                if color == Game.PlayerColor:color='b'
                elif color == Game.AIColor:color='w'
                else:color = "None"
                rowwrite = number_of_pieces,color
                csvwriter.writerow(rowwrite)
        black_bar = Bar.getNoPieces(Game.PlayerColor)
        white_bar = Bar.getNoPieces(Game.AIColor)
        csvwriter.writerow([black_bar,white_bar])
        csvwriter.writerow(list(Dice.getRollList()))
        csvwriter.writerow(Game.getTurn())
        csvwriter.writerow(Game.getBothMoves())
        save_file.close()
    except:
        save_file.close()
        tkinterMessageBox(1,"Error","Unable to save game")
        pygame.quit()
        exit()

def askSave(): #ask user if they wish to save the game
    save = tkinterMessageBox(2,"Warning","Would you like to save your game?")

    if save:
        saveGame("saved_game.csv")
    pygame.quit()
    exit()
    
def undoSave(): #save the game to undo stack (temporary save)
    tempBoard = []
    for i in range(2):
        for k in range(12):
            number_of_pieces = Board[i][k].getNumberOfPieces()
            color = Board[i][k].getContainsColor()
            if color == Game.PlayerColor:color='b'
            elif color == Game.AIColor:color='w'
            else:color = "None"
            tempBoard.append([number_of_pieces,color])
    bar_black = Bar.getNoPieces(Game.PlayerColor)
    bar_white = Bar.getNoPieces(Game.AIColor)
    tempBoard.append([bar_black,bar_white])
    tempBoard.append(list(Dice.getRollList()))
    tempBoard.append(Game.getTurn())
    tempBoard.append(Game.getBothMoves())
    undo.add(tempBoard)

def undoLoad(): #load game from the undo stack
    tempBoard = undo.remove()
    if tempBoard != False:
        initialiseBoard('empty')
        Bar.pieces = []
        save_list = []
        for row in range(24):
            #row[0] number of pieces
            #row[1] color
            contains = int(tempBoard[row][0])
            if tempBoard[row][1] == 'b':
                set_color = Game.PlayerColor
            elif tempBoard[row][1] == 'w':
                set_color = Game.AIColor
            else:
                set_color = None
            save_list.append([contains,set_color])

        count = 0
        for i in range(2):
            for k in range(12):
                Board[i][k].setNumberOfPieces(save_list[count][0])
                Board[i][k].setContainsColor(save_list[count][1])
                count+=1

        for i in range(tempBoard[24][0]):
            Bar.set_piece(Game.PlayerColor)
        for k in range(tempBoard[24][1]):
            Bar.set_piece(Game.AIColor)
        rolls_left = tempBoard[25]
        Dice.setRollList(rolls_left)
        color_turn = tempBoard[26]
        Game.setTurn(color_turn)
        Game.setBothMoves(int(tempBoard[27][0]),int(tempBoard[27][1]))
    else:
        tkinterMessageBox(1,"Error","You can only undo 5 times. Please make some moves first.")
#____________________________________________________RENDER______________________________________________________#

def renderText(text,font_size,color,x,y): #render text pass variables: text, font size, color and x,y coordinates to blit to
    font = pygame.font.Font("{}//Fonts//calibri.ttf".format(current_directory), font_size)
    text = screen.blit((font.render(text, 1, color)),(x,y))
    return text

def render():
    screen.fill(background)
    addBorders()
    Bar.displayBarRect()
    setSpikeImage()
    displayPieces()
    screen.blit(undoButton.getImage(),(undoButton.getX(),undoButton.getY()))
    screen.blit(instructionsButtonInGame.getImage(),(instructionsButtonInGame.getX(),instructionsButtonInGame.getY()))
    screen.blit(settingsButtonInGame.getImage(),(settingsButtonInGame.getX(),settingsButtonInGame.getY()))
    Dice.displayDice()
    getPip()
    pygame.display.update()

def tkinterMessageBox(box_type,title,description):
    root = tkinter.Tk()
    root.withdraw()
    if box_type == 1:
        response = mb.showerror(title,description)
    elif box_type == 2:
        response = mb.askyesno(title,description)
    root.update()
    return response
#____________________________________________________GAME FUNCTIONS___________________________________________________#
    #___________________VALIDATION_______________#
def checkValidBarMove(dest): #check if bar move is valid
    if Game.getTurn() == Game.PlayerColor:
        spike_target = dest.getSpikeNo()
    else: spike_target = 25 - dest.getSpikeNo()
        
    if spike_target in Dice.getRollList():
        if (dest.getNumberOfPieces() == 0) or (dest.getNumberOfPieces() == 1 and dest.getContainsColor() != Game.getTurn()) or (dest.getContainsColor() == Game.getTurn()):
            return True
    return False

def checkValidPlayerMove(piece,target): #check if player move is valid
        current_color,opposite_color = Game.getColorOpposite()
        if current_color == Game.PlayerColor:
            target_no = piece.getSpikeNo()+target	#get the spike number of the destination
            if target_no <= piece.getSpikeNo() or target_no > 24: #return false if the spike number is less than the pieces spike number because can't move backwards
                return False
        else:
            target_no = piece.getSpikeNo()-target
            if target_no >= piece.getSpikeNo() or target_no < 1: #return false if the spike number is less than the pieces spike number because can't move backwards
                return False
        target_spike = getSpikeFromNumber(target_no)
        if (target_spike.getContainsColor() in [current_color,None]) or (target_spike.getContainsColor() == opposite_color and target_spike.getNumberOfPieces() == 1):
            return True
        else: return False
    
def getPip(): #get pip scores for both players
    blackPip = 0
    whitePip = 0
    for i in range(2):
        for k in range(12):
            if Board[i][k].getContainsColor() == Game.PlayerColor:
                for piece in range(Board[i][k].getNumberOfPieces()):
                    blackPip += (25 - Board[i][k].getSpikeNo())
            elif Board[i][k].getContainsColor() == Game.AIColor:
                for piece in range(Board[i][k].getNumberOfPieces()):
                    whitePip += ((0 - Board[i][k].getSpikeNo())*-1)

    blackPip += 25*Bar.getNoPieces(Game.PlayerColor)
    whitePip += 25*Bar.getNoPieces(Game.AIColor)
    
    p1Text = "Player 1 Pip: {}".format(blackPip)
    p2Text = "Player 2 Pip: {}".format(whitePip)
    if Game.getTurn() == Game.PlayerColor:
        c1,c2 = validGreen,white
    else: c1,c2 = white,validGreen
    renderText(p1Text,15,c1,130,5)
    renderText(p2Text,15,c2,420,5)

    #show what piece colours turn it is
    if Game.getTurn() == Game.PlayerColor:
        pygame.draw.circle(screen,yellow,(335,13),12,0)
    else: pygame.draw.circle(screen,yellow,(365,13),12,0)
    pygame.draw.circle(screen,black,(335,13),10,0)
    pygame.draw.circle(screen,white,(365,13),10,0)
    return blackPip,whitePip

def getClearPieces(color): #determine if players pieces are all in the take off quarter
    if Bar.getNoPieces(color) > 0:
        return False
    if color == Game.PlayerColor:
        board_1,board_2 = 0,1
    else:
        board_1,board_2 = 1,0
    i = 0
    while i < len(Board[board_1]):
        if Board[board_1][i].getContainsColor() == color:
            if Board[board_1][i].getNumberOfPieces() > 0:
                return False
        i+=1
    i = 6
    while i < 12:
        if Board[board_2][i].getContainsColor() == color:
            if Board[board_2][i].getNumberOfPieces() > 0:
                return False
        i+=1
    return True

def getPieceDest(selected): #get piece/dest from user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            askSave()

        mx, my = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            i = 0
            k = 0
            while i < 2:
                while k < 12:
                    if Board[i][k].getImage().collidepoint(mx,my):
                        selected = True
                        return Board[i][k], selected
                    else:
                        k+=1
                i+=1
                k=0
            if Bar.getBarImg().collidepoint(mx,my):
                n = Bar.getNoPieces(Game.getTurn())
                if n != 0:
                    selected = True
                    return "bar",selected
            elif mx >= 0 and mx <= 25:
                if my >= size[1]/2 and my <= size[1]-25 or my >= 25 and my <= size[1]/2:
                        return "takeoff",True
            elif undoButton.getWithin(mx,my):
                return False, False
            elif instructionsButtonInGame.getWithin(mx,my):
                showInstructions()
                render()
            elif settingsButtonInGame.getWithin(mx,my):
                settingsEvents()
                render()
    return None,selected

def getNoValidMoves(): #determine the number of different moves the player could make
    valid_moves = 0
    valid_moves+=len(getValidDests('bar'))
    if valid_moves == 0:
        for i in range(2):
            for k in range(12):
                if Board[i][k].getContainsColor() == Game.getTurn():
                    valid_moves += len(getValidDests(Board[i][k]))
    return valid_moves

def getValidDests(piece): #get list of all destinations that could be moved to
    valid_dests = []
    if piece != "bar":
        for number in Dice.getRollList():
            valid = checkValidPlayerMove(piece,number)
            if valid:
                if Game.getTurn() == Game.PlayerColor:
                    valid_dests.append(piece.getSpikeNo()+number)
                else:
                    valid_dests.append(piece.getSpikeNo()-number)
                
        n = len(Dice.getRollList())
        count = 0
        if getClearPieces(Game.getTurn()):
            while count < n:
                if Game.getTurn() == Game.PlayerColor:
                    if piece.getNumberOfPieces() > 0 and (piece.getSpikeNo() + Dice.getRollList()[count]) == 25:
                        valid_dests.append("takeoff")
                        break
                    else:
                        highest = getHighestSpike(Game.getTurn())
                        if highest.getSpikeNo()+Dice.getRollList()[count] > 25 and piece == highest:
                            valid_dests.append("takeoff")
                            break
                elif Game.getTurn() == Game.AIColor:
                    if piece.getNumberOfPieces() > 0 and (piece.getSpikeNo() - Dice.getRollList()[count]) == 0:
                        valid_dests.append("takeoff")
                        break
                    else:
                        highest = getHighestSpike(Game.getTurn())
                        if highest.getSpikeNo()-Dice.getRollList()[count] < 0 and piece == highest:
                            valid_dests.append("takeoff")
                            break
                count+=1
    elif piece == "bar":
        for i in range(Bar.getNoPieces(Game.getTurn())):
            for n in Dice.getRollList():
                if Game.getTurn() == Game.PlayerColor:
                    dest = Board[0][n-1]
                else:
                    dest = Board[1][n-1]
                val = checkValidBarMove(dest)
                if val:
                    valid_dests.append(dest.getSpikeNo())
    return valid_dests

def displayValidDest(piece): #show valid destinations as a green spike to signify a valid move
    valid_dest = getValidDests(piece)
    if "takeoff" in valid_dest:
        if Game.getTurn() == Game.PlayerColor:
            for n in Dice.getRollList():
                if piece.getSpikeNo() + n == 25:
                    pygame.draw.rect(screen,validGreen,(0,size[1]/2,25,size[1]/2-25),0)
                else:
                    highest = getHighestSpike(Game.getTurn())
                    if piece == highest and n + piece.getSpikeNo() > 25:
                        pygame.draw.rect(screen,validGreen,(0,size[1]/2,25,size[1]/2-25),0)
        else:
            for n in Dice.getRollList():
                if piece.getSpikeNo() - n == 0:
                    pygame.draw.rect(screen,validGreen,(0,25,25,size[1]/2),0)
                else:
                    highest = getHighestSpike(Game.getTurn())
                    if piece == highest and piece.getSpikeNo() - n < 0:
                        pygame.draw.rect(screen,validGreen,(0,25,25,size[1]/2),0)
        valid_dest.pop(-1)
    
    for i in valid_dest:
        spike = getSpikeFromNumber(i)
        pygame.draw.polygon(screen,validGreen,((spike.getLeftCoord()[0],spike.getLeftCoord()[1]),(spike.getRightCoord()[0],spike.getRightCoord()[1]),(spike.getCenterCoord()[0],spike.getCenterCoord()[1])),0)

def checkValidPiece(piece): #check if selected piece is valid
    if piece != None:
        if Bar.getNoPieces(Game.getTurn()) > 0 and piece != "bar":
            tkinterMessageBox(1,"Invalid Piece Selection","Must move piece off bar first.")
            return False
        elif piece == "bar":
            if Bar.getNoPieces(Game.getTurn()) == 0:
                return False
            else:
                return True
        elif piece == "takeoff":
            return False
        elif piece.getContainsColor() == Game.getTurn():
            if len(getValidDests(piece)) > 0:
                return True
        elif piece.getContainsColor() != None:
            tkinterMessageBox(1,"Invalid Piece Selection","Cannot select opponents piece.")
        else:
            return False
    return False

def checkValidDest(piece,dest,valid_dest): #check if selected destination is valid
    if dest != None:
        if dest != "bar":
            if dest == "takeoff":
                if dest in valid_dest:
                    return True
                else: return False
            elif dest.getSpikeNo() in valid_dest:
                return True
    return False

def getRemovablePiece():
    i = 0
    k = 0
    while i < 2:
        while k < 12:
            piece = Board[i][k]
            n = len(Dice.getRollList())
            count = 0
            if getClearPieces(Game.getTurn()):
                while count < n:
                    if Game.getTurn() == Game.PlayerColor:
                        if piece.getNumberOfPieces() > 0 and (piece.getSpikeNo() + Dice.getRollList()[count]) == 25:
                            return piece
                        else:
                            highest = getHighestSpike(Game.getTurn())
                            if highest.getSpikeNo()+Dice.getRollList()[count] > 25 and piece == highest:
                                return piece
                    elif Game.getTurn() == Game.AIColor:
                        if piece.getNumberOfPieces() > 0 and (piece.getSpikeNo() - Dice.getRollList()[count]) == 0:
                            return piece
                        else:
                            highest = getHighestSpike(Game.getTurn())
                            if highest.getSpikeNo()-Dice.getRollList()[count] < 0 and piece == highest:
                                return piece
                    count+=1
            k+=1
        i+=1
        k = 0
    return False

def getRandomPiece():
    optional_pieces = []
    for i in range(2):
        for k in range(12):
            if Board[i][k].getContainsColor() == Game.getTurn() and Board[i][k].getNumberOfPieces()>0:
                optional_pieces.append(Board[i][k])
    selected_valid = False
    while not selected_valid:
        piece = random.choice(optional_pieces)
        selected_valid = checkValidPiece(piece)
    return piece

def getRandomDest(piece):
    while True:
        valid_dest = getValidDests(piece)
        dest = random.choice(valid_dest)
        dest = getSpikeFromNumber(dest)
        validDestination = checkValidDest(piece,dest,valid_dest)
        if not validDestination: piece = getRandomPiece()
        else: return dest

def canAIClear(piece):
    n = len(Dice.getRollList())
    count = 0
    if getClearPieces(Game.getTurn()):
        while count < n:
            if Game.getTurn() == Game.PlayerColor:
                if piece.getNumberOfPieces() > 0 and (piece.getSpikeNo() + Dice.getRollList()[count]) == 25:
                    return True
                else:
                    highest = getHighestSpike(Game.getTurn())
                    if highest.getSpikeNo()+Dice.getRollList()[count] > 25 and piece == highest:
                        return True
            elif Game.getTurn() == Game.AIColor:
                if piece.getNumberOfPieces() > 0 and (piece.getSpikeNo() - Dice.getRollList()[count]) == 0:
                    return True
                else:
                    highest = getHighestSpike(Game.getTurn())
                    if highest.getSpikeNo()-Dice.getRollList()[count] < 0 and piece == highest:
                        return True
            count+=1
    return False

def getInitialValidation():
    n = Bar.getNoPieces(Game.getTurn())
    if n != 0: valid = len(getValidDests('bar'))
    else: valid = 1
    if valid == 0: return None
    number_of_valid_moves = getNoValidMoves()
    if number_of_valid_moves == 0:
        return None
    return True
#____________________________________________________PIECE MOVE______________________________________________________#

def movePiece(piece,target):
    piece.setNumberOfPieces(-1)      #-1 from number of pieces spike contains
    target.setNumberOfPieces(1)      #Add a piece to spike
    if target.getNumberOfPieces() == 1:
        target.setContainsColor(Game.getTurn())
            
def makeTakeMove(piece,target):
    Bar.set_piece(target.getContainsColor()) #move opposite piece to the bar
    new_color = piece.getContainsColor()    #get new colour for destination
    target.setContainsColor(new_color)      #change the colour the destination contains
    piece.setNumberOfPieces(-1)             #remove 1 piece from the piece

def makeBarMove(dest):
    dest.setContainsColor(Game.getTurn())   #set destination to contain your colour
    dest.setNumberOfPieces(1)               #add 1 piece to the destination
    Bar.remove_piece(Game.getTurn())        #remove a piece from the bar

def makeBarTakeMove(dest):
    color,oppositeColor = Game.getColorOpposite()
    Bar.remove_piece(color)             #remove players piece from the bar
    Bar.set_piece(oppositeColor)        #set opponents piece to the bar
    dest.setContainsColor(color)        #set destination to contain your colour

def normalMove(piece,dest,player):
    if Game.getTurn() == Game.PlayerColor:
        number_used = dest.getSpikeNo() - piece.getSpikeNo() #work out the number used to remove from dice list
    else:
        number_used = piece.getSpikeNo() - dest.getSpikeNo()

    if player == "player": undoSave() #save the game if it is a manual player move
    if dest.getNumberOfPieces() == 1 and dest.getContainsColor() != Game.getTurn():
        makeTakeMove(piece,dest)
    else:
        movePiece(piece,dest)
    Dice.removeNumber(number_used)  #remove the number used to move from the dice list
    render()

def barMove(dest,player):
    if player == "player": undoSave()
    if dest.getNumberOfPieces() == 1 and dest.getContainsColor() != Game.getTurn():
            makeBarTakeMove(dest)
    else:
        makeBarMove(dest)
    number_used = dest.getSpikeNo()         #get number used to remove from dice list
    if Game.getTurn() == Game.AIColor:
        number_used = 25%number_used       #adjust number to 1-6 for AI
    Dice.removeNumber(number_used)
    render()

def clearPieceMove(piece,player):
    if player == "player": undoSave()
    piece.setNumberOfPieces(-1)
    number = piece.getSpikeNo()
    if Game.getTurn() == Game.PlayerColor: number = 25%number
    if number in Dice.getRollList():
        Dice.removeNumber(number)
    else:
        highest = max(Dice.getRollList())
        Dice.removeNumber(highest)
    render()
#______________________________________________TURNS_____________________#

def hardAI():
    if getInitialValidation() == None:
        return None
    canClear = False
    
    if Bar.getNoPieces(Game.getTurn()) > 0:
        piece = "bar"
        dest = hard_ai.canSafelyMoveBarPiece(Board,Game,Dice)
        if not dest:
            valid_dest = getValidDests(piece)
            dest = random.choice(valid_dest)
            dest = getSpikeFromNumber(dest)
    elif getClearPieces(Game.getTurn()):
        piece = getRemovablePiece()
        if piece != False:
            dest = "takeoff"
        else:
            piece = getRandomPiece()
            dest = getRandomDest(piece)
                 
    else:
        black_pip,white_pip = getPip()
        if Game.getTurn() == Game.AIColor: diff = white_pip - black_pip
        else: diff = black_pip - white_pip
        if hard_ai.getInLateGame2(1,Board,Game) == True or (diff >= 20) or (getClearPieces(Game.getColorOpposite()[1])):
            print("late game strategy")
            found_valid = False
            rank = 1
            while not found_valid:
                piece = hard_ai.getHighestCurrentSpike2(rank,Game.getTurn(),Board,Game)
                if checkValidPiece(piece) == False:
                    rank+=1
                else:
                    found_valid = True
            dest = getRandomDest(piece)
        else:
            piece,dest = hard_ai.getSafeMove(Board,Game,Dice)
            if not piece and not dest:
                potential_moves = []
                for i in range(3):
                    piece = getRandomPiece()
                    dest = getRandomDest(piece)
                    potential_moves.append([piece,dest,hard_ai.evaluateSafety(dest.getSpikeNo(),Board,Game)])
                potential_moves = sorted(potential_moves, key=lambda x: x[2])
                piece,dest = potential_moves[0][0],potential_moves[0][1]
    #make move
    if dest == "takeoff":
        clearPieceMove(piece,"ai") #clear piece move
    elif piece == "bar":
        barMove(dest,"ai") #bar move
    else:
        normalMove(piece,dest,"ai") #normal move
    return True

def easyAI():
    if getInitialValidation() == None:
        return None
    canClear = False
    
    #piece selection
    if Bar.getNoPieces(Game.getTurn()) > 0:
        piece = "bar"
        selected = True
    else:
        piece = getRandomPiece()

    #dest selection
    if getClearPieces(Game.getTurn()):
        canClear = canAIClear(piece)
        if canClear:
            dest = "takeoff"
    else:
        dest = getRandomDest(piece)
    #make move
    if dest == "takeoff":
        clearPieceMove(piece,"ai") #clear piece move
    elif piece == "bar":
        barMove(dest,"ai") #bar move
    else:
        normalMove(piece,dest,"ai") #normal move
    return True
    
def PlayerMove():
    if getInitialValidation() == None:
        tkinterMessageBox(1,"No valid moves","No valid moves. Skipping turn.")
        return None

    selected_piece = False
    while not selected_piece:
        piece, selected_piece = getPieceDest(selected_piece)
        if piece == False and selected_piece == False:
            return "undo"
        selected_piece = checkValidPiece(piece)

    if toggleHighlightMoves.getStatus():
        displayValidDest(piece)
        displayPieces()
        pygame.display.update()
    valid_dest = getValidDests(piece)
        
    selected_dest = False
    while not selected_dest:
        dest, selected_dest = getPieceDest(selected_dest)
        if dest == False and selected_dest == False:
            return "undo"
    validDestination = checkValidDest(piece,dest,valid_dest)
    if not validDestination:
        return False

    #make move
    if dest == "takeoff":
        clearPieceMove(piece,"player") #clear piece move
    elif piece == "bar":
        barMove(dest,"player") #bar move
    else:
        normalMove(piece,dest,"player") #normal move
    return True
    
def GameLoop(against_ai,hard_ai):
    GameOver = False
    Game.setInGame(True)
    while not GameOver:
        Dice.displayDice()
        render()
        if len(Dice.getRollList()) == 0:
            rolled = getRollButtonEvents()
        else:
            rolled = True
        if rolled:
            render()
            pygame.display.update()
            turns = len(Dice.getRollList())
            while turns > 0:
                if against_ai == False: #not against ai
                    moved = PlayerMove()
                else:
                    if Game.getTurn() == Game.PlayerColor:
                        moved = PlayerMove()
                    else:
                        if toggleAIPause.getStatus():
                            time.sleep(AIPAUSE/2)
                        if  hard_ai == False: moved = easyAI() #EASY
                        else: moved = hardAI()
                        if toggleAIPause.getStatus():
                            time.sleep(AIPAUSE/2)
                    
                if moved == 'undo':
                    tempColor = Game.getTurn()
                    undoLoad()
                    if Game.getTurn() != Game.PlayerColor and Game.getTurn() != Game.AIColor:
                        Game.setTurn(tempColor)
                    turns+=1
                elif moved:
                    turns -=1
                    Game.setIncreaseMove()
                elif moved == None: turns = 0
                render()
                GameOver = Game.getGameOver(Board,Bar)
                if GameOver:
                    return Game.getTurn(),Game.getMoves()
            Dice.setRollList([])
            rolled = False
            Game.setChangeTurn()
        clock.tick(32)
#_______________________________________________MENU_____________________________________________#

def displaySortOptions(c1,c2,c3,c4):
    firstname_txt = renderText("firstname",25,c1,10,120)
    surname_txt = renderText("surname",25,c2,10,150)
    score_txt = renderText("score",25,c3,10,180)
    recent_txt = renderText("most recent",25,c4,10,210)
    return firstname_txt,surname_txt,score_txt,recent_txt

def displayOrderOptions(c1,c2):
    ascending_txt = renderText("Ascending",25,c1,10,275)
    descending_txt = renderText("Descending",25,c2,10,295)
    return ascending_txt,descending_txt

def leaderBoardEvents(sortType,orderType):
    back_txt = renderText("Back",25,white,0,0)
    renderText("Sort by:",25,white,0,80)
    renderText("Order by",25,white,0,250)
    if sortType == 1:
        firstname_txt,surname_txt,score_txt,recent_txt = displaySortOptions(validGreen,white,white,white)
    elif sortType == 2:
        firstname_txt,surname_txt,score_txt,recent_txt = displaySortOptions(white,validGreen,white,white)
    elif sortType == 3:
        firstname_txt,surname_txt,score_txt,recent_txt = displaySortOptions(white,white,validGreen,white)
    elif sortType == 4:
        firstname_txt,surname_txt,score_txt,recent_txt = displaySortOptions(white,white,white,validGreen)
    if orderType == 1:
        ascending_txt,descending_txt = displayOrderOptions(validGreen,brightRed)
    else:
        ascending_txt,descending_txt = displayOrderOptions(brightRed,validGreen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            mx, my = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_txt.collidepoint(mx,my): return False
                elif firstname_txt.collidepoint(mx,my): return 1
                elif surname_txt.collidepoint(mx,my): return 2
                elif score_txt.collidepoint(mx,my): return 3
                elif recent_txt.collidepoint(mx,my): return 4
                elif ascending_txt.collidepoint(mx,my): return 5
                elif descending_txt.collidepoint(mx,my): return 6
        pygame.display.update()


def addBackdrop(width,height,x,y,alpha_level):
    backdrop = pygame.Surface((width,height))
    backdrop.set_alpha(alpha_level)
    backdrop.fill(grey)
    screen.blit(backdrop,(x,y))
    
def leaderBoards():
    leaderboard.loadLeaderboard()
    stagger_distance = 40
    sortType = 1
    orderType = 1
    text_color = white
    while True:
        stagger = 0
        screen.blit(leaderboardBackground,(0,0))
        addBackdrop(330,400,250,75,75) #transluscent backdrop for scores
        addBackdrop(200,300,0,80,75)   #transluscent backdrop for sort by
        sorted_lb = leaderboard.getSortedList(sortType)
        if orderType == 1: a,b,c,count,change_count = 0,10,1,1,1
        elif orderType == 2: a,b,c,count,change_count = len(sorted_lb)-1,len(sorted_lb)-11,-1,len(sorted_lb),-1
        if orderType == 1 and sortType == 3: a,b,c,count,change_count = 0,10,1,len(sorted_lb),-1
        if orderType == 2 and sortType == 3: a,b,c,count,change_count = len(sorted_lb)-1,len(sorted_lb)-11,-1,1,1
        for i in range(a,b,c): 
            if orderType == 2 and sortType == 3:
                if count == 1: text_color = (255, 224, 51)
                elif count == 2: text_color = (166,166,166)
                elif count == 3: text_color = (204, 41, 0)
                else: text_color = white
            renderText((str(count)+") "+" ".join(sorted_lb[i])),25,text_color,size[0]-450,75+stagger)
            stagger+=stagger_distance
            count+=change_count
                
        pygame.display.update()
        clock.tick(16)
        new_sort_type = leaderBoardEvents(sortType,orderType)
        if new_sort_type == False: break
        elif new_sort_type == 5:
            orderType = 1
        elif new_sort_type == 6:
            orderType = 2
        else: sortType = new_sort_type

def showInstructions():
    x,y = 100,100
    addBackdrop(525,270,x,y,200)

    instructions_text = open('instructions.txt','r').readlines()
    stagger = 0
    for line in instructions_text:
        renderText(line.strip(),15,black,x+10,y+10+stagger)
        stagger+=30
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return

def settingsEvents():
    while True:
        back_txt = DisplaySettings()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            mx, my = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if toggleHighlightMoves.getWithin(mx,my):
                    toggleHighlightMoves.setSwitchStatus()
                elif toggleAIDifficulty.getWithin(mx,my):
                    if Game.getInGame() == False:
                        toggleAIDifficulty.setSwitchStatus()
                    else:
                        tkinterMessageBox(1,"Error","Cannot change this setting during a game.")
                elif togglePieceColor.getWithin(mx,my):
                    togglePieceColor.setSwitchStatus()
                elif toggleDiceAnimation.getWithin(mx,my):
                    toggleDiceAnimation.setSwitchStatus()
                elif toggle12Player.getWithin(mx,my):
                    if Game.getInGame() == False:
                        toggle12Player.setSwitchStatus()
                    else:
                        tkinterMessageBox(1,"Error","Cannot change this setting during a game.")
                elif back_txt.collidepoint(mx,my): return
                elif toggleAIPause.getWithin(mx,my):
                    toggleAIPause.setSwitchStatus()

def DisplaySettings():
    settings_text_color = white
    screen.blit(settingsBackground,(0,0))
    back_txt = renderText("Back",25,white,0,0)
    renderText(toggleHighlightMoves.getText(),20,settings_text_color,toggleHighlightMoves.getX(),toggleHighlightMoves.getY())
    screen.blit(toggleHighlightMoves.getImage(),(toggleHighlightMoves.getX(),toggleHighlightMoves.getY()))
    renderText(toggleAIDifficulty.getText(),20,settings_text_color,toggleAIDifficulty.getX(),toggleAIDifficulty.getY())
    screen.blit(toggleAIDifficulty.getImage(),(toggleAIDifficulty.getX(),toggleAIDifficulty.getY()))
    renderText(togglePieceColor.getText(),20,settings_text_color,togglePieceColor.getX(),togglePieceColor.getY())
    screen.blit(togglePieceColor.getImage(),(togglePieceColor.getX(),togglePieceColor.getY()))
    renderText(toggleDiceAnimation.getText(),20,settings_text_color,toggleDiceAnimation.getX(),toggleDiceAnimation.getY())
    screen.blit(toggleDiceAnimation.getImage(),(toggleDiceAnimation.getX(),toggleDiceAnimation.getY()))
    renderText(toggle12Player.getText(),20,settings_text_color,toggle12Player.getX(),toggle12Player.getY())    
    screen.blit(toggle12Player.getImage(),(toggle12Player.getX(),toggle12Player.getY()))
    renderText(toggleAIPause.getText(),20,settings_text_color,toggleAIPause.getX(),toggleAIPause.getY())    
    screen.blit(toggleAIPause.getImage(),(toggleAIPause.getX(),toggleAIPause.getY()))
    pygame.display.update()
    clock.tick(32)
    return back_txt

def menuEvents():
    DisplayMenuButtons()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        mx, my = pygame.mouse.get_pos()
        if new.getWithin(mx,my): new.setImage(newGameHoverImg)
        else: new.setImage(newGameImg)
        if load.getWithin(mx,my): load.setImage(loadGameHoverImg)
        else: load.setImage(loadGameImg)
        if Quit.getWithin(mx,my): Quit.setImage(quitHoverImg)
        else: Quit.setImage(quitImg)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if new.getWithin(mx,my): return 1
            elif load.getWithin(mx,my): return 2
            elif Quit.getWithin(mx,my): return 3
            elif leaderboardButton.getWithin(mx,my): leaderBoards()
            elif instructionsButtonMenu.getWithin(mx,my): showInstructions()
            elif settingsButtonMenu.getWithin(mx,my): settingsEvents()

def DisplayMenuButtons():
    screen.blit(new.getImage(),(new.getX(),new.getY()))
    screen.blit(load.getImage(),(load.getX(),load.getY()))
    screen.blit(Quit.getImage(),(Quit.getX(),Quit.getY()))
    screen.blit(leaderboardButton.getImage(),(leaderboardButton.getX(),leaderboardButton.getY()))
    screen.blit(instructionsButtonMenu.getImage(),(instructionsButtonMenu.getX(),instructionsButtonMenu.getY()))
    screen.blit(settingsButtonMenu.getImage(),(settingsButtonMenu.getX(),settingsButtonMenu.getY()))

def menuLoop():
    while True:
        screen.blit(menu_img,(0,0))
        option = menuEvents()
        if option == 1:
            return 'new'
        elif option == 2:
            return 'load'
        elif option == 3:
            pygame.quit()
            exit()
        pygame.display.update()

def getValidName(name):
    name_copy = name
    number_of_spaces = 0
    for i in name:
        if i == " ":
            number_of_spaces +=1
    if number_of_spaces == 1:
        name = name.split(" ")
        name = [x for x in name if x]
        if len(name) == 2:
            return True
        else:
            tkinterMessageBox(1,"Invalid Name","'{}' is an invalid name. Please insert a first and last name. Example: 'John Smith'".format(name_copy))
            return False
    else:
        tkinterMessageBox(1,"Invalid Name","'{}' is an invalid name. Please insert a first and last name. Example: 'John Smith'".format(name_copy))
        return False
    
def gameOverMenu(winner,score):
    winner_name = ""
    while True:
        screen.blit(gameOverBackground,(0,0))
        text = "{} Wins! Score {}".format(winner,score)
        renderText(text,30,white,220,150)
        renderText(winner_name,40,white,380,230)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                import keyboard_input
                letter = keyboard_input.getLetter(event.key)
                if letter!= None and letter!= True and letter!= False:
                    winner_name += letter
                elif letter == True:
                    valid_name = getValidName(winner_name)
                    if valid_name:
                        print("Valid")
                        return winner_name.split(" ")
                    else:
                        print("Invalid")
                        winner_name = ""
                elif letter == False:
                    length = len(winner_name)
                    winner_name = winner_name[:length-1]

#__________________________________________MAIN CODE_______________________________________________________#
if __name__ == "__main__":
    leaderboard = MyLeaderboard('{}//CSV//highscores.csv'.format(current_directory))
    Game = MyGame(PlayerColor,AIColor)
    undo = MyStack() #stack class for undoing
    screen,clock = initPygame()
    while True:
        initialise_type = menuLoop()
        Board = [[None for i in range(12)]for dimension in range(2)]
        Bar = MyBar()
        Dice = MyDice()
        initialiseBoard(initialise_type)
        winner,score = GameLoop(toggle12Player.getStatus(),toggleAIDifficulty.getStatus())
##        winner = Game.PlayerColor
##        score = 129
        winner_name = gameOverMenu(winner,score)
        leaderboard.appendScore(winner_name[0],winner_name[1],score)
