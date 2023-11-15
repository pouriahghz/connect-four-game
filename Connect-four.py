import numpy as np

# اندازه تخته بازی
ROW_COUNT = 6
COLUMN_COUNT = 7

# مقادیر نمایشی برای خانه‌های تخته بازی
PLAYER_1_PIECE = 1
PLAYER_2_PIECE = 2
EMPTY = 0


# ایجاد تخته بازی خالی
def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=int)

# اضافه کردن قطعه به تخته بازی
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# بررسی آیا در ستون خاصی می‌توان قطعه افزود
def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

# پیدا کردن اولین خانه خالی در ستون خاص
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

# چاپ تخته بازی
def print_board(board):
    print(np.flip(board, 0))

# بررسی آیا بازی به پایان رسیده است
def is_terminal_node(board):
    return winning_move(board, PLAYER_1_PIECE) or winning_move(board, PLAYER_2_PIECE) or len(get_valid_locations(board)) == 0

# بررسی آیا بازی تساوی شده است
def is_tie(board):
    return len(get_valid_locations(board)) == 0

# ارزیابی مقدار تخته بازی برای بازیکن فعلی
def evaluate_window(window, piece):
    score = 0
    opponent_piece = PLAYER_1_PIECE if piece == PLAYER_2_PIECE else PLAYER_2_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opponent_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

# ارزیابی مقدار تخته بازی به صورت کلی
def score_position(board, piece):
    score = 0

    # ارزیابی سطر ‌ها
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + 4]
            score += evaluate_window(window, piece)

    # ارزیابی ستون‌ها
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + 4]
            score += evaluate_window(window, piece)

    # ارزیابی قطرها (مثبت و منفی)
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

# پیدا کردن مکان بهینه برای قرار دادن قطعه توسط الگوریتم Minimax
def minimax(board, depth, alpha, beta, maximizing_player):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, PLAYER_2_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_1_PIECE):
                return (None, -10000000000000)
            else:  # تساوی
                return (None, 0)
        else:  # توقف در عمق 0
            return (None, score_position(board, PLAYER_2_PIECE))

    if maximizing_player:
        value = -np.Inf
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, PLAYER_2_PIECE)
            new_score = minimax(temp_board, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # minimizing player
        value = np.Inf
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, PLAYER_1_PIECE)
            new_score = minimax(temp_board, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

# پیدا کردن تمام مکان‌های معتبر برای قرار دادن قطعه
def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

# بررسی آیا بازی به پایان رسیده و یکی از بازیکنان برنده شده است
def winning_move(board, piece):
    # چک کردن برنده شدن در ستون‌ها
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    # چک کردن برنده شدن در سطرها
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    # چک کردن برنده شدن در قطرها به شکل مثبت
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    # چک کردن برنده شدن در قطرها به شکل منفی
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            if board[r + 3][c] == piece and board[r + 2][c + 1] == piece and board[r + 1][c + 2] == piece and board[r][c + 3] == piece:
                return True

    return False

# بازی Connect Four با الگوریتم Minimax و هرس Alpha-Beta
def play_connect_four():
    board = create_board()
    game_over = False
    turn = 0

    while not game_over:
        # نمایش تخته بازی
        print_board(board)

        # تعیین بازیکن فعلی
        if turn % 2 == 0:
            col = int(input("Player 1, enter your move (0-6): "))
            piece = PLAYER_1_PIECE
        else:
            col, minimax_score = minimax(board, 4, -np.Inf, np.Inf, True)
            piece = PLAYER_2_PIECE

        # قرار دادن قطعه در تخته بازی
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, piece)

            # بررسی آیا بازی به پایان رسیده است
            if winning_move(board, piece):
                print_board(board)
                print(f"Player {piece} wins!")
                game_over = True
            elif is_tie(board):
                print_board(board)
                print("The game is a tie!")
                game_over = True

            turn += 1

# اجرای بازی
play_connect_four()
