class AbstractGame(object):
    """
    Abstract class to encapsulate game information
    """

    def __init__(self, nPlayers):
        """
        Initialises the game to have nPlayers. Assuming that player 1 always starts (counting from 1).
        :param nPlayers: number of players in the game
        :return None.
        """
        self.state = None
        self.winner = None
        self.players = nPlayers
        self.playerTurn = 1

    def _updatePlayer(self):
        """
        Automatically update which player's turn it is.
        :return: None, but update state of object.
        """
        self.playerTurn = self.playerTurn % self.players + 1

    def checkWin(self):
        """
        Should check to see if the game has been won yet. Sets winner to playerTurn if won.
        :return: bool. True if game won, false otherwise.
        """
        raise NotImplementedError

    def _updateState(self, move):
        """
        Updates the state of the game.
        :param move: type depends on specific game implementation.
        :return: None, but update state of object.
        """
        raise NotImplementedError

    def turn(self, move):
        """
        Take a turn in the game. Should update self.state somehow.
        :param move: type depends on specific game implementation.
        :return: None, but update state of object.
        """
        if self._updateState(move):
            self._updatePlayer()  # Automatically update player, if move successful.

    def setPlayer(self, player):
        """
        Override who's turn it is. Useful for composition of games.
        :param player: Integer. Who's turn is it now?
        :return: None, but update state of object.
        """
        assert isinstance(player, int)
        self.playerTurn = player


class TicTacToe(AbstractGame):
    """
    TicTacToe game. Input for turn must be an array with matrix coordinate of square to play in.
    Game state is stored as a matrix of all zeros to start. Then the player number who
    """
    def __init__(self):
        """
        Initialises the TicTacToe game, to have 2 players.
        :return:
        """
        super(TicTacToe, self).__init__(2)  # Run the AbstractGame init function
        self.state = [[0 for x in range(3)] for x in range(3)]

    def checkWin(self):
        """
        Should check to see if the game has been won yet. Sets winner to playerTurn if won.
        :return: bool. True if game won, false otherwise.
        """
        won = False
        # Check the rows and columns first
        for i in range(3):
            won = (self.state[0][i] == self.state[1][i] == self.state[2][i] != 0)
            winner = self.state[0][i]
            if won:
                break
            won = (self.state[i][0] == self.state[i][1] == self.state[i][2] != 0)
            winner = self.state[i][0]
            if won:
                break

        # Check diagonals if not there yet
        if not won:
            won = ((self.state[0][0] == self.state[1][1] == self.state[2][2] != 0) or
                   (self.state[0][2] == self.state[1][1] == self.state[2][0] != 0))
            winner = self.state[1][1]
        # Have checked all possibilities.
        if won:
            self.winner = winner
        return won


    def _boundCheck(self, move):
        """
        Check move is between 0 and 2 (inclusive)
        :param move: integer
        :return: bool True if move is between 0 and 2
        """
        return (move >= 0) & (move <= 2) & (isinstance(move, int))

    def _acceptableMove(self, move):
        """
        Tests move to see if it is legal, within the rules of Tic Tac Toe, and of the right format.
        :param move: must be an array of length 2
        :return: bool. True if move is ok, false otherwise
        """
        inbounds = self._boundCheck(move[0]) & self._boundCheck(move[1])
        notplayed = False
        if inbounds:
            notplayed = (self.state[move[0]][move[1]] == 0)
        return inbounds & notplayed

    def _updateState(self, move):
        """
        Change the matrix to have the player as it's entry
        :param move: array of length 2 with row and column of matrix to change.
        :return: Bool. True if successful update, false otherwise.
        """
        updated = False
        if self._acceptableMove(move):
            self.state[move[0]][move[1]] = self.playerTurn
            self.checkWin()
            updated = True
        else:
            print("Invalid move. Try again.")
        return updated

    def _matConvert(self, coord):
        """
        Convert matrix representation to character
        :param coord: matrix coordinate of spot in game to change
        :return: character of played state
        """
        num = self.state[coord[0]][coord[1]]
        character = ' '
        if num == 1:
            character = 'X'
        if num == 2:
            character = 'O'
        return character

    def _strLine(self, line):
        """
        Generate a string representing a row of the matrix
        :param line: integer representing row to print. Starting from 0.
        :return: string representing the row. Eg " X |   | O "
        """
        return ' {0} | {1} | {2} '.format(self._matConvert([line, 0]),
                                          self._matConvert([line, 1]),
                                          self._matConvert([line, 2]))

    def __str__(self):
        """
        String representation of the game state.
        :return: string
        """
        output = self._strLine(0)
        output += '\n-----------'
        output += '\n' + self._strLine(1)
        output += '\n-----------'
        output += '\n' + self._strLine(2)
        return output + '\n'
