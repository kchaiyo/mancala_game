from random import randrange


def isValidMove(move, boardState):
    if move in range(1, 7):
        pitName = 'A' + str(move)
        return boardState[pitName] > 0
    else:
        return False


class SampleAgent:
    def makeMove(self, boardState, player):  # Not implemented parameters are isExtraTurn:Boolean and turnNumber:Integer
        '''
        Decide the move that player is going to make, given the board state and other parameters
        :param boardState: A dictionary representing the board state. Each key is a string referring to the pit's name.
            Each value is the amount of stones inside the pit.
            Pit names are
                - A[1-6], the 6 playable pits from left to right (furthest from the player's score hole to nearest)
                - AS, the player's score pit
                - B[1-6], the opponent's playable pits
                - BS, the opponent's score pit
        :param player: 1 if this player started first, 2 if this player started second
        :return: integer between 1-6 inclusive, referring to the pit that this player decided to play

        Note: if the player made an invalid move (return pit number outside of range or pick empty pit), the player will
            immediately lose. Use the method isValidMove to check before returning the move.
        '''
        for i in range(500):
            randomedMove = randrange(6) + 1
            if isValidMove(randomedMove, boardState):
                break
        else:
            print("No valid move after 500 random")
            return 0    #obviously invalid move
        return randomedMove
