import numpy as np
import pygame
import random

pygame.init()

################## Functions ##############################
def textObjects(text, font, colour = (0,0,0)):
	textSurface = font.render(text, True, colour)
	return textSurface, textSurface.get_rect()


def randLocInt(grid):
	#print(type(grid))
	grid=np.array(grid)
	zero_locs = np.argwhere(grid==0 ) #list of points
	#print('ZEROS', zero_locs)
	#print('LEN ZERO LIST', len(zero_locs[0]))
	rand = random.randint(0,len(zero_locs)-1)#random cell in list of zeros
	#print(rand)
	grid[zero_locs[rand][0]][zero_locs[rand][1]] = random.choice([2,4])
	return grid
	#print(grid)
	#dfdfdfd

def transposeGrid(grid):
	return [[grid[i][x] for i in range(0,len(grid))] for x in range(0,len(grid))]
	
def adjacencyCheck(my_list):
	pairs = [[my_list[i],my_list[i+1]] for i in range(0,len(my_list)-1)]
	#print('pairs', pairs)
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
		#print('prePAD', grid)
		for r in grid:
			while len(r) < 4:
				r.append(0)
			padded_grid.append(r)
		#print('PAD',padded_grid)
	elif (shift == 'r' or shift=='d') and iteration == 'first':
		for r in grid:
			#print('Prefirst PAD', r)
			while len(r) < 4:
				r.insert(0,0)
			padded_grid.append(r[::-1]) #reversed for processing in calcSum()
			ppadded_grid.append(r) #unreversed for printing and verification
		#print('Pad-first',ppadded_grid) 
	elif (shift == 'r' or shift=='d') and iteration == 'second':
		#print('PreSecond Pad', grid)
		#print('HERE',padded_grid)
		for r in grid:
			#print('r', r)
			while len(r) < 4:
				r.insert(0,0)
			padded_grid.append(r)
		#print('PadSecond', padded_grid)
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
			#print('full row', r)
			rs.extend(r)
			full_count+=1
			if full_count == 4:
				#GAME OVER FUNCTION
				print('FAIL')
				#exit()
		else:
			for i in range(0,3):
				if r[i] == r[i+1] and recent_sum == False:
					rs.append(r[i]*2)
					score+= r[i]*2 ##Update global score
					#cancel_next = True
					recent_sum = True
				elif recent_sum == True:
					rs.append(0)
					recent_sum = False
					#cancel_next = False
				else:
					rs.append(r[i])
					#cancel_next = False
			if len(r)==4 and r[-1] !=0 and recent_sum == False:
				rs.append(r[-1])

		if shift =='l' or shift == 'u':
			summed_grid.append(rs)
		elif shift == 'r' or shift == 'd':
			summed_grid.append(rs[::-1]) #

	#print('SUMMED',summed_grid)
	return summed_grid, score
	
def gameOverCheck(grid):
	full_count = 0
	full_combo = [i for i in grid]
	full_combo.extend(j for j in transposeGrid(grid))
	print('COMBO',full_combo)

	for r in full_combo:
		#Trigger end game if all full
		#print(len(np.argwhere(grid==0 )))
		if adjacencyCheck(r) == False and len(np.argwhere(grid==0 ))== 0:
			#print('full row', r)
			full_count+=1
			if full_count == 8:
				print('FAIL')
				return True
	return False

def processGrid(grid, shift, score, transposed = False):
	#print(transposed, shift)
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
background_c = (200,200,200)
title_panel_c = (0,200,200)
score_panel_c = (0,100,100)
grid_outline = (0,0,0)
empty_cell = (100,100,100)
#filled_cell = (50,50,230)
filled_cell = {'2': (230, 25, 75),
				'4': (60, 180, 75),
				'8': (0, 130, 200),
				'16': (245, 130, 48),
				'32': (145, 30, 180),
				'64': (70, 240, 240),
				'128': (240, 50, 230),
				'256': (210, 245, 60),
				'512': (170,255,195),
				'1024': (255,215,180),
				'2048': (250,190,190) }




#Fonts and text
words = ['2048',
		 'Score:',
		 str(score)]
fonts_info = [pygame.font.Font('freesansbold.ttf', 65),
			  pygame.font.Font('freesansbold.ttf', 30),
			  pygame.font.Font('freesansbold.ttf', 50)]
word_center = [(w_height + padding * 1.5 + title_panel_side / 2, padding + title_panel_side / 2),
			   (w_height + padding * 1.5 + title_panel_side / 2, (padding + (title_panel_side / 2)) *3),
			   (w_height + padding * 1.5 + title_panel_side / 2 , (padding + (title_panel_side / 2)) *3+ 100)]

game_over_notice = ['Game Over!', pygame.font.Font('freesansbold.ttf', 50), (w_height + padding * 1.5 + title_panel_side / 2 , (padding + (title_panel_side / 2)) *3 + 175), (255,0,0)]

window = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption('2048 -- James Version')

cell_font = pygame.font.Font('freesansbold.ttf', 40)
running = True

################# Create initial grid ################
#Two random start locations
grid = np.zeros((4,4))
#print(grid)

#start with two random nos
grid = randLocInt(grid)
grid = randLocInt(grid)


################## Main Loop ##########################
print(grid)
while running:

	#Get user input
	game_over = False
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

	#print(verified)
	##Draw shapes
	# Fill background
	window.fill(background_c)
	#Main Grid
	pygame.draw.rect(window, grid_outline, (padding, padding, total_grid_side, total_grid_side))
	#Title box
	pygame.draw.rect(window, title_panel_c, (w_height+padding*1.5, padding,title_panel_side,title_panel_side))
	#Score caption box
	pygame.draw.rect(window, score_panel_c, (w_height+padding*1.5, 300, title_panel_side,title_panel_side))

	#Draw inactive and active grid
	for w in range(0,4):
		for h in range(0,4):
			pygame.draw.rect(window, empty_cell, (grid_origin + cell_origin_spacing*w, grid_origin + cell_origin_spacing*h, grid_square_side, grid_square_side ) )
			cell = str(int(grid[h][w]))
			if cell!='0':
				pygame.draw.rect(window, filled_cell[cell], (grid_origin + cell_origin_spacing * w, grid_origin + cell_origin_spacing * h, grid_square_side, grid_square_side))
				TextSurf, TextRect = textObjects(str(int(cell)), cell_font)
				TextRect.center = ((grid_origin + cell_origin_spacing*w)+grid_square_side/2, (grid_origin + cell_origin_spacing*h)+grid_square_side/2)
				window.blit(TextSurf, TextRect)

	# Text Update
	words[2] = str(int(score))
	for word, font_info, word_loc in zip(words, fonts_info, word_center):
		TextSurf, TextRect = textObjects(word, font_info)
		TextRect.center = (word_loc)
		window.blit(TextSurf, TextRect)

	if game_over:
		print('TRIGGEED')
		pygame.draw.rect(window, title_panel_c, (w_height+padding*1.5, 450, title_panel_side,title_panel_side))
		TextSurf, TextRect = textObjects(game_over_notice[0],game_over_notice[1], game_over_notice[3])
		TextRect.center = (game_over_notice[2])
		window.blit(TextSurf,TextRect)
		pygame.display.update()
		#Give user option to restart
		inactive = True
		while inactive:
		
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				if event.type == pygame.KEYDOWN:
					key = pygame.key.get_pressed()
					if key[pygame.K_SPACE]:
						print('RESET')
						exit()
	pygame.display.update()
pygame.quit()
print('end')
