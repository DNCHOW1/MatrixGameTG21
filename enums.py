from enum import Enum

class Card(Enum):
	INVALID = "invalid"
	SWITCHCORNERS = "switchcorners"
	SWITCHEDGES = "switchedges"
	SHIFTNORTH = "shiftnorth"
	SHIFTSOUTH = "shiftsouth"
	SHIFTWEST = "shiftwest"
	SHIFTEAST = "shifteast"
	SWAPEVEN = "swapeven"
	SWAPODD = "swapodd"
	ROTATECLOCKWISE = "rotateclockwise"
	ROTATECOUNTERCLOCKWISE = "rotatecounterclockwise"

def getFullDeck():
	res = []
	for i in range(2):
		res.append(Card.SWITCHCORNERS)
	for i in range(2):
		res.append(Card.SWITCHEDGES)
	for i in range(2):
		res.append(Card.SHIFTNORTH)
	for i in range(2):
		res.append(Card.SHIFTSOUTH)
	for i in range(2):
		res.append(Card.SHIFTEAST)
	for i in range(2):
		res.append(Card.SHIFTWEST)
	for i in range(2):
		res.append(Card.SWAPEVEN)
	for i in range(2):
		res.append(Card.SWAPODD)
	for i in range(2):
		res.append(Card.ROTATECLOCKWISE)
	for i in range(2):
		res.append(Card.ROTATECOUNTERCLOCKWISE)
	return res

class Position(Enum):
	NORTH = 0
	SOUTH = 1
	WEST = 2
	EAST = 3