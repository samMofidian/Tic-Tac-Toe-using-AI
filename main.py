"""
AI Final Project: Tic Tac Toe
Author: sAm Mofidian
Last Update: 1/22/2023
"""
from game import Game


def run():
    """
    select playing algorithm
    :return:
    """
    # initial message
    print("*"*51)
    print(" "*20 + "Tic-Tac-Toe" + " "*20)
    print("*"*51)
    # init game
    game = Game()
    # choose algorithm(minimax vs alpha-beta)
    alg = input("Choose the algorithm\n\t1: Alpha-Beta\n\t2: minimax\nEnter the algorithm number: ")
    if alg == '1':
        game.play_alpha_beta()
    elif alg == '2':
        game.play_minimax()
    # invalid input
    else:
        print("Invalid input!")
        return run()


if __name__ == '__main__':
    run()
