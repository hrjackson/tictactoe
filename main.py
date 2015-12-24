import game

tic = game.TicTacToe()

print tic

while True:
    print 'Please enter a move.\n'
    row = input('Row:')
    col = input('Col:')
    tic.turn([row, col])
    print tic

