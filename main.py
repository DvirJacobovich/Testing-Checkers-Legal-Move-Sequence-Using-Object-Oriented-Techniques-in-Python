import Checkers
import sys

def main():
    with open(sys.argv[1]) as file:
        lines = file.readlines()
        lines = [list(map(int, line.rstrip().split(','))) for line in lines]
        moves = list(map(lambda move: ((move[0], move[1]), (move[2], move[3])), lines))
        checkers = Checkers.Checkers(moves)
        checkers.game_runner()

if __name__ == "__main__":
    main()







