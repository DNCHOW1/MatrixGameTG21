# Game Definition

## Introduction ##

This game is a two-player game based around a 3x3 matrix of numbers.  An example board is shown below.

4	6	3  
7	9	2  
1	8	5  

Each player's score is the sum of the three numbers right in front of them. For the example above, the South player's score is 1+8+5=14 and the North player's score is 4+6+3=13. At the beginning of the game, each player is dealt a hand of ten cards.  Each card, when played, rearranges the board in some way.  This allows players to increase their own score and decrease their opponents' scores.  The play goes in rounds, with each player playing one card, until the players run out of cards.  There is no draw pile; after one round, each player will have nine cards.  After two rounds, each player will have eight cards, and so on until they run out. At the end of ten rounds, the highest scoring player wins.

## Game Rules

### Turn Order

The turn order changes each round based on the players' score. The highest scoring player will always go first, followed by the second-highest score, then the third-highest score, then finally the lowest score. In the example above, the South player will go first, followed by the North player. After one round, the turn order is reevaluated based on the new board position.

### Cards

Note: General card descriptions are contained here. See the coding guide for more specific details on how to play each card.

#### Switch Corners ####

This card switches two corners of the board. In the example above, this could be swapping 4 and 3, or 4 and 1, etc.  
Quantity: 2

#### Switch Edges ####

This card switches two edges of the board (specifically excluding corners). In the example above, this could be swapping 6 and 7, or 7 and 2, etc.  
Quantity: 2

#### Shift North ####

This card shifts one column to the North. In the example above, this could be rotating the column 4-7-1 to 7-1-4.  
Quantity: 2

#### Shift South ####

This card shifts one column to the South. In the example above, this could be rotating the column 4-7-1 to 1-4-7.  
Quantity: 2

#### Shift West ####

This card shifts one row to the West. In the example above, this could be rotating the row 7-9-2 to 9-2-7.  
Quantity: 2

#### Shift East ####

This card shifts one row to the East. In the example above, this could be rotating the row 7-9-2 to 2-7-9.  
Quantity: 2

#### Swap Even ####

This card swaps one even number with the middle number. In the example above, this could be swapping the 6 with the 9.  
Quantity: 2

#### Swap Odd ####

This card swaps one odd number with the middle number. In the example above, this could be swapping the 1 with the 9.  
Quantity: 2

#### Rotate Clockwise ####

This card rotates the entire board clockwise. The middle number stays the same, and the rest of the numbers will rotate.  
Quantity: 2

#### Rotate CounterClockwise ####

This card rotates the entire board counterclockwise. The middle number stays the same, and the rest of the numbers will rotate.  
Quantity: 2