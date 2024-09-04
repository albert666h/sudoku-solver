import numpy as np
import pygame

# Creating a simple UI with pygame

pygame.init()

window = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
fps = 60

# Colours

BG = (255, 203, 154)
GRID = (44, 53, 50)
TEXT = (15, 100, 102)
SELECTED = (255, 52, 37)

# Rendering

font = pygame.font.Font('font.ttf', 50)

def draw_number(n, pos):
    text = font.render(f'{n}', True, GRID)
    window.blit(text, pos)

def grid():
    pygame.draw.rect(window, GRID, (30, 30, 540, 540), 4, 10)
    for i in range(1, 9, 1):
        w = 3
        if i % 3 == 0: w = 4
        pygame.draw.line(window, GRID, (30 + 60 * i, 30), (30 + 60 * i, 569), w)
        pygame.draw.line(window, GRID, (30, 30 + 60 * i), (569, 30 + 60 * i), w)

def fill_grid():
    for y in range(9):
        for x in range(9):
            if puzzle[y][x]: draw_number(puzzle[y][x], (45 + x * 60, 40 + y * 60))

def selected_grid(pos):
    pygame.draw.rect(window, SELECTED, (30 + pos[0] * 60, 30 + pos[1] * 60, 60, 60), 4, 10)

# The actual Sudoku solver
puzzle = np.zeros((9, 9), dtype="int")


# Creating a binary map for all of the digits (index 0 -> digit 1 etc.)
temp = np.ones((9 ,9, 9))

# Sets all the illegal squares for the given digit to 0
def clear_for(i: int):
    i -= 1
    for y in range(9):
        for x in range(9):
            if puzzle[y][x] == i + 1:
                # Checking 3x3 squares
                for a in range(3):
                    for b in range(3):
                        if not (a == y and b == x):
                            temp[i][y - (y % 3) + a][x - (x % 3) + b] = 0
                # Checking horizontal and vertical lines
                for j in range(9):
                    if not j == x: temp[i][y][j] = 0
                    if not j == y: temp[i][j][x] = 0
            elif puzzle[y][x]:
                temp[i][y][x] = 0

# Checks the individual map of the digit to evaluate if there are any definite soultions and writes them to the puzzle
def write_for(i: int):
    i -= 1
    r = False
    for y in range(9):
        for x in range(9):
            if temp[i][y][x]:
                s = 0
                # Chechking 3x3 squares
                for a in range(3):
                    for b in range(3):
                        s += temp[i][y - (y % 3) + a][x - (x % 3) + b]
                # Checking if there is only one cancidate in the 3x3 square
                if s == 1:
                    puzzle[y][x] = i + 1
                    r = True
                else:
                    # Checking horizontal and vertical lines
                    for j in range(9):
                        s += temp[i][y][j]
                        s += temp[i][j][x]
                    if s <= 3:
                        puzzle[y][x] = i + 1
                        r = True
    return r
                    
if __name__ == "__main__":
    # Creating a mode for the program (0 -> user input 1 -> solve)
    mode = False
    run = True
    pos = np.array([0, 0])
    while run:
        window.fill(BG)
        clock.tick(fps)

        grid()
        fill_grid()
        
        if mode:
            for i in range(9):
                clear_for(i + 1)
                write_for(i + 1)
            if  np.sum(puzzle) == 405:
                mode = False
        else:
            selected_grid(pos)

        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
                break
            if e.type == pygame.KEYDOWN:
                if not mode:
                    # Moving the selected cell
                    if e.key == pygame.K_w:
                        if pos[1] > 0:
                            pos[1] -= 1
                    elif e.key == pygame.K_s:
                        if pos[1] < 8:
                            pos[1] += 1
                    elif e.key == pygame.K_a:
                        if pos[0] > 0:
                            pos[0] -= 1
                    elif e.key == pygame.K_d:
                        if pos[0] < 8:
                            pos[0] += 1
                    
                    # Writing into the cell
                    elif e.key == pygame.K_0:
                        puzzle[pos[1]][pos[0]] = 0
                    elif e.key == pygame.K_1:
                        puzzle[pos[1]][pos[0]] = 1
                    elif e.key == pygame.K_2:
                        puzzle[pos[1]][pos[0]] = 2
                    elif e.key == pygame.K_3:
                        puzzle[pos[1]][pos[0]] = 3
                    elif e.key == pygame.K_4:
                        puzzle[pos[1]][pos[0]] = 4
                    elif e.key == pygame.K_5:
                        puzzle[pos[1]][pos[0]] = 5
                    elif e.key == pygame.K_6:
                        puzzle[pos[1]][pos[0]] = 6
                    elif e.key == pygame.K_7:
                        puzzle[pos[1]][pos[0]] = 7
                    elif e.key == pygame.K_8:
                        puzzle[pos[1]][pos[0]] = 8
                    elif e.key == pygame.K_9:
                        puzzle[pos[1]][pos[0]] = 9

                # Pressing Enter  will switch the mode
                if e.key == pygame.K_RETURN:
                    mode = not mode
                        
 
    
    pygame.quit()

   
    