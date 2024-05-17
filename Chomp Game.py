import pygame
import sys
import random
import math
from copy import deepcopy


def initialize_game(screen_width, screen_height):
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Chomp Game")
    return screen


def draw_board(screen, board, cell_size):
    screen.fill((255, 255, 255))
    for row in range(len(board)):
        for col in range(len(board[0])):
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (col * cell_size, row * cell_size, cell_size, cell_size),
                0,
            )
            if board[row][col]:
                if row == len(board) - 1 and col == 0:
                    pygame.draw.circle(
                        screen,
                        (0, 255, 0),
                        (
                            col * cell_size + cell_size // 2,
                            row * cell_size + cell_size // 2,
                        ),
                        cell_size // 3,
                    )
                else:
                    pygame.draw.circle(
                        screen,
                        (210, 105, 30),
                        (
                            col * cell_size + cell_size // 2,
                            row * cell_size + cell_size // 2,
                        ),
                        cell_size // 3,
                    )
    pygame.display.flip()


def update_board(board, row, col):
    for r in range(row, -1, -1):
        for c in range(col, len(board[0])):
            board[r][c] = 0


def display_result(board, rows, cols, is_win):
    pygame.init()
    screen = pygame.display.set_mode((400, 400))
    pygame.display.set_caption("Game Over!")
    FONT_SIZE = 32
    ORANGE = (230, 82, 41)
    BLACK = (0, 0, 0)
    font = pygame.font.Font(None, FONT_SIZE)

    if is_win:
        game_over_text = "You Win :)"
    else:
        game_over_text = "You Lose :("

    game_text = font.render(game_over_text, True, ORANGE)
    text_rect = game_text.get_rect(
        center=(screen.get_width() // 2, screen.get_height() // 2)
    )

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)
        screen.blit(game_text, text_rect)
        pygame.display.flip()


def game_over(row, col):
    last_cell = row, col
    if last_cell == (rows - 1, 0):
        return True
    return False


def dimensions_input_screen(width, height):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Input Screen")
    FONT_SIZE = 32
    BUTTON_WIDTH = 100
    BUTTON_HEIGHT = 50

    rows_input_rect = pygame.Rect(100, 100, 50, 50)
    cols_input_rect = pygame.Rect(250, 100, 50, 50)
    start_button_rect = pygame.Rect(
        width // 2 - BUTTON_WIDTH // 2, 200, BUTTON_WIDTH, BUTTON_HEIGHT
    )
    rows = 0
    cols = 0

    running = True

    rows_text = ""
    cols_text = ""

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        rows = int(rows_text)
                        cols = int(cols_text)
                        if rows <= 0 or rows == cols or cols <= 0:
                            print(
                                "Number of rows and columns cannot be equal or zero or negative."
                            )
                            rows_text = ""
                            cols_text = ""
                        else:
                            return rows, cols
                    except ValueError:
                        print("Please enter valid numbers for rows and columns.")
                        rows_text = ""
                        cols_text = ""
                elif rows_input_rect.collidepoint(pygame.mouse.get_pos()):
                    rows_text += event.unicode
                elif cols_input_rect.collidepoint(pygame.mouse.get_pos()):
                    cols_text += event.unicode

            # was the start button clicked?...
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(pygame.mouse.get_pos()):
                    try:
                        rows = int(rows_text)
                        cols = int(cols_text)
                        if rows <= 0 or rows == cols or cols <= 0:
                            print(
                                "Number of rows and columns cannot be equal or zero or negative."
                            )
                            rows_text = ""
                            cols_text = ""
                        else:
                            return rows, cols
                    except ValueError:
                        print("Please enter valid numbers for rows and columns.")
                        rows_text = ""
                        cols_text = ""

        screen.fill((60, 80, 171))
        ORANGE = (235, 145, 103)
        GRAY = (200, 200, 200)
        BLACK = (0, 0, 0)
        # Draw input fields
        pygame.draw.rect(screen, GRAY, rows_input_rect, 2)
        pygame.draw.rect(screen, GRAY, cols_input_rect, 2)
        font = pygame.font.Font(None, FONT_SIZE)
        # Draw text
        rows_surface = font.render(rows_text, True, BLACK)
        cols_surface = font.render(cols_text, True, BLACK)
        screen.blit(
            rows_surface,
            (
                rows_input_rect.x + 5,
                rows_input_rect.centery - rows_surface.get_height() // 2,
            ),
        )
        screen.blit(
            cols_surface,
            (
                cols_input_rect.x + 5,
                cols_input_rect.centery - cols_surface.get_height() // 2,
            ),
        )

        # Draw start button
        pygame.draw.rect(screen, (113, 127, 189), start_button_rect)
        start_text = font.render("Start", True, ORANGE)
        screen.blit(
            start_text,
            (
                start_button_rect.x + BUTTON_WIDTH // 2 - start_text.get_width() // 2,
                start_button_rect.y + BUTTON_HEIGHT // 2 - start_text.get_height() // 2,
            ),
        )

        rows_label_surface = font.render("Rows:", True, (255, 255, 255))
        cols_label_surface = font.render("Cols:", True, (255, 255, 255))

        # Draw labels
        screen.blit(
            rows_label_surface,
            (25, rows_input_rect.centery - rows_label_surface.get_height() // 2),
        )
        screen.blit(
            cols_label_surface,
            (185, cols_input_rect.centery - cols_label_surface.get_height() // 2),
        )

        # Draw input fields
        pygame.draw.rect(screen, GRAY, rows_input_rect, 2)
        pygame.draw.rect(screen, GRAY, cols_input_rect, 2)

        # Draw text
        rows_surface = font.render(rows_text, True, ORANGE)
        cols_surface = font.render(cols_text, True, ORANGE)
        screen.blit(
            rows_surface,
            (
                rows_input_rect.x + 5,
                rows_input_rect.centery - rows_surface.get_height() // 2,
            ),
        )
        screen.blit(
            cols_surface,
            (
                cols_input_rect.x + 5,
                cols_input_rect.centery - cols_surface.get_height() // 2,
            ),
        )

        pygame.display.flip()


def evaluate(board, is_ai_turn, rows, cols):

    if board[rows - 1][0] == 0:
        if is_ai_turn:
            return -10
        else:
            return 10

    num_remaining_squares = len(non_empty_cells(board, rows, cols))
    score = num_remaining_squares

    for i in range(rows):
        for j in range(cols):
            if board[i][j]:
                score += (rows - i) * (cols - j)

    if is_ai_turn:
        return score
    else:
        return -score


def minimax(board, depth, alpha, beta, is_max_player, r, c):
    if depth == 0 or len(non_empty_cells(board, r, c)) == 0:
        return evaluate(board, is_max_player, r, c)

    if is_max_player:
        max_eval = -sys.maxsize
        for non_empty_cell in non_empty_cells(board, r, c):
            x, y = non_empty_cell
            copied_board = deepcopy(board)
            update_board(copied_board, x, y)
            eval = minimax(copied_board, depth - 1, alpha, beta, False, r, c)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = sys.maxsize
        for non_empty_cell in non_empty_cells(board, r, c):
            x, y = non_empty_cell
            copied_board = deepcopy(board)
            update_board(copied_board, x, y)
            eval = minimax(copied_board, depth - 1, alpha, beta, True, r, c)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


def non_empty_cells(board, rows, cols):
    non_empty_cells = []
    for x in range(rows):
        for y in range(cols):
            if board[x][y]:
                non_empty_cells.append((x, y))
    return non_empty_cells


def find_best_move(board, rows, cols):
    best_eval = -math.inf
    best_move = None
    alpha = -sys.maxsize
    beta = sys.maxsize
    for non_empty_cell in non_empty_cells(board, rows, cols):
        x, y = non_empty_cell
        copied_board = deepcopy(board)
        row = x
        col = y
        update_board(copied_board, row, col)
        eval = minimax(copied_board, 3, alpha, beta, True, rows, cols)
        if eval > best_eval:
            best_eval = eval
            best_move = (x, y)
        alpha = max(alpha, eval)
    return best_move


def ai_turn(board, rows, cols):
    # now we will call best move to find the best current move for the ai
    move = find_best_move(board, rows, cols)
    for i in range(rows):
        for j in range(cols):
            print(board[i][j], end=" ")
        print()
    return move


def start_game_graphics(rows, cols):
    cell_size = 50

    screen_width = cols * cell_size
    screen_height = rows * cell_size

    screen = initialize_game(screen_width, screen_height)
    board = [[1] * cols for _ in range(rows)]
    draw_board(screen, board, cell_size)
    running = True
    first_turn = round(random.randint(1, 2), 0)  # 1 for AI 2 for human

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if first_turn == 2:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    col = mouse_pos[0] // cell_size
                    row = mouse_pos[1] // cell_size
                    if 0 <= row < rows and 0 <= col < cols:
                        update_board(board, row, col)
                        draw_board(screen, board, cell_size)

                        if game_over(row, col):
                            display_result(board, rows, cols, False)
                            running = False
                        else:
                            first_turn = 1
                            continue

                        # running = False
            elif first_turn == 1:
                print("ai's turn...")
                move = ai_turn(board, rows, cols)
                row, col = move
                update_board(board, row, col)
                draw_board(screen, board, cell_size)
                if game_over(row, col):
                    display_result(board, rows, cols, True)
                    running = False
                else:
                    first_turn = 2
                    continue

                # running = False

        pygame.display.update()


if __name__ == "__main__":
    rows, cols = dimensions_input_screen(400, 400)
    start_game_graphics(rows, cols)
