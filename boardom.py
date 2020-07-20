##Current issues to fix:                           x=done, maybe | X=done, definitely
# [] General ugliness of code (make it readable)
# [] Ugly code part 2 (make it efficient)
# [] some edge cases may be ultra buggy
# [] pawn promotion and castling
# am considering making all the global terms IN ALL CAPS now that I have more knowledge, should 
# help making things clearer to understand


#▒ welcome to boardom ▒#
#This is a chess engine implemented in python without using `import` statements. It is a
#project for me cut my teeth on, as it were. My goal is to start learning C, and learning
#it well, which is a daunting task - so if this script goes well, it'll be my little
#farewell to beginner's python. And it'll help me to claim that I finished what I started!


print("▒ welcome to boardom ▒")


##this part sets up the dictionary and function to allow for A1 as input, instead of (0,0)
coordict = {
}

letters = "ABCDEFGH"
for number in range(7):
    coordict.update(dict.fromkeys([letters[number], str(number+1)], number))

def coordtrans(thing):
    x = coordict[thing[0]] #is the letter
    y = coordict[thing[1]] #is the number
    return (x, y)


##this part allows you to control the display and check whose turn it is
def refreshdisplay():
    global board
    board = [ [], [], [], [], [], [], [], [] ]
    for row in board:
        for number in range(8):
            row.append("0")

def display(pieces):
    refreshdisplay()
    for item in pieces:
        board[item.locy][item.locx] = item.getsym()
    count = 1
    print("Turn "+str(turn)+": "+whoseturn("normal")+"'s move \n")
    print("   A  B  C  D  E  F  G  H ")
    for row in board:
        print(str(count)+" ["+"][".join(row)+"]")
        count+=1
    print("\n")

def whoseturn(state):
    modturn = turn+1 if state == "reverse" else turn #we want to modify the turn to reverse the outcome if necessary
    player = "White" if modturn % 2 == 1 else "Black" #self-explanatory
    return player



##set up the piece classes. (locx, locy) is the current position.
##attackbox refers to what squares the piece is "threatening" and movebox is where it can go -
##pawns are the reason this distinction has been made.
class Piece():
    def __init__(self, colour, locx, locy):
        self.locx = locx
        self.locy = locy
        self.colour = colour


class Pawn(Piece):
    def getsym(self):
        if self.colour == "White":
            return "P"
        elif self.colour == "Black":
            return "p"

    def attackbox(self):
        response = []
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
        response = []
        if self.colour == "White":
            if self.locy == 7:
                return #code for promotion is inserted here????? maybe??? i dunno
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
        else:
            if self.locy == 0:
                return
            else:
                response.append((self.locx, self.locy+1))
                if turn == 2:
                    response.append((self.locx, self.locy+2))
                for item in pieces:
                    if item.locx == self.locx and item.locy == self.locy+1:
                        response.remove((self.locx, self.locy+1))
                    elif item.locx == self.locx+1 and item.locy == self.locy+1:
                        response.append((item.locx, item.locy))
                    elif item.locx == self.locx-1 and item.locy == self.locy+1:
                        response.append((item.locx, item.locy))
        return response

class Rook(Piece):
    def getsym(self):
        if self.colour == "White":
            return "R"
        elif self.colour == "Black":
            return "r"

    def attackbox(self):
        return rookcheck(self)

    def movebox(self):
        return rookcheck(self)

def rookcheck(self): #rook and bishop still suck, the functions that is
    left = [] 
    right = [] # <= turn these 4 into one dict
    up = []
    down = []
    for item in pieces:
        if item.locx == self.locx and self.locy - item.locy < 0:
            down.append(item)
        elif item.locx == self.locx and self.locy - item.locy > 0:
            up.append(item)
        elif item.locy == self.locy and self.locx - item.locx < 0:
            right.append(item)
        elif item.locy == self.locy and self.locx - item.locx > 0:
            left.append(item)
    leftmost = getclosestpiece(left, "locx", -1)
    rightmost = getclosestpiece(right, "locx", 8)
    upmost = getclosestpiece(up, "locy", -1)
    downmost = getclosestpiece(down, "locy", 8)
    response = []
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

def getclosestpiece(selection, orientation, polarity):  # selection is list, orientation is locx or locy?
    templist = []                                       # polarity is positive or negative relative to current loc
    response = polarity                                 # (closer to 8? or closer to -1?)
    if polarity == 8 or polarity == -1:                                
        if selection:
            for item in selection:                              
                if orientation == "locx": templist.append(item.locx)
                if orientation == "locy": templist.append(item.locy)

            response = max(templist)+1 if polarity == 8 else min(templist)-1

    return response

class Knight(Piece):
    def getsym(self):
        if self.colour == "White":
            return "K"
        elif self.colour == "Black":
            return "k"

    def movebox(self):
        response = []
        #we're simply looping every possible L-move and checking if it's on the board
        xmod, ymod = 2, 1
        for i in range(9): 
            if self.locx+xmod in range(8) and self.locy+ymod in range(8):
                response.append((self.locx+xmod, self.locy+ymod))
            
            ymod = ymod*(-1)
            if i % 4 == 1:
                xmod = xmod*(-1)
            if i == 3:
                xmod, ymod = 1, 2
            
        colourstrip(response, self)
        return response

    def attackbox(self):
        return self.movebox()

class Bishop(Piece):
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
    # 1 is top-right, 2 is top-left, 3 is bottom-left, 4 is bottom-right
    # (diagonals)
    one = []
    two = []
    three = []
    four = []
    for item in pieces:
        if (item.locx, item.locy) == (self.locx, self.locy):
            pass
        elif (item.locx - self.locx)**2 == (item.locy-self.locy)**2:
            # this checks if a piece is on the diagonal, now we want 'em sorted
            # into the 4 quadrant groups.
            if item.locx-self.locx > 0:
                if item.locy-self.locy > 0:
                    four.append((item.locx, item.locy))
                else:  # item.locy-self.locy <0
                    one.append((item.locx, item.locy))
            else:  # item.locx-self.locx<0
                if item.locy-self.locy > 0:
                    three.append((item.locx, item.locy))
                else:  # item.locy-self.locy <0
                    two.append((item.locx, item.locy))

##the bit that follows needs to be cleaned up despearately lolll
##later on I'll clean it up, right now, I just want something that works.
    response = []
    if not one: ##if we look just at the 'one' diagonal, we will see that it's possible for it to be empty or full.
        confx, confy  = self.locx, self.locy
        tempx, tempy = confx, confy
        while tempx in range(0, 8) and tempy in range(0, 8):  # since we are +1
            # at end, make it 6+1
            confx, confy = tempx, tempy
            tempx, tempy = tempx+1, tempy-1
            if (confx, confy) != (self.locx, self.locy):
                response.append((confx, confy))
    else:
        rr = min(one)
        confx, confy = self.locx, self.locy
        tempx, tempy = confx, confy
        while tempx in range(rr[0]+1) or tempy in range(rr[1], 7-rr[1]+1):
            # since we are +1 at end, make it 6+1
            confx, confy = tempx, tempy
            tempx, tempy = tempx+1, tempy-1
            if (confx, confy) != (self.locx, self.locy):
                response.append((confx, confy))
    if not two:
        confx, confy = self.locx, self.locy
        tempx, tempy = confx, confy
        while tempx in range(0, 8) and tempy in range(0, 8):
            confx, confy = tempx, tempy
            tempx, tempy = tempx-1, tempy-1
            if (confx, confy) != (self.locx, self.locy):
                response.append((confx, confy))
    else:
        rr = max(two)
        confx, confy = self.locx, self.locy
        tempx, tempy = confx, confy
        while tempx in range(rr[0], 7-rr[0]+1) or tempy in range(rr[1],
                                                                 7-rr[1] + 1):
            confx, confy = tempx, tempy
            tempx, tempy = tempx-1, tempy-1
            if (confx, confy) != (self.locx, self.locy):
                response.append((confx, confy))
    if not three:
        confx, confy = self.locx, self.locy
        tempx, tempy = confx, confy
        while tempx in range(0, 8) and tempy in range(0, 8):
            confx, confy = tempx, tempy
            tempx, tempy = tempx-1, tempy+1
            if (confx, confy) != (self.locx, self.locy):
                response.append((confx, confy))
    else:
        rr = max(three)
        confx, confy = self.locx, self.locy
        tempx, tempy = confx, confy
        while tempx in range(rr[0], 7-rr[0]+1) or tempy in range(rr[1]+1):
            confx, confy = tempx, tempy
            tempx, tempy = tempx-1, tempy+1
            if (confx, confy) != (self.locx, self.locy):
                response.append((confx, confy))
    if not four:
        confx, confy = self.locx, self.locy
        tempx, tempy = confx, confy
        while tempx in range(0, 8) and tempy in range(0, 8):
            confx, confy = tempx, tempy
            tempx, tempy = tempx+1, tempy+1
            if (confx, confy) != (self.locx, self.locy):
                response.append((confx, confy))
    else:
        rr = min(four)
        confx, confy = self.locx, self.locy
        tempx, tempy = confx, confy
        while tempx in range(rr[0]+1) or tempy in range(rr[1]+1):
            confx, confy = tempx, tempy
            tempx, tempy = tempx+1, tempy+1
            if (confx, confy) != (self.locx, self.locy):
                response.append((confx, confy))    
    colourstrip(response, self)        
    return response

class Queen(Piece):
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
    def movebox(self):
        return attackbox(self)

class King(Piece):
    def getsym(self):
        if self.colour == "White":
            return "G"
        if self.colour == "Black":
            return "g"

    def movebox(self):
        response = self.attackbox()
        return response
        
    def attackbox(self): ##this all needs to be fixed, it looks shonky
        response = []
        for x in range(-1, 2):
            for y in range (-1, 2):
                if self.locx+x > 7 or self.locx+x < 0 or self.locy+y >7  or self.locy+y <0 or (x==0 and y ==0):
                    pass
                else:
                    response.append((self.locx+x, self.locy+y))
        colourstrip(response, self)
        return response

def checkcheck(listing, kingcolour): #is the king of colour kingcolour in check?
    attackboxes=[]
    for piece in listing:
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

def colourstrip(response, piece): #you can't capture your own piece!
    for item in pieces:
        if item.colour == piece.colour and (item.locx, item.locy) in list(response):
            response.remove((item.locx, item.locy))
    return response

  
  
##scenario testing for debugging here

turn=1

pieces=[]

pieces.append(Rook("White", 1, 2))

pieces.append(Rook("White", 2, 2))

pieces.append(Rook("White", 2, 6))

pieces.append(Rook("Black", 2, 1))

pieces.append(Rook("Black", 5, 5))

pieces.append(King("White", 1, 4))

pieces.append(King("Black", 0, 0))

print(pieces[2].attackbox())
##end scenario testing


def reset():
    global turn, pieces

    turn=1
    pieces = []
    for number in range(8):
        pieces.append(Pawn("White", number, 6))
        pieces.append(Pawn("Black", number, 1))

    row, colour = 0, "Black"
    while row < 8:
        pieces.append(Rook(colour, 0, row))
        pieces.append(Rook(colour, 7, row))
        pieces.append(Knight(colour, 1, row))
        pieces.append(Knight(colour, 6, row))
        pieces.append(Bishop(colour, 2, row))
        pieces.append(Bishop(colour, 5, row))
        pieces.append(Queen(colour, 3, row))
        pieces.append(King(colour, 4, row))
        row, colour = row+7, "White"

reset()


def mainloop():
    global turn
    cache=None
    display(pieces)
    starting, ending = getmove()
    moveflag = confirmmove(starting, ending)
    if moveflag == True:
        cache = executemove(starting, ending)
        if checkcheck(pieces, whoseturn("normal")):
            print("But this would put your own king in check! Refreshing turn")
            executemove(ending, starting)
            if cache:
                pieces.append(cache)
        else:
            if checkcheck(pieces, whoseturn("reverse")):
                print("Check!") #opposite context to the one within confirmmove
            turn=turn+1
    else:
        print("Input unsuccessful, refreshing turn...")

def getmove():
    start = input("Which piece do you want to move? Use notation E7 \n")
    end = input("Where do you want to move it? Same notation again please. \n")
    start = coordtrans(start)
    end = coordtrans(end)
    return start, end

def confirmmove(start, end): #we want to find the piece with the starting co-ords and call movebox on it. Then we check if movebox matches the end-coords suggested. Then we call checkcheck.
    flag=False
    error = "Hmm, I don't think that's a piece you're allowed to move."
    for piece in pieces:
        if (piece.locx, piece.locy) == start and piece.colour == whoseturn("normal"): #if there's a piece there ur allowed to control
            try:
                for item in piece.movebox():
                    if item == end:
                        flag=True
                    #we also need to check if the player put their own king in check, but this is sorta hard since the executemove hasn't happened yet. maybe a "fakepieces"
                    else:
                        error = "You can't move there."
            except:
                error="Looks like that piece has no-where to move"
    if flag==False:
        print("Something went wrong, try again - "+ error)
    return flag

def executemove(start, end):
#we want to remove anything in the `end` position and then change the loc values of the piece in `start` to be `end` 
    cache=None
    for item in pieces:
        if (item.locx, item.locy) == end:
            pieces.remove(item)
            cache = item
        elif (item.locx, item.locy) == start:
            item.locx = end[0]
            item.locy = end[1]
    return cache

def debug(group):
    for item in group:
        print((item.locx, item.locy))

while True:
    mainloop()
