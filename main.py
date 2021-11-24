"""
Snake!

Snake game built with pygame package.
pretty normal snake game other than instead of an apple 
being eaten i made a mouse, mouse as in a grey rectangle
but its more realistic. I also added the fact that the snake 
could move over itself just a bit more realistic again...

More info in readme.md
"""

import pygame
from random import randint


class Game:
    """Game Rendering, game loops, and event handlers"""
    
    # Important variables
    clock = pygame.time.Clock()
    running = True
    screen = pygame.display.set_mode((800,600))
    curr_display = "start_screen"
    Icon = pygame.image.load("resources/snake.png")

    def grid_render(blocks_x=40, blocks_y=30):
        square = pygame.Rect(0,0,20,20)
        for row in range(blocks_y):
            for block in range(blocks_x):
                pygame.draw.rect(Game.screen,(255,255,255),square,1)
                square.x += 20
            square.x = 0
            square.y += 20
    

    def game_loop():
        """Main game loop, scene handling etc"""
       
        # Pygame inits 
        pygame.font.init()
        pygame.init()
       
        # Game loop rendering etc
        while Game.running == True:
            if Game.curr_display == "start_screen":
                Events.start_screen()
                Events.on_button_hover()
            elif Game.curr_display == "main_game":
                Game.screen.fill((0,0,0))
                Game.clock.tick(15)
                
                Snake.check_wall_colision()
                Snake.movement(Snake.move_direction)
                Snake.draw()
                Snake.update_player_rects()

                Food.check_food_collision()
                Food.draw()            
            elif Game.curr_display == "game_over":
                Events.game_over()
                Events.on_button_hover()
            
            # event hander call and display updates
            Game.event_handler()
            pygame.display.flip() 
            
    
    def event_handler():
        """All events being handled, Keyboard input mouse events etc"""
        for event in pygame.event.get():
            # window quit
            if event.type == pygame.QUIT:
                Game.running = False    
            
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if Events.on_button_hover() == 1:
                    Game.curr_display = "main_game"
                elif Events.on_button_hover() == 2:
                    Game.running = False
                elif Events.on_button_hover() == 3:
                    Events.reset_game()
                    Game.curr_display = "main_game"
                elif Events.on_button_hover() == 4:
                    Game.running = False
                
            # keyboard input
            if event.type == pygame.KEYDOWN:
                 # Press Q to quit
                if event.key == pygame.K_q:
                    Game.running = False
                
                if event.key == pygame.K_UP:
                    Snake.move_direction = "up"
                    
                elif event.key == pygame.K_DOWN:
                    Snake.move_direction = "down"
                    
                elif event.key == pygame.K_LEFT:
                    Snake.move_direction = "left"

                elif event.key == pygame.K_RIGHT:
                    Snake.move_direction = "right"
                
class Snake:
    """
    Everything snake/snake related
    movement, edge/wall colision, drawing the snake
    and snake updates that causes the slither animation
    """  
    
    # Critical variables
    snake_pos = [140,300]
    snake = [[140,300]]
    move_direction = None
    
    
    def update_player_rects():
        Snake.snake.insert(0, list(Snake.snake_pos))
        Snake.snake.pop()

    def check_wall_colision():
        if Snake.snake_pos[0] < 0 or Snake.snake_pos[0] > 800:
            Game.curr_display = "game_over"
            
        elif Snake.snake_pos[1] < 0 or Snake.snake_pos[1] > 600:
            Game.curr_display = "game_over"
            
    def draw():
        # Draw rect for every tuple of positions in snake.snake
        for square in Snake.snake:
            pygame.draw.rect(Game.screen, (0,255,0),(square[0], square[1],20,20))
            
    def movement(direction=None):
        if direction == None:
            pass
        if direction == "down":
            Snake.snake_pos[1] += 20
        if direction == "up":
            Snake.snake_pos[1] -= 20
        if direction == "right":
            Snake.snake_pos[0] += 20
        if direction == "left":
            Snake.snake_pos[0] -= 20
class Food:
    """Drawing and checking collisions"""
    
    # Random food location on multiples of 20 (20,440,280) etc
    rand_x_position = randint(1,38)*20
    rand_y_position = randint(1,28)*20
    
    def draw():
        food_rect = pygame.Rect(Food.rand_x_position, Food.rand_y_position,20,20)
        pygame.draw.rect(Game.screen,(50,50,50), food_rect)
    
    def check_food_collision():
        # redefine snake rects and food rects both draw methods
        player_rect = pygame.Rect(Snake.snake_pos[0], Snake.snake_pos[1], 20,20 )
        food_rect = pygame.Rect(Food.rand_x_position, Food.rand_y_position, 20, 20)
        
        if player_rect.colliderect(food_rect):
            # move food to different spot
            Food.rand_x_position = randint(1,38)*20
            Food.rand_y_position = randint(1,28)*20
            Snake.snake.append((Snake.snake_pos))

class Events:
    
    def start_screen(button_to_change_color=None):
        
        # other styling
        Game.screen.fill((50,50,50))
        outer_rect = pygame.draw.rect(Game.screen,(0,0,0),pygame.Rect(0,0,800,600),50)
        
        # define fonts
        big_font = pygame.font.Font("resources/font.ttf", 64)
        small_font = pygame.font.Font("resources/font.ttf", 32)
       
        # define and render text
        snake_game_text = big_font.render("Snake Game!", True,(0,0,0))
        start_text = small_font.render("Start...", True, (0,0,0))
        exit_text = small_font.render("Exit...", True, (0,0,0))           
     
        # Blit/display text to Game.screen
        Game.screen.blit(snake_game_text, (200,100)) 
        Game.screen.blit(start_text,(175,400))
        Game.screen.blit(exit_text, (515, 400))
     
        # Changing colour on hover
        if button_to_change_color == None:
            pass
        if button_to_change_color == "start":
            start_text = small_font.render("Start...", True, (255,255,255))
            Game.screen.blit(start_text,(175,400))
        if button_to_change_color == "exit":
            exit_text = small_font.render("Exit...", True, (255,255,255))
            Game.screen.blit(exit_text, (515, 400))

    def game_over(button_to_change_color=None):
        # styling 
        Game.screen.fill((50,50,50))
        top_rect = pygame.draw.rect(Game.screen,(0,0,0),pygame.Rect(0,0,800,30))
        bottom_rect = pygame.draw.rect(Game.screen,(0,0,0),pygame.Rect(0,570,800,30))
        # define fonts
        big_font = pygame.font.Font("resources/font.ttf", 64)
        small_font = pygame.font.Font("resources/font.ttf", 32)
        
        # Define and render text
        exit_text = small_font.render("Exit...", True, (0,0,0))
        game_over_text = big_font.render("You Died!", True, (0,0,0))
        retry_text = small_font.render("Retry...", True, (0,0,0))
        # Blit/display text to Game.screen
        Game.screen.blit(game_over_text, (225,100))
        Game.screen.blit(exit_text, (515,400))
        Game.screen.blit(retry_text, (175, 400))

        # Change button colour on hover      
        if button_to_change_color == None:
            pass
        if button_to_change_color == "retry":
            start_text = small_font.render("retry...", True, (255,255,255))
            Game.screen.blit(start_text,(175,400))
        if button_to_change_color == "exit":
            exit_text = small_font.render("Exit...", True, (255,255,255))
            Game.screen.blit(exit_text, (515, 400))

    def on_button_hover():
        mouse_position = pygame.mouse.get_pos()
        
        # determine mouse position for button 1 (start button)
        if Game.curr_display == "start_screen" and mouse_position[0] > 172 and mouse_position[0] < 285:
            if mouse_position[1] > 400 and mouse_position[1] < 429:
                Events.start_screen("start")
                return 1
        # determine mouse position for button 2 (exit button)
        if Game.curr_display == "start_screen" and mouse_position[0] > 510 and mouse_position[0] < 610:
            if mouse_position[1] > 400 and mouse_position[1] < 425:
                Events.start_screen("exit")
                return 2
        # determine mouse position for button 3 (retry button) in game_over screen
        if Game.curr_display == "game_over" and mouse_position[0] > 172 and mouse_position[0] < 285:
            if mouse_position[1] > 400 and mouse_position[1] < 429:
                Events.game_over(button_to_change_color="retry")
                return 3
        # determine mouse position for button 4 (exit button) in game_over screen 
        if Game.curr_display == "game_over" and mouse_position[0] > 510 and mouse_position[0] < 610:
            if mouse_position[1] > 400 and mouse_position[1] < 425:
                Events.game_over(button_to_change_color="exit")
                return 4
    
    # Game reset
    def reset_game():
        Snake.snake_pos = [140, 300]
        Snake.move_direction = None


# Trigger Game loop
if __name__ == '__main__':
    pygame.display.set_caption("Snake.")
    pygame.display.set_icon(Game.Icon)
    Game.game_loop()