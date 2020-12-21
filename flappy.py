import pygame
import time
import sys
import random
# print(pygame.__version__)
# Note: using pygame version: 2.0.0.dev6 with python 3.7.6

def draw_floor():
    # Adding 2 touching floor surfaces next to each other
    # so that it creates a fluid floor animation effect --
    # Note: we will call this animation in the event loop below
    screen.blit(floor_surface,(floor_x_pos,900))
    screen.blit(floor_surface,(floor_x_pos + 576,900))

def create_pipe():
    # Function to add a rect on a newly create pipe surface
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (700,random_pipe_pos - 300))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    # Function which takes in a list of pipes
    # Moves each pipe to the left by a certain amount
    # Returns the list of newly moved pipes
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    # Function which takes in a list of pipes
    # Draws every pipe in the list
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface,pipe)
        else:
            # Create inverted pipes at the top --
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe,pipe)

def check_collision(pipes):
    # Function to check collision between the bird and pipes
    for pipe in pipes:
        # Check if bird collided with the pipes, the colliderect() returns a boolean: True --
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False

    # Check if bird goes way up the screen or hits the floor, then we treat that as collision --         
    if(bird_rect.top < -100 or bird_rect.bottom >= 900):
        return False

    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement*3, 1)
    return new_bird

def bird_animation():
    # Function to take a bird image and put a rectangle around it --
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    # Function to add current score at the top and high score at the bottom of the screen --
    if(game_state == 'main_game'):
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface,score_rect)
    
    elif(game_state == 'game_over'):
        # score_surface = game_font.render("Score: {}".format(str(int(score))),True,(255,255,255))
        score_surface = game_font.render("Score: {}".format(str(int(score))),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface,score_rect)

        # Also display high score at the end of the game --
        high_score_surface = game_font.render("High Score: {}".format(str(int(high_score))),True,(255,255,255))
        # high_score_surface = game_font.render(str(int(high_score)),True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (288,850))
        screen.blit(high_score_surface,high_score_rect)

def update_score(score, high_score):
    # Function to update high score
    if score > high_score:
        high_score = score
    
    return high_score


# Initialize pygame and pygame.mixer to avoid lag when sound plays in the game--
pygame.init()
pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)

# Define canvas to draw game objects --
screen = pygame.display.set_mode((576,1024))
pygame.display.set_caption("Murtaza's Flappy Bird")

# Adding frames per second to determine how quickly objects move on the game window
fps = 120
clock = pygame.time.Clock()

# Adding fonts to the game to show scores --
game_font = pygame.font.Font('04B_19.ttf', 40)

# Game variables to control the bird's movements --
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

# Note: Display surface is the main window of the game which you see when the game runs --
# Note: Every other image inside the window is a regular surface

# Creating a reference to the background image of the window --
# Add as many background images to choose from in the background_list --
background_list = ['game_images/background-night.png','game_images/background-night.png']
selected_bg = random.choice(background_list)
bg_surface = pygame.image.load(selected_bg).convert_alpha()
# Note: The convert() function is optional as it only makes the image load faster on the screen
# Note: To actually load this on the screen, we use the blit() method in the game loop

# To scale the background image to 2x on the screen (or to double the bg_surface in size), we use another function --
bg_surface = pygame.transform.scale2x(bg_surface)

# Adding a floor surface to the game in the same way as the bg_surface --
floor_surface = pygame.image.load('game_images/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

# Adding bird flaps to the game --
# Creating list of available birds -- Red, Blue and Yellow --
bird_list = [('game_images/redbird-downflap.png','game_images/redbird-midflap.png','game_images/redbird-upflap.png'),
            ('game_images/bluebird-downflap.png','game_images/bluebird-midflap.png','game_images/bluebird-upflap.png'),
            ('game_images/yellowbird-downflap.png','game_images/yellowbird-midflap.png','game_images/yellowbird-upflap.png')]

selected_bird = random.choice(bird_list)

bird_downflap = pygame.image.load(selected_bird[0]).convert_alpha()
bird_downflap = pygame.transform.scale2x(bird_downflap)
bird_midflap = pygame.image.load(selected_bird[1]).convert_alpha()
bird_midflap = pygame.transform.scale2x(bird_midflap)
bird_upflap = pygame.image.load(selected_bird[2]).convert_alpha()
bird_upflap = pygame.transform.scale2x(bird_upflap)

bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100, 512))

# Now we pick a new bird image (from downflap,midflap,upflap) every 2 milliseconds --
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)

'''
# Adding the bird surface to the game --
bird_surface =  pygame.image.load('game_images/bluebird-midflap.png').convert_alpha()
bird_surface = pygame.transform.scale2x(bird_surface)
# Now we draw a rect around the bird surface, since rectangles allow detection of collisions --
bird_rect = bird_surface.get_rect(center = (100, 512))
# Note: Just like the bg_surface and the floor_surface, we will blit() this also in the event loop
'''

# Adding the pipe surface to the game --
available_pipes = ['game_images/pipe-green.png','game_images/pipe-green.png']
selected_pipe = random.randint(0, len(available_pipes) - 1)
pipe_surface = pygame.image.load(available_pipes[selected_pipe]).convert_alpha()
pipe_surface = pygame.transform.scale2x(pipe_surface)

# Now we want to create a new pipe every 1.2 seconds on the screen. We will put the rect on
# top of the pipe surface and add those newly created pipes to the pipe_list --  
pipe_list = []
# Note: pygame.USEREVENT is a user event which doesn't depend the user clicking something
# Instead it is dictated internally by a timer --
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
pipe_height = [400,500,600,800]

game_over_surface = pygame.image.load('game_images/message.png').convert_alpha()
game_over_surface = pygame.transform.scale2x(game_over_surface)
game_over_rect = game_over_surface.get_rect(center = (288,512)) 

# Adding sounds to the bird's movements (flapping) --
flap_sound = pygame.mixer.Sound('game_sounds/sfx_wing.wav')
death_sound = pygame.mixer.Sound('game_sounds/sfx_hit.wav')
score_sound = pygame.mixer.Sound('game_sounds/sfx_point.wav')
score_sound_countdown = 100

# Display the window using flip() --
pygame.display.flip()

# Game Loop to add game logic and update character movements on canvas--
while True:
    # Adding an Event Loop to capture and respond to events --
    # Events can be: clicking mouse, keystroke, closing windows, etc.

    for event in pygame.event.get():
        # Closing the window in response to a quit event --
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active == True:
                # Make the bird jump each time we press the spacebar --
                bird_movement = 0
                bird_movement -= 8
                flap_sound.play()
            
            if event.key == pygame.K_SPACE and game_active == False:
                # Restart the game and re-initialize the bird's position and clear the pipe locations --
                game_active = True
                del pipe_list [:]
                bird_rect.center = (100,512)
                bird_movement = 0
                score = 0
        
        # Each time the event list detects SPAWNPIPE (which is a pygame.USEREVENT),
        # then we add a new pipe to the screen 
        elif event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
            # print(pipe_list)
        
        elif event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            
            bird_surface, bird_rect = bird_animation()

    # The blit() method would put the background image at top left (0,0) --
    screen.blit(bg_surface,(0,0))
    
    if game_active:
        # Moving the bird --
        bird_movement += gravity 
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)
        game_active = check_collision(pipe_list)

        # Moving the pipes --
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Updating game score --
        score += 0.01
        score_display('main_game')
        # score_sound_countdown -= 1

        # if(score_sound_countdown <= 0):
        #     score_sound.play()
        #     score_sound_countdown = 100
    
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display('game_over')

    # Moving the floor --
    # Since we want the floor animation to flow towards the left --
    floor_x_pos -= 1
    # Adding a constantly moving floor --
    draw_floor()
    if(floor_x_pos < -576):
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(fps)
