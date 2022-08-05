import random
import  sys
import math

def get_piece():
    piece = input('CHOOSE A PIECE(X OR O): ')
    while True:
        if piece == 'X':
            return ['X', 'O']
        else:
            return ['O', 'X']
        piece = input('CHOOSE A PIECE(X OR O): ')

def bo_list():
    list = [[' ']*8 for _ in range(8)]
    return list

def bo_ascii(board):
    print('  12345678')
    print('  ========')
    for x in range(8):
        print(f'{x+1}|', end='')
        for y in range(8):
            print(f'{board[x][y]}',end='')
        print('|')
    print('  ========')
        
def reset_bo(bo):
    for x in range(8):
        for y in range(8):
            bo[x][y] = ' '

    bo[3][3] = 'X'
    bo[3][4] = 'O'
    bo[4][3] = 'O'
    bo[4][4] = 'X'

    return bo

def first():
    turn = random.randrange(0, 2)

    if turn == 1:
        return 'player'
    else:
        return 'computer'

def play_again():
    qn = input('Do you want to play again?')
    return qn.lower().startswith('y')

def on_board(x, y):
    if (x >= 0 and x <= 7) and (y >= 0 and  y <= 7):
        return True
    return False

def valid_moves(board, piece, xstart, ystart):
    flip_pieces = []

    if piece == 'X':
        other = 'O'
    else:
        other = 'X'

    if not on_board(xstart, ystart) or board[xstart][ystart] != ' ':
        return False

    #temporarily place piece
    board[xstart][ystart] = piece
    #print(board)
    for xdir,ydir in [[-1,-1], [0,-1], [1,-1], [-1, 0], [1,0], [-1,1], [0,1], [1,1]]:
        x,y = xstart, ystart 
        x += xdir
        y += ydir

        if on_board(x,y) and board[x][y] == other:
            x += xdir
            y += ydir
            if not on_board(x,y):
                continue

            while board[x][y] == other:
                x += xdir
                y += ydir
                if not on_board(x,y):
                    break
            if not on_board(x, y):
                continue

            if board[x][y] == piece:
                while True:
                    x -= xdir
                    y -= ydir
                    if x == xstart and y == ystart:
                        break
                    flip_pieces.append([x,y])

        board[xstart][ystart] = ' '

    if len(flip_pieces) == 0:
        return False
    return flip_pieces

def get_valid_moves(bo, piece):
    valid = []
    for x in range(8):
        for y in range(8):
            if valid_moves(bo, piece, x, y) != False:
                valid.append([x,y])
    return valid

def dupe(bo):
    du = bo_list()

    for x in range(8):
        for y in range(8):
            du[x][y] = bo[x][y]
    
    return du

def hints_bo(bo, piece):
    du = dupe(bo)
    valids = get_valid_moves(bo, piece)

    for x,y in valids:
        du[x][y] = '.'
    return du
        
def player_input(bo, piece):
    valid_digits = [int(i) for i in '12345678']

    while True:
        print("Type 'moves?' if you need to view possible moves.....and type 'off' if you don't need to see them anymore")
        move = input('Type a number (row, col) to place your piece: ')
        if move == 'moves?':
            return 'moves?'
        elif move == 'off':
            return 'off'
        elif move == 'quit':
            return 'quit'
        if len(move) == 2 and int(move[0]) in valid_digits and int(move[1]) in valid_digits:
            x, y = int(move[0])-1, int(move[1])-1
            if valid_moves(bo, piece, x, y) == False:
                continue
            else:
                break
        else:
            print('INVALID MOVE')
    return [x,y]

def make_move(bo, piece, x, y):
    flip = valid_moves(bo, piece, x, y)
    print(flip)
    bo[x][y] = piece  
    for i,j in flip:
        bo[i][j] = piece

def score(bo):
    x_score = 0
    o_score = 0

    for x in range(8):
        for y in range(8):
            if bo[x][y] == 'X':
                x_score += 1
            if bo[x][y] == 'O':
                o_score += 1
    return {'X':x_score, 'O':o_score}

def show_scores(bo, player, comp):
    print(f'THE COMPUTER HAS {score(bo)[comp]}. THE HUMAN HAS {score(bo)[player]}')

def evaluate(bo, eval_piece):
    if eval_piece == 'X':
        other = 'O'
    else:
        other = 'X'

    evaluation = score(bo)

    if evaluation[eval_piece] > evaluation[other]:
        return 10
    elif evaluation[other] > evaluation[eval_piece]:
        return -10
    else:
        return 0

def minimax(bo, depth, ismaxim, piece, alpha, beta):
    if piece == 'X':
        other_piece = 'O'
    else:
        other_piece = 'X'

    minimax_score = evaluate(bo, piece)

    if minimax_score == 10:
        return minimax_score - depth
    if minimax_score == -10:
        return minimax_score + depth
    if get_valid_moves(bo, piece) == []:
        return 0

    if ismaxim:
        best = -math.inf
        for x in range(8):
            for y in range(8):
                if valid_moves(bo, piece, x, y) != False:
                    make_move(bo, piece, x, y)
                    val = minimax(bo,depth+1,False, piece, alpha, beta)
                    best = max(best,val)
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        break
                    bo[x][y] = ' '
        return best
    else:
        best = math.inf
        for x in range(8):
            for y in range(8):
                if valid_moves(bo, piece, x, y) != False:
                    make_move(bo, piece, x, y)
                    val = minimax(bo,depth+1,True,piece, alpha, beta)
                    best = min(best,val)
                    beta = min(beta, best)
                    if beta <= alpha:
                        break
                    bo[x][y] = ' '
        return best

def computer_moves(bo,computer_piece):
    value = -math.inf
    best_move = None

    for x in range(8):
        for y in range(8):
            if valid_moves(bo,computer_piece,x,y) != False:
                make_move(bo, computer_piece, x, y)
                move_value = minimax(bo,0,True,computer_piece,-math.inf,math.inf)
                if move_value > value:
                    value = move_value
                    best_move = [x,y]
                    
                bo[x][y] = ' '
    return best_move

while True:
    board = bo_list()
    reset_bo(board)
    turn = first()
    player_piece, comp_piece = get_piece()
    hints = False

    print('REVERSI')
    while True:
        if turn == 'player':
            if hints == True:
                hint = hints_bo(board, player_piece)
                bo_ascii(hint)
            else:
                bo_ascii(board)

            show_scores(board, player_piece, comp_piece)
            move = player_input(board, player_piece)

            if move == 'moves?':
                hints = True
                continue
            elif move == 'off':
                hints = False
                continue
            elif move == 'quit':
                print('Goodbye')
                sys.exit()
            else:
                make_move(board, player_piece, move[0], move[1])

            if get_valid_moves(board, player_piece) == []:
                break
            else:
                turn = 'computer'
        else:  #turn = computer
            bo_ascii(board)
            show_scores(board, player_piece,comp_piece)
            input('Enter to see computer move: ')

            x,y = computer_moves(board, comp_piece)
    
            make_move(board,comp_piece,x,y)

            if get_valid_moves(board,comp_piece) == []:
                break 
            else:
                turn = 'player'

    player_score = score(board)[player_piece]
    cmp_score = score(board)[comp_piece]

    bo_ascii(board)

    if player_score > cmp_score:
        print('YOU WIN!!!')
    else:
        print('MINIMAX SEARCH WINS!!!')

    if not play_again():
        break            
