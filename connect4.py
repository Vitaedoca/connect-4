import numpy as np
import random
import math

# Define as peças
PLAYER_PIECE = 1
AI_PIECE = 2

# Função para criar o tabuleiro
def create_board():
    board = [[0] * 7 for _ in range(6)]
    return board

# Verifica se a coluna é válida (não está cheia)
def is_valid_location(board, col):
    return board[5][col] == 0

# Encontra a próxima linha disponível na coluna
def get_next_open_row(board, col):
    for row in range(6):
        if board[row][col] == 0:
            return row
    return -1

# Adiciona uma peça no tabuleiro
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Verifica se alguém ganhou (horizontal, vertical, diagonal)
def winning_move(board, piece):
    # Verificar linhas, colunas e diagonais
    for c in range(7 - 3):
        for r in range(6):
            if all(board[r][c + i] == piece for i in range(4)):
                return True

    for c in range(7):
        for r in range(6 - 3):
            if all(board[r + i][c] == piece for i in range(4)):
                return True

    for c in range(7 - 3):
        for r in range(6 - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True

    for c in range(7 - 3):
        for r in range(3, 6):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True

    return False

# Função de avaliação simples, pontuando com base na vitória
def score_position(board, piece):
    if winning_move(board, piece):
        return 1000  # Grande recompensa por ganhar
    else:
        return 0  # Caso contrário, não há recompensa

# Função minimax (sem poda alfa-beta)
def minimax(board, depth, maximizingPlayer):
    valid_locations = [col for col in range(7) if is_valid_location(board, col)]
    
    # Caso base: profundidade 0 ou vitória
    if depth == 0 or not valid_locations:
        return None, score_position(board, AI_PIECE) if maximizingPlayer else score_position(board, PLAYER_PIECE)

    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)  # Escolher uma coluna aleatória como fallback
        for col in valid_locations:
            row = get_next_open_row(board, col)
            board_copy = [row.copy() for row in board]  # Copiar o tabuleiro
            drop_piece(board_copy, row, col, AI_PIECE)
            new_score = minimax(board_copy, depth-1, False)[1]
            if new_score > value:
                value = new_score
                column = col
        return column, value
    else:
        value = math.inf
        column = random.choice(valid_locations)  # Escolher uma coluna aleatória como fallback
        for col in valid_locations:
            row = get_next_open_row(board, col)
            board_copy = [row.copy() for row in board]  # Copiar o tabuleiro
            drop_piece(board_copy, row, col, PLAYER_PIECE)
            new_score = minimax(board_copy, depth-1, True)[1]
            if new_score < value:
                value = new_score
                column = col
        return column, value

# Função principal para jogar
def play_game():
    board = create_board()
    game_over = False
    while not game_over:
        # Jogador
        col = int(input("Escolha uma coluna (0-6): "))
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, PLAYER_PIECE)

            if winning_move(board, PLAYER_PIECE):
                print("Você ganhou!")
                game_over = True

        # Computador (AI)
        if not game_over:
            print("É a vez da AI!")
            col, _ = minimax(board, 4, True)  # A profundidade pode ser ajustada
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)

            if winning_move(board, AI_PIECE):
                print("A AI ganhou!")
                game_over = True

        # Exibir o tabuleiro
        for row in board:
            print(row)

# Iniciar o jogo
play_game()
