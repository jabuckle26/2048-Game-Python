import numpy as np
import pygame
import random

pygame.init() #Initiate pygame

################## Classes ###################################
class DisplayText():
	def __init__(self, words, font_info, co_ord, colour):
		self.words = words
		self.font_info = font_info
		self. co_ord = co_ord
		self.colour = colour

	def genTextObject(self):
		textSurface = self.font_info.render(self.words, True, self.colour)
		return textSurface, textSurface.get_rect()

################## Functions ##############################
def newGridGen(window):
	window.fill(grey)
	grid = np.zeros((4,4))
	grid = randLocInt(grid)
	grid = randLocInt(grid)
	return grid, True, False, 0
	
def randLocInt(grid):
	grid=np.array(grid)
	zero_locs = np.argwhere(grid==0 ) #list of points
	rand = random.randint(0,len(zero_locs)-1)#random cell in list of zeros
	grid[zero_locs[rand][0]][zero_locs[rand][1]] = random.choice([2,4])
	return grid

def transposeGrid(grid):
	return [[grid[i][x] for i in range(0,len(grid))] for x in range(0,len(grid))]
	
def adjacencyCheck(my_list):
	pairs = [[my_list[i],my_list[i+1]] for i in range(0,len(my_list)-1)]
	for p in pairs:
		if p[0] == p[1]:
			return True
	return False
	
def filterZeros(grid):
	filtered_grid = []
	for r in grid:
		filtered_grid.append(list(filter(lambda x: x!= 0, r)))
	return filtered_grid

def paddZeros(grid, shift, iteration ='first'):
	padded_grid = []
	ppadded_grid = []
	if (shift =='l' or shift =='u'):
		for r in grid:
			while len(r) < 4:
				r.append(0)
			padded_grid.append(r)
	elif (shift == 'r' or shift=='d') and iteration == 'first':
		for r in grid:
			while len(r) < 4:
				r.insert(0,0)
			padded_grid.append(r[::-1]) #reversed for processing in calcSum()
			ppadded_grid.append(r) #unreversed for printing and verification 
	elif (shift == 'r' or shift=='d') and iteration == 'second':
		for r in grid:
			while len(r) < 4:
				r.insert(0,0)
			padded_grid.append(r)
	return padded_grid
	

def calcSum(grid, shift, score, iteration = 'first'):
	summed_grid = []
	full_count = 0
	for r in grid:
		rs = []
		cancel_next = False
		recent_sum = False
		#Do nothing if all full
		if adjacencyCheck(r) == False and 0 not in r:
			rs.extend(r)
			full_count+=1
			if full_count == 4:
				print('FAIL')
		else:
			for i in range(0,3):
				if r[i] == r[i+1] and recent_sum == False:
					rs.append(r[i]*2)
					score+= r[i]*2 ##Update global score
					recent_sum = True
				elif recent_sum == True:
					rs.append(0)
					recent_sum = False
				else:
					rs.append(r[i])
			if len(r)==4 and r[-1] !=0 and recent_sum == False:
				rs.append(r[-1])

		if shift =='l' or shift == 'u':
			summed_grid.append(rs)
		elif shift == 'r' or shift == 'd':
			summed_grid.append(rs[::-1]) #

	return summed_grid, score
	
def gameOverCheck(grid):
	full_count = 0
	full_combo = [i for i in grid]
	full_combo.extend(j for j in transposeGrid(grid))
	print('COMBO',full_combo)

	for r in full_combo:
		if adjacencyCheck(r) == False and (0 not in r):
			full_count+=1
			if full_count == 8:
				print('FAIL')
				print('Game over grid', grid)
				return True
	return False

def processGrid(grid, shift, score, transposed = False):
	orig_grid = grid.copy()
	# Filter
	grid = filterZeros(grid)
	# Padd
	grid = paddZeros(grid, shift)
	##summ
	grid,score = calcSum(grid, shift, score)
	# Filter again
	grid = filterZeros(grid)
	# Padd again
	try:
		grid = np.array(paddZeros(grid, shift, 'second'))
	except:
		print(grid)
		exit()

	#Only add random if we've moved something
	if not np.array_equal(orig_grid, grid):
		grid=randLocInt(grid)
	
	if transposed == True:
		grid = transposeGrid(grid)
	
	print(shift)
	print(np.array(grid))

	return grid,score

######################################################################################################
################### Fixed Variables #######################
#Spatial parameters
padding = 10
int_padding = 5
grid_square_side = 150
total_grid_side = (grid_square_side*4) + (int_padding*5)

cell_origin_spacing = grid_square_side + int_padding
grid_origin = padding + int_padding

w_height = total_grid_side + (padding*2)
w_width = w_height + 200

title_panel_side = 160

grid_matrix = []

##Score
global score
score = 0

#Colours
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

#Fonts and text
Title = DisplayText('2048', pygame.font.Font('freesansbold.ttf', 65),(w_height + padding * 1.5 + title_panel_side / 2, padding + title_panel_side / 2),white)
Score_t = DisplayText('Score:', pygame.font.Font('freesansbold.ttf', 30), (w_height + padding * 1.5 + title_panel_side / 2, (padding + (title_panel_side / 2)) *3), black)
Score_v = DisplayText(str(score),pygame.font.Font('freesansbold.ttf', 50), (w_height + padding * 1.5 + title_panel_side / 2 , (padding + (title_panel_side / 2)) *3+ 100), black)
Game_over_t = DisplayText('Game Over !', pygame.font.Font('freesansbold.ttf', 50), (w_width / 2 , w_height/2), red)
Cell_formats = DisplayText(None, pygame.font.Font('freesansbold.ttf', 40), None, black)

constant_text_displayed = [Title, Score_t, Score_v]

#Game parameters
window = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption('2048 -- James Version')
grid, running, game_over, score = newGridGen(window)

#Draw Main Grid
pygame.draw.rect(window, black, (padding, padding, total_grid_side, total_grid_side))
#Title box
pygame.draw.rect(window, black, (w_height+padding*1.5, padding,title_panel_side,title_panel_side))

################## Main Loop ##########################
print(grid)
while running:
	#Get user input
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			key = pygame.key.get_pressed()
			if key[pygame.K_DOWN]:
				grid,score = processGrid(transposeGrid(grid), 'd', score, True)
			if key[pygame.K_UP]:
				grid,score = processGrid(transposeGrid(grid), 'u', score,True)
			if key[pygame.K_LEFT]:
				grid,score = processGrid(grid, 'l',score, False)
			if key[pygame.K_RIGHT]:
				grid,score = processGrid(grid, 'r',score, False)
			game_over = gameOverCheck(grid)

	#Draw inactive and active grid
	for w in range(0,4):
		for h in range(0,4):
			pygame.draw.rect(window, dark_grey, (grid_origin + cell_origin_spacing*w, grid_origin + cell_origin_spacing*h, grid_square_side, grid_square_side ) )
			cell = str(int(grid[h][w]))
			Cell_formats.words = cell
			Cell_formats.co_ord = ((grid_origin + cell_origin_spacing*w)+grid_square_side/2, (grid_origin + cell_origin_spacing*h)+grid_square_side/2)
			if cell!='0':
				pygame.draw.rect(window, tile_colours[cell], (grid_origin + cell_origin_spacing * w, grid_origin + cell_origin_spacing * h, grid_square_side, grid_square_side))
				TextSurf, TextRect = Cell_formats.genTextObject()
				TextRect.center = Cell_formats.co_ord
				window.blit(TextSurf, TextRect)

	# Text Update
	pygame.draw.rect(window, black, (w_height+padding*1.5-5, 300-5, title_panel_side+10,title_panel_side+10))
	pygame.draw.rect(window, white, (w_height+padding*1.5, 300, title_panel_side,title_panel_side))
	Score_v.words = str(int(score))
	for item in constant_text_displayed:
		TextSurf, TextRect = item.genTextObject()
		TextRect.center = item.co_ord
		window.blit(TextSurf, TextRect)

	if game_over:
		print('TRIGERED')
		TextSurf, TextRect = Game_over_t.genTextObject()
		TextRect.center = Game_over_t.co_ord
		window.blit(TextSurf,TextRect)
		pygame.display.update()
		#Give user option to restart
		inactive = True
		while inactive:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
					inactive = False
				if event.type == pygame.KEYDOWN:
					key = pygame.key.get_pressed()
					if key[pygame.K_SPACE]:
						print('RESET')
						grid, running, game_over, score = newGridGen(window)
						inactive=False
						#Main Grid
						pygame.draw.rect(window, black, (padding, padding, total_grid_side, total_grid_side))
						#Title box
						pygame.draw.rect(window, black, (w_height+padding*1.5, padding,title_panel_side,title_panel_side))
	pygame.display.update()
pygame.quit()
print('end')
