import pygame
from sys import exit
import random

GAME_WIDTH = 590
GAME_HEIGHT = 500

TileSize = 22
GridSize = 21

row = 22
columns = 22

Grid = [[0 for c in range(columns)] for r in range(row)]

Player_X, Player_Y = 10, 10
Grid[Player_X][Player_Y] = 1

Snake_Segments = [(Player_X, Player_Y)] 

Points = -1
Direction = ""
Pause_text = ""

Tongue_X = 5
Tongue_Y = -9

Eye_L_R_X = 5
Eye_L_R_Y = 5

MOVEMENT_X = 0
MOVEMENT_Y = 0

pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
    

def draw():
    window.fill("black")

    global Tongue_X, Tongue_Y
    global Eye_L_R_X, Eye_L_R_Y

    if Direction == "w":
        Tongue_X = 5
        Tongue_Y = -9

        Eye_L_R_X = 5
        Eye_L_R_Y = 5
    if Direction == "s":
        Tongue_X = 5
        Tongue_Y = 19

        Eye_L_R_X = 5
        Eye_L_R_Y = 17
    if Direction == "d":
        Tongue_X = 19
        Tongue_Y = 5
    if Direction == "a":
        Tongue_X = -9
        Tongue_Y = 5

    # Drawing the board
    for c in range(columns - 1):
        for r in range(row - 1):
            if Grid[c][r] == 0: # Grid
                pygame.draw.rect(window, "white", (TileSize * c, TileSize * r, TileSize, TileSize), 1)
            elif Grid[c][r] == 1: # Snake Head
                pygame.draw.rect(window, (184, 114, 166), (TileSize * c + Tongue_X, TileSize * r + Tongue_Y, 11, 11)) # Tongue
                pygame.draw.rect(window, (34, 139, 34), (TileSize * c, TileSize * r, TileSize, TileSize))
                pygame.draw.rect(window, (30, 92, 43), (TileSize * c, TileSize * r, TileSize, TileSize), 1)

                pygame.draw.circle(window, ("white"), (TileSize * c + Eye_L_R_X, TileSize * r + Eye_L_R_Y), 3) #Left Eye
                pygame.draw.circle(window, ("black"), (TileSize * c + Eye_L_R_X, TileSize * r + Eye_L_R_Y - 1), 2)
                pygame.draw.circle(window, ("white"), (TileSize * c + Eye_L_R_X+11, TileSize * r + Eye_L_R_Y), 3) #Right Eye
                pygame.draw.circle(window, ("black"), (TileSize * c + Eye_L_R_X+11, TileSize * r + Eye_L_R_Y - 1), 2)

            elif Grid[c][r] == 2: # Tail Segment
                pygame.draw.rect(window, (71, 168, 71), (TileSize * c, TileSize * r, TileSize, TileSize))
                pygame.draw.rect(window, (30, 92, 43), (TileSize * c, TileSize * r, TileSize, TileSize), 1)
            elif Grid[c][r] == 3: # Apple
                Leaf = font.render("1", True, "green")
                window.blit(Leaf, ((TileSize * c) + 5, (TileSize * r) - 13))
                pygame.draw.circle(window, ("red"), (TileSize * c + 11, TileSize * r + 11), TileSize/2)


        
def points_on_grid():
    Apple_exists = any(3 in row_ for row_ in Grid)
    global Points

    if not Apple_exists:
        Points += 1
        Apple_X = random.randint(0, row - 2)
        Apple_Y = random.randint(0, columns - 2)

        if Grid[Apple_X][Apple_Y] == 1 or Grid[Apple_X][Apple_Y] == 2: # Prevent spawning Apples on the Snake
            return points_on_grid()
        Grid[Apple_X][Apple_Y] = 3


# Game Loop
Pasue = False
Playing = True
Running = True

while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
    
    fps = str(int(clock.get_fps()))
    pygame.display.set_caption(f"Snake v.0.3 by Berni | Snake Lenght: {len(Snake_Segments)} | " + Pause_text) # Window name + fps + + points + coordinates

    keys = pygame.key.get_pressed()

    if Pasue == False:
        if keys[pygame.K_w] and not Direction == "s":
            MOVEMENT_Y, MOVEMENT_X = -1, 0
            Direction = "w"
        if keys[pygame.K_s] and not Direction == "w":
            MOVEMENT_Y, MOVEMENT_X = 1, 0
            Direction = "s"
        if keys[pygame.K_a] and not Direction == "d":
            MOVEMENT_Y, MOVEMENT_X = 0, -1
            Direction = "a"
        if keys[pygame.K_d] and not Direction == "a":
            MOVEMENT_Y, MOVEMENT_X = 0, 1
            Direction = "d" 

    if keys[pygame.K_p]:
        if Pasue == True:
            Pasue = False
            Playing = True
            Pause_text = " "
        else:
            Pasue = True
            Playing = False
            Pause_text = "PAUSE" 


    if Playing == True:
        Player_X += MOVEMENT_X
        Player_Y += MOVEMENT_Y

        Snake_Segments.insert(0, (Player_X, Player_Y)) # Head at the beginning

        if len(Snake_Segments) > Points + 1:
            Last_X, Last_Y = Snake_Segments.pop() # Last element on the list
            Grid[Last_X][Last_Y] = 0
            Grid[Player_X][Player_Y] = 1
        
        for i, (Segment_X, Segment_Y) in enumerate(Snake_Segments):
            if i == 0:
                Grid[Segment_X][Segment_Y] = 1
            else:
                Grid[Segment_X][Segment_Y] = 2
            Grid[Player_X][Player_Y] = 1

        points_on_grid()
        draw()

        points_text = font.render(f"Points {Points} / 400 \n\nx:{Player_X + 1}, y:{Player_Y + 1} \nFPS: {fps} / 11 \n\nkeys: w a s d \nP - Pause", True, "white") # Displays points
        window.blit(points_text, (465, 10))
    

    if Player_X < 0 or Player_Y < 0 or Player_X == row - 1 or Player_Y == columns - 1: # Grid Borders
        GameOver_text = font.render(f"Game Over", True, "red") # Game Over text
        window.blit(GameOver_text, (465, GAME_HEIGHT/2))
        Playing = False
    
    if Points == 400:
        Winning_text = font.render(f"You Won!", True, "green") # Winning text
        window.blit(Winning_text, (465, GAME_HEIGHT/2))
        Playing = False


    pygame.display.update()
    clock.tick(11) # fps

pygame.quit()