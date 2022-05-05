import pygame
import pygame_widgets as pw
from pygame_widgets.button import Button
import sys


def DrawGrid():
    bg = pygame.image.load('anh/bg.jpg')
    screen.blit(bg,(0,0))
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                pygame.draw.rect(screen, (255,239,213), (i * inc, j * inc, inc + 1, inc + 1))
                text = a_font.render(str(grid[i][j]), True, (0, 0, 0))
                screen.blit(text, (i * inc + 15, j * inc + 10))
    for i in range(10):
        if i % 3 == 0:
            width = 10
        else:
            width = 5
        pygame.draw.line(screen, (0, 0, 0), (i * inc, 0), (i * inc, 500), width)
        pygame.draw.line(screen, (0, 0, 0), (0, i * inc), (500, i * inc), width)

def DeleteBox(x,y):
    pygame.draw.rect(screen, (255,255,255), (x * inc, y * inc, inc + 1, inc + 1))

def form(gridArray):
    matrix = []
    for i in range(9):
        row = []
        for j in range(9):
            row.append(gridArray[j][i])
        matrix.append(row)
    return matrix

def FirstPos(gridArray):
    a = []
    for k in range(81):
        a.append({1,2,3,4,5,6,7,8,9}) #Thêm các giá trị từ 1 đến 9 vào mỗi ô trong ma trận
    for i in range(9):
        for j in range(9):
            if gridArray[i][j] == 0: #Các vị trí =0 có 1 list từ 1 -> 9 các giá trị thỏa mãn
                for ii in range(9): #Kiểm tra các hàng và cột của ô cần xét xem các giá trị nào đã có và loại bỏ nó khỏi list
                    a[i*9+j].discard(gridArray[ii][j])
                    a[i*9+j].discard(gridArray[i][ii])
                ii = i // 3
                jj = j // 3
                for i1 in range(ii * 3, ii * 3 + 3): #Vòng lặp giúp kiểm tra 9 ô vuông
                    for j1 in range(jj * 3, jj * 3 + 3):
                        a[i*9+j].discard(gridArray[i1][j1])
    min = 10
    x = -1 #x là hàng
    y = -1 #y là cột
    se = {} # tập thỏa mãn
    for k in range(81): 
        if (len(a[k])) < min and gridArray[k//9][k%9] == 0: #Với các len() của a nhỏ nhất và với vị trí trong bảng == 0
            x = k//9
            y = k%9
            min = len(a[k]) #lấy độ dài list nhỏ nhất 
            se = a[k].copy() #Tập các giá trị thỏa mãn
    return (x,y,se)

def SolveGrid(gridArray, i, j):

    global IsSolving
    IsSolving = False
    i = FirstPos(gridArray)[0]
    j = FirstPos(gridArray)[1]
    print(str(i)+" "+str(j))
    if i == -1 and j == -1:
        return True
    pygame.event.pump()
    for V in range(1, 10):
        if IsUserValueValid(gridArray, i, j, V):
            gridArray[i][j] = V
            if SolveGrid(gridArray, i, j):
                return True
            else:
                gridArray[i][j] = 0
        screen.fill((255, 255, 255))
        DrawGrid()
        DrawSelectedBox()
        DrawModes()
        pygame.display.update()
        pygame.time.delay(0)
    return False


def SetMousePosition(p):
    global x, y
    if p[0] < 500 and p[1] < 500:
        x = p[0] // inc
        y = p[1] // inc


def IsUserValueValid(m, i, j, v):
    for ii in range(9):
        if m[i][ii] == v or m[ii][j] == v:
            return False

    ii = i // 3
    jj = j // 3
    for i in range(ii * 3, ii * 3 + 3):
        for j in range(jj * 3, jj * 3 + 3):
            if m[i][j] == v:
                return False
    return True


def DrawSelectedBox():
    for i in range(2):
        pygame.draw.line(screen, (0, 0, 255), (x * inc, (y + i) * inc), (x * inc + inc, (y + i) * inc), 5)
        pygame.draw.line(screen, (0, 0, 255), ((x + i) * inc, y * inc), ((x + i) * inc, y * inc + inc), 5)


def InsertValue(Value):
    grid[int(x)][int(y)] = Value
    text = a_font.render(str(Value), True, (0, 0, 0))
    screen.blit(text, (x * inc + 15, y * inc + 15))


def IsUserWin():
    for i in range(9):
        for j in range(9):
            if grid[int(i)][int(j)] == 0:
                return False
    return True


def DrawModes():
    TitleFont = pygame.font.SysFont("times", 20, "bold")
    AttributeFont = pygame.font.SysFont("times", 20)
    screen.blit(TitleFont.render("Game Settings", True, (0, 0, 0)), (15, 505))
    screen.blit(AttributeFont.render("C: clear", True, (0, 0, 0)), (30, 530))
    screen.blit(AttributeFont.render("X: Xóa", True, (0, 0, 0)), (30, 555))
    screen.blit(TitleFont.render("Modes", True, (0, 0, 0)), (15, 580))
    screen.blit(AttributeFont.render("E: Easy", True, (0, 0, 0)), (30, 605))
    screen.blit(AttributeFont.render("A: Average", True, (0, 0, 0)), (30, 630))
    screen.blit(AttributeFont.render("H: Hard", True, (0, 0, 0)), (30, 655))
    screen.blit(TitleFont.render("Space: auto", True, (0, 0, 0)), (350, 580))


def DisplayMessage(Message, Interval, Color):
    screen.blit(a_font.render(Message, True, Color), (220, 530))
    pygame.display.update()
    pygame.time.delay(Interval)
    screen.fill((255, 255, 255))
    DrawModes()


def SetGridMode(Mode):
    global grid
    screen.fill((255, 255, 255))
    DrawModes()
    if Mode == 0:
        grid = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
    elif Mode == 1:
        grid = [
            [4, 1, 0, 2, 7, 0, 8, 0, 5],
            [0, 8, 5, 1, 4, 6, 0, 9, 7],
            [0, 7, 0, 5, 8, 0, 0, 4, 0],
            [9, 2, 7, 4, 5, 1, 3, 8, 6],
            [5, 3, 8, 6, 9, 7, 4, 1, 2],
            [1, 6, 4, 3, 2, 8, 7, 5, 9],
            [8, 5, 2, 7, 0, 4, 9, 0, 0],
            [0, 9, 0, 8, 0, 2, 5, 7, 4],
            [7, 4, 0, 9, 6, 5, 0, 2, 8],
        ]
    elif Mode == 2:
        grid = [
            [7, 8, 0, 4, 0, 0, 1, 2, 0],
            [6, 0, 0, 0, 7, 5, 0, 0, 9],
            [0, 0, 0, 6, 0, 1, 0, 7, 8],
            [0, 0, 7, 0, 4, 0, 2, 6, 0],
            [0, 0, 1, 0, 5, 0, 9, 3, 0],
            [9, 0, 4, 0, 6, 0, 0, 0, 5],
            [0, 7, 0, 3, 0, 0, 0, 1, 2],
            [1, 2, 0, 0, 0, 7, 4, 0, 0],
            [0, 4, 9, 2, 0, 6, 0, 0, 7]
        ]
    elif Mode == 3:
        grid = [
            [0, 0, 0, 0, 0, 5, 7, 0, 0],
            [0, 5, 0, 0, 2, 0, 0, 4, 0],
            [0, 0, 7, 9, 0, 0, 0, 0, 8],
            [0, 0, 1, 0, 0, 8, 0, 0, 3],
            [0, 9, 0, 0, 1, 0, 0, 8, 0],
            [7, 0, 0, 5, 0, 0, 9, 0, 0],
            [3, 0, 0, 0, 0, 2, 6, 0, 0],
            [0, 8, 0, 0, 6, 0, 0, 7, 0],
            [0, 0, 9, 1, 0, 0, 0, 0, 0],
        ]


def HandleEvents():
    global IsRunning, grid, x, y, UserValue
    myF = FirstPos(grid)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            IsRunning = False
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            SetMousePosition(pygame.mouse.get_pos())
        if event.type == pygame.KEYDOWN:
            if not IsSolving:
                if event.key == pygame.K_LEFT:
                    x -= 1
                if event.key == pygame.K_RIGHT:
                    x += 1
                if event.key == pygame.K_UP:
                    y -= 1
                if event.key == pygame.K_DOWN:
                    y += 1
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    UserValue = 1
                if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    UserValue = 2
                if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    UserValue = 3
                if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    UserValue = 4
                if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    UserValue = 5
                if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    UserValue = 6
                if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    UserValue = 7
                if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    UserValue = 8
                if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    UserValue = 9
                if event.key == pygame.K_c:
                    SetGridMode(0)
                if event.key == pygame.K_e:
                    SetGridMode(1)
                if event.key == pygame.K_a:
                    SetGridMode(2)
                if event.key == pygame.K_h:
                    SetGridMode(3)
                if event.key == pygame.K_SPACE:
                    SolveGrid(grid,0,0)
                if event.key == pygame.K_s:
                    print("Cot: "+ str(myF[0]+1)+" Hang: "+str(myF[1]+1))
                    print(myF[2])
                if event.key == pygame.K_x:
                    print(str(x)+" "+str(y))
                    grid[x][y] = 0
                    DeleteBox(x,y)
                if event.key == pygame.K_p:
                    for i in range(9):
                        print(grid[i])
            DrawUserValue()


def DrawUserValue():
    global UserValue, IsSolving
    if UserValue > 0:
        if IsUserValueValid(grid, x, y, UserValue):
            if grid[int(x)][int(y)] == 0:
                InsertValue(UserValue)
                UserValue = 0
                if IsUserWin():
                    IsSolving = False
                    DisplayMessage("YOU WON!!!!", 5000, (0, 255, 0))
            else:
                UserValue = 0
        else:
            DisplayMessage("Incorrect Value", 500, (255, 0, 0))
            UserValue = 0


def InitializeComponent():
    DrawGrid()
    DrawSelectedBox()
    DrawModes()
    pygame.display.update()


def GameThread():
    InitializeComponent()
    while IsRunning:
        bg = pygame.image.load('anh/bg.jpg')
        screen.blit(bg,(0,0))
        HandleEvents()
        DrawGrid()
        DrawModes()
        DrawSelectedBox()
        DrawUserValue()
        pygame.display.update()


if __name__ == '__main__':
    pygame.font.init()
    screen = pygame.display.set_mode((500, 675))
    screen.fill((255, 255, 255))
    pygame.display.set_caption("SudokuApp")
    a_font = pygame.font.SysFont("times", 30, "bold")
    b_font = pygame.font.SysFont("times", 15, "bold")
    inc = 500 // 9
    x = 0
    y = 0
    UserValue = 0
    grid = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7],
    ]
    IsRunning = True
    IsSolving = False
    GameThread()
