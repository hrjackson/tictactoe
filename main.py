import game

tic = game.TicTacToe()

print tic

while not tic.checkWin():
    print 'Please enter a move.\n'
    row = input('Row:')
    col = input('Col:')
    tic.turn([row, col])
    print tic

print 'We have a winner! It is player '
print tic.winner

