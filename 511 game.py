import pygame
import time
import random

pygame.init()

white = (255,255,255) # Define colors using rgb
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)
pastel_red = (255, 105, 97)

block_size = 100

display_width = block_size * 3
display_height = block_size * 3

gameDisplay = pygame.display.set_mode((display_width,display_height)) #creates display block_width wide and block_height tall
pygame.display.set_caption('511') # title of window

clock = pygame.time.Clock()

FPS = 30

font = pygame.font.SysFont(None, 20)
num_font = pygame.font.SysFont(None, 35)
smallfont = pygame.font.SysFont('None', 20)
medfont = pygame.font.SysFont(None, 50)
largefont = pygame.font.SysFont(None, 80)

gameExit = False
gameOver = False
gameWin = False

def game_intro(): #prints info about game to screen
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(white)
        message_to_screen('Welcome to 511', green, -100, 'medium')
       
        message_to_screen('The objective of the game is to add the tiles', black, -30, 'small')
        message_to_screen('until you reach 511.', black, -15, 'small')
        
        message_to_screen('You can move the tiles using the arrow keys.', black, 10, 'small')
        
        message_to_screen('If two tiles of the same value bump', black, 30, 'small')
        message_to_screen('into each other', black, 45, 'small')
        message_to_screen('they will merge into one.', black, 60, 'small')
        
        message_to_screen('Press C to play or Q to quit', red, 120, 'small')
        pygame.display.update()
        clock.tick(15)

def main():
    global gameExit
    global gameOver
    global gameWin

    gameExit = False
    gameOver = False
    gameWin = False

    grid = [[0,0,0],
            [0,0,0],
            [0,0,0]]

    new_num_val = 1

    #spawn the first two random values
    spawn_value(grid, new_num_val)
    spawn_value(grid, new_num_val)
    draw_grid(grid)

    while not gameExit:
        
        while gameOver == True:
            gameDisplay.fill(white)
            if gameWin:
                message_to_screen('You Win!', red, y_displace= -50, size= 'large')
            else:
                message_to_screen('Game over', red, y_displace= -50, size= 'large')
            message_to_screen('Press C to play again or Q to quit', black, 50)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        main()

        before = copy_grid(grid)

        for event in pygame.event.get(): #event handling
            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    grid = move_left(grid)
                elif event.key == pygame.K_RIGHT:
                    grid = move_right(grid)
                elif event.key == pygame.K_UP:
                    grid = move_up(grid)
                elif event.key == pygame.K_DOWN:
                    grid = move_down(grid)

                try:
                    if before != grid: #only adds a new value if the player moved any values
                        spawn_value(grid, new_num_val)
                    
                    draw_grid(grid)
                    game_status(grid)
                except ValueError:                    
                    draw_grid(grid)
                    game_status(grid)
        
        clock.tick(FPS)    
    
    pygame.quit()
    quit()

def spawn_value(grid, new_num_val): #fills a random empty spot on the board with new_num_val
    zero_spots = find_zero_spots(grid)

    empty_index = random.randrange(len(zero_spots))
    empty_spot = zero_spots[empty_index]
    rand_row = empty_spot[0]
    rand_col = empty_spot[1]
    del zero_spots[empty_index]
    grid[rand_row][rand_col] = new_num_val

def find_zero_spots(grid): #finds all empty spots on the board (all spots with zeroes)
    empty_spots = []

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == 0:
                empty_spots.append([row,col])
    return empty_spots

def move_right(grid): #shifts and merges grid to the right
    for row in range(len(grid)): #move right
        for col in range(len(grid[row]) - 1, 0, -1):
            current = grid[row][col]
            left = grid[row][col-1]

            if current == 0 and left != 0:  #if empty and left isn't empty, then move to the right
                grid[row][col] = left
                grid[row][col-1] = 0
    
    for row in range(len(grid)): #merge right
        for col in range(len(grid[row]) - 1, 0, -1):
            current = grid[row][col]
            left = grid[row][col-1]

            if current == left and current != 0:
                grid[row][col] = current * 2
                grid[row][col-1] = 0

    for row in range(len(grid)): #move right
        for col in range(len(grid[row]) - 1, 0, -1):
            current = grid[row][col]
            left = grid[row][col-1]

            if current == 0 and left != 0:
                grid[row][col] = left
                grid[row][col-1] = 0        
    return grid

def move_down(grid): #shifts and merges grid down
    for row in range(len(grid) - 1, 0, -1): #move down
        for col in range(len(grid[row])):
            current = grid[row][col]
            above = grid[row-1][col]

            if current == 0 and above != 0:
                grid[row][col] = above
                grid[row-1][col] = 0

    for row in range(len(grid) - 1, 0, -1): #merge down
        for col in range(len(grid[row])):
            current = grid[row][col]
            above = grid[row-1][col]

            if current == above and current != 0:
                grid[row][col] = current * 2
                grid[row-1][col] = 0

    for row in range(len(grid) - 1, 0, -1): #move down
        for col in range(len(grid[row])):
            current = grid[row][col]
            above = grid[row-1][col]

            if current == 0 and above != 0:
                grid[row][col] = above
                grid[row-1][col] = 0            
    return grid

def move_left(grid): #shifts and merges grid to the left
    for row in range(len(grid)): #move left
        for col in range(len(grid[row])-1):
            current = grid[row][col]
            right = grid[row][col+1]
            
            if current == 0 and right != 0:
                grid[row][col] = right
                grid[row][col+1] = 0
    
    for row in range(len(grid)): #merge left
        for col in range(len(grid[row])-1):
            current = grid[row][col]
            right = grid[row][col+1]

            if current == right and current != 0:
                grid[row][col] = current * 2
                grid[row][col+1] = 0
    
    for row in range(len(grid)): #move left
        for col in range(len(grid[row])-1):
            current = grid[row][col]
            right = grid[row][col+1]
            
            if current == 0 and right != 0:
                grid[row][col] = right
                grid[row][col+1] = 0

    return grid

def move_up(grid): #shifts and merges grid up
    for row in range(len(grid) - 1): #move up
        for col in range(len(grid[row])):
            current = grid[row][col]
            below = grid[row+1][col]

            if current == 0 and below != 0:
                grid[row][col] = below 
                grid[row+1][col] = 0

    for row in range(len(grid) - 1): #merge up
        for col in range(len(grid[row])):
            current = grid[row][col]
            below = grid[row+1][col]
            
            if current == below and current != 0:
                grid[row][col] = current * 2
                grid[row+1][col] = 0

    for row in range(len(grid) - 1): #move up
        for col in range(len(grid[row])):
            current = grid[row][col]
            below = grid[row+1][col]

            if current == 0 and below != 0:
                grid[row][col] = below 
                grid[row+1][col] = 0
    return grid

def game_status(grid): #Checks if the user won or lost
    global gameExit
    global gameOver
    global gameWin

    is_full = True

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == 511:
                gameWin = True
                gameOver = True
    
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == 0:
                is_full = False
    
    if is_full == True:
        simulation = []
        for row in range(len(grid)): # make a separate copy of the grid
            temp = []
            for cell in grid[row]:
                temp.append(cell)
            simulation.append(temp)

        simulation = move_up(simulation)
        simulation = move_down(simulation)
        simulation = move_right(simulation)
        simulation = move_left(simulation)

        if simulation == grid:
            gameOver = True

def copy_grid(grid): #copies a list without sharing the same space in memory
    temp1 = []
    for row in range(len(grid)):
        temp2 = []
        for cell in grid[row]:
            temp2.append(cell)
        temp1.append(temp2)
    return temp1

def text_objects(text, color, size):
    if size == 'small':
        textSurface = smallfont.render(text, True, color)
    elif size == 'medium':
        textSurface = medfont.render(text, True, color)
    elif size == 'large':
        textSurface = largefont.render(text, True, color)

    #text_font = font
    #if text.isdigit():
    #    text_font = num_font

    #textSurface = text_font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg, color, y_displace=0, size = 'small'): #write a message to the screen
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (display_width / 2), (display_height / 2)+y_displace
    gameDisplay.blit(textSurf, textRect)

def draw_grid(grid): #draws the grid to screen
    gameDisplay.fill(white)
    grid_coords = []

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] != 0:
                grid_coords.append([grid[row][col], col * block_size, row * block_size])
    
    draw_blocks(grid_coords) #sends coordinates of all filled spaces on the grid
    pygame.display.update()

def draw_blocks(grid_coordinates): # draws every block in the grid that has a value > 0
    for xy in grid_coordinates:
        pygame.draw.rect(gameDisplay, pastel_red, [xy[1], xy[2], block_size, block_size]) #draw rect at every filled cell
        draw_block_num(str(xy[0]), [xy[1], xy[2]]) #add 10 to x and y

def draw_block_num(msg, coords): #draws the number in the middle of each block
    textSurf, textRect = text_objects(msg, black, 'medium')
    textRect.center = (coords[0] + (block_size / 2)), (coords[1] + (block_size / 2))
    gameDisplay.blit(textSurf, textRect)

game_intro()
main()