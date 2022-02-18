from playerHandle import PlayerHandle

class myJankBot(PlayerHandle):
    
    def takeTurn(self, order, pos, board, cards):
        """
        order: 0-3, representing bot order this round. 0 - first, 1 - second.
        pos: either Position.NORTH or Position.SOUTH from enums.py
        board: BoardState obj that holds current board's pos and history of all previous moves
            at: return value at index
            getPos: return index of val, -1 if not found
            playCard: play given card stored in MoveObj(includes card to be played a list of args for card),
                      DOESN'T CHANGE BOARDSTATE, BUT RETURNS A NEW ONE
        card: 
        """
        #return super().takeTurn(order, pos, board, cards)