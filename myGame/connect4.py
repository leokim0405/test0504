import pgzrun

WIDTH = 1000
HEIGHT = 700
#WHITE = 0,0,0
nemopan = Rect((100, 30), (700, 600))
circle_list = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]
]
turn = 1

def draw():
  screen.clear()
  screen.draw.rect(nemopan, 'white')
  
  for row in range(6):
    for column in range(7):
      screen.draw.filled_circle((150+100*column,80+100*row),50,'white')
  for row2 in range(6):
    for column2 in range(7):
      if circle_list[row2][column2] == 1:
        screen.draw.filled_circle((150+100*column2, 80+100*row2), 50, 'red')
      elif circle_list[row2][column2] == 2:
        screen.draw.filled_circle((150+100*column2, 80+100*row2), 50, 'blue')
  if turn == 1:
    screen.draw.text("player 1's turn",(830,30))
  elif turn == 2:
    screen.draw.text("player 2's turn",(830,30))
  elif turn == 3:
    screen.draw.text("player 2 win",(830,30))
  elif turn == 4:
    screen.draw.text("player 1 win",(830,30))

def on_mouse_down(pos):
  global turn
  print("Mouse button clicked at", pos)
  if turn == 1:
    if pos[0] > 100 and pos[0] < 200:
      #circle_list[5][0] = 1
      paint(0)
    elif pos[0] > 200 and pos[0] < 300:
      #circle_list[5][1] = 1
      paint(1)
    elif pos[0] > 300 and pos[0] < 400:
      #circle_list[5][2] = 1
      paint(2)
    elif pos[0] > 400 and pos[0] < 500:
      #circle_list[5][3] = 1
      paint(3)
    elif pos[0] > 500 and pos[0] < 600:
      #circle_list[5][4] = 1
      paint(4)
    elif pos[0] > 600 and pos[0] < 700:
      #circle_list[5][5] = 1
      paint(5)
    elif pos[0] > 700 and pos[0] < 800:
      #circle_list[5][6] = 1
      paint(6)
  elif turn == 2:
    if pos[0] > 100 and pos[0] < 200:
      #circle_list[5][0] = 1
      paint(0)
    elif pos[0] > 200 and pos[0] < 300:
      #circle_list[5][1] = 1
      paint(1)
    elif pos[0] > 300 and pos[0] < 400:
      #circle_list[5][2] = 1
      paint(2)
    elif pos[0] > 400 and pos[0] < 500:
      #circle_list[5][3] = 1
      paint(3)
    elif pos[0] > 500 and pos[0] < 600:
      #circle_list[5][4] = 1
      paint(4)
    elif pos[0] > 600 and pos[0] < 700:
      #circle_list[5][5] = 1
      paint(5)
    elif pos[0] > 700 and pos[0] < 800:
      #circle_list[5][6] = 1
      paint(6)
  print("Mouse button clicked at", pos)
  
def update():
  global turn
  
  if win_check(turn):
    turn = turn + 2

def win_check(player):
  global turn

  for c in range(4):
    for r in range(6):
      if circle_list[r][c] == player and circle_list[r][c+1] == player and circle_list[r][c+2] == player and circle_list[r][c+3] == player:
        return True

  for c in range(7):
    for r in range(3):
      if circle_list[r][c] == player and circle_list[r+1][c] == player and circle_list[r+2][c] == player and circle_list[r+3][c] == player:
        return True

  for c in range(4):
    for r in range(3):
      if circle_list[r][c] == player and circle_list[r+1][c+1] == player and circle_list[r+2][c+2] == player and circle_list[r+3][c+3] == player:
        return True

  for c in range(4):
    for r in range(3, 6):
      if circle_list[r][c] == player and circle_list[r-1][c+1] == player and circle_list[r-2][c+2] == player and circle_list[r-3][c+3] == player:
        return True

def paint(x):
  global turn
  turn = -turn + 3
  for floor in range(5,-1,-1):
    if circle_list[floor][x] != 0:
      continue
    else:
      circle_list[floor][x] = turn
      break
  
  
  

pgzrun.go()