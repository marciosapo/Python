import pygame
import sys
import os


if __name__ == "__main__":
    # Initialize pygame
    pygame.init()

    # game Variables
    turno = ""
    whiteVictories = 0
    blackVictories = 0
    gameDraws = 0
    whiteFirstMove = True
    blackFirstMove = True

    canMoveTo = []
    whiteDead = []
    blackDead = [] 

    # Constants
    WINDOW_WIDTH, WINDOW_HEIGHT = 1300, 700
    BOARD_SIZE = 600
    ROWS, COLS = 8, 8
    SQUARE_SIZE = BOARD_SIZE // COLS
    MARGIN = (WINDOW_HEIGHT - BOARD_SIZE) // 2

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    DARK_BROWN = (101, 67, 33)
    LIGHT_BROWN = (222, 184, 135)
    SELECTED_COLOR = (255, 0, 0)  # Red color for selection
    MOVE_COLOR = (0, 255, 0)  # Red color for selection

    # Load images
    IMAGES = {}

def load_images():
    pieces = ['bp', 'br', 'bn', 'bb', 'bq', 'bk', 
              'wp', 'wr', 'wn', 'wb', 'wq', 'wk']
    for piece in pieces:
        image_path = os.path.join('chess', 'pieces', f'{piece}.png')
        try:
            IMAGES[piece] = pygame.transform.scale(
                pygame.image.load(image_path), (SQUARE_SIZE, SQUARE_SIZE))
            print(f"Loaded: {image_path}")
        except pygame.error as e:
            print(f"Error loading image {image_path}: {e}")

# Draw chessboard
def draw_board(win):
    colors = [LIGHT_BROWN, DARK_BROWN]
    for row in range(ROWS):
        for col in range(COLS):
            color = colors[(row + col) % 2]
            pygame.draw.rect(win, color, (col * SQUARE_SIZE, MARGIN + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Draw white dead pieces board         
def draw_white_dead(win):
    x_offset = 650  # x position where the grid should start
    y_offset = 330  # y position where the grid should start
    for row in range(2):
        for col in range(8):
            pygame.draw.rect(win, LIGHT_BROWN, (x_offset + col * SQUARE_SIZE, y_offset + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Draw black dead pieces board
def draw_black_dead(win):
    x_offset = 650  # x position where the grid should start
    y_offset = 500  # y position where the grid should start
    for row in range(2):
        for col in range(8):
            pygame.draw.rect(win, DARK_BROWN, (x_offset + col * SQUARE_SIZE, y_offset + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Draw white dead pieces
def draw_white_dead_pieces(win):
    x_offset = 650  # x position where the grid should start
    y_offset = 320  # y position where the grid should start
    for i, piece in enumerate(whiteDead):
        # Calculate row and column for piece placement
        row = i // 8
        col = i % 8
        # Check and draw the piece
        if piece in IMAGES:
            piece_image = IMAGES[piece]
            if piece_image:
                x = x_offset + col * SQUARE_SIZE
                y = y_offset + row * SQUARE_SIZE
                win.blit(piece_image, (x, y))
            else:
                print(f"Image not loaded for {piece}")
        else:
            print(f"Piece {piece} not found")
# Draw black dead pieces
def draw_black_dead_pieces(win):
    x_offset = 650  # x position where the grid should start
    y_offset = 490  # y position where the grid should start
    for i, piece in enumerate(blackDead):
        # Calculate row and column for piece placement
        row = i // 8
        col = i % 8
        # Check and draw the piece
        if piece in IMAGES:
            piece_image = IMAGES[piece]
            if piece_image:
                x = x_offset + col * SQUARE_SIZE
                y = y_offset + row * SQUARE_SIZE
                win.blit(piece_image, (x, y))
            else:
                print(f"Image not loaded for {piece}")
        else:
            print(f"Piece {piece} not found")

# Draw pieces
def draw_pieces(win, board):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != '':
                win.blit(IMAGES[piece], (col * SQUARE_SIZE, MARGIN + row * SQUARE_SIZE))

# Create initial board setup
def create_board():
    board = [
        ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
        ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
        ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']
    ]
    return board

# Get the board position based on mouse click
def get_board_position(x, y):
    col = (x) // SQUARE_SIZE
    row = (y - MARGIN) // SQUARE_SIZE
    if 0 <= col < COLS and 0 <= row < ROWS:
        return row, col
    return None, None

# Highlight selected position
def highlight_square(win, row, col, color):
    if row is not None and col is not None:
        pygame.draw.rect(win, color, (col * SQUARE_SIZE, MARGIN + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)
    

# Draw text
def draw_text(win, text, size, color, pos):
    font = pygame.font.SysFont('Arial', size)
    text_surface = font.render(text, True, color)
    win.blit(text_surface, pos)
 
 

def is_king_in_check(board, king_position, opponent_pieces):
    king_row, king_col = king_position
    for piece in opponent_pieces:
        # Simulate moves for each opponent piece
        possible_moves = getPossibleMovement(piece, board)
        if king_position in possible_moves:
            return True
    return False 

def is_checkmate(board, king_position, player_pieces, opponent_pieces):
    if not is_king_in_check(board, king_position, opponent_pieces):
        return False
    
    # Simulate all legal moves for the player
    for piece in player_pieces:
        original_position = get_piece_position(piece, board)
        possible_moves = getPossibleMovement(piece, board)
        
        for move in possible_moves:
            # Make the move
            simulate_move(board, original_position, move)
            
            # Check if the king is still in check
            if not is_king_in_check(board, king_position, opponent_pieces):
                # Undo the move and return False
                undo_move(board, original_position, move)
                return False
            
            # Undo the move
            undo_move(board, original_position, move)
    
    return True  # No legal moves to get out of check
 
# GetPossibleMovements function
def getPossibleMovement(piece, row, col, board):
    canMoveTo.clear()
    if piece == "wp":
        # Move one square forward
        if row > 0 and board[row-1][col] == '':
            canMoveTo.append((row-1, col))
            # Move two squares forward from the starting position
            if whiteFirstMove and row == 6 and board[row-2][col] == '':
                canMoveTo.append((row-2, col))
        # Capture diagonally
        if row > 0 and col > 0 and board[row-1][col-1] != '' and board[row-1][col-1][0] == 'b':
            canMoveTo.append((row-1, col-1))
        if row > 0 and col < 7 and board[row-1][col+1] != '' and board[row-1][col+1][0] == 'b':
            canMoveTo.append((row-1, col+1))
    elif piece == "bp":
        # Move one square forward
        if row < 7 and board[row+1][col] == '':
            canMoveTo.append((row+1, col))
            # Move two squares forward from the starting position
            if blackFirstMove and row == 1 and board[row+2][col] == '':
                canMoveTo.append((row+2, col))
        # Capture diagonally
        if row < 7 and col > 0 and board[row+1][col-1] != '' and board[row+1][col-1][0] == 'w':
            canMoveTo.append((row+1, col-1))
        if row < 7 and col < 7 and board[row+1][col+1] != '' and board[row+1][col+1][0] == 'w':
            canMoveTo.append((row+1, col+1))
    elif piece == 'wr' or piece == 'br':
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for direction in directions:
            dir_row, dir_col = row, col
            while True:
                dir_row += direction[0]
                dir_col += direction[1]
                if 0 <= dir_row < len(board) and 0 <= dir_col < len(board[0]):
                    if board[dir_row][dir_col] == '':
                        canMoveTo.append((dir_row, dir_col))
                    else:
                        # Capture logic: If the piece encountered is an opponent's piece, add it as a valid move
                        if (piece == 'wr' and board[dir_row][dir_col][0] == 'b') or \
                        (piece == 'br' and board[dir_row][dir_col][0] == 'w'):
                            canMoveTo.append((dir_row, dir_col))
                        # Stop after capturing or encountering any piece
                        break
                else:
                    break
    elif piece == 'wb' or piece == 'bb':
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for direction in directions:
            dir_row, dir_col = row, col
            while True:
                dir_row += direction[0]
                dir_col += direction[1]
                if 0 <= dir_row < len(board) and 0 <= dir_col < len(board[0]):
                    if board[dir_row][dir_col] == '':
                        canMoveTo.append((dir_row, dir_col))
                    else:
                        # Capture logic: If the piece encountered is an opponent's piece, add it as a valid move
                        if (piece == 'wb' and board[dir_row][dir_col][0] == 'b') or \
                        (piece == 'bb' and board[dir_row][dir_col][0] == 'w'):
                            canMoveTo.append((dir_row, dir_col))
                        # Stop after capturing or encountering any piece
                        break
                else:
                    # Stop if the edge of the board is reached
                    break
    elif piece == 'wq' or piece == 'bq':
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),  # vertical and horizontal
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # diagonals
        ]
        for direction in directions:
            dir_row, dir_col = row, col
            while True:
                dir_row += direction[0]
                dir_col += direction[1]
                if 0 <= dir_row < len(board) and 0 <= dir_col < len(board[0]):
                    if board[dir_row][dir_col] == '':
                        canMoveTo.append((dir_row, dir_col))
                    else:
                        # Capture logic: If the piece encountered is an opponent's piece, add it as a valid move
                        if (piece == 'wq' and board[dir_row][dir_col][0] == 'b') or \
                        (piece == 'bq' and board[dir_row][dir_col][0] == 'w'):
                            canMoveTo.append((dir_row, dir_col))
                        # Stop after capturing or encountering any piece
                        break
                else:
                    # Stop if the edge of the board is reached
                    break
    elif piece == 'wn' or piece == 'bn':
        directions = [
            (-2, -1), (-1, -2), (1, -2), (2, -1),
            (2, 1), (1, 2), (-1, 2), (-2, 1)
        ]
        for direction in directions:
            dir_row = row + direction[0]
            dir_col = col + direction[1]
            if 0 <= dir_row < len(board) and 0 <= dir_col < len(board[0]):
                if board[dir_row][dir_col] == '' or board[dir_row][dir_col][0] != board[row][col][0]:
                    canMoveTo.append((dir_row, dir_col))
    elif piece == 'wk' or piece == 'bk':
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),  # vertical and horizontal
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # diagonals
        ]
        for direction in directions:
            dir_row = row + direction[0]
            dir_col = col + direction[1]
            if 0 <= dir_row < len(board) and 0 <= dir_col < len(board[0]):
                # King can move to an empty square or capture an opponent's piece
                if board[dir_row][dir_col] == '' or board[dir_row][dir_col][0] != board[row][col][0]:
                    canMoveTo.append((dir_row, dir_col))
                
                      
# Main function
def main():
    global whiteFirstMove, blackFirstMove, turno
    turno = "White"
    piece_info = "SELECTED PIECE: No piece selected"
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Chess')

    load_images()
    board = create_board()
    
    selected_square = None


    clock = pygame.time.Clock()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row, col = get_board_position(x, y)
                if selected_square is not None and (row, col) == selected_square:
                        # Unselect the square
                    selected_square = None
                    piece_info = "SELECTED PIECE: No piece selected"
                else:
                    if selected_square is not None:
                        moveRow, moveCol = selected_square
                        piece = board[moveRow][moveCol]
                        if (row, col) in canMoveTo:
                            # Move the piece to the new location
                            if board[row][col] != '':
                                PieceCaptured = board[row][col]
                                if PieceCaptured[0] == 'w':
                                    whiteDead.append(PieceCaptured)
                                    print("ADDED: " + PieceCaptured)
                                else:
                                    blackDead.append(PieceCaptured)
                                    print("ADDED: " + PieceCaptured)
                            board[moveRow][moveCol] = ''
                            board[row][col] = piece
                            # Clear selected square after move
                            selected_square = None
                            piece_info = "SELECTED PIECE: No piece selected"
                            if turno == "White":
                                whiteFirstMove = False
                            else:
                                blackFirstMove = False
                            # Update turn after a valid move
                            if turno == "White": 
                                turno = "Black"
                            else: 
                                turno = "White"
                        else:
                            # Invalid move attempt
                            selected_square = None
                            piece_info = "INVALID MOVE: No piece selected"
                    else:
                        if row is None:
                            break
                        if col is None:
                            break
                        piece = board[row][col]
                        if turno == "White" and piece in ["wb", "wp", "wk", "wq", "wn", "wr"]:
                            piece_info = f"SELECTED PIECE: {piece}"
                            selected_square = (row, col)
                            getPossibleMovement(piece, row, col, board)  # Update possible moves
                        elif turno == "Black" and piece in ["bb", "bp", "bk", "bq", "bn", "br"]:
                            piece_info = f"SELECTED PIECE: {piece}"
                            selected_square = (row, col)
                            getPossibleMovement(piece, row, col, board)  # Update possible moves
                        else:
                            piece_info = "SELECTED PIECE: No piece selected"
                            selected_square = None

        win.fill(WHITE)
        draw_board(win)
        draw_pieces(win, board)
        draw_white_dead(win)
        draw_black_dead(win)
        draw_white_dead_pieces(win)
        draw_black_dead_pieces(win)
        
        # Highlight the selected square
        if selected_square:
            highlight_square(win, *selected_square, SELECTED_COLOR)
            for f in canMoveTo:
                highlight_square(win, *f, MOVE_COLOR)
                
            
        # Draw piece information
        draw_text(win, "Player 1: White", 24, BLACK, (650, 60))
        draw_text(win, "Player 2: Black", 24, BLACK, (650, 90))
        draw_text(win, "Turno: " + turno, 24, BLACK, (650, 120))
        
        draw_text(win, "Player 1 Victories: " + str(whiteVictories), 24, BLACK, (650, 170))
        draw_text(win, "Player 2 Victories: " + str(blackVictories), 24, BLACK, (650, 200))
        draw_text(win, "Draws: " + str(gameDraws), 24, BLACK, (650, 230))
        
        draw_text(win, piece_info, 24, BLACK, (650, 260))
        
        draw_text(win, "White dead Pieces", 20, BLACK, (650, 310))
        draw_text(win, "Black dead Pieces", 20, BLACK, (650, 480))
        
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()