/*
This program allows you to calculate possible jumps in a Checkers board's current state.
*/

#include <iostream>
#include <string>
#include <sstream>
using namespace std;



//function prototypes and structure definition
//uses a struct because the instructions specify that a structure needs to be used
struct CheckerBoard {
	//format is board[row][column]
	string board[8][8]{ "" };
};
void setPositionsOnBoard(int, int, CheckerBoard&, string);
int calculateValidJumps(int, int, CheckerBoard&, bool&);



int main() {
	//define and initialize variables
	int lineCount = 1,
		rowPosition = 0,
		columnPosition = 0,
		numberOfOpponentCheckers = 0,
		playerRow = 0,
		playerColumn = 0,

		validJumps = 0;
	char dummyCharacter;
	string input;
	CheckerBoard currentBoard;
	bool kingMe = false;

	//get the first line from the user input
	cout << lineCount << ". ";
	getline(cin, input, '\n');
	stringstream line(input);

	//extract the data from stringstream and use dummyCharacter to move read point forward
	line >> rowPosition >> dummyCharacter >> columnPosition >> dummyCharacter >> numberOfOpponentCheckers;
	//begin looping through to handle input and get next input until first three numbers are 0
	while (rowPosition != 0 || columnPosition != 0 || numberOfOpponentCheckers != 0) {
		//run the actual code to place checkers on the board
		try {
			//set the position of the player's single checker
			setPositionsOnBoard(rowPosition, columnPosition, currentBoard, "player");
			playerRow = rowPosition - 1;
			playerColumn = columnPosition - 1;
			//set the position of the opponent's multiple checkers
			for (int i = 0; i < numberOfOpponentCheckers; i += 1) {
				line >> dummyCharacter >> rowPosition >> dummyCharacter >> columnPosition;
				setPositionsOnBoard(rowPosition, columnPosition, currentBoard, "opponent");
			}
			//calculate possible moves and whether the player can become a king
			validJumps = calculateValidJumps(playerRow, playerColumn, currentBoard, kingMe);
			//use results of calculateValidJumps to print output
			if (kingMe) {
				cout << validJumps << ", KING" << endl;
			}
			else {
				cout << validJumps << endl;
			}
		}
		//error message will print if any checkers would not fit on the board
		catch (string errorMsg) {
			cout << "ERROR: " << errorMsg << endl;
		}

		//reset the variables so that the loop will end if the user does not input anything and no issue due to accumulation of data
		rowPosition = 0;
		columnPosition = 0;
		numberOfOpponentCheckers = 0;
		playerRow = 0;
		playerColumn = 0;
		for (int i = 0; i < 8; i += 1) {
			for (int j = 0; j < 8; j += 1) {
				currentBoard.board[i][j] = "";
			}
		}
		validJumps = 0;
		kingMe = false;
		line.clear();
		line.str("");

		//get the next line of input
		lineCount += 1;
		cout << lineCount << ". ";
		getline(cin, input, '\n');
		line.str(input);
		line >> rowPosition >> dummyCharacter >> columnPosition >> dummyCharacter >> numberOfOpponentCheckers;
	}

	return 0;
}

//function definition to shift the location of different pieces on the board
void setPositionsOnBoard(int row, int column, CheckerBoard& currentBoard, string checkerMoved) {
	//define errorMessage as string object to prevent error from catch block
	string errorMessage = "";

	//ensure the position number would actually fit on the board
	if (row < 1 || row > 8) {
		errorMessage = "Row number is out-of-bounds";
		throw errorMessage;
	}
	else if (column < 1 || column > 8) {
		errorMessage = "Column number is out-of-bounds";
		throw errorMessage;
	}

	//actually place the checker on the board; convert inputted row and column # into indexes
	currentBoard.board[row - 1][column - 1] = checkerMoved;
}

int calculateValidJumps(int row, int column, CheckerBoard& currentBoard, bool& kingMe) {
	//initialize all variables
	int validJumps = 0;
	int rowBeingEnteredByPlayer = 0;
	int validColumnsBeingEnteredByPlayer[2]{ 0 };

	//determine what squares the player's checker could enter if moving normally
	rowBeingEnteredByPlayer = row + 1;
	validColumnsBeingEnteredByPlayer[0] = column - 1;
	validColumnsBeingEnteredByPlayer[1] = column + 1;

	//start checking whether certain moves are valid
	//check whether a move to the left would go off of the board
	if (!(validColumnsBeingEnteredByPlayer[0] < 0 || rowBeingEnteredByPlayer > 7)) {
		//if there is an opponent checker on the left square
		if (currentBoard.board[rowBeingEnteredByPlayer][validColumnsBeingEnteredByPlayer[0]] == "opponent") {
			//check whether jump would go off of the board
			if (!((validColumnsBeingEnteredByPlayer[0] - 1) < 0 || (rowBeingEnteredByPlayer + 1) > 7)) {
				//check whether there is a checker in the jumping spot
				if (currentBoard.board[rowBeingEnteredByPlayer + 1][validColumnsBeingEnteredByPlayer[0] - 1] != "opponent") {
					//increment the number of valid jumps
					validJumps += 1;
					//recursively check whether there are more valid jumps from new location due to multi-jump rule
					validJumps += calculateValidJumps(rowBeingEnteredByPlayer + 1, validColumnsBeingEnteredByPlayer[0] - 1, currentBoard, kingMe);
					//check whether the new square would be in the opponent's home row
					if ((rowBeingEnteredByPlayer + 1) == 7) {
						kingMe = true;
					}
				}
			}
		}
	}

	//check whether a move to the right would go off of the board
	if (!(validColumnsBeingEnteredByPlayer[1] > 7 || rowBeingEnteredByPlayer > 7)) {
		//if there is an opponent checker on the left square
		if (currentBoard.board[rowBeingEnteredByPlayer][validColumnsBeingEnteredByPlayer[1]] == "opponent") {
			//check whether jump would go off of the board
			if (!((validColumnsBeingEnteredByPlayer[1] + 1) > 7 || (rowBeingEnteredByPlayer + 1) > 7)) {
				//check whether there is a checker in the jumping spot
				if (currentBoard.board[rowBeingEnteredByPlayer + 1][validColumnsBeingEnteredByPlayer[1] + 1] != "opponent") {
					//increment the number of valid jumps
					validJumps += 1;
					//recursively check whether there are more valid jumps from new location due to multi-jump rule
					validJumps += calculateValidJumps(rowBeingEnteredByPlayer + 1, validColumnsBeingEnteredByPlayer[1] + 1, currentBoard, kingMe);
					//check whether the new square would be in the opponent's home row
					if ((rowBeingEnteredByPlayer + 1) == 7) {
						kingMe = true;
					}
				}
			}
		}
	}

	return validJumps;
}