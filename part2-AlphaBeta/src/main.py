from alphabeta import TicTacToe
from alphabeta import alpha_beta_value

def gameover(state, me, ai):
    if state.won(me):
        print("You won!")
        return True
    if state.won(ai):
        print("Better luck next time!")
        return True
    if state.is_end_state():
        print("It's a tie")
        return True
    return False

def play(state):
    """Makes turn and prints the result of it until the game is over
    :param state: The initial state of the game (TicTacToe)
    """
    me = input("Play as x or o: ")
    if me == "x": ai = "o"
    else: ai = "x"
    print("Starting position")
    print(state)
    if me == "x":
        while True:
            i = int(input("Your turn, type (0-8): "))
            board = list(state.getstate())
            board[i] = "x"
            state = TicTacToe("".join(board), False)
            print(state)
            if gameover(state, me, ai): break
            print("AI's turn")
            state, val = alpha_beta_value(state)
            print(state)
            if gameover(state, me, ai): break
    else:
        while True:
            print("AI's turn")
            state, val = alpha_beta_value(state)
            print(state)
            if gameover(state, me, ai): break
            i = int(input("Your turn, type (0-8): "))
            board = list(state.getstate())
            board[i] = "o"
            state = TicTacToe("".join(board), True)
            print(state)
            if gameover(state, me, ai): break
        
def main():
    """You need to implement the following functions/methods:
    play(state): makes turn and prints the result of it until the game is over
    value() in TicTacToe class: returns the current score of the game
    generate_children() in TicTacToe class: returns a list of all possible states after this turn
    alpha_beta_value(node): implements the MinMax algorithm with alpha-beta pruning
    max_value(node, alpha, beta): implements the MinMax algorithm with alpha-beta pruning
    min_value(node, alpha, beta):implements the MinMax algorithm with alpha-beta pruning
    """
    empty_board = 3 * '???'
    board = "xoo?x??xo"
    state = TicTacToe(empty_board, True)
    play(state)

if __name__ == '__main__':
    main()
