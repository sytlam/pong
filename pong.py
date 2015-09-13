# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
paddle1_vel = 0
paddle2_vel = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]

    # get random initial speed for the ball
    if (direction == RIGHT):
        ball_vel = [random.randrange(2, 4), -random.randrange(1, 3)]
    else:
        ball_vel = [-random.randrange(2, 4), -random.randrange(1, 3)]


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    # paddle1_pos and paddle2_pos refer to the upper left corner of the paddles
    paddle1_pos = [0, HEIGHT / 2 - HALF_PAD_HEIGHT]
    paddle2_pos = [WIDTH - PAD_WIDTH, HEIGHT / 2 - HALF_PAD_HEIGHT]
    
    # set paddle velocities
    paddle1_vel = paddle2_vel = 0
    
    score1 = score2 = 0
    spawn_ball(RIGHT)

def check_collision(pos):
    # collision with top or bottom wall
    if (pos[1] <= BALL_RADIUS or pos[1] >= HEIGHT - BALL_RADIUS):
        return "wall"
    # past the left gutter
    elif (pos[0] <= BALL_RADIUS + PAD_WIDTH): 
        if (pos[1] >= paddle1_pos[1] and pos[1] <= paddle1_pos[1] + PAD_HEIGHT):
            return "deflect"
        else:
            return "left score"
    # past the right gutter
    elif (pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS):
        if (pos[1] >= paddle2_pos[1] and pos[1] <= paddle2_pos[1] + PAD_HEIGHT):
            return "deflect"
        else:
            return "right score"
    else:
        return "none"

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel

    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    if check_collision(ball_pos) == "wall": # reverse ball direction
        #ball_vel[0] = -ball_vel[0]
        ball_vel[1] = -ball_vel[1]
    elif check_collision(ball_pos) == "deflect": # reverse ball direction + increase speed of ball
        ball_vel[0] *= 1.10
        ball_vel[1] *= 1.10
        ball_vel[0] = -ball_vel[0] 
    elif check_collision(ball_pos) == "left score":
        score2 += 1
        spawn_ball(RIGHT)
    elif check_collision(ball_pos) == "right score":
        score1 += 1
        spawn_ball(LEFT)
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos[1] += paddle1_vel
    paddle2_pos[1] += paddle2_vel
    
    # going off bottom of left gutter
    if (paddle1_pos[1] + PAD_HEIGHT >= HEIGHT): 
        paddle1_pos[1] = HEIGHT - PAD_HEIGHT
    # going off top of left gutter
    elif (paddle1_pos[1] <= 0):
        paddle1_pos[1] = 0
    # going off bottom of right gutter
    if (paddle2_pos[1] + PAD_HEIGHT >= HEIGHT):
        paddle2_pos[1] = HEIGHT - PAD_HEIGHT
    # going off top of right gutter
    elif (paddle2_pos[1] <= 0):
        paddle2_pos[1] = 0
    
    # draw paddles
    canvas.draw_polygon([(paddle1_pos[0], paddle1_pos[1]), (PAD_WIDTH, paddle1_pos[1]), (PAD_WIDTH, paddle1_pos[1] + PAD_HEIGHT), (0, paddle1_pos[1] + PAD_HEIGHT)], 1, "White", "White")
    canvas.draw_polygon([(paddle2_pos[0], paddle2_pos[1]), (WIDTH, paddle2_pos[1]), (WIDTH, paddle2_pos[1] + PAD_HEIGHT), (paddle2_pos[0], paddle2_pos[1] + PAD_HEIGHT)], 1, "White", "White")
       
    # draw scores
    canvas.draw_text(str(score1), [200, 75], 40, "White")
    canvas.draw_text(str(score2), [400, 75], 40, "White")
        
def keydown(key):
    global paddle1_vel, paddle2_vel

    # paddle movement
    if (key == simplegui.KEY_MAP['w']):
        paddle1_vel = -4
    elif (key == simplegui.KEY_MAP['s']):
        paddle1_vel = 4
    elif (key == simplegui.KEY_MAP['up']):
        paddle2_vel = -4
    elif (key == simplegui.KEY_MAP['down']):
        paddle2_vel = 4
   
def keyup(key):
    global paddle1_vel, paddle2_vel

    # stop paddle movement
    if (key == simplegui.KEY_MAP['w']):
        paddle1_vel = 0
    elif (key == simplegui.KEY_MAP['s']):
        paddle1_vel = 0
    elif (key == simplegui.KEY_MAP['up']):
        paddle2_vel = 0
    elif (key == simplegui.KEY_MAP['down']):
        paddle2_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game, 100)

# start frame
new_game()
frame.start()