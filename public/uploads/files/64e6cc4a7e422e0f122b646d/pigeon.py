import pygame
import random
import os

pygame.init()
screen_w = 600
screen_h = 760
screen = pygame.display.set_mode((screen_w,screen_h))
pygame.display.set_caption("Pigeon poop catcher!")
#need scale too
d_text = pygame.font.SysFont("Impact", 20)
score_text = pygame.font.SysFont("Impact",24)
highscore_text = pygame.font.SysFont("Impact",24)
life_text = pygame.font.SysFont("Impact",35)
coin_text = pygame.font.SysFont("Impact",35)

b_c_text = pygame.font.SysFont("Impact", 16)			# added in text_bar (new)
b_v_text = pygame.font.SysFont("Impact", 16)			# later
b_l_text = pygame.font.SysFont("Impact", 16)

p_c_text = pygame.font.SysFont("Impact", 18)			# add in list n use for loop
p_v_text = pygame.font.SysFont("Impact", 18)
p_l_text = pygame.font.SysFont("Impact", 18)
gameover = pygame.font.SysFont("Impact", 18)

b_text = [b_c_text,b_v_text,b_l_text]
prize_text = [p_c_text, p_v_text, p_l_text]
prize_d = [100, 200, 500]

basket = pygame.image.load("basket.png").convert()
branch = pygame.image.load("branch.png").convert()
pigeon = pygame.image.load("pigeon.png").convert()
button_coin = pygame.image.load("coin_button.png").convert()
button_velocity = pygame.image.load("velocity.png").convert()		# the image break down! # solution: make the image small in the figma
button_life = pygame.image.load("life.png").convert()
prize = pygame.image.load("prize.png").convert()
coin = pygame.image.load("coin.png")
life_heart = pygame.image.load("life_heart.png").convert()
white_del = (245,245,245)
branch.set_colorkey(white_del)
branch  = pygame.transform.scale(branch, (int(branch.get_width()), int(branch.get_height() * 0.8)))

if not os.path.exists("highscore_pi.txt"):
	f = open("highscore_pi.txt", "x")
	with open("highscore_pi.txt", "w") as f:
		f.write("0")
	highscore = 0
else:
	with open("highscore_pi.txt", "r") as f:
		highscore = int(f.read())

text_fd = ""
bar_length = screen_w
bar_h = 110		# need scale
score = 0
life = 15
coin_d = 100
increase_coin = 10
number_of_pigeons = 0

#color
sky = (115,215,255)
brown = (134,74,27)
bar_color = (208,183,46)
white = (255,255,255)
black = (0, 0, 0)

pigeon_w = 70
pigeon_h = 80
pigeon_x = 50
pigeon_y = 225
changepix = 0

poops = 10
poopx = (pigeon_x + (pigeon_w/2)) - poops/2
poopy = (pigeon_y + pigeon_h) - poops/2
p_gravity = 0
velocitypx = 0.3

branch_length = (pigeon_y+pigeon_h) - 30

#bar
xb = 0
yb = (1 - (1/5.4))*screen_h + 1
b_h = (1/5.4)*screen_h

list_pix = [0,110,220,330,440]
list_px = []
list_changed = []
scores = []


#All of this need scale if wanna make program more flexible

class Parent():
	def __init__(self, image,x,y):
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Pigeon(Parent):
	def __init__(self, image, x, y):
		image.set_colorkey(white_del)
		self.image = image
		super().__init__(image,x,y)

	def draw_p(self):
		# scale_p = (self.image.get_height()/(self.image.get_height()+self.rect.y-branch_length))
		screen.blit(self.image, (self.rect.x,self.rect.y - (self.image.get_height()/7)))

class Basket(Parent):
	def __init__(self,image,x,y,scale):
		width = image.get_width()
		height = image.get_height()
		image.set_colorkey(white_del)
		self.image = pygame.transform.scale(image,(int(width * scale), int(height * scale)))
		super().__init__(image,x,y)
		self.clicked = False

	def draw(self):
		screen.blit(self.image, (self.rect.x,self.rect.y))

class P_poop():
	def __init__(self,width, height, x, y,gravity):
		self.width = width
		self.height = height 
		self.x = x 
		self.y = y + gravity
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

	def draw(self):
		pygame.draw.rect(screen,brown,self.rect,border_radius=50)

class Button(Parent):
	def __init__(self, image, color_del,scale,x,y):
		width = image.get_width()
		height = image.get_height()
		image.set_colorkey(color_del)
		self.image = pygame.transform.scale(image,(int(width * scale), int(height * scale)))
		super().__init__(image,x,y)
		self.clicked = False

	def draw_b(self):
		screen.blit(self.image, (self.rect.x, self.rect.y))

class Bar():
	def __init__(self, image, x, y, color1, color2,width, height):	# i think imma but this all in the Parent class ;-;
		#bar
		self.width = width
		self.height = height
		self.x = x
		self.y = y
		self.color1 = color1
		self.color2 = color2
		#image (x,y)
		image.set_colorkey(white_del)
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x + 3 +12
		self.rect.y = y + 3 + 8

	def draw(self):
		pygame.draw.rect(screen, self.color1,(self.x, self.y, self.width, self.height), border_radius= 100)
		pygame.draw.rect(screen, self.color2, (self.x+3, self.y+3, self.width-6, self.height-6), border_radius= 100)
		screen.blit(self.image, (self.rect.x, self.rect.y))

class Textbox():
	def __init__(self, text, type_text, font_size, xtb, ytb, padding):
		self.xtb = xtb
		self.ytb = ytb
		self.wtb = len(text)*(font_size/2.2) + padding		#number(2.5) is temporary
		self.htb = (font_size + 3) + padding		# (3) temporary
		self.xt = xtb + padding/2 + 5
		self.yt = ytb + padding/2
		self.render = type_text.render(str(text), True, black)

	def draw_t(self):
		pygame.draw.rect(screen, black,(self.xtb, self.ytb, self.wtb+4, self.htb+4), border_radius= 12)
		pygame.draw.rect(screen, white, (self.xtb+2, self.ytb+2, self.wtb, self.htb), border_radius= 10)
		screen.blit(self.render, (self.xt, self.yt))


def display_ob(object):
	object.draw_b()


# x_pnsa = screen_w - pause.get_width() - 4
# y_pnsa = 3
# pause_st_button = Button(pause, white_del,1, x_pnsa, y_pnsa)

#need to be calculated with the game_height
basket_object = Basket(basket,(1/6)*screen_w, 0.65*screen_h, 0.5)
# adjust those scale n specific number
distance = 12 + button_coin.get_width()		# no need to be button_coin tho, it should be each button but need more code to be profeesion
button1 = Button(button_coin,white_del, 1, 10, yb+15)
button2 = Button(button_velocity,white_del, 1, 10 + distance, yb+15)	# need scaling
button3 = Button(button_life,white_del,1, 10 + 2*distance,yb+15)

# Mission bout scaling:
# - scaling picture: pigeon, 3 button, branch
# - scaling other bar: life bar, coin bar, white bar
# - scale_button(x) = sth => 12
# - scale_button(y) = yb + sth => yb + 13

buttons = [button1, button2, button3]

prize_b_list = []
xp_list = []
yp_list = []
for i in range(len(buttons)):		# fun fact: could set buttons[i].get_height() if in class Button has self.image.get_height()
	xp = (buttons[i].rect.x + 14 + 5)
	yp = (buttons[i].rect.y + (buttons[i].image.get_height() - (prize.get_height()+14)))
	xp_list.append(xp)
	yp_list.append(yp)
	prize_b = Button(prize,white_del,1, xp, yp)
	prize_b_list.append(prize_b)	# dude, u need to find sth that need self.image.get_width()/get_height()

cb_w = 234	#need scale
cb_h = 73
last_p = buttons[len(prize_b_list)-1]
xcb = last_p.rect.x + last_p.image.get_width() + 12
ycb = yb + b_h/2 - cb_h/2
coin_bar = Bar(coin, xcb, ycb, white, black, cb_w, cb_h)

lb_w = 160 #need scale
lb_h = 70
xlb = 14
ylb = 0 + bar_h/2 - lb_h/2
life_bar = Bar(life_heart, xlb, ylb, black, white, lb_w, lb_h)

vertical_line_x = lb_w + 2*xlb

text_c = "Increase the amount of the picked coins!"
text_v = "Reset the velocity of those pigeon's poop!"
text_l = "Gain 1 extra life!"
text = [text_c,text_v,text_l]
# box_v = Textbox(text_c, b_c_text, 16, 100, 100, 15)
# box_c = Textbox(text_v, b_v_text, 16, 100, 100, 15)
# box_l = Textbox(text_l, b_l_text, 16, 100, 100, 15)

boxes = []
padding = 10
for i in range(len(text)):
	xt = buttons[i].rect.x + (buttons[i].image.get_width()/3)
	yt = (yb + 15) - (16 + 3) - padding - 4
	box = Textbox(text[i], b_text[i], 16, xt, yt, padding)
	boxes.append(box)

check = 0
running = True
check_if_added_api = True
check_score = 0
while running:
	screen.fill(sky)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:
				if increase_coin < 200 and coin_d >= prize_d[0]:
					coin_d -= prize_d[0]
					if prize_d[0] < 2000:
						prize_d[0] += 100
					increase_coin += 10
					text_fd = "You can now get {} coins every time you catch the poop!".format(increase_coin)

			if event.key == pygame.K_s:
				if prize_d[1] < 4000:
					if coin_d >= prize_d[1]:
						coin_d -= prize_d[1]
						prize_d[1] += 200
						velocitypx = 0.3
						text_fd = "You reseted the velocity of the pigeon's poop!"

			if event.key == pygame.K_d:
				if life < 50 and coin_d >= prize_d[2]:
					coin_d -= prize_d[2]
					if prize_d[2] < 10000:
						prize_d[2] += 500
					life += 1
					text_fd = "You get an extra life!"

			for i in range(len(buttons)):
				if prize_d[0] == 2000 or prize_d[1] == 4000 or prize_d[2] == 10000:
					prize_d.remove(prize_d[i])
					prize_d.insert(i, "MAX")


		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				pos = pygame.mouse.get_pos()
				if basket_object.rect.collidepoint(pos):
					basket_object.clicked = True
				for i in range(len(buttons)):
					if buttons[i].rect.collidepoint(pos):
						if i == 0:
							if increase_coin < 200 and coin_d >= prize_d[0]:
								coin_d -= prize_d[0]
								if prize_d[0] < 2000:
									prize_d[0] += 100
								increase_coin += 10
								text_fd = "You can now get {} coins every time you catch the poop!".format(increase_coin)
						if i == 1:
							if prize_d[1] < 4000:
								if coin_d >= prize_d[1]:
									coin_d -= prize_d[1]
									prize_d[1] += 200
									velocitypx = 0.3
									text_fd = "You reseted the velocity of the pigeon's poop!"
						if i == 2:
							if life < 50 and coin_d >= prize_d[2]:
								coin_d -= prize_d[2]
								if prize_d[2] < 10000:
									prize_d[2] += 500
								life += 1
								text_fd = "You get an extra life!"

						if prize_d[0] == 2000 or prize_d[1] == 4000 or prize_d[2] == 10000:
							prize_d.remove(prize_d[i])
							prize_d.insert(i, "MAX")

		if event.type == pygame.MOUSEBUTTONUP:
			basket_object.clicked = False

		if event.type == pygame.MOUSEMOTION:
			if basket_object.clicked == True:
				pos = pygame.mouse.get_pos()
				basket_object.rect.x = pos[0] - (basket_object.image.get_width()/2)
				basket_object.rect.y = pos[1] - (basket_object.image.get_height()/2)
	
	if coin_d > 1000000:
		coin_d = 999000

	if life <= 0:
		running = False
		print("game over")

	if number_of_pigeons == 0:
		changepix = random.choice(list_pix)
		list_changed.append(changepix)

		list_px.append(changepix)
		list_pix.remove(changepix)

		number_of_pigeons += 1

	if number_of_pigeons == 1:
		pigeon_ob = Pigeon(pigeon, pigeon_x+list_changed[0], pigeon_y) #here 1
		pigeon_ob.draw_p()
		poop = P_poop(poops,poops,poopx + changepix, poopy, p_gravity)
		poopx = ((pigeon_x + (pigeon_w/2)) - poops/2)

	p_gravity += float(velocitypx)

	if pygame.Rect.colliderect(poop.rect,basket_object.rect) or p_gravity > (screen_h - pigeon_y):
		p_gravity = 0
		poopx = ((pigeon_x + (pigeon_w/2)) - poops/2)
		poopx += (random.choice(list_px))
		if pygame.Rect.colliderect(poop.rect,basket_object.rect):
			score += 10
			coin_d += increase_coin
			check_score += 10
		else:
			score -= 10
			life -= 1
			check_score -= 10
				# need to change here
		if check_score == 50 and velocitypx < 1.4:
			check_score = 0
			velocitypx += 0.06
		print(list_px,list_pix,list_changed, velocitypx, check_score, score)

	if score == 400 or score == 300 or score == 200 or score == 100:
		if score not in scores:
			scores.append(score)
			if check_if_added_api:
				if number_of_pigeons >= 5:
					check_if_added_api = False
				pigeon_x = 50
				poopx_x = (pigeon_x + (pigeon_w/2)) - poops/2

				changepix = random.choice(list_pix)
				list_changed.append(changepix)

				list_px.append(changepix)
				list_pix.remove(changepix)

				number_of_pigeons += 1

	if number_of_pigeons > 1:
		poop = P_poop(poops,poops,poopx,poopy,p_gravity)
		# demo: if number of pi > 2 => rand 3 poop
		for i in list_changed:
			pigeon_ob = Pigeon(pigeon, pigeon_x + i, pigeon_y) #here 2
			pigeon_ob.draw_p()

	pygame.draw.rect(screen,white,(0,0,bar_length,bar_h))
	pygame.draw.line(screen,black,(0,0),(bar_length, 0), width= 5)
	pygame.draw.line(screen,black,(vertical_line_x,0),(vertical_line_x,bar_h), width= 3)
	pygame.draw.line(screen,black,(0,bar_h),(bar_length,bar_h), width= 3)

	screen.blit(branch, (0, branch_length))

	pygame.draw.rect(screen, bar_color, (xb, yb, screen_w, b_h))
	pygame.draw.line(screen, black, (0, yb - 1), (screen_w, yb - 1), width= 5)	# number (1) is also unknown to scale

	for i in range(len(boxes)):
		pos = pygame.mouse.get_pos()
		if buttons[i].rect.collidepoint(pos):
			boxes[i].draw_t()

	coin_bar.draw()
	life_bar.draw()

	d_text_render = d_text.render(text_fd, True, black)
	screen.blit(d_text_render, (5, bar_h + 5))
	score_render = score_text.render("Score: " + str(score), True,black)
	screen.blit(score_render,(vertical_line_x + 20, 20)) #temporary (20, 40)

	if score > highscore:
		highscore = score
	highscore_render = highscore_text.render("High Score: " + str(highscore), True, black)
	screen.blit(highscore_render, (vertical_line_x + 20, 40 + 24))
	life_render = life_text.render(str(life), True, black)	# equation below is just temporary			# the number of (35) is the font size
	screen.blit(life_render,(life_bar.rect.x + life_bar.image.get_width() + 21, (life_bar.rect.y + life_bar.image.get_height()/2) - 35/2 - 6)) #number (6) is kinda unknown to scale
	coin_render = coin_text.render(str(coin_d), True, white)
	screen.blit(coin_render, (coin_bar.rect.x + coin_bar.image.get_width() + 21, (coin_bar.rect.y + coin_bar.image.get_height()/2) - 35/2 - 6))

	for button in buttons:
		display_ob(button)

	for i in range(len(prize_b_list)):
		xt = xp_list[i] + 10 				# (18) is also the font_size
		yt = yp_list[i] + prize_b_list[i].image.get_height()/2 - 18/2 - 3 	#unknown (3)
		display_ob(prize_b_list[i])
		prize_render = prize_text[i].render(str(prize_d[i]), True, black)
		screen.blit(prize_render, (xt, yt))

	poop.draw()
	basket_object.draw()
	pygame.display.update()

with open("highscore_pi.txt", "w") as f:
	f.write(str(highscore))

pygame.quit()

# sum up what i have learn:
# - sprite, sprite.Group(), .add(sprite_class)
# - pygame.image.load("sth.png").set_colorkey(need_transparent_color)
# - new_image = pygame.transform.scale(image,(new_width,new_height))
# - pygame.image.load("sth.png").get_rect().collidepoint((x,y)); pygame.Rect.coliderect((rect1,rect2))
# - pygame.mouse.get_pos() => (x,y)
# - sound = pygame.mixer.Sound("sth.wav") => sound.play()
# - get_rect()