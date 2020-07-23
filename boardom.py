##Current issues to fix:                           x=done, maybe | X=done, definitely
# [] General ugliness of code (make it readable)
# [] Ugly code part 2 (make it efficient)
# [] some edge cases may be ultra buggy
# [x] pawn promotion
# [x] castling
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
for number in range(8):
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
        board[item.locy][item.locx] = item.sym
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
    def __init__(self, locx, locy, colour):
        self.locx = locx
        self.locy = locy
        self.colour = colour


class Pawn(Piece):
    def __init__(self, locx, locy, colour):
        super().__init__(locx, locy, colour)
        self.sym = "P" if self.colour == "White" else "p"

    def attackbox(self):
        response = []
        if self.colour == "White":
            #if self.locy == 0:
            for item in pieces:
                if (item.locx, item.locy) == (self.locx+1, self.locy-1):
                    response.append((item.locx, item.locy))
                elif (item.locx, item.locy) == (self.locx-1, self.locy-1):
                    response.append((item.locx, item.locy))
        else:
            for item in pieces:
                if item.locx == self.locx+1 and item.locy == self.locy+1:
                    response.append((item.locx, item.locy))
                elif item.locx == self.locx-1 and item.locy == self.locy+1:
                    response.append((item.locx, item.locy))
        return response

    def movebox(self): #this could definitely be cleaned up to not have so much White/Black distinction
        response = []
        if self.colour == "White":
            if self.locy == 0:
                pass
            else:
                response.append((self.locx, self.locy-1))
                if self.locy == 6:
                    response.append((self.locx, self.locy-2))
                for item in pieces:
                    if (item.locx, item.locy) == (self.locx, self.locy-1):
                        response.remove((self.locx, self.locy-1))
                    elif (item.locx, item.locy) == (self.locx+1, self.locy-1):
                        response.append((item.locx, item.locy))
                    elif (item.locx, item.locy) == (self.locx-1, self.locy-1):
                        response.append((item.locx, item.locy))
        else:
            if self.locy == 7:
                pass
            else:
                response.append((self.locx, self.locy+1))
                if self.locy == 1:
                    response.append((self.locx, self.locy+2))
                for item in pieces:
                    if (item.locx, item.locy) == (self.locx, self.locy+1):
                        response.remove((self.locx, self.locy+1))
                    elif (item.locx, item.locy) == (self.locx+1, self.locy+1):
                        response.append((item.locx, item.locy))
                    elif (item.locx, item.locy) == (self.locx-1, self.locy+1):
                        response.append((item.locx, item.locy))
        return response

def pawnpromotion(): #does it need to be colour specific? idk
    for item in pieces:
        if (item.locy == 0 and item.sym == "P") or (item.locy == 7 and item.sym == "p"):
            pawnloc = (item.locx, item.locy)
            print("Congrats, your pawn has made it to the final row")
            newpiece = input("Should it be promoted to Queen, Rook, Knight or Bishop? ")
            if newpiece.lower() == "queen": pieces.append(Queen(item.locx, item.locy, item.colour))
            if newpiece.lower() == "rook": pieces.append(Rook(item.locx, item.locy, item.colour))
            if newpiece.lower() == "knight": pieces.append(Knight(item.locx, item.locy, item.colour))
            if newpiece.lower() == "bishop": pieces.append(Bishop(item.locx, item.locy, item.colour))

            for item in pieces:
                if (item.locx, item.locy) == pawnloc and item.sym.lower() == "p":
                    pieces.remove(item)

class Rook(Piece):
    def __init__(self, locx, locy, colour):
        super().__init__(locx, locy, colour)
        self.sym = "R" if self.colour == "White" else "r"    

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
    leftmost = getclosestpiecerook(left, "locx", -1)
    rightmost = getclosestpiecerook(right, "locx", 8)
    upmost = getclosestpiecerook(up, "locy", -1)
    downmost = getclosestpiecerook(down, "locy", 8)
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

def getclosestpiecerook(selection, orientation, polarity):  # selection is list, orientation is locx or locy?
    templist = []                                       # polarity is positive or negative relative to current loc
    response = polarity                                 # (closer to 8? or closer to -1?)
    if polarity == 8 or polarity == -1:                                
        if selection:
            for item in selection:                           
                if orientation == "locx": 
                    templist.append(item.locx)
                if orientation == "locy": 
                    templist.append(item.locy)
            response = min(templist)+1 if polarity == 8 else max(templist)-1
    return response

class Knight(Piece):
    def __init__(self, locx, locy, colour):
        super().__init__(locx, locy, colour)
        self.sym = "K" if self.colour == "White" else "k"

    def movebox(self):
        response = []
        #we're simply looping every possible L-move and checking if it's on the board
        xmod, ymod = 2, 1
        for i in range(9): 
            if self.locx+xmod in range(8) and self.locy+ymod in range(8):
                response.append((self.locx+xmod, self.locy+ymod))
            
            ymod = ymod*(-1)
            if i % 4 == 1: xmod = xmod*(-1)
            if i == 3: xmod, ymod = 1, 2
            
        colourstrip(response, self)
        return response

    def attackbox(self):
        return self.movebox()

class Bishop(Piece):
    def __init__(self, locx, locy, colour):
        super().__init__(locx, locy, colour)
        self.sym = "B" if self.colour == "White" else "b"

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
        elif (item.locx - self.locx)**2 == (item.locy - self.locy)**2:
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

#we churn down each of the two diagonals, from st->eb and from sb->et, given piece's context

#st-"start-top", sb-"end-top", et-"end-top", eb-"end-bottom"

    if two: 
        st = max(two)
    else:
        st = ((self.locx-self.locy), 0) if self.locx > self.locy else (0, (self.locy-self.locx))

    if three:
        sb = max(three)
    else:
        sb = (0, (self.locx+self.locy)) if self.locx+self.locy <= 7 else ((self.locx+self.locy-7), 7)
    

    et = min(one) if one else "nil"
    eb = min(four) if four else "nil"

    response = []
    for item in findpiecesbishop(st,eb, 1, (self.locx, self.locy)):
        response.append(item)
    for item in findpiecesbishop(sb,et, -1, (self.locx, self.locy)):
        response.append(item)

    colourstrip(response, self)
    return response

#basically how this func works is we start at the leftmost piece <or empty square> (startpos) 
#and we loop all the way up/down to the rightmost (endpos), epic style. of course, this can 
#either be swooping from (1) top to bottom, or from (2)bottom to top 

def findpiecesbishop(startpos, endpos, orientation, currentpos): #orientation = 1 means top to bottom, -1 = bottom to top
    response = []
    loopos = startpos
    while True:
        if loopos != currentpos: #we don't want the piece to move to its own position!
            response.append(loopos)
        if loopos == endpos or loopos[0] not in range(8) or loopos[1] not in range(8):
            return response #do I need to break??

        loopos = (loopos[0]+1, loopos[1]+orientation)


class Queen(Piece):
    def __init__(self, locx, locy, colour):
        super().__init__(locx, locy, colour)
        self.sym = "Q" if self.colour == "White" else "q"

    def attackbox(self):
        response = []
        for item in rookcheck(self):
            response.append(item)
        for item in bishopcheck(self):
            response.append(item)
        colourstrip(response, self)
        return response

    def movebox(self):
        return self.attackbox()

class King(Piece):
    def __init__(self, locx, locy, colour):
        super().__init__(locx, locy, colour)
        self.sym = "G" if self.colour == "White" else "g"

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
        elif piece.sym.lower() == "g":
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

CASTLEDATA = {"White0":True, "White7":True, "Black0":True, "Black7":True}

def checkcastle(colour, side): #set side up as 0-side or 7-side. kinginit is where king was
    success = False
    if CASTLEDATA[colour+side] == True:  #king goes to 6 or 1, rook 5 or 2
        #if checkcheck(pieces, colour) == False:
        kingspot = 6 if side == "7" else 1
        rookspot = 5 if side == "7" else 2

        if colour == "White": #rookspot, kingspot are where we're moving things
            rookspot = (rookspot, 7)
            kingspot = (kingspot, 7)
        else:
            rookspot = (rookspot, 0)
            kingspot = (kingspot, 0)
        for piece in pieces:
            if piece.sym == Rook(0, 0, colour).sym and (piece.locx, piece.locy) == (int(side), rookspot[1]):
                if rookspot in piece.movebox() and kingspot in piece.movebox(): #valid since the rook acts like a "sweeper" for movecheck
                    pieces.remove(piece)
                    for piece in pieces:
                        if (piece.locx, piece.locy) == (4, kingspot[1]):
                            pieces.remove(piece)
                            success = True
                            break

    if success:
            pieces.append(Rook(rookspot[0], rookspot[1], whoseturn("normal")))
            pieces.append(King(kingspot[0], kingspot[1], whoseturn("normal")))
            CASTLEDATA[colour+"0"], CASTLEDATA[colour+"7"] = False, False
            return True
    else:
        print("Invalid attempt to castle.")
        return False
    
    


def reset():
    global turn, pieces

    turn=1
    pieces = []
    for number in range(8):
        pieces.append(Pawn(number, 6, "White"))
        pieces.append(Pawn(number, 1, "Black"))

    row, colour = 0, "Black"
    while row < 8:
        pieces.append(Rook(0, row, colour))
        pieces.append(Rook(7, row, colour))
        pieces.append(Knight(1, row, colour))
        pieces.append(Knight(6, row, colour))
        pieces.append(Bishop(2, row, colour))
        pieces.append(Bishop(5, row, colour))
        pieces.append(Queen(3, row, colour))
        pieces.append(King(4, row, colour))
        row, colour = row+7, "White"

reset()

def mainloop():
    global turn
    cache=None
    display(pieces)
    starting, ending = getmove()
    moveflag = confirmmove(starting, ending)
    if moveflag == "normal":
        cache = executemove(starting, ending)
        if checkcheck(pieces, whoseturn("normal")):
            print("But this would put your own king in check! Refreshing turn")
            executemove(ending, starting)
            if cache:
                pieces.append(cache)
        else:
            if checkcheck(pieces, whoseturn("reverse")):
                print("Check!") #opposite context to the one within confirmmove
            pawnpromotion()
            turn=turn+1
    elif moveflag == "castle":
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
                try:
                    if piece.sym == King(1, 1, whoseturn("normal")).sym and checkcheck(pieces, whoseturn("normal")) == False:
                        if (piece.locx, piece.locy) == start:
                            if end[0] == 1:
                                #checkcastle(whoseturn("normal"), "0")
                                flag = "castle" if checkcastle(whoseturn("normal"), "0") else False
                            elif end[0] == 6:
                                #checkcastle(whoseturn("normal"), "7")
                                flag = "castle" if checkcastle(whoseturn("normal"), "7") else False
                except:
                    print("Failure of castling")
                for item in piece.movebox():
                    if item == end:
                        flag="normal"
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
            if item.sym.lower() == "g":
                CASTLEDATA[item.colour+"0"], CASTLEDATA[item.colour+"7"] = False, False
            elif item.sym.lower() == "r" and (item.locx == "7" or "0"):
                CASTLEDATA[item.colour+str(item.locx)] = False
            item.locx = end[0]
            item.locy = end[1]
    return cache

while True:
    mainloop()
