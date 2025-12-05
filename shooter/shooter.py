import pygame
import random
import sys
class Input_Box:
    def __init__(self, rect):
        self.rect = rect
        self.text = ""
    

    def event_handle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key != pygame.K_SPACE and event.unicode in "qwertyuiopasdfghjklzxcvbnm1234567890":
                if len(self.text) <= 8:
                    self.text += event.unicode.upper()
    def draw(self):
        pygame.draw.rect(SCREEN, (0,0,0), self.rect)
        pygame.draw.rect(SCREEN, (255,255,255), self.rect, 2)

        txt_surf = SCOREFONT.render(self.text, True, (255,255,255))
        SCREEN.blit(txt_surf, (self.rect.x + 10, self.rect.y))
    


class Cursor:
    def __init__(self):
        self.coords = [0,0]
        self.texture = pygame.image.load("crosshair.png")
        self.texture = pygame.transform.scale(self.texture, [50,50])
    def refresh(self):
        self.coords = pygame.mouse.get_pos()
    def draw(self):
        SCREEN.blit(self.texture, [self.coords[0]-25, self.coords[1]-25]) #display full hearts

pygame.init()

class Player:
    def __init__(self):
        self.health = 10
        self.score = 0

        self.heart = pygame.image.load("heart.png") #full heart image
        self.heart = pygame.transform.scale(self.heart, [25, 25])

        self.empty_heart = pygame.image.load("heart_empty.png") #empty heart image
        self.empty_heart = pygame.transform.scale(self.empty_heart, [25, 25])


    def display_health(self):
        """displays the health bar"""

        for heart in range(self.health):
            SCREEN.blit(self.heart, [heart*25+WIDTH/3,HEIGHT-25]) #display full hearts
        for damaged_heart in range(10-self.health):
            SCREEN.blit(self.empty_heart, [self.health*25+damaged_heart*25+WIDTH/3, HEIGHT-25]) #display empty hearts
    def damage(self):
        """decreases health by one"""

        self.health -= 1 #yeah this function was unnecessary 


class Target:
    def __init__(self,x,y):
        """class for target objects"""
        self.x = x
        self.y = y

        self.move_to = [random.random()*(WIDTH),random.random()*(HEIGHT)] #where the targets move towards


        self.WIDTH = TARGET_WIDTH #the size of each target
        self.HEIGHT = TARGET_HEIGHT

        self.colour = (255,0,0) #red
        self.hidden_timer = 0 #how long they are hidden for, 0 at beginning as they begin unhidden

        self.texture = pygame.image.load("target.png") #tnt texture
        self.texture = pygame.transform.scale(self.texture, [self.WIDTH, self.HEIGHT]) #scale to the size of target
        self.rect = pygame.rect.Rect(self.x, self.y, self.WIDTH, self.HEIGHT) #collision rect for handling mouse clicks
        self.time = LIFETIME #how long until they deal damage to player

        self.colour = [random.random()*100 for i in range(3)]
    def click(self, location):
        """takes in coordinates as list or tuple returns boolean for collision"""
        return self.rect.collidepoint(location)
    # this function is a bit stupid as it just does what pygames click does
        
        
    def refresh(self, deltaT):
        """This function moves targets, decreases relevant timers and unhides if needed. 
        Delta T is the length of the last frame, normalises movement and animation, 
        measured in ms. It will return true on damage, otherwise None"""

        self.x, self.y = pygame.math.lerp(self.x, self.move_to[0], 0.001), pygame.math.lerp(self.y, self.move_to[1], 0.001) #linear interpilation function, moves quicker with more distance
        self.rect = pygame.rect.Rect(self.x, self.y, self.WIDTH, self.HEIGHT) #reset the collision rect as coordinates have changed

        if self.hidden_timer > 0: #decrease the hidden timer if the object is hidden
            self.hidden_timer -= deltaT
        else:
            self.draw() #draw the sprite
        if self.time < 0:
            self.hide()
            return True
        self.time -= deltaT #decrease damage timer
        
    
    def hide(self):
        self.colour = [random.random()*100 for i in range(3)]

        """moves sprite to random location and hides it for HIDDEN_TIME seconds"""
        self.hidden_timer = HIDDEN_TIME #set hidden timer
        self.x, self.y = random.random()*(WIDTH-self.WIDTH), random.random()*(HEIGHT-self.HEIGHT) #reset coordinates
        self.time = LIFETIME+HIDDEN_TIME
        self.rect = pygame.rect.Rect(self.x, self.y, self.WIDTH, self.HEIGHT) # reset rect as coordinates have changed
        sound = pygame.mixer.Sound("explode.mp3")
        sound.set_volume(0.3)
        pygame.mixer.find_channel(True).play(sound)
        self.move_to = [random.random()*(WIDTH),random.random()*(HEIGHT)] #where the targets move towards


    def draw(self):
        """draws the target sprite"""
        SCREEN.blit(self.texture, [self.x, self.y])

WIDTH = 800 #window width
HEIGHT = 600 #window height
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT)) #object for the window
HIDDEN_TIME = 500 #constant for how long targets are hidden for after being clicked
SCOREFONT = pygame.font.SysFont("Minecraft", 50) #font object
LIFETIME = 4000  #how long targets last til they do damage, in miliseconds

BACKGROUND = pygame.image.load("moon.jpg") #image bg
BACKGROUND = pygame.transform.scale(BACKGROUND, [WIDTH, HEIGHT]) #scale to window size
TARGET_WIDTH = 51.2*2
TARGET_HEIGHT = 42.8*2

input_name_box = Input_Box(pygame.rect.Rect(WIDTH/2-200, 500, 340, 50))
pygame.mouse.set_visible(False)

def main():
    cursor = Cursor()

    time = 0 # global timer for player
    spawn_timer = 0 # timer for every new enemy spawn

    target_list = [Target(random.random()*(WIDTH-TARGET_WIDTH), random.random()*(HEIGHT-TARGET_HEIGHT))] #list[Target..]
    player = Player() #contains health and score as well as heart textures
    clock=pygame.time.Clock()

    playing = True

    while playing:
        delta_time = clock.tick() #ms
        SCREEN.blit(BACKGROUND, [0,0]) #print bg
        time += delta_time #increment time by length of last frame
        spawn_timer += delta_time
        if 40000 > spawn_timer > 10000:
            target_list.append(Target(random.random()*WIDTH, random.random()*HEIGHT))
            spawn_timer = 0 # append a new target every 10000 ms (10s)

        for event in pygame.event.get(): #pygame input handler
            if event.type == pygame.MOUSEBUTTONDOWN: #left click
                sound = pygame.mixer.Sound("sound/miss.mp3")
                for target in target_list:

                    if target.click(pygame.mouse.get_pos()): # collision for each target
                        target.hide()
                        player.score += 1
                        sound = pygame.mixer.Sound("sound/shoot.mp3")
                sound.set_volume(0.5)

                pygame.mixer.find_channel(True).play(sound)
            if event.type == pygame.QUIT: #quit 
                pygame.quit()
                sys.exit()
                range("hello")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    player.health = 0

        for target in target_list: 
            if target.refresh(delta_time): #refresh target data, returns true after tnt has lasted > 4s
                player.damage() #-1 hp

        
        SCREEN.blit(SCOREFONT.render(f"Points: {player.score} Time: {round(time/100)/10}", False, (255,255,255)), (0,0)) #Score:... Time:...
        player.display_health() #`draw`s heart icons

        if player.health <= 0: #loss condition, breaks loop
            playing = False
        cursor.refresh()
        cursor.draw()
        pygame.display.flip() # update window

    return(player.score) #returns score upon loss
score = 0
higher = 0
first_play = True
while True:
    flag = True
    
    while flag:
        SCREEN.fill((0,0,0))
        if first_play:
            losertext = SCOREFONT.render(f"Press space to continue", False, (255,0,0))
            SCREEN.blit(losertext, (WIDTH/2-losertext.get_width()/2,HEIGHT/2-2*losertext.get_height()/2))

            losertext = SCOREFONT.render(f"Input name below", False, (255,0,0))
            SCREEN.blit(losertext, (WIDTH/2-losertext.get_width()/2,HEIGHT/2+2*losertext.get_height()/2))
        else:
            SCREEN.fill((0,0,0))

            losertext = SCOREFONT.render(f"You Died!", False, (255,255,255)) #displaying text
            SCREEN.blit(losertext, (WIDTH/2-losertext.get_width()/2,100))


            losertext = SCOREFONT.render(f"Press space to continue", False, (255,0,0))
            SCREEN.blit(losertext, (WIDTH/2-losertext.get_width()/2,HEIGHT/2-2*losertext.get_height()/2))

            losertext = SCOREFONT.render(f"Input name below", False, (255,0,0))
            SCREEN.blit(losertext, (WIDTH/2-losertext.get_width()/2,HEIGHT/2))
        for event in pygame.event.get():
            input_name_box.event_handle(event)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    flag = False
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                range("hello")
        input_name_box.draw()
        pygame.display.update()
    score = main()
    first_play = False
