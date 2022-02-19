from sklearn.metrics import SCORERS
from playerHandle import PlayerHandle
from moveObj import MoveObj
from enums import Card
from util import *
import random


class myJankBot(PlayerHandle):

    def takeTurn(self, order, pos, board, cards):
        """
        Parameters
            order: 0-3, representing bot order this round. 0 - first, 1 - second.
            pos: either Position.NORTH or Position.SOUTH from enums.py
            board: BoardState obj that holds current board's pos and history of all previous moves
                at: return value at index
                getPos: return index of val, -1 if not found
                playCard: play given card stored in MoveObj(includes card to be played a list of args for card),
                        DOESN'T CHANGE BOARDSTATE, BUT RETURNS A NEW ONE
            cards: array of Card(enums.py), representing player hand. Card is enum listing list of all possible cards.
        Return
            MoveObj:
                - If null returned, returned object's card is null/invalid so no card is played and card at index 0 removed
                - If appropriate card selected but args bad, card removed from player's hand but no action taken
                - holds Card and list of integer args -> card type is move and integers are affected
        Function
            Minimax algorithm with search depth of 3 with more optimizations
        """

        # The deck always represents the sum total of your and your opponents cards.
        # deck and hand have the same structure: they're dictionaries that map cards
        # to the number of those respective cards in the deck/hand
        deck = getCurDeck(board)
        hand = {}

        for c in cards:
            hand[c] = hand.get(c, 0) + 1

        self.pos = pos
        self.oppPos = Position.SOUTH if pos == Position.NORTH else Position.NORTH

        # I want a depth of 3 for now, will increase with more optimizations
        searchLimit = 8

        bestScore = 0
        bestCard = Card.INVALID
        bestArgs = [0, 0]

        for c in hand:
            if hand[c] == 0:
                continue

            # For rotating, there are no args to iterate through
            if c in [Card.ROTATECLOCKWISE, Card.ROTATECOUNTERCLOCKWISE]:
                newBoard = board.playCard(MoveObj(self.pos, c, []))
                deck[c] -= 1
                hand[c] -= 1

                # calculate score with minimax and alpha beta pruning here
                score = self.backtrack(order, 0, searchLimit, 1, newBoard, getRemainingDeck(hand, deck), deck)

                deck[c] += 1
                hand[c] += 1
                if score > bestScore:
                    bestScore = score
                    bestCard = c
                    bestArgs = []

            else:
                for args in getPossibleArgs(board, c):
                    newBoard = board.playCard(MoveObj(self.pos, c, args))
                    deck[c] -= 1
                    hand[c] -= 1

                    # calculate score with minimax and alpha beta pruning here
                    score = self.backtrack(order, 0, searchLimit, 1, newBoard, getRemainingDeck(hand, deck), deck)

                    deck[c] += 1
                    hand[c] += 1
                    if score > bestScore:
                        bestScore = score
                        bestCard = c
                        bestArgs = args

        return MoveObj(self.pos, bestCard, bestArgs)

    def setupBacktrackCompare(self, order, depth, limit, pid, newBoard, hand, deck, card, bestScore):
        """
        This function abstracts away the process of setting up and calling the function backtrack()

        The important thing to note here is that if you're at the end of the round (i.e. order == 1)
        you need to evalute who goes first the next round. If player 0's board score is higher than 
        player 1, then player 0 goes first, otherwise player 1 goes first.

        If you're not at the end of the round, you just switch perspectives from player 0 to player 1
        or vice versa.
        """

        # Modify the deck and hand before recursing
        deck[card] -= 1
        hand[card] -= 1

        # Get the board scores you'll need to check who goes first next round
        # (if order == 1)
        yourScore = getScore(newBoard, self.pos)
        oppScore = getScore(newBoard, self.opp_pos)

        score = 0
        # Rounds consist of two moves, so order is either 0 or 1 (with 1 being
        # the end of the round)
        if order == 1:
            if yourScore >= oppScore:
                score = self.backtrack(
                    0, depth+1, limit, 0, newBoard, hand if pid == 0 else getRemainingDeck(hand, deck), deck)
            else:
                score = self.backtrack(
                    0, depth+1, limit, 1, newBoard, hand if pid == 1 else getRemainingDeck(hand, deck), deck)
        else:
            score = self.backtrack(
                1, depth+1, limit, pid ^ 1, newBoard, getRemainingDeck(hand, deck), deck)

        hand[card] += 1
        deck[card] += 1

        if (pid == 0 and score > bestScore) or (pid == 1 and score < bestScore):
            # Return score since it's the new best value
            return score

        # Return the same best score passed in as a parameter since you were unable to
        # find something better
        return bestScore

    def backtrack(self, order, depth, limit, pid, board, hand, deck):

        # Base case: no more cards
        if sum((hand[c] != 0) for c in hand.keys()) == 0:
            return getScore(board, self.pos)

        # Base case: depth == limit or you don't have any more cards
        if depth >= limit:
            return getScore(board, self.pos)

        # So you want to iteratively find the best score right?
        # If you're player 1, you should start the best score really high and
        # lower threshold as you find better moves. Do the exact opposite if you're
        # player 0
        bestScore = 9999 if pid != 0 else 0

        # Recursively explore every move available to you
        for c in hand.keys():
            if hand[c] == 0:
                continue

            if c == Card.ROTATECLOCKWISE or c == Card.ROTATECOUNTERCLOCKWISE:
                newBoard = board.playCard(
                    MoveObj(self.pos if pid == 0 else self.opp_pos, c, [])
                )
                bestScore = self.setupBacktrackCompare(
                    order, depth, limit, pid, newBoard, hand, deck, c, bestScore
                )
            else:
                for args in getPossibleArgs(board, c):
                    newBoard = board.playCard(
                        MoveObj(self.pos if pid == 0 else self.opp_pos, c, args)
                    )
                    bestScore = self.setupBacktrackCompare(
                        order, depth, limit, pid, newBoard, hand, deck, c, bestScore
                    )

        return bestScore
