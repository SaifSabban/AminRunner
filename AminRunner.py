import pygame
from sys import exit
from random import randint, choice
import webbrowser

game_name = 'Amin Runner'

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption(game_name)
clock = pygame.time.Clock()

pygame.display.set_icon(pygame.image.load('graphics\icon.ico'))

test_font = pygame.font.Font('font/Pixeltype.ttf',50)
game_active = False
start_time = 0
final_score = 0
best_Score = 0

sky_surf = pygame.image.load('graphics/sky.png').convert_alpha()
sky_surf2 = sky_surf
ground_surf = pygame.image.load('graphics/ground.png').convert()
ground_surf2 = ground_surf
background_position = 0

title_surf = pygame.image.load('graphics/TitleScreen.png').convert()

Floor = 300
Start_Point = 80
volume = 0.5

#Audio
bg_music = pygame.mixer.Sound('audio/music.wav')
Title_music = pygame.mixer.Sound('audio/TitleScreen.wav')
jump_sound = pygame.mixer.Sound('audio/jump.mp3')
bg_music.set_volume(volume)
Title_music.set_volume(volume)
jump_sound.set_volume(volume)

speed_subtractor = 0
last_timer = 0

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		player_walk1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
		player_walk2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
		self.player_walk = [player_walk1,player_walk2]
		self.player_index = 0
		self.player_jump = pygame.image.load('graphics/player/player_jump.png').convert_alpha()

		self.image = self. player_walk[self.player_index]
		self.rect = self.image.get_rect(midbottom = (Start_Point,Floor))
		self.mask = pygame.mask.from_surface(self.image)
		self.gravity = 0

	def player_input(self):
		keys = pygame.key.get_pressed()
		if game_active:
			if (keys[pygame.K_SPACE] or keys[pygame.K_w]  or keys[pygame.K_UP] ) and  (self.rect.bottom) >= Floor:
				self.gravity = -13
				jump_sound.play()

			if keys[pygame.K_a] or keys[pygame.K_LEFT]:
				self.rect.x -= 4
				if self.rect.left <= 0:
					self.rect.left = 0

			if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
				self.rect.x += 4
				if self.rect.right >= 800:
					self.rect.right = 800

			if keys[pygame.K_s] or keys[pygame.K_DOWN] and (self.rect.bottom) > Floor:
				self.rect.bottom -= 20

	def apply_gravity(self):
		self.gravity += 0.5
		self.rect.y += self.gravity
		if self.rect.bottom >= Floor:
			self.rect.bottom = Floor

	def animation_state(self):
		if self.rect.bottom < Floor: 
			self.image = self.player_jump
		else:
			self.player_index += 0.1
			if self.player_index >= len(self.player_walk): self.player_index = 0
			self.image = self.player_walk[int(self.player_index)]

	def update(self):
		self.player_input()
		self.apply_gravity()
		self.animation_state()

class Obstacle(pygame.sprite.Sprite):
	def __init__(self, type):
		super().__init__()
		if type == 'Burger':
			burger_frame1 = pygame.image.load('graphics/Burger/Burger1.png').convert_alpha()
			burger_frame2 = pygame.image.load('graphics/Burger/Burger2.png').convert_alpha()
			burger_frame3 = pygame.image.load('graphics/Burger/Burger3.png').convert_alpha()
			burger_frame4 = pygame.image.load('graphics/Burger/Burger4.png').convert_alpha()
			self.frames = [burger_frame1,burger_frame2,burger_frame3,burger_frame4]
			y_pos  = 150
		else:
			pizza_frame1 = pygame.image.load('graphics/Pizza/Pizza1.png').convert_alpha()
			pizza_frame2 = pygame.image.load('graphics/Pizza/Pizza2.png').convert_alpha()
			pizza_frame3 = pygame.image.load('graphics/Pizza/Pizza3.png').convert_alpha()
			pizza_frame4 = pygame.image.load('graphics/Pizza/Pizza4.png').convert_alpha()
			self.frames = [pizza_frame1,pizza_frame2,pizza_frame3,pizza_frame4]
			y_pos = Floor

		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))
		self.mask = pygame.mask.from_surface(self.image)

	def animation_state(self):
		self.animation_index += 0.1 
		if self.animation_index >= len(self.frames): self.animation_index = 0
		self.image = self.frames[int(self.animation_index)]

	def update(self):
		self.animation_state()
		self.rect.x -= 5 + int(final_score/10)
		self.destroy()

	def destroy(self):
		if self.rect.x <= -100: 
			self.kill()

class Volume_button(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		global volume
		Volumepoint = (volume * 100) + 25

		self.button = pygame.image.load('graphics/VolButton.png').convert_alpha()
		self.image = self.button
		self.rect = self.image.get_rect(center = (Volumepoint,35))
		self.mask = pygame.mask.from_surface(self.image)
		self.toggle = False

	def mouse_input(self, event):
		global volume
		mouse_pos = pygame.mouse.get_pos()

		if self.rect.collidepoint(mouse_pos) and event.type == pygame.MOUSEBUTTONDOWN:
			self.toggle = True
		elif event.type == pygame.MOUSEBUTTONUP:
			self.toggle = False

		if self.toggle:
				if pygame.mouse.get_pos()[0] <= 125 and pygame.mouse.get_pos()[0] >= 25:
					Volumepoint = int(pygame.mouse.get_pos()[0])
					self.rect.centerx = Volumepoint
					volume = (Volumepoint - 25)/100
					jump_sound.set_volume(volume)
					bg_music.set_volume(volume)
					Title_music.set_volume(volume)

	def update(self, event):				
		self.mouse_input(event)

class Link_button(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()

		self.button = pygame.image.load('graphics/links.png').convert_alpha()
		self.image = self.button
		self.rect = self.image.get_rect(center = (75,70))
		self.mask = pygame.mask.from_surface(self.image)
		self.toggle = False

	def mouse_input(self, event):
		global volume
		mouse_pos = pygame.mouse.get_pos()

		if self.rect.collidepoint(mouse_pos) and event.type == pygame.MOUSEBUTTONDOWN:
			self.toggle = True
		elif event.type == pygame.MOUSEBUTTONUP:
			self.toggle = False

		if self.toggle:
			webbrowser.open('https://zez.am/amin_nafar_fit', new=2)
			self.toggle = False

	def update(self, event):				
		self.mouse_input(event)

def collision_sprite():
	if pygame.sprite.spritecollide(player.sprite,obstacle_group,False, pygame.sprite.collide_mask):
		obstacle_group.empty()
		Title_music.play(loops = -1)
		player.sprite.rect.x = Start_Point
		player.sprite.rect.y = Floor
		return False
	else: return True

def display_score():
	current_time = pygame.time.get_ticks() - start_time
	Score = int(current_time/1000)
	score_surf = test_font.render(f'Score: {Score}', False, (73,97,255))
	score_rect = score_surf.get_rect(center = (400,50))
	screen.blit(score_surf, score_rect)
	return Score

def backgrond_movement():
	global background_position
	background_position -= 1
	if background_position <= -800: background_position = 0
	screen.blit(sky_surf,(background_position,0))
	screen.blit(sky_surf2,(800 + background_position,0))
	screen.blit(ground_surf,(background_position,Floor))
	screen.blit(ground_surf2,(800 + background_position,Floor))
	return background_position

def Final_score():
	global best_Score
	Final_Score_font = pygame.font.Font('font/Pixeltype.ttf',100)
	
	title_surf = Final_Score_font.render(game_name, False, 'Black')
	Final_Score_surf = Final_Score_font.render(f'Score: {final_score}', False, 'Black')
	start_instruction_surf = Final_Score_font.render('Press Space To Start', False, 'Black')
	
	title_rect = title_surf.get_rect(center = (400,50))
	Final_Score_rect = Final_Score_surf.get_rect(center = (400,350))
	start_instruction_rect = start_instruction_surf.get_rect(center = (400,350))

	best_score_font = pygame.font.Font('font/Pixeltype.ttf',35)
	best_Score_surf = best_score_font.render(f'Best Score: {best_Score}', False, 'Black')
	best_Score_rect = Final_Score_surf.get_rect(center = (750,50))

	screen.blit(title_surf,title_rect)

	if final_score != 0:
		screen.blit(Final_Score_surf,Final_Score_rect)
	else:
		screen.blit(start_instruction_surf,start_instruction_rect)

	if best_Score < final_score:
		best_Score = final_score
	
	screen.blit(best_Score_surf,best_Score_rect)

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

volume_button = pygame.sprite.GroupSingle()
volume_button.add(Volume_button())

link_button = pygame.sprite.GroupSingle()
link_button.add(Link_button())

obstacle_group = pygame.sprite.Group()

#Player Onj Screen
player_stand = pygame.transform.rotozoom(pygame.image.load('graphics/player/player_stand.png').convert_alpha(), 0, 2)
player_stand_rect = player_stand.get_rect(center = (400,200))

# Timer
obstacle_timer = pygame.USEREVENT + 1
obstacle_Clock = randint(1000, 1500)
pygame.time.set_timer(obstacle_timer, obstacle_Clock)

Title_music.play(loops = -1)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
			pygame.quit()
			exit()

		if game_active:
			if event.type == obstacle_timer:
				obstacle_group.add(Obstacle(choice(['Burger','Pizza'])))
			if int(final_score/10) != last_timer:
				speed_subtractor += 100
				pygame.time.set_timer(obstacle_timer,obstacle_Clock - speed_subtractor)
				last_timer = int(final_score/10)

		else:
			if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
						start_time = pygame.time.get_ticks()
						game_active = True
						speed_subtractor = 0
						Title_music.stop()
						bg_music.play(loops = -1)
			
			volume_button.update(event)
			link_button.update(event)


	if game_active:
		backgrond_movement()
		final_score = display_score()

		player.update()
		player.draw(screen)

		obstacle_group.draw(screen)
		obstacle_group.update()

		game_active = collision_sprite()

	else:
		bg_music.stop()
		
		screen.blit(title_surf,(0,0))
		Final_score()
		screen.blit(player_stand, player_stand_rect)
	
		# Volume
		volume_font = pygame.font.Font('font/Pixeltype.ttf',30)
		volume_surf = volume_font.render(f'Volume: {int(volume*100)}', False, 'Black')
		volume_rect = volume_surf.get_rect(center = (75,20))
		pygame.draw.line(screen,'Black', (25,35),(125,35))
		screen.blit(volume_surf,volume_rect)
		
		volume_button.draw(screen)
		link_button.draw(screen)

	pygame.display.update()
	clock.tick(60)