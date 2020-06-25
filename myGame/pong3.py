import pygame
import pgzrun
import sys
from random import *

INCREASESPEED = 5
TITLE = 'Pong'

WIDTH = 800
HEIGHT = 600

WINDOWWIDTH = WIDTH
WINDOWHEIGHT = HEIGHT

BASICFONTSIZE = 20
BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

#Global Variables to be used through our program
LINETHICKNESS = 10
PADDLESIZE = 100
PADDLEOFFSET = 20

# Set up the colours
BLACK     = (0  ,0  ,0  )
WHITE     = (255,255,255)

# width and height of a player paddle
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT)) 

predict_y = WINDOWHEIGHT/2

#Draws the arena the game will be played in. 
def drawArena():
    DISPLAYSURF.fill((0,0,0))
    #Draw outline of arena
    pygame.draw.rect(DISPLAYSURF, WHITE, ((0,0),(WINDOWWIDTH,WINDOWHEIGHT)), LINETHICKNESS*2)
    #Draw centre line
    pygame.draw.line(DISPLAYSURF, WHITE, (int(WINDOWWIDTH/2),0),(int(WINDOWWIDTH/2),WINDOWHEIGHT), int(LINETHICKNESS/4))

#Draws the paddle
def drawPaddle(paddle):
    #Stops paddle moving too low
    if paddle.bottom > WINDOWHEIGHT - LINETHICKNESS:
        paddle.bottom = WINDOWHEIGHT - LINETHICKNESS
    #Stops paddle moving too high
    elif paddle.top < LINETHICKNESS:
        paddle.top = LINETHICKNESS
    #Draws paddle
    pygame.draw.rect(DISPLAYSURF, WHITE, paddle)

#draws the ball
def drawBall(ball):
    pygame.draw.rect(DISPLAYSURF, WHITE, ball)

#moves the ball returns new position
def moveBall(ball, ballDirX, ballDirY):
    ball.x += (ballDirX * INCREASESPEED)
    ball.y += (ballDirY * INCREASESPEED)
    return ball

#Checks for a collision with a wall, and 'bounces' ball off it.
#Returns new direction
def checkEdgeCollision(ball, ballDirX, ballDirY):
    if ball.top == (LINETHICKNESS) or ball.bottom == (WINDOWHEIGHT - LINETHICKNESS):
        ballDirY = ballDirY * -1
        #print(ball.top)
        #print(ball.bottom)
    if ball.left == (LINETHICKNESS) or ball.right == (WINDOWWIDTH - LINETHICKNESS):
        ballDirX = ballDirX * -1
        calculate2(ball.y)
    return ballDirX, ballDirY

#Checks is the ball has hit a paddle, and 'bounces' ball off it.     
def checkHitBall(ball, paddle1, paddle2, ballDirX):
    global predict_y
    if ballDirX == -1 and paddle1.right == ball.left and paddle1.top < ball.top and paddle1.bottom > ball.bottom:
        print(calculate1(ball.y))
        return -1
    elif ballDirX == 1 and paddle2.left == ball.right and paddle2.top < ball.top and paddle2.bottom > ball.bottom:
        print(ball.x)
        return -1
    else: return 1

#Checks to see if a point has been scored returns new score
def checkPointScored(paddle1, ball, score, ballDirX):
    #reset points if left wall is hit
    if ball.left == LINETHICKNESS: 
        return 0
    #1 point for hitting the ball
    elif ballDirX == -1 and paddle1.right == ball.left and paddle1.top < ball.top and paddle1.bottom > ball.bottom:
        score += 1
        return score
    #5 points for beating the other paddle
    elif ball.right == WINDOWWIDTH - LINETHICKNESS:
        score += 5
        return score
    #if no points scored, return score unchanged
    else: return score

#Artificial Intelligence of computer player       
def artificialIntelligence(ball, ballDirX, paddle2):
    #If ball is moving away from paddle, center bat
    if ballDirX < 0 :
        if paddle2.centery < (WINDOWHEIGHT/2):
            paddle2.y += INCREASESPEED
        elif paddle2.centery > (WINDOWHEIGHT/2):
            paddle2.y -= INCREASESPEED
    #if ball moving towards bat, track its movement. 
    elif ballDirX > 0:
        if paddle2.centery < ball.centery:
            paddle2.y += INCREASESPEED
        else:
            paddle2.y -= INCREASESPEED
    return paddle2

def artificialIntelligenceleft(ball,ballDirX, paddle1):
  if ballDirX == 1 :
    if paddle1.centery < WINDOWHEIGHT/2:
        paddle1.y += INCREASESPEED
    elif paddle1.centery > WINDOWHEIGHT/2:
        paddle1.y -= INCREASESPEED
  elif ballDirX == -1:
    if paddle1.centery < ball.centery:
         paddle1.y += round(2*random()) * INCREASESPEED
    else:
        paddle1.y += -round(2*random()) *INCREASESPEED
  return paddle1

def calculate1(ballY):   #공격이 성공 했을 때 공의 경로를 예측
    global ballDirY
    global predict_y
    if ballDirY > 0:
        if ballY > 400:
            predict_y = ballY - 400
        else:
            predict_y = 400 - ballY
    else:
        if ballY < 180:
            predict_y = 400 + ballY
        else:
            predict_y = 760 - ballY
    return predict_y

def calculate2(ballY):   #공격이 실패 했을 때 공의 경로를 예측
    global ballDirY
    global predict_y
    if ballDirY > 0:
        if ballY > 420:
            predict_y = ballY - 420
        else:
            predict_y = 420 - ballY
    else:
        if ballY < 160:
            predict_y = 420 + ballY
        else:
            predict_y = 740 - ballY
    return predict_y    

def smartArtificialIntelligence(ball,ballDirX,paddle2): #예측한 방향으로 paddle을 보냄
    global predict_y
    if ballDirX < 0:
        if paddle2.centery < (WINDOWHEIGHT/2):
            paddle2.y += INCREASESPEED
        elif paddle2.centery > (WINDOWHEIGHT/2):
            paddle2.y -= INCREASESPEED
    elif ballDirX > 0:
        if paddle2.centery < predict_y:
            paddle2.y += INCREASESPEED
        else:
            paddle2.y -= INCREASESPEED
    return paddle2

#Displays the current score on the screen
def displayScore(score):
    resultSurf = BASICFONT.render('Score = %s' %(score), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (WINDOWWIDTH - 150, 25)
    screen.blit(resultSurf, resultRect)

#Initiate variable and set starting positions
#any future changes made within rectangles
ballX = WINDOWWIDTH/2 - LINETHICKNESS/2
ballY = WINDOWHEIGHT/2 - LINETHICKNESS/2
playerOnePosition = (WINDOWHEIGHT - PADDLESIZE) /2
playerTwoPosition = (WINDOWHEIGHT - PADDLESIZE) /2
score = 0

#Keeps track of ball direction
ballDirX = -1 ## -1 = left 1 = right
ballDirY = -1 ## -1 = up 1 = down

#Creates Rectangles for ball and paddles.
paddle1 = Rect(PADDLEOFFSET,playerOnePosition, LINETHICKNESS,PADDLESIZE)
paddle2 = Rect(WINDOWWIDTH - PADDLEOFFSET - LINETHICKNESS, playerTwoPosition, LINETHICKNESS,PADDLESIZE)
ball = Rect(ballX, ballY, LINETHICKNESS, LINETHICKNESS)

pygame.mouse.set_visible(0) # make cursor invisible

def on_mouse_move(pos):
    #mousex, mousey = pos
    #paddle1.y = mousey
    #print("Mouse button clicked at", pos)
    pass

def on_mouse_down(pos):
    print("mouse button cliked at", pos)

def draw():
    drawArena()
    drawPaddle(paddle1)
    drawPaddle(paddle2)
    drawBall(ball)

    displayScore(score)

def update():
    global ball
    global ballDirX, ballDirY
    global score
    global paddle1, paddle2
 
    ball = moveBall(ball, ballDirX, ballDirY)
    ballDirX, ballDirY = checkEdgeCollision(ball, ballDirX, ballDirY)
    score = checkPointScored(paddle1, ball, score, ballDirX)
    ballDirX = ballDirX * checkHitBall(ball, paddle1, paddle2, ballDirX)
    #paddle2 = artificialIntelligence (ball, ballDirX, paddle2)
    paddle2 = smartArtificialIntelligence(ball,ballDirX, paddle2)
    paddle1 = artificialIntelligenceleft(ball, ballDirX, paddle1)
    

pgzrun.go()