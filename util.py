from enums import Position, Card, getFullDeck

def getScore(board, pos):
	if pos == Position.NORTH:
		return board.at(0, 0) + board.at(0, 1) + board.at(0, 2)
	if pos == Position.SOUTH:
		return board.at(2, 0) + board.at(2, 1) + board.at(2, 2)
	if pos == Position.WEST:
		return board.at(0, 0) + board.at(1, 0) + board.at(2, 0)
	return board.at(0, 2) + board.at(1, 2) + board.at(2, 2)

def getCurDeck(b):
	full_deck = getFullDeck()
	deck = {}
	for c in full_deck:
		if c not in deck:
			deck[c] = 0
		deck[c] += 1 

	for move in b.history:
		deck[move.card] -= 1

	return deck

def getRemainingDeck(cards, deck):

	res = {}
	for c in deck.keys():
		res[c] = deck[c] - (0 if not c in cards else cards[c])

	return res
	

# does not return EVERY possible arg, just the ones which produce a unique board state (see SHIFTNORTH, SHIFTSOUTH, etc.)
def getPossibleArgs(board, card):
	res = []
	if card == Card.SWITCHCORNERS:
		res.append([board.at(0, 0), board.at(0, 2)])
		res.append([board.at(0, 0), board.at(2, 2)])
		res.append([board.at(0, 0), board.at(2, 0)])
		res.append([board.at(0, 2), board.at(2, 2)])
		res.append([board.at(0, 2), board.at(2, 0)])
		res.append([board.at(2, 2), board.at(2, 0)])
	elif card == Card.SWITCHEDGES:
		res.append([board.at(0, 1), board.at(1, 0)])
		res.append([board.at(0, 1), board.at(1, 2)])
		res.append([board.at(0, 1), board.at(2, 1)])
		res.append([board.at(1, 0), board.at(1, 2)])
		res.append([board.at(1, 0), board.at(2, 1)])
		res.append([board.at(1, 2), board.at(2, 1)])
	elif card == Card.SHIFTNORTH or card == Card.SHIFTSOUTH or card == Card.SHIFTEAST or card == Card.SHIFTWEST:
		res.append([board.at(0, 0)])
		res.append([board.at(1, 1)])
		res.append([board.at(2, 2)])
	elif card == Card.SWAPODD:
		for i in [1, 3, 5, 7, 9]:
			if board.getPos(i) != 4: # if not already in middle
				res.append([i])
	elif card == Card.SWAPEVEN:
		for i in [2, 4, 6, 8]:
			if board.getPos(i) != 4: # if not already in middle
				res.append([i])
	else:
		res.append([])
	
	return res
	# TODO: given a board and a card, return every possible set of args that can be used

logging = True

def setLogging(val):
	global logging
	logging = val

def log(val):
	global logging
	if logging:
		print(val)