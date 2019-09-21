import pygame
pygame.init()

black = (0,0,0)
grey = (200,200,200)
dark_grey = (100,100,100)
red = (255,0,0)
orange = (204,102,0)
light_yellow = (204,204,0) 
light_green = (0,153,0)
light_blue = (0,255,204) 
blue = (0,102,204)
dark_blue = (0,0,153)
lavender = (102,102,255)
purple = (102,0,255)
pink = (255,153,255)
white =(255,255,255)
	
tile_colours ={'2': red,
				'4': orange,
				'8': light_yellow,
				'16': light_green,
				'32': light_blue,
				'64': blue,
				'128': dark_blue,
				'256': lavender,
				'512': purple,
				'1024': pink,
				'2048': white }



		
score = '0'
Title = DisplayText('2048', pygame.font.Font('freesansbold.ttf', 65),(50,50),black)
Score_t = DisplayText('Score:', pygame.font.Font('freesansbold.ttf', 30), (50,50), black)
Score_v = DisplayText(str(score),pygame.font.Font('freesansbold.ttf', 50), (50,50), black)
Game_over_t = DisplayText('Game Over !', pygame.font.Font('freesansbold.ttf', 50), (50,50), red)
#Cell_formats = DisplayText('', cell_font = pygame.font.Font('freesansbold.ttf', 40), (50,50), black)

constant_text_displayed = [Title, Score_t, Score_v]

print(Score_v.words)
Score_v.words = '50'

print(Score_v.words)

