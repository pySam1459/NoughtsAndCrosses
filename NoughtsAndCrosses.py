from random import random, choice, sample
from pickle import dump, load
from math import inf


class Board:
    w = h = 3
    chars = {0: ' ', 1: 'X', -1: 'O'}

    def __init__(self, table):
        self.arr = [[0 for _ in range(3)] for _ in range(3)]
        #self.arr = [[1, 1, 0], [0, -1, 0], [0, 0, -1]]
        self.turn = 1

        self.table = table
        self.ijs = self.getIJs()

    def ai(self):
        maxfQ = [-inf, (1, 1)]
        for j in range(3):
            for i in range(3):
                if self.arr[j][i] == 0:
                    temp = self.getTemp([i, j])

                    if temp in self.table:
                        q = self.table[temp]
                        if q > maxfQ[0]:
                            maxfQ = [q, (i, j)]
        if maxfQ[0] == -inf:
            return None
        return maxfQ

    def randomAction(self):
        pos = [(i, j) for i in range(3) for j in range(3) if self.arr[j][i] == 0]

        act = choice(pos)
        temp = self.getTemp(act)
        fq = 0
        if temp in self.table:
            fq = self.table[temp]

        return fq, act

    def set(self, act):
        self.arr[act[1]][act[0]] = self.turn
        self.turn = -self.turn

    def checkWin(self):
        for ijs in self.ijs:
            winner = 0
            for i, j in ijs:
                if self.arr[j][i] == 0:
                    break
                elif self.arr[j][i] == winner or winner == 0:
                    winner = self.arr[j][i]
                elif self.arr[j][i] != winner:
                    break
            else:
                return winner

        draw = True
        for j in range(3):
            for i in range(3):
                if self.arr[j][i]  == 0:
                    draw = False

        if draw:
            return 2

        return 0

    @staticmethod
    def getIJs():
        array = []
        for j in range(Board.h):
            array += [[(i, j) for i in range(Board.w)]]
        for i in range(Board.w):
            array += [[(i, j) for j in range(Board.h)]]
        array += [[(k, k) for k in range(min(Board.w, Board.h))]]
        array += [[(k, 2-k) for k in range(min(Board.w, Board.h))]]
        return array

    def getTemp(self, act):
        return tuple(tuple(self.turn if act[0] == i2 and act[1] == j2 else c for i2, c in enumerate(row)) for j2, row in enumerate(self.arr))

    def getObs(self):
        return tuple([tuple(row) for row in self.arr])

    def print(self):
        for j in range(self.h):
            for i in range(self.w):
                print(self.chars[self.arr[j][i]], end="")
                if i < self.w-1:
                    print("|", end="")
                else:
                    print()
            if j < self.h-1:
                print("-+"*(self.w-1) + "-")


def main():
    EPISODES = 5000000
    EPSILON = 1.0
    DECAY = 0.99999
    DISCOUNT = 0.9
    LR = 0.2
    ITERATIONS = 9
    DISPLAY_UPDATE = 25000
    DEFAULT_QVALUE = 0

    REWARDS = [1, -1, 0.5]
    X, Y = [], []
    NUM_AVR = 2500

    LOAD_TABLE_FROM_FILE = False
    if LOAD_TABLE_FROM_FILE:
        with open("saves/save.pkl", "rb") as file:
            table = load(file)
    else:
        table = {}

    episodesReward = 0
    for ep in range(1, EPISODES+1):
        b = Board(table)

        if ep % DISPLAY_UPDATE == 0:  # SHOW RESULTS OF TRAINING
            print(f"Episode {ep}  |  Epsilon {EPSILON}")
            with open("saves/save2.pkl", "wb") as file, open("graphdata/graph.pkl", "wb") as file2:
                dump(table, file)
                dump({"X": X, "Y": Y}, file2)

        winner = 0
        history = []
        for _ in range(ITERATIONS):
            randomize = True
            act, cq = None, 0
            if random() > EPSILON:
                cq = b.ai()
                if cq is not None:
                    randomize = False
                    cq, act = cq

            if randomize:
                cq, act = b.randomAction()


            b.set(act)
            fq = b.ai()
            fq = DEFAULT_QVALUE if fq is None else fq[0]
            history.append([b.getObs(), -b.turn, cq, fq])

            w =  b.checkWin()
            if w:
                winner = w
                if winner != 2:
                    history[-1][3] = REWARDS[0]
                elif winner == 2:
                    history[-1][3] = REWARDS[2]

                break


        if winner == 2:
            rc = rn = REWARDS[2]

        else:
            rc = REWARDS[0] if winner == 1 else REWARDS[1]
            rn = REWARDS[0] if winner == -1 else REWARDS[1]
            episodesReward += winner

        for state in sample(history, 5):  #min(5, len(history))):
            reward = rc if state[1] == 1 else rn
            newQ = (1 - LR) * state[2] + LR * (reward - DISCOUNT * state[3])

            table[state[0]] = newQ


        if EPSILON/DECAY >= 0.025:
            EPSILON *= DECAY

        if ep % NUM_AVR == 0:
            X.append(ep//NUM_AVR)
            Y.append(episodesReward/NUM_AVR)
            episodesReward = 0



if __name__ == '__main__':
    main()
