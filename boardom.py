## key:     0 - empty square       
##          p - pawn
##          r - rook
##          k - knight
##          b - bishop
##          q - queen
##          g - king
## lowercase letters denotes black piece, UPPERCASE LETTERS DENOTE WHITE

##Here: have a board map!
#    0    1    2    3    4    5    6    7
# 0['r', 'k', 'b', 'q', 'g', 'b', 'k', 'r']
# 1['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p']
# 2['0', '0', '0', '0', '0', '0', '0', '0']
# 3['0', '0', '0', '0', '0', '0', '0', '0']
# 4['0', '0', '0', '0', '0', '0', '0', '0']
# 5['0', '0', '0', '0', '0', '0', '0', '0']
# 6['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P']
# 7['R', 'K', 'B', 'Q', 'G', 'B', 'K', 'R']


##Current issues to fix:                           x=done, maybe | X=done, definitely
# [] General ugliness of code
# [] some edge cases may be ultra buggy
# [x] fix the main loop
# [x] MAKE THE MOVE-CHECKS COLOUR SENSITIVE SINCE YOU *ARE* ALLOWED TO TAKE THE PIECE'S SQUARE IF IT IS A DIFFERENT COLOUR!
#   ^current plan for this one is to make >all< the pieces return "as if" all pieces were opposite colour, ie. "takeable",
#   then shake it up with a function that "filters out" pieces of the same colour    
# [] inconsistency with "movebox" vs "attackbox", although that's tricky for pawn
# [x] they should all be returning, not printing like I did for the debugging
# [] fix checkcheck



#▒ welcome to boardom ▒#
print("▒ welcome to boardom ▒")

def refreshdisplay():
    global board
    board = [ [], [], [], [], [], [], [], [] ]
    for row in board:
        for number in range(8):
            row.append("0")

def whoseturn():
    if turn % 2 ==1:
        return "White"
    else:
        return "Black"

def oppositeturn():
    if turn%1 ==1:
        return "Black"
    else:
        return "White"

def display(pieces):
    refreshdisplay()
    for item in pieces:
        board[item.locy][item.locx]=item.getsym()
    count=0
    print("Turn "+str(turn)+": "+whoseturn()+"'s move")
    print("   0  1  2  3  4  5  6  7 ")
    for row in board:
        print(str(count)+" ["+"][".join(row)+"]")
        count+=1
    

##So it turns out the way I had everything set out with ""attackbox"" and ""movebox"" was just really stupid, I should have just made the pawn
##check more sophisticated, it'll be done. some time.

class piece():
    def __init__(self,colour,locx,locy):
        self.locx = locx
        self.locy = locy
        self.colour = colour

class pawn(piece):
    def getsym(self):
        if self.colour == "White":
            return "P"
        elif self.colour == "Black":
            return "p"
    def attackbox(self):
        response=[]
        if self.colour == "White":
            for item in pieces:
                if item.locx == self.locx+1 and item.locy == self.locy-1:
                    response.append((item.locx, item.locy))
                elif item.locx == self.locx-1 and item.locy == self.locy-1:
                    response.append((item.locx, item.locy))
        else:
            for item in pieces:
                if item.locx == self.locx+1 and item.locy == self.locy+1:
                    response.append((item.locx, item.locy))
                elif item.locx == self.locx-1 and item.locy == self.locy+1:
                    response.append((item.locx, item.locy))
        return response

    def movebox(self):
        response=[]
        if self.colour=="White":
            if self.locy == 7:
                return
            else:
                response.append((self.locx, self.locy-1))
                if turn == 1:
                    response.append((self.locx, self.locy-2))
                for item in pieces:
                    if item.locx == self.locx and item.locy == self.locy-1:
                        response.remove((self.locx, self.locy-1))
                    elif item.locx == self.locx+1 and item.locy == self.locy-1:
                        response.append((item.locx, item.locy))
                    elif item.locx == self.locx-1 and item.locy == self.locy-1:
                        response.append((item.locx, item.locy))
        elif self.colour=="Black": #really, this is just an `else` but yolo
            if self.locy==0:
                return
            else:
                response.append((self.locx, self.locy+1))
                if turn == 2:
                    response.append((self.locx, self.locy-2))
                for item in pieces:
                    if item.locx == self.locx and item.locy == self.locy+1:
                        response.remove((self.locx, self.locy+1))
                    elif item.locx == self.locx+1 and item.locy == self.locy+1:
                        response.append((item.locx, item.locy))
                    elif item.locx == self.locx-1 and item.locy == self.locy+1:
                        response.append((item.locx, item.locy))
        return response

class rook(piece):
    def getsym(self):
        if self.colour == "White":
            return "R"
        elif self.colour == "Black":
            return "r"
    def attackbox(self):
        return rookcheck(self)
    def movebox(self):
        return rookcheck(self)

def rookcheck(self):
    left=[] 
    right=[]
    up=[]
    down=[]
    for item in pieces:
        if item.locx == self.locx and self.locy - item.locy < 0:
            down.append(item)
        elif item.locx == self.locx and self.locy - item.locy > 0:
            up.append(item)               
        elif item.locy == self.locy and self.locx - item.locx < 0:
            right.append(item)
        elif item.locy == self.locy and self.locx - item.locx > 0:
            left.append(item)          
        else:
            pass
    templist = []
    for item in left:
        templist.append(item.locx)
    try:
        leftmost = min(templist)-1
    except:
        leftmost = -1
    templist = []
    for item in right:
        templist.append(item.locx)
    try:
        rightmost = max(templist)+1 #since we are expecting a negative number and we want the "least negative"
    except:
        rightmost = 8
    templist = []
    for item in up:
        templist.append(item.locy)
    try:
        upmost = min(templist)-1
    except:
        upmost = -1
    templist = []
    for item in down:
        templist.append(item.locy)
    try:
        downmost = max(templist)+1
    except:
        downmost = 8
    response=[]
    for number in range(0, self.locx-leftmost):
        if (self.locx-number, self.locy) != (self.locx, self.locy):
            response.append((self.locx-number, self.locy))
    for number in range(0, rightmost-self.locx):
        if (self.locx+number, self.locy) != (self.locx, self.locy):
            response.append((self.locx+number, self.locy))
    for number in range(0, self.locy-upmost):
        if (self.locx, self.locy-number) != (self.locx, self.locy):
            response.append((self.locx, self.locy-number))
    for number in range(0, downmost-self.locy):
        if (self.locx, self.locy+number) != (self.locx, self.locy):
            response.append((self.locx, self.locy+number))
    colourstrip(response, self)
    return response    

class knight(piece):
    def getsym(self):
        if self.colour == "White":
            return "K"
        elif self.colour == "Black":
            return "k"
    def movebox(self):
        response=[]
        if self.locx+2 in range(8) and self.locy+1 in range(8):
            response.append((self.locx+2, self.locy+1))
        if self.locx+2 in range(8) and self.locy-1 in range(8):
            response.append((self.locx+2, self.locy-1))
        if self.locx-2 in range(8) and self.locy+1 in range(8):
            response.append((self.locx-2, self.locy+1))
        if self.locx-2 in range(8) and self.locy-1 in range(8):
            response.append((self.locx-2, self.locy-1))
        if self.locx+1 in range(8) and self.locy+2 in range(8):
            response.append((self.locx+1, self.locy+2))
        if self.locx-1 in range(8) and self.locy+2 in range(8):
            response.append((self.locx-1, self.locy+2))
        if self.locx+1 in range(8) and self.locy-2 in range(8):
            response.append((self.locx+1, self.locy-2))
        if self.locx-1 in range(8) and self.locy-2 in range(8):
            response.append((self.locx-1, self.locy-2))
        colourstrip(response, self)
        return response
    def attackbox(self):
        return self.movebox()

class bishop(piece):
    def getsym(self):
        if self.colour == "White":
            return "B"
        if self.colour == "Black":
            return "b"
    def attackbox(self):
        return bishopcheck(self)
    def movebox(self):
        return bishopcheck(self)
        
def bishopcheck(self):
    ##1 is top-right, 2 is top-left, 3 is bottom-left, 4 is bottom-right (diagonals)
    one=[]
    two=[]
    three=[]
    four=[]
    for item in pieces:
        if (item.locx, item.locy) == (self.locx, self.locy):
            pass
        elif (item.locx - self.locx)**2 == (item.locy-self.locy)**2 :
            ##this checks if a piece is on the diagonal, now we want 'em sorted into the 4 quadrant groups.
            if item.locx-self.locx > 0:
                if item.locy-self.locy >0:
                    four.append((item.locx, item.locy))
                else: #item.locy-self.locy <0
                    one.append((item.locx, item.locy))
            else: #item.locx-self.locx<0
                if item.locy-self.locy >0:
                    three.append((item.locx, item.locy))
                else: #item.locy-self.locy <0
                    two.append((item.locx, item.locy))

##the bit that follows needs to be cleaned up despearately lolll, the if/elses aren't really that necessary and sorta repetitive, I just worked on each case at a time.
##later on I'll clean it up, right now, I just want something that works.
    response=[]
    if not one: ##if we look just at the 'one' diagonal, we will see that it's possible for it to be empty or full.
        confx, confy  = self.locx, self.locy
        tempx, tempy = confx, confy
        while tempx in range(0, 8) and tempy in range(0, 8): #since we are +1 at end, make it 6+1
            confx, confy = tempx, tempy
            tempx, tempy = tempx+1, tempy-1
            if (confx, confy) != (self.locx, self.locy):
                response.append((confx, confy))
    else:
        rr = min(one)
        confx, confy  = self.locx, self.locy
        tempx, tempy = confx, confy
        while tempx in range(rr[0]+1) or tempy in range(rr[1], 7-rr[1]+1): #since we are +1 at end, make it 6+1
            confx, confy = tempx, tempy
            tempx, tempy = tempx+1, tempy-1
            if (confx, confy) != (self.locx, self.locy):
                response.append((confx, confy))
    if not two: 
        confx, confy  = self.locx, self.locy
        tempx, tempy = confx, confy
        while tempx in range(0, 8) and tempy in range(0, 8):
            confx, confy = tempx, tempy
            tempx, tempy = tempx-1, tempy-1
            if (confx, confy) != (self.locx, self.locy):
                response.append((confx, confy))
    else:
        rr = max(two)
        confx, confy  = self.locx, self.locy
        tempx, tempy = confx, confy
        while tempx in range(rr[0], 7-rr[0]+1) or tempy in range(rr[1], 7-rr[1]+1):
            confx, confy = tempx, tempy
            tempx, tempy = tempx-1, tempy-1
            if (confx, confy) != (self.locx, self.locy):
                response.append((confx, confy))
    if not three: 
        confx, confy  = self.locx, self.locy
        tempx, tempy = confx, confy
        while tempx in range(0, 8) and tempy in range(0, 8):
            confx, confy = tempx, tempy
            tempx, tempy = tempx-1, tempy+1
            if (confx, confy) != (self.locx, self.locy):
                response.append((confx, confy))
    else:
        rr = max(three)
        confx, confy  = self.locx, self.locy
        tempx, tempy = confx, confy
        while tempx in range(rr[0], 7-rr[0]+1) or tempy in range(rr[1]+1):
            confx, confy = tempx, tempy
            tempx, tempy = tempx-1, tempy+1
            if (confx, confy) != (self.locx, self.locy):
                response.append((confx, confy))
    if not four: 
        confx, confy  = self.locx, self.locy
        tempx, tempy = confx, confy
        while tempx in range(0, 8) and tempy in range(0, 8):
            confx, confy = tempx, tempy
            tempx, tempy = tempx+1, tempy+1
            if (confx, confy) != (self.locx, self.locy):
                response.append((confx, confy))
    else:
        rr = min(four)
        confx, confy  = self.locx, self.locy
        tempx, tempy = confx, confy
        while tempx in range(rr[0]+1) or tempy in range(rr[1]+1):
            confx, confy = tempx, tempy
            tempx, tempy = tempx+1, tempy+1
            if (confx, confy) != (self.locx, self.locy):
                response.append((confx, confy))    
    colourstrip(response, self)        
    return response

class queen(piece):
    def getsym(self):
        if self.colour == "White":
            return "Q"
        if self.colour == "Black":
            return "q"
    def attackbox(self):
        response = []
        for item in rookcheck(self):
            response.append(item)
        for item in bishopcheck(self):
            response.append(item)
        colourstrip(response, self)
        return response

class king(piece):
    def getsym(self):
        if self.colour == "White":
            return "G"
        if self.colour == "Black":
            return "g"
    def movebox(self):
        response = self.attackbox()
        
    def attackbox(self):
        response = []
        for x in range(-1, 2):
            for y in range (-1, 2):
                if x == 0 and y == 0:
                    #print("non-valide")
                    #print(x)
                    #print(y)
                    pass
                elif self.locx+x > 7 or self.locx+x < 0 or self.locy+y >7  or self.locy+y <0:
                    pass
                    #print("non-valid")
                    #print((self.locx+x, self.locy+y))
                    #print((self.locx+x, self.locy+y))
                else:
                    response.append((self.locx+x, self.locy+y))
                    #print("nice")
                    #print(x)
                    #print(y)
        for item in pieces:
            for thing in response:
                if (item.locx, item.locy) == thing:
                    response.remove(thing)
        colourstrip(response, self)
        return response


def checkcheck(pieces, kingcolour): #is the king of colour kingcolour in check?
    attackboxes=[]
    for piece in pieces:
        if piece.colour != kingcolour:
            g = piece.attackbox()
            if g:
                for p in g:
                    attackboxes.append(p)
        elif piece.getsym().lower() == "g":
            kingloc = (piece.locx, piece.locy)
    if kingloc in attackboxes:
        return True
    else:
        return False
    #return fullresponse  #compare King-of-opposite-colour's location to this



def colourstrip(response, piece): #this function sucks.
    for item in pieces:
        #print(response)
        if item.colour == piece.colour and (item.locx, item.locy) in list(response):
            response.remove((item.locx, item.locy))
    return response

turn=1

pieces=[]

pieces.append(pawn("White", 1, 2))

pieces.append(king("White", 2, 2))

pieces.append(knight("White", 2, 6))

pieces.append(pawn("Black", 2, 1))

pieces.append(knight("Black", 3, 4))

pieces.append(bishop("White", 1, 4))

#print(checkcheck(pieces, "White"))


def reset():
    global turn, pieces
    turn=1
    pieces = []
    for number in range(8):
        pieces.append(pawn("White", number, 6))
        pieces.append(pawn("Black", number, 1))
    pieces.append(rook("White", 0, 7))
    pieces.append(rook("White", 7, 7))
    pieces.append(knight("White", 1, 7))
    pieces.append(knight("White", 6, 7))
    pieces.append(bishop("White", 2, 7))
    pieces.append(bishop("White", 5, 7))
    pieces.append(queen("White", 3, 7))
    pieces.append(king("White", 4, 7))
    pieces.append(rook("Black", 0, 0))
    pieces.append(rook("Black", 7, 0))
    pieces.append(knight("Black", 1, 0))
    pieces.append(knight("Black", 6, 0))
    pieces.append(bishop("Black", 2, 0))
    pieces.append(bishop("Black", 5, 0))
    pieces.append(queen("Black", 3, 0))
    pieces.append(king("Black", 4, 0))

reset()

def mainloop():
    global turn
    display(pieces)
    starting, ending = getmove()
    moveflag = confirmmove(starting, ending) #confirmmove returns True or False, but also prints what went wrong if False.
    if moveflag == True:
        executemove(starting, ending)
        checkcheck(pieces, oppositeturn()) #opposite context to the one within confirmmove
        turn=turn+1
    else:
        print("Input unsuccessful, refreshing turn")


def getmove():
    start = input("Which piece do you want to move? Use co-ordinate notation (x, y) \n")
    end = input("Where do you want to move it? Co-ordinate notation again please. \n")
    return start, end

def confirmmove(start, end): #we want to find the piece with the starting co-ords and call movebox on it. Then we check if movebox matches the end-coords suggested. Then we call checkcheck.
    flag=False
    for piece in pieces:
        if str((piece.locx, piece.locy)) == start and piece.colour == whoseturn(): #if there's a piece there ur allowed to control
            #print("this bit works")
            try:
                for item in piece.movebox():
                    if str(item) == end:
                        print("Valid move!")
                        flag=True
                    #we also need to check if the player put their own king in check, but this is sorta hard since the executemove hasn't happened yet. maybe a "fakepieces"
                    #then we're good to go!
                    else:
                        error = "You can't move there."
            except:
                error = "It seems the piece you chose is unable to move."
        else:
            error = "Hmm, I don't think that's a piece you're allowed to move."

    if flag==False:
        print("Something went wrong, try again -"+ error)  #maybe add more helpful error codes later
    return flag
    
def executemove(start, end):
#we want to remove anything in the `end` position and then change the loc values of the piece in `start` to be `end` 
    for item in pieces:
        if str((item.locx, item.locy)) == end:
            pieces.remove(item)

        elif str((item.locx, item.locy)) == start:
            item.locx = int(end[1])
            item.locy = int(end[4])

while True:
    mainloop()
