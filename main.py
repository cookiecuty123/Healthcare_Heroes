import pygame
import random
import math
from pygame import mixer

# initiate
pygame.init()

# create screen
screen = pygame.display.set_mode((720, 450))

# background
background = pygame.image.load("background.png")

#misc
score = 0
font = pygame.font.Font('GillSansMTBold.ttf', 32)

scoreX = 12
scoreY = 12

def showScore(x,y):
	theScore = font.render("Score: " + str(score), True, (50, 162, 225))
	screen.blit(theScore, (x,y))

#game over
gameOver = pygame.image.load("gameOver.png")

#success
success = pygame.image.load('success.png')

#lives
lives = 3

def showLives(x,y):
	theLives = font.render("Lives: " + str(lives), True, (50, 162, 225))
	screen.blit(theLives, (x,y))

# character
charX = 350
charY = 592
charXchange = 5
charYchange = 5

charIdleFront = pygame.image.load("character/characterIdleFront.png")
charIdleBack = pygame.image.load("character/characterIdleBack.png")
charIdleLeft = pygame.image.load("character/characterIdleLeft.png")
charIdleRight = pygame.image.load("character/characterIdleRight.png")

walkLeft = [pygame.image.load("character/characterWalkLeft.png"), pygame.image.load("character/characterIdleLeft.png"), pygame.image.load("character/characterWalkLeft2.png")]
walkRight = [pygame.image.load("character/characterWalkRight.png"), pygame.image.load("character/characterIdleRight.png"), pygame.image.load("character/characterWalkRight2.png")]

left = False
right = False
front = False
back = False

direction = ""

walkCount = 0

#virus
virusImg = []
virusXchange = []
virusYchange = []
virusX = []
virusY = []
numVirus = 16

for v in range(numVirus):
	virusImg.append(pygame.image.load('virus.png'))
	virusX.append(random.randint(0, 700))
	virusY.append(random.randint(0, 250))
	virusXchange.append(4)
	virusYchange.append(10)

nbrVirus = 0

#canon
canon = pygame.image.load("canon.png")

canonX = charX - 30
canonY = charY

#vaccine
vaccine = pygame.image.load("vaccine.png")

vaccineY = charY + 10
vaccineX = charX - 30

vaccineYchange = 10

state = "ready"




# functions
def redrawGameWindow():
	global walkCount
	global direction
	global virusImg
	global nbrVirus
	global virusX
	global virusY
	global canon
	global canonX
	global canonY
	global vaccineX
	global vaccineY
	global vaccine
	global lives
	global live1
	global live2
	global live3

	screen.blit(background, (0, 0))

	#character
	if walkCount >= 9:
		walkCount = 0

	if left:
		screen.blit(walkLeft[walkCount//3], (charX,charY))
		walkCount += 1
		direction = "left"
	
	elif right:
		screen.blit(walkRight[walkCount//3], (charX,charY))
		walkCount += 1
		direction = "right"

	elif front:
		screen.blit(charIdleFront, (charX,charY))
		walkCount += 1
		direction = "front"

	elif back:
		screen.blit(charIdleBack, (charX,charY))
		walkCount += 1
		direction = "back"
	
	else:
		if direction == "right":
			screen.blit(charIdleRight, (charX, charY))
		if direction == "left":
			screen.blit(charIdleLeft, (charX, charY))
		if direction == "front":
			screen.blit(charIdleFront, (charX, charY))
		if direction == "back":
			screen.blit(charIdleBack, (charX, charY))
		else:
			screen.blit(charIdleFront, (charX, charY))

	# vaccine

	screen.blit(vaccine, (vaccineX, vaccineY))
	#canon
	screen.blit(canon, (charX - 30, charY + 40))

	for v in range(numVirus):
		virus(virusX[v], virusY[v], v)

	showScore(scoreX, scoreY)

	showLives(580, 8)

	pygame.display.update()

def virus(x, y, v):
	screen.blit(virusImg[v], (x, y))

def throwVaccine(x, y):
	global state
	global vaccine
	state = "throw"

	screen.blit(vaccine, (x, y))

def isCollision(x, y, vaccineX, vaccineY):
	distance = math.sqrt((math.pow(x - vaccineX, 2)) + (math.pow(y - vaccineY, 2)))
	if distance < 27:
		return True

def updateVaccine():
	global vaccineX
	global vaccineY
	global vaccineYchange
	vaccineY = charY + 10
	vaccineX = charX - 30
	vaccineYchange = 10

def showGameOver():
	screen.blit(gameOver, (0, 0))
	pygame.display.update()
def showSuccess():
	screen.blit(success, (0, 0))
	pygame.display.update()

#screens
running = True

while running:
	lives = 3

	for event in pygame.event.get():
		#quit
		if event.type == pygame.QUIT:
			running = False
		
		#keys
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				charYchange = -5
				right = False
				left = False
				front = False
				back = True
			if event.key == pygame.K_DOWN:
				charYchange = 5
				right = False
				left = False
				front = True
				back = False
			if event.key == pygame.K_LEFT:
				charXchange = -5
				right = False
				left = True
				front = False
				back = False
			if event.key == pygame.K_RIGHT:
				charXchange = 5
				right = True
				left = False
				front = False
				back = False

			if event.key == pygame.K_SPACE:
				if state == "ready":
					#bullet_sound = mixer.Sound('laser.wav')
					#bullet_sound.play()
					state = "throw"
					throwVaccine(vaccineX, vaccineY)

			updateVaccine()

		else:
			charXchange = 0
			charYchange = 0
			left = False
			right = False
			front = True
			back = False
			walkCount = 0

	lives = 3
	#collision
	for v in range(numVirus):

		virusX[v] += virusXchange[v]
		if virusX[v] <= 0:
			virusXchange[v] = 7
			virusY[v] += virusYchange[v]
		elif virusX[v] >= 600:
			virusXchange[v] = -7
			virusY[v] += virusYchange[v]
		collision = isCollision(virusX[v], virusY[v], vaccineX, vaccineY)

		# lose lives
		if virusY[v] >= 580:
			lives -= 1

		if collision:
			vaccineY = 480
			state = "ready"
			score += 1
			#print(score_value)
			virusX[v] = random.randint(0, 700)
			virusY[v] = random.randint(0, 250)

		virus(virusX[v], virusY[v], v)

	if score == 20:
		showSuccess()
		pygame.display.update()
		break

	if lives == 0:
		showGameOver()
		pygame.display.update()
		break

	#movement
	charX += charXchange
	charY += charYchange

	if vaccineY <= 0:
		vaccineY = charY + 10
		state = "ready"
	if state == "throw":
		throwVaccine(vaccineX, vaccineY)
		vaccineY -= vaccineYchange

	#border
	if charX <= 0:
		charX = 0

	if charX >= 592:
		charX = 592
	
	if charY <= 0:
		charY = 0

	if charY >= 322:
		charY = 322



	redrawGameWindow()

	pygame.display.update()

