import pygame
from pickle import load
from math import inf
pygame.init()


FRAMEWIDTH, FRAMEHEIGHT = 600, 600
CELLSIZE = FRAMEWIDTH//3
screen = pygame.display.set_mode((FRAMEWIDTH, FRAMEHEIGHT))

with open("saves/save.pkl", "rb") as file:
    QTABLE = load(file)


class Board:
    w = h = 3

    def __init__(self):
        self.arr = [[0 for _ in range(self.w)] for _ in range(self.h)]
        #self.arr = [[1, 1, 0], [0, -1, 0], [0, 0, -1]]
        self.turn = 1

        self.prev = False


    def tick(self):
        self.press()
        self.render()

    def press(self):
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()

            i, j = pos[0]//CELLSIZE, pos[1]//CELLSIZE

            if self.arr[j][i] == 0:
                self.arr[j][i] = self.turn
                self.turn = -self.turn

        if pygame.mouse.get_pressed()[2]:
            if not self.prev:
                self.getAIMove()

                self.prev = True
        else:
            self.prev = False


    def render(self):
        for j, row in enumerate(self.arr):
            for i, cell in enumerate(row):
                if cell == 1:
                    pygame.draw.line(screen, [0, 0, 0], [int((i+0.1)*CELLSIZE), int((j+0.1)*CELLSIZE)], [int((i+0.9)*CELLSIZE), int((j+0.9)*CELLSIZE)], 4)
                    pygame.draw.line(screen, [0, 0, 0], [int((i+0.1)*CELLSIZE), int((j+0.9)*CELLSIZE)], [int((i+0.9)*CELLSIZE), int((j+0.1)*CELLSIZE)], 4)

                elif cell == -1:
                    pygame.draw.circle(screen, [0, 0, 0], [int((i+0.5)*CELLSIZE), int((j+0.5)*CELLSIZE)], int(CELLSIZE*0.425), 4)


        for i in range(1, 3):
            pygame.draw.line(screen, [10, 10, 10], [i*CELLSIZE, 0], [i*CELLSIZE, FRAMEHEIGHT], 2)
            pygame.draw.line(screen, [10, 10, 10], [0, i*CELLSIZE], [FRAMEWIDTH, i*CELLSIZE], 2)

    def getMaxfQ(self):
        maxQ = [None, -inf]
        for j, row in enumerate(self.arr):
            for i, c in enumerate(row):
                if c == 0:
                    temp = tuple(tuple(self.turn if i == i2 and j == j2 else c for i2, c in enumerate(row)) for j2, row in enumerate(self.arr))

                    if temp in QTABLE:
                        print(f"From Table :: Q >{QTABLE[temp]}  IJ >[{i}, {j}]")
                        if maxQ[1] < QTABLE[temp]:
                            maxQ = ([i, j], QTABLE[temp])
                            #print(f"From Table :: Q >{QTABLE[temp]}  IJ >[{i}, {j}]")
                    elif maxQ[1] == -inf:
                        maxQ = ((i, j), 0)

                    #print(f"i: {i}  j: {j}  temp: {temp} qtable: {QTABLE[temp]}  maxQ: {maxQ}")
        print()
        return maxQ


    def getAIMove(self):
        maxfQ = self.getMaxfQ()
        act = maxfQ[0]

        if self.arr[act[1]][act[0]] == 0:
            self.arr[act[1]][act[0]] = self.turn
            self.turn = -self.turn

        else:
            print(f"Problem >> {act}")

    def getObs(self):
        return tuple([tuple(row) for row in self.arr])



def main():
    b = Board()

    while True:
        screen.fill([255, 255, 255])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        b.tick()

        pygame.display.update()


if __name__ == '__main__':
    main()

