# Coding Guide #

## Installation Instructions ##

Switch to Python from Java...
The code for this game is found [here](https://github.tamu.edu/dpuckett98/MatrixGame/Python). It is entirely written in Python 3.8.2.  Other versions of Python are untested, but no incompatabilities are expected.

Once Python is installed and the game code is downloaded, the game can be run from the command line using the following:

```
python main.py
```

## Programming a Bot ##

In order to program a bot for this game, create a new class that extends [PlayerHandle](https://github.tamu.edu/dpuckett98/MatrixGame/blob/master/Python/playerHandle.py). One function in particular must be implemented. The player's cards and the current board state are given as inputs, and the bot must output a card to play.

```python
def takeTurn(self, order, pos, board, cards)
```

### Inputs ###

`order` is an integer from 0 to 3, representing the bot's order in this round. For example, if this bot is going second this round, then `order` will be 1.

`pos` is either `Position.NORTH` or `Position.SOUTH` from [enums.py](https://github.tamu.edu/dpuckett98/MatrixGame/blob/master/Python/enums.py).

`BoardState` is an object which holds the current board's position and contains a history of all the previous moves. The implementation is available [here](https://github.tamu.edu/dpuckett98/MatrixGame/blob/master/Python/boardState.py). The methods of this class are listed below:

```python
def getPos(self, x, y)
```
`getPos` returns the number at a specific row and column of the board. The rows and columns are listed from 0 to 2.

```python
def playCard(self, moveObj)
```
`playCard` plays the given card stored in a `MoveObj`. A `MoveObj` includes the card to be played and a list of arguments for that card. This function does not change the `BoardState` at all. Instead, it creates a new `BoardState` and returns it.

```python
def printBoard(self)
```
`printBoard` prints the current board.

`card` is an array of `Card`, found in [enums.py](https://github.tamu.edu/dpuckett98/MatrixGame/blob/master/Python/enums.py) which represents the player's current hand.
`Card` is an enum which lists all of the possible cards. This includes the cards listed [here](#card-descriptions) as well as `Card.Invalid`.

### Outputs ###

The bot must return a `MoveObj` (described below) each turn. If a `null` object is returned, the return object's card is `null` or Invalid, or the card given is not from the player's hand, then no card is played, and the card at index 0 is removed from the player's hand. If an appropriate Card is selected, but the arguments are incorrect or missing, then that Card is removed from the player's hand and no action is taken.

`MoveObj` is a class which holds a Card and a list of integer arguments. The implementation is available [here](https://github.tamu.edu/dpuckett98/MatrixGame/blob/master/Python/moveObj.py). The methods are listed below:

```python
def __init__(self, card, args)
```
This constructor creates a new `MoveObj` given a card and its arguments.

### Card Descriptions ###

The board below is used as an example, and is referenced by the card descriptions.

4 2 8  
3 9 1  
5 6 7  

#### SwitchCorners ####

This card switches two corners of the board. It requires two args, the numbers to be switched. "SwitchCorners 4 7" produces the following board:  
<pre>
4 2 8		7 2 8
3 9 1	->	3 9 1
5 6 7		5 6 4
</pre>  

#### SwitchEdges ####

This card switches two edges of the board (specifically excluding corners). It requires two args, the numbers to be switched. "SwitchEdges 2 1" produces the following board:  
<pre>
4 2 8		4 1 8
3 9 1	->	3 9 2
5 6 7		5 6 7
</pre>  

#### ShiftNorth ####

This card shifts one column to the North. It requires one argument, which is simply one of the numbers in the column to be rotated.  "RotateNorth 2" produces the following board:  
<pre>
4 2 8		4 9 8
3 9 1	->	3 6 1
5 6 7		5 2 7
</pre>  

#### ShiftSouth ####

This card shifts one column to the South. It requires one argument, which is simply one of the numbers in the column to be rotated.  "RotateSouth 2" produces the following board:  
<pre>
4 2 8		4 6 8
3 9 1	->	3 2 1
5 6 7		5 9 7
</pre>  

#### ShiftWest ####

This card shifts one row to the West. It requires one argument, which is simply one of the numbers in the column to be rotated.  "RotateWest 2" produces the following board:  
<pre>
4 2 8		2 8 4
3 9 1	->	3 9 1
5 6 7		5 6 7
</pre>  

#### ShiftEast ####

This card shifts one row to the West. It requires one argument, which is simply one of the numbers in the column to be rotated.  "RotateWest 2" produces the following board:  
<pre>
4 2 8		8 4 2
3 9 1	->	3 9 1
5 6 7		5 6 7
</pre>  

#### SwapEven ####

This card swaps one even number with the middle number. It requires one argument, the number to be swapped.  "SwapEven 2" produces the following board:  
<pre>
4 2 8		4 9 8
3 9 1	->	3 2 1
5 6 7		5 6 7
</pre>  

#### SwapOdd ####

This card swaps one odd number with the middle number. It requires one argument, the number to be swapped.  "SwapOdd 1" produces the following board:  
<pre>
4 2 8		4 2 8
3 9 1	->	3 1 9
5 6 7		5 6 7
</pre>  

#### RotateClockwise ####

This card rotates the entire board clockwise by one position. It requires no arguments.  "RotateClockwise" produces the following board:  
<pre>
4 2 8		3 4 2
3 9 1	->	5 9 8
5 6 7		6 7 1
</pre>  

#### RotateCounterClockwise ####

This card rotates the entire board counterclockwise by one position. It requires no arguments.  "RotateCounterClockwise" produces the following board:  
<pre>
4 2 8		2 8 1
3 9 1	->	4 9 7
5 6 7		3 5 6
</pre>  

## Integrating Bot with Rest of Game ##

Replace the given bot with your bot in main.py