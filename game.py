import sys
import time


class Game:
    def __init__(self, turn='X'):
        """
        initialize games board and player turn
        :param turn: could be X or O
        """
        self.board = [
            ['.', '.', '.'],
            ['.', '.', '.'],
            ['.', '.', '.']
        ]
        self.turn = turn
        # use to reset turn
        self.game_starter = turn

    def __str__(self):
        """
        return board current state str
        :return:
        """
        game_str = ""
        for i in range(3):
            for j in range(3):
                game_str += f"{self.board[i][j]} "
            game_str += '\n'
        # remove last \n
        game_str = list(game_str)[0:-2]
        return ''.join(game_str)

    def draw_board(self):
        """
        draw current board status
        :return:
        """
        for i in range(3):
            for j in range(3):
                print(f'{self.board[i][j]}', end=" ")
            print()
        print('-'*20)

    def reset_board(self):
        """
        reset board to initial state
        :return:
        """
        for i in range(3):
            for j in range(3):
                self.board[i][j] = '.'

    def is_valid(self, x, y):
        """
        check if move is valid
        :param x: coordinate
        :param y: coordinate
        :return: true if move is valid
        """
        # out of board
        if x < 0 or x > 2 or y < 0 or y > 2:
            return False
        # full
        elif self.board[x][y] != '.':
            return False
        else:
            return True

    def is_end(self):
        """
        check if game has ended and return winner or announce draw
        :return: string sign to show condition
        """
        # vertical win
        for i in range(3):
            if (
                    self.board[0][i] != '.' and
                    self.board[0][i] == self.board[1][i] and
                    self.board[1][i] == self.board[2][i]
            ):
                return self.board[0][i]
        # horizontal win
        for i in range(3):
            if (
                    self.board[i][0] != '.' and
                    self.board[i][0] == self.board[i][1] and
                    self.board[i][0] == self.board[i][2]
            ):
                return self.board[i][0]
        # main diagonal win
        if (
                self.board[0][0] != '.' and
                self.board[0][0] == self.board[1][1] and
                self.board[0][0] == self.board[2][2]
        ):
            return self.board[0][0]
        # second diagonal win
        if (
                self.board[0][2] != '.' and
                self.board[0][2] == self.board[1][1] and
                self.board[0][2] == self.board[2][0]
        ):
            return self.board[0][2]

        if self._is_board_full():
            # It's a draw
            return '.'

        return None

    def _is_board_full(self):
        """
        check if board is full
        used in is_end function
        :return: true if board is full
        """
        for i in range(3):
            for j in range(3):
                # there's an empty field
                if self.board[i][j] == '.':
                    return False
        return True

    def max_minimax(self, depth=0, max_depth=999, max_player='O', min_player='X'):
        """
        maximizer
        :param max_player: could be X or O
        :param min_player: could be O or X
        :param depth: current depth
        :param max_depth: maximum depth algorithm would traverse
        :return:
        """
        # control algorithm level
        if depth > max_depth:
            return 0, 0, 0
        # worse than the worst case
        max_val = -2
        # init x and y(coordinates)
        x = None
        y = None
        # check if game is finished
        result = self.is_end()
        if result == min_player:
            return -1, 0, 0
        elif result == max_player:
            return 1, 0, 0
        elif result == '.':
            return 0, 0, 0
        #  find best move recursively
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '.':
                    # on the empty field max player makes a move and calls min
                    self.board[i][j] = max_player
                    m, min_i, min_j = self.min_minimax(depth+1, max_depth, max_player, min_player)
                    # change m value then set new x & y
                    if m > max_val:
                        max_val = m
                        x = i
                        y = j
                    # set back the field to empty
                    self.board[i][j] = '.'
        return max_val, x, y

    def min_minimax(self, depth=0, max_depth=999, max_player='O', min_player='X'):
        """
        minimizer
        :param max_player: could be X or O
        :param min_player: could be O or X
        :param depth: current depth
        :param max_depth: maximum depth algorithm would traverse
        :return:
        """
        # control algorithm level
        if depth > max_depth:
            return 0, 0, 0
        # worse than the worst case
        min_val = 2
        # init x and y(coordinates)
        x = None
        y = None
        # check if game is finished
        result = self.is_end()
        if result == min_player:
            return -1, 0, 0
        elif result == max_player:
            return 1, 0, 0
        elif result == '.':
            return 0, 0, 0
        #  find best move recursively
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '.':
                    # on the empty field max player makes a move and calls min
                    self.board[i][j] = min_player
                    m, max_i, max_j = self.max_minimax(depth+1, max_depth, max_player, min_player)
                    # change m value then set new x & y
                    if m < min_val:
                        min_val = m
                        x = i
                        y = j
                    # set back the field to empty
                    self.board[i][j] = '.'
        return min_val, x, y

    def max_alpha_beta(self, alpha, beta, depth=0, max_depth=999):
        """
        maximizer using alpha-beta pruning
        :param alpha:
        :param beta:
        :param depth: current depth
        :param max_depth: maximum depth algorithm would traverse
        :return:
        """
        # control algorithm level
        if depth > max_depth:
            return 0, 0, 0
        # worse than the worst case
        max_val = -2
        # init x and y(coordinates)
        x = None
        y = None
        # check if game is finished
        result = self.is_end()
        if result == 'X':
            return -1, 0, 0
        elif result == 'O':
            return 1, 0, 0
        elif result == '.':
            return 0, 0, 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '.':
                    self.board[i][j] = 'O'
                    (m, min_i, in_j) = self.min_alpha_beta(alpha, beta, depth+1, max_depth=max_depth)
                    if m > max_val:
                        max_val = m
                        x = i
                        y = j
                    self.board[i][j] = '.'
                    if max_val >= beta:
                        # print("beta cut")
                        return max_val, x, y
                    if max_val > alpha:
                        alpha = max_val

        return max_val, x, y

    def min_alpha_beta(self, alpha, beta, depth=0, max_depth=999):
        """
        minimizer using alpha-beta pruning
        :param alpha:
        :param beta:
        :param depth: current depth
        :param max_depth: maximum depth algorithm would traverse
        :return:
        """
        # control algorithm level
        if depth > max_depth:
            return 0, 0, 0
        # worse than the worst case
        min_val = 2
        # init x and y(coordinates)
        x = None
        y = None
        # check if game is finished
        result = self.is_end()
        if result == 'X':
            return -1, 0, 0
        elif result == 'O':
            return 1, 0, 0
        elif result == '.':
            return 0, 0, 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '.':
                    self.board[i][j] = 'X'
                    (m, max_i, max_j) = self.max_alpha_beta(alpha, beta, depth+1, max_depth=max_depth)
                    if m < min_val:
                        min_val = m
                        x = i
                        y = j
                    self.board[i][j] = '.'
                    if min_val <= alpha:
                        # print("alpha cut")
                        return min_val, x, y
                    if min_val < beta:
                        beta = min_val
        return min_val, x, y

    def play_minimax(self):
        """
        playing the game(minimax)
        :return:
        """
        print("Choose game mode:")
        game_mode = int(
            input("\t1: Human vs AI\n\t2: AI vs Human\n\t3: Human vs Human\n\t4: AI vs AI\nEnter your choice number: ")
        )
        # Human vs AI(human is the game starter)
        if game_mode == 1:
            lvl = self._set_level_minimax()
            while True:
                # check if game is finished and what to do next
                self._end_play_minimax()

                if self.turn == 'X':
                    while True:
                        # calculate time of evaluating and its' value
                        start = time.time()
                        (m, ax, ay) = self.min_minimax(max_player='O', min_player='X')
                        end = time.time()
                        print(f'Evaluation time: {round(end-start, 2)}s')
                        # print(f'Evaluation value: {m}')
                        print(f'Recommended move: X = {ax}, Y = {ay}')
                        # choose move
                        px = int(input('Insert the X coordinate: '))
                        py = int(input('Insert the Y coordinate: '))
                        # make move
                        if self.is_valid(px, py):
                            self.board[px][py] = 'X'
                            self.turn = 'O'
                            break
                        # invalid move
                        else:
                            print('The move is not valid! Try again.')
                # If it's AI's turn
                else:
                    # calculate time of evaluating and its' value
                    start = time.time()
                    (m, ax, ay) = self.max_minimax(max_depth=lvl, max_player='O', min_player='X')
                    end = time.time()
                    print(f'Evaluation time: {round(end - start, 2)}s')
                    # print(f'Evaluation value: {m}')
                    print(f'Move: X = {ax}, Y = {ay}')
                    self.board[ax][ay] = 'O'
                    self.turn = 'X'

        # AI vs Human(ai is the game starter)
        if game_mode == 2:
            lvl = self._set_level_minimax()
            while True:
                # check if game is finished and what to do next
                self._end_play_minimax()

                if self.turn == 'X':
                    # calculate time of evaluating and its' value
                    start = time.time()
                    (m, ax, ay) = self.min_minimax(max_depth=lvl, max_player='O', min_player='X')
                    end = time.time()
                    print(f'Evaluation time: {round(end-start, 2)}s')
                    # print(f'Evaluation value: {m}')
                    print(f'Move: X = {ax}, Y = {ay}')
                    self.board[ax][ay] = 'X'
                    self.turn = 'O'
                else:
                    while True:
                        # calculate time of evaluating and its' value
                        start = time.time()
                        (m, ax, ay) = self.max_minimax(max_player='O', min_player='X')
                        end = time.time()
                        print(f'Evaluation time: {round(end - start, 2)}s')
                        # print(f'Evaluation value: {m}')
                        print(f'Recommended move: X = {ax}, Y = {ay}')
                        # choose move
                        px = int(input('Insert the X coordinate: '))
                        py = int(input('Insert the Y coordinate: '))
                        # make move
                        if self.is_valid(px, py):
                            self.board[px][py] = 'O'
                            self.turn = 'X'
                            break
                        # invalid move
                        else:
                            print('The move is not valid! Try again.')

        # Human vs Human
        elif game_mode == 3:
            while True:
                # check if game is finished and what to do next
                self._end_play_minimax()

                if self.turn == 'X':
                    while True:
                        # calculate time of evaluating and its' value
                        # start = time.time()
                        # (m, ax, ay) = self.min_minimax(max_player='O', min_player='X')
                        # end = time.time()
                        # print(f'Evaluation time: {round(end-start, 2)}s')
                        # print(f'Evaluation value: {m}')
                        # print(f'Recommended move: X = {ax}, Y = {ay}')
                        # choose move
                        px = int(input('Insert the X coordinate: '))
                        py = int(input('Insert the Y coordinate: '))
                        # make move
                        if self.is_valid(px, py):
                            self.board[px][py] = 'X'
                            self.turn = 'O'
                            break
                        # invalid move
                        else:
                            print('The move is not valid! Try again.')
                else:
                    while True:
                        # calculate time of evaluating and its' value
                        # start = time.time()
                        # (m, ax, ay) = self.max_minimax(max_player='O', min_player='X')
                        # end = time.time()
                        # print(f'Evaluation time: {round(end-start, 2)}s')
                        # print(f'Evaluation value: {m}')
                        # print(f'Recommended move: X = {ax}, Y = {ay}')
                        # choose move
                        px = int(input('Insert the X coordinate: '))
                        py = int(input('Insert the Y coordinate: '))
                        # make move
                        if self.is_valid(px, py):
                            self.board[px][py] = 'O'
                            self.turn = 'X'
                            break
                        # invalid move
                        else:
                            print('The move is not valid! Try again.')

        # AI vs AI
        elif game_mode == 4:
            while True:
                # check if game is finished and what to do next
                self._end_play_minimax()

                if self.turn == 'X':
                    # calculate time of evaluating and its' value
                    start = time.time()
                    (m, ax, ay) = self.min_minimax(max_player='O', min_player='X')
                    end = time.time()
                    print(f'Evaluation time: {round(end - start, 2)}s')
                    # print(f'Evaluation value: {m}')
                    print(f'Move: X = {ax}, Y = {ay}')
                    self.board[ax][ay] = 'X'
                    self.turn = 'O'
                else:
                    # calculate time of evaluating and its' value
                    start = time.time()
                    (m, ax, ay) = self.max_minimax(max_player='O', min_player='X')
                    end = time.time()
                    print(f'Evaluation time: {round(end - start, 2)}s')
                    # print(f'Evaluation value: {m}')
                    print(f'Move: X = {ax}, Y = {ay}')
                    self.board[ax][ay] = 'O'
                    self.turn = 'X'
        # Invalid input for game mode
        else:
            print("Invalid input")
            self.play_minimax()

    def _end_play_minimax(self):
        """
        check if game is finished and what happen next(used in play_minimax)
        :return:
        """
        if self._playing_state():
            self.reset_board()
            self.turn = self.game_starter
            print("If you want to play again enter <p> otherwise enter any key to quit: ")
            user_input = input()
            if user_input == 'p':
                return self.play_minimax()
            else:
                sys.exit()

    def _set_level_minimax(self):
        """
        set AI level for minimax(used in play_minimax)
        :return: max_depth
        """
        print("Choose AI level:")
        lvl = input("\t1: Hard\n\t2: Easy\nEnter your choice number: ")
        if lvl == '1':
            return 999
        elif lvl == '2':
            return 3
        else:
            print("Invalid input!")
            return self._set_level_minimax()

    def play_alpha_beta(self):
        """
        playing the game(alpha-beta)
        :return:
        """
        print("Choose game mode:")
        game_mode = int(
            input("\t1: Human vs AI\n\t2: AI vs Human\n\t3: Human vs Human\n\t4: AI vs AI\nEnter your choice number: ")
        )
        # Human vs AI(human is the game starter)
        if game_mode == 1:
            lvl = self._set_level_alpha_beta()
            while True:
                # check if game is finished and what to do next
                self._end_play_minimax()

                if self.turn == 'X':
                    while True:
                        # calculate time of evaluating and its' value
                        start = time.time()
                        (m, ax, ay) = self.min_alpha_beta(-2, 2)
                        end = time.time()
                        print(f'Evaluation time: {round(end-start, 2)}s')
                        # print(f'Evaluation value: {m}')
                        print(f'Recommended move: X = {ax}, Y = {ay}')
                        # choose move
                        px = int(input('Insert the X coordinate: '))
                        py = int(input('Insert the Y coordinate: '))
                        # make move
                        if self.is_valid(px, py):
                            self.board[px][py] = 'X'
                            self.turn = 'O'
                            break
                        # invalid move
                        else:
                            print('The move is not valid! Try again.')
                # If it's AI's turn
                else:
                    # calculate time of evaluating and its' value
                    start = time.time()
                    (m, ax, ay) = self.max_alpha_beta(-2, 2, max_depth=lvl)
                    end = time.time()
                    print(f'Evaluation time: {round(end - start, 2)}s')
                    # print(f'Evaluation value: {m}')
                    print(f'Move: X = {ax}, Y = {ay}')
                    self.board[ax][ay] = 'O'
                    self.turn = 'X'

        # AI vs Human(ai is the game starter)
        if game_mode == 2:
            lvl = self._set_level_alpha_beta()
            while True:
                # check if game is finished and what to do next
                self._end_play_minimax()

                if self.turn == 'X':
                    # calculate time of evaluating and its' value
                    start = time.time()
                    (m, ax, ay) = self.min_alpha_beta(-2, 2, max_depth=lvl)
                    end = time.time()
                    print(f'Evaluation time: {round(end-start, 2)}s')
                    # print(f'Evaluation value: {m}')
                    print(f'Move: X = {ax}, Y = {ay}')
                    self.board[ax][ay] = 'X'
                    self.turn = 'O'
                else:
                    while True:
                        # calculate time of evaluating and its' value
                        start = time.time()
                        (m, ax, ay) = self.max_alpha_beta(-2, 2)
                        end = time.time()
                        print(f'Evaluation time: {round(end - start, 2)}s')
                        # print(f'Evaluation value: {m}')
                        print(f'Recommended move: X = {ax}, Y = {ay}')
                        # choose move
                        px = int(input('Insert the X coordinate: '))
                        py = int(input('Insert the Y coordinate: '))
                        # make move
                        if self.is_valid(px, py):
                            self.board[px][py] = 'O'
                            self.turn = 'X'
                            break
                        # invalid move
                        else:
                            print('The move is not valid! Try again.')

        # Human vs Human
        elif game_mode == 3:
            while True:
                # check if game is finished and what to do next
                self._end_play_minimax()

                if self.turn == 'X':
                    while True:
                        # calculate time of evaluating and its' value
                        # start = time.time()
                        # (m, ax, ay) = self.min_alpha_beta(-2, 2)
                        # end = time.time()
                        # print(f'Evaluation time: {round(end-start, 2)}s')
                        # print(f'Evaluation value: {m}')
                        # print(f'Recommended move: X = {ax}, Y = {ay}')
                        # choose move
                        px = int(input('Insert the X coordinate: '))
                        py = int(input('Insert the Y coordinate: '))
                        # make move
                        if self.is_valid(px, py):
                            self.board[px][py] = 'X'
                            self.turn = 'O'
                            break
                        # invalid move
                        else:
                            print('The move is not valid! Try again.')
                else:
                    while True:
                        # calculate time of evaluating and its' value
                        # start = time.time()
                        # (m, ax, ay) = self.max_alpha_beta(-2, 2)
                        # end = time.time()
                        # print(f'Evaluation time: {round(end-start, 2)}s')
                        # print(f'Evaluation value: {m}')
                        # print(f'Recommended move: X = {ax}, Y = {ay}')
                        # choose move
                        px = int(input('Insert the X coordinate: '))
                        py = int(input('Insert the Y coordinate: '))
                        # make move
                        if self.is_valid(px, py):
                            self.board[px][py] = 'O'
                            self.turn = 'X'
                            break
                        # invalid move
                        else:
                            print('The move is not valid! Try again.')
        # AI vs AI
        elif game_mode == 4:
            while True:
                # check if game is finished and what to do next
                self._end_play_minimax()

                if self.turn == 'X':
                    # calculate time of evaluating and its' value
                    start = time.time()
                    (m, ax, ay) = self.min_alpha_beta(-2, 2)
                    end = time.time()
                    print(f'Evaluation time: {round(end - start, 2)}s')
                    # print(f'Evaluation value: {m}')
                    print(f'Recommended move: X = {ax}, Y = {ay}')
                    self.board[ax][ay] = 'X'
                    self.turn = 'O'
                else:
                    # calculate time of evaluating and its' value
                    start = time.time()
                    (m, ax, ay) = self.max_alpha_beta(-2, 2)
                    end = time.time()
                    print(f'Evaluation time: {round(end - start, 2)}s')
                    # print(f'Evaluation value: {m}')
                    print(f'Recommended move: X = {ax}, Y = {ay}')
                    self.board[ax][ay] = 'O'
                    self.turn = 'X'
        # Invalid input for game mode
        else:
            print("Invalid input")
            self.play_alpha_beta()

    def _end_play_alpha_beta(self):
        """
        check if game is finished and what happen next(used in play_alpha_beta)
        :return:
        """
        if self._playing_state():
            # reset board to the initial state
            self.reset_board()
            # reset turn to initial one
            self.turn = self.game_starter
            # play again or quit
            user_input = input("If you want to play again enter <p> otherwise enter any key to quit: ")
            if user_input == 'p':
                return self.play_alpha_beta()
            else:
                sys.exit()

    def _set_level_alpha_beta(self):
        """
        set AI level for alpha-beta(used in play_alpha_beta)
        :return: max_depth
        """
        print("Choose AI level:")
        lvl = input("\t1: Hard\n\t2: Easy\nEnter your choice number: ")
        if lvl == '1':
            return 999
        elif lvl == '2':
            return 3
        else:
            print("Invalid input!")
            return self._set_level_minimax()

    def _playing_state(self):
        """
        used in play and check game result and draw game current state
        :return:
        """
        self.draw_board()
        result = self.is_end()
        # Printing the appropriate message if the game has ended
        if result is not None:
            if result == 'X':
                print('X Win!')
            elif result == 'O':
                print('O Win!')
            elif result == '.':
                print("Draw!")
            return True
