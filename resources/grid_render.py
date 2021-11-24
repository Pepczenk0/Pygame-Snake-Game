""" 
If you want a grid render for display in this snake game
here it is to get it running put this function in the "Game"
class and call it in game_loop() under 
"elif Game.curr_display == "main_game"
note it is a bit buggy so dont trust it to much
"""


def grid_render(blocks_x=40, blocks_y=30):
        square = pygame.Rect(0,0,20,20)
        for row in range(blocks_y):
            for block in range(blocks_x):
                pygame.draw.rect(Game.screen,(255,255,255),square,1)
                square.x += 20
            square.x = 0
            square.y += 20
