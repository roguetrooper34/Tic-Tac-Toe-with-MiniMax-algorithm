from random import randint

winning_moves = (0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)

playerA_score = {"Wins": 0, "Losses": 0, "Ties": 0}
playerB_score = {"Wins": 0, "Losses": 0, "Ties": 0}
AI_score = {"Wins": 0, "Losses": 0, "Ties": 0}
AIsmart_score = {"Wins": 0, "Losses": 0, "Ties": 0}

game_board = [0] * 9


def print_game_board():
    for i, x in enumerate(game_board):
        end = ' | '
        if i % 3 == 2:
            end = ' \n'
            end += '---------\n'
        char = ' '
        if x == 1:
            char = "O"
        elif x == 2:
            char = "X"
        print(char, end=end)


def input_player_move(turn):
    if turn % 2 == 1:
        turn = 1
    elif turn % 2 == 0:
        turn = 2
    move = int(input("Please enter a move[1-9] for player {0}: ".format(turn)))
    while not (1 <= move <= 9) or game_board[move - 1] != 0:
        print("Invalid move!")
        move = int(input("Please enter a move[1-9] for player {0}: ".format(turn)))

    if turn == 1:
        game_board[move - 1] = 1
    else:
        game_board[move - 1] = 2
    print_game_board()
    print(f"\nPlayer {turn} makes a move to {move} square.\n")


def game_won():
    player_won = 0
    for tup in winning_moves:
        if game_board[tup[0]] == 1 and game_board[tup[1]] == 1 and game_board[tup[2]] == 1:
            player_won = 1
            break
        if game_board[tup[0]] == 2 and game_board[tup[1]] == 2 and game_board[tup[2]] == 2:
            player_won = 2
            break
    return player_won


def make_game_board():
    global game_board
    game_board = [0] * 9


def human_vs_human(alternate_player):
    global playerA_score
    global playerB_score
    player_turn = 1
    make_game_board()
    print_game_board()
    input_player_move(player_turn)
    player_turn += 1
    while 0 in game_board:
        input_player_move(player_turn)
        if game_won() == 1:
            print("Player 1 won!")
            if alternate_player:
                playerB_score["Wins"] += 1
                playerA_score["Losses"] += 1
            else:
                playerA_score["Wins"] += 1
                playerB_score["Losses"] += 1
            break
        elif game_won() == 2:
            print("Player 2 won!")
            if alternate_player:
                playerA_score["Wins"] += 1
                playerB_score["Losses"] += 1
            else:
                playerB_score["Wins"] += 1
                playerA_score["Losses"] += 1
            break
        player_turn += 1
    if game_won() == 0:
        print("Game is a tie!")
        playerA_score["Ties"] += 1
        playerB_score["Ties"] += 1


def human_vs_ai():
    print("Not coded yet\n\n")


def human_vs_smartai(alternate_move):
    def minimax(other_turn):  # AI Char must be 1 or -1, 1 representing first turn playing Os, and -1
        # representing second turn playing Xs
        if game_won() == 1:
            return 1 * (1 + game_board.count(0))
        if game_won() == 2:
            return -1 * (1 + game_board.count(0))
        if 0 not in game_board:
            return 0

        if other_turn:
            best = 1000
            for i, x in enumerate(game_board):
                if x == 0:
                    game_board[i] = 2
                    best = min(best, minimax(False))
                    game_board[i] = 0
            return best
        else:
            best = -1000
            for i, x in enumerate(game_board):
                if x == 0:
                    game_board[i] = 1
                    best = max(best, minimax(True))
                    game_board[i] = 0
            return best

    def minimax_reverse(other_turn):
        if game_won() == 2:
            return 1 * (1 + game_board.count(0))
        if game_won() == 1:
            return -1 * (1 + game_board.count(0))
        if 0 not in game_board:
            return 0

        if other_turn:
            best = 1000
            for i, x in enumerate(game_board):
                if x == 0:
                    game_board[i] = 1
                    best = min(best, minimax_reverse(False))
                    game_board[i] = 0
            return best

        else:
            best = -1000
            for i, x in enumerate(game_board):
                if x == 0:
                    game_board[i] = 2
                    best = max(best, minimax_reverse(True))
                    game_board[i] = 0
            return best

    def input_smartai_move(aifirst):
        best_val = -1000
        bestmove = -1

        if aifirst == 1:
            if game_board.count(0) == 9:
                game_board[randint(0, 8)] = 1
                return 0

            for i, x in enumerate(game_board):
                if x == 0:
                    game_board[i] = 1
                    move_val = minimax(True)
                    game_board[i] = 0

                    if move_val > best_val:
                        bestmove = i
                        best_val = move_val

            game_board[bestmove] = 1
            print_game_board()
            print(f"\nAI has finally moved to {bestmove + 1}\n")

        else:
            for i, x in enumerate(game_board):
                if x == 0:
                    game_board[i] = 2
                    move_val = minimax_reverse(True)
                    game_board[i] = 0
                    if move_val > best_val:
                        bestmove = i
                        best_val = move_val

            game_board[bestmove] = 2
            print_game_board()
            print(f"\nAI has finally moved to {bestmove + 1}\n")

    global AIsmart_score
    if alternate_move:
        make_game_board()
        input_smartai_move(1)
        print_game_board()
        input_player_move(2)
        print_game_board()
        current_turn = 1
        while 0 in game_board:
            if current_turn % 2 == 1:
                input_smartai_move(1)
                print_game_board()
                if game_won() == 1:
                    print("AI wins!")
                    AIsmart_score["Wins"] += 1
                    break
                current_turn += 1
            elif current_turn % 2 == 0:
                input_player_move(2)
                print_game_board()
                if game_won() == 2:
                    print("You have done the impossible! Player wins!")
                    AIsmart_score["Losses"] += 1
                    break
                current_turn += 1
    else:
        make_game_board()
        print_game_board()
        input_player_move(1)
        input_smartai_move(-1)
        current_turn = 1
        while 0 in game_board:
            if current_turn % 2 == 1:
                input_player_move(1)
                if game_won() == 1:
                    print("You have done the impossible! Player wins!")
                    AIsmart_score["Losses"] += 1
                    break
                current_turn += 1
            elif current_turn % 2 == 0:
                input_smartai_move(-1)
                if game_won() == 2:
                    print("AI wins!")
                    AIsmart_score["Wins"] += 1
                    break
                current_turn += 1
    if game_won() == 0:
        print("Game is a tie!")
        AIsmart_score["Ties"] += 1


def ask_player_game_option():
    print("Welcome to Tic-Tac-Toe project for IST 1st Semester")
    print("Option 0: Close game")
    print("Option 1: Human vs Human")
    print("Option 2: Human vs AI")
    print("Option 3: Human vs Smart AI")
    game_option = int(input("Please enter a valid option [0-3]: "))
    return game_option


def main():
    try:
        game_option = ask_player_game_option()
        while not (0 <= game_option <= 3):
            print("Invalid choice!")
            game_option = int(input("Please enter a valid option [0-3]: "))
        while True:
            match game_option:
                case 0:
                    print("Ending game")
                    break
                case 1:  # Human Player
                    print("Is Player A going first? (type Y for yes)")
                    who_first = input("")
                    if who_first.lower() == "y":
                        human_vs_human(False)
                    else:
                        human_vs_human(True)
                    print("Score for player A is {0}".format(playerA_score))
                    print("Score for player B is {0}".format(playerB_score))
                    print("\n\n")
                    game_option = ask_player_game_option()
                case 2:  # AI
                    human_vs_ai()
                    game_option = ask_player_game_option()
                case 3:  # Smart AI
                    print("Are you going to play first?")
                    which_first = input("Type Y to confirm: ")
                    if which_first.lower() == "y":
                        human_vs_smartai(False)
                    else:
                        human_vs_smartai(True)

                    print()
                    print(f"Score for Smart AI is {AIsmart_score}")
                    print("\n\n")
                    game_option = ask_player_game_option()
    except ValueError:
        print("\n\nPlease only enter integer values! Program crashing...")
    except KeyboardInterrupt:
        print("\n\nClosing program forcefully...")


main()
