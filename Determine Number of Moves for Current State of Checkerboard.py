#function definition to shift the location of different pieces on the board
def setPositionsOnBoard(row, column, checkerMoved, currentBoard):
    #ensure the position number would actually fit on the board
    if (row < 1 or row > 8):
        raise Exception("Row number is out-of-bounds")
    if (column < 1 or column > 8):
        raise Exception("Column number is out-of-bounds")
        
    #actually place the checker on the board; convert inputted row and column # into indexes
    currentBoard[row - 1][column - 1] = checkerMoved

#function definition to recursively calculate the number of valid jumps on the current turn
def calculateValidJumps(row, column, currentBoard):
    #initialize all variables
    validJumpsSoFar = 0
    rowBeingEnteredByPlayer = 0
    validColumnsBeingEnteredByPlayer = [0 for x in range(2)]
    
    #determine what squares the player's checker could enter if moving normally
    rowBeingEnteredByPlayer = row + 1
    validColumnsBeingEnteredByPlayer[0] = column - 1
    validColumnsBeingEnteredByPlayer[1] = column + 1
    
    #start checking whether certain moves are valid
    #check whether a move to the left would go off of the board
    if (not (validColumnsBeingEnteredByPlayer[0] < 0 or rowBeingEnteredByPlayer > 7)):
        #if there is an opponent checker on the left square
        if (currentBoard[rowBeingEnteredByPlayer][validColumnsBeingEnteredByPlayer[0]] == "opponent"):
            #check whether jump would go off of the board
            if (not ((validColumnsBeingEnteredByPlayer[0] - 1) < 0 or (rowBeingEnteredByPlayer + 1) > 7)):
                #check whether there is a checker in the jumping spot
                if (currentBoard[rowBeingEnteredByPlayer + 1][validColumnsBeingEnteredByPlayer[0] - 1] != "opponent"):
                    #increment the number of valid jumps
                    validJumpsSoFar += 1
                    #recursively check whether there are more valid jumps from new location due to multi-jump rule
                    validJumpsSoFar += calculateValidJumps(rowBeingEnteredByPlayer + 1, validColumnsBeingEnteredByPlayer[0] - 1, currentBoard)
    
    #check whether a move to the right would go off of the board
    if (not (validColumnsBeingEnteredByPlayer[1] > 7 or rowBeingEnteredByPlayer > 7)):
        #if there is an opponent checker on the left square
        if (currentBoard[rowBeingEnteredByPlayer][validColumnsBeingEnteredByPlayer[1]] == "opponent"):
            #check whether jump would go off of the board
            if (not ((validColumnsBeingEnteredByPlayer[1] + 1) > 7 or (rowBeingEnteredByPlayer + 1) > 7)):
                #check whether there is a checker in the jumping spot
                if (currentBoard[rowBeingEnteredByPlayer + 1][validColumnsBeingEnteredByPlayer[1] + 1] != "opponent"):
                    #increment the number of valid jumps
                    validJumpsSoFar += 1
                    #recursively check whether there are more valid jumps from new location due to multi-jump rule
                    validJumpsSoFar += calculateValidJumps(rowBeingEnteredByPlayer + 1, validColumnsBeingEnteredByPlayer[1] + 1, currentBoard)
                       
    return validJumpsSoFar

#function definition to recursively determine whether a checker will jump into opponent's home row since Python doesn't have reference variables
def shouldBeKing(row, column, currentBoard, isKing):
    #initialize all variables
    rowBeingEnteredByPlayer = 0
    validColumnsBeingEnteredByPlayer = [0 for x in range(2)]
    
    #determine what squares the player's checker could enter if moving normally
    rowBeingEnteredByPlayer = row + 1
    validColumnsBeingEnteredByPlayer[0] = column - 1
    validColumnsBeingEnteredByPlayer[1] = column + 1
    
    if not isKing:
        #start checking whether certain moves are valid
        #check whether a move to the left would go off of the board
        if (not (validColumnsBeingEnteredByPlayer[0] < 0 or rowBeingEnteredByPlayer > 7)):
            #if there is an opponent checker on the left square
            if (currentBoard[rowBeingEnteredByPlayer][validColumnsBeingEnteredByPlayer[0]] == "opponent"):
                #check whether jump would go off of the board
                if (not ((validColumnsBeingEnteredByPlayer[0] - 1) < 0 or (rowBeingEnteredByPlayer + 1) > 7)):
                    #check whether there is a checker in the jumping spot
                    if (currentBoard[rowBeingEnteredByPlayer + 1][validColumnsBeingEnteredByPlayer[0] - 1] != "opponent"):
                        #recursively check whether there are more valid jumps from new location due to multi-jump rule
                        isKing = shouldBeKing(rowBeingEnteredByPlayer + 1, validColumnsBeingEnteredByPlayer[0] - 1, currentBoard, isKing)
                        #check whether the new square would be in the opponent's home row
                        if ((rowBeingEnteredByPlayer + 1) == 7):
                            isKing = True
        
        #check whether a move to the right would go off of the board
        if (not (validColumnsBeingEnteredByPlayer[1] > 7 or rowBeingEnteredByPlayer > 7)):
            #if there is an opponent checker on the left square
            if (currentBoard[rowBeingEnteredByPlayer][validColumnsBeingEnteredByPlayer[1]] == "opponent"):
                #check whether jump would go off of the board
                if (not ((validColumnsBeingEnteredByPlayer[1] + 1) > 7 or (rowBeingEnteredByPlayer + 1) > 7)):
                    #check whether there is a checker in the jumping spot
                    if (currentBoard[rowBeingEnteredByPlayer + 1][validColumnsBeingEnteredByPlayer[1] + 1] != "opponent"):
                        #recursively check whether there are more valid jumps from new location due to multi-jump rule
                        isKing = shouldBeKing(rowBeingEnteredByPlayer + 1, validColumnsBeingEnteredByPlayer[1] + 1, currentBoard, isKing)
                        #check whether the new square would be in the opponent's home row
                        if ((rowBeingEnteredByPlayer + 1) == 7):
                           isKing = True
    
    return isKing

#define and initialize variables for main operation
lineCount = 1
rowPosition = 0
columnPosition = 0
numberOfOpponentCheckers = 0
playerRow = 0
playerColumn = 0
validJumps = 0
inputString = ""
kingMe = False
currentBoard = [["" for x in range(8)] for y in range(8)]

#gets the first line from the user input, split into array using comma as delimiter, and strip out spaces
print (str(lineCount) + '. ')
inputString = input()
line = inputString.split(',')
for i, s in enumerate(line):
    line[i] = s.strip()

#store relevant values from line in variables
rowPosition = int(line[0])
columnPosition = int(line[1])
numberOfOpponentCheckers = int(line[2])

#begin looping through to handle input and get next input until first three numbers are 0
while (rowPosition != 0 or columnPosition != 0 or numberOfOpponentCheckers != 0) :
    #run the actual code to place checkers on the board
    try:
        #set the position of the player's single checker
        setPositionsOnBoard(rowPosition, columnPosition, 'player', currentBoard)
        playerRow = rowPosition - 1
        playerColumn = columnPosition - 1
        #set the position of the opponent's multiple checkers
        index = 0
        while index < numberOfOpponentCheckers:
            rowPosition = int(line[3+(index*2)])
            columnPosition = int(line[4+(index*2)])
            setPositionsOnBoard(rowPosition, columnPosition, 'opponent', currentBoard)
            index += 1
        #calculate possible moves and whether the player can become a king
        validJumps = calculateValidJumps(playerRow, playerColumn, currentBoard)
        kingMe = shouldBeKing(playerRow, playerColumn, currentBoard, kingMe)
        #use results of calculateValidJumps to print output
        if (kingMe):
            print(str(validJumps) + ', KING')
        else:
            print(str(validJumps))
    #error message will print if any checkers would not fit on the board
    except errorMsg:
        print('ERROR: ' + str(errorMsg))
    
    #reset the variables so that the loop will end if the user does not input anything and no issue due to accumulation of data
    rowPosition = 0
    columnPosition = 0
    numberOfOpponentCheckers = 0
    playerRow = 0
    playerColumn = 0
    validJumps = 0
    kingMe = False
    currentBoard = [["" for x in range(8)] for y in range(8)]
	
	#get the next line of input
    lineCount += 1
    print (str(lineCount) + '. ')
    inputString = input()
    line = inputString.split(',')
    for i, s in enumerate(line):
        line[i] = s.strip()
    #store relevant values from next line in variables
    rowPosition = int(line[0])
    columnPosition = int(line[1])
    numberOfOpponentCheckers = int(line[2])