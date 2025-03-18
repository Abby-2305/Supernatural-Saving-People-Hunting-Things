import pygame

pygame.init() # Initialising the modules used

black = (0,0,0)
DarkRed = (30, 0, 0)
purple = (144, 41, 204)
red = (156, 18, 0)
i = 0
Jump = False
jumpCount = 10

infoObject = pygame.display.Info() # Creating variables of the resolution of the screen
Screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h)) # Creating the canvas

pygame.display.set_caption('Supernatural:"Saving People Hunting Things"') # Set game title

clock = pygame.time.Clock() # Defining pygame clock object

bg_img = pygame.image.load("pixil-frame-0.png")
bg_img = pygame.transform.scale(bg_img,(infoObject.current_w, infoObject.current_h))
############################################CLASSES##########################################################################################################
class Background():
    def __init__(self,image,speed):
        self.bgimage = pygame.image.load(image) # Loading the image
        self.bgimage = pygame.transform.scale(self.bgimage,((infoObject.current_w, infoObject.current_h)))
        self.rectBGimg= self.bgimage.get_rect()

        self.bgY1 = 0
        self.bgX1 = 0

        self.bgY2 = 0
        self.bgX2 = self.rectBGimg.width

        self.movingSpeed = speed # setting the speed of the background

    def update(self):
        self.bgX1 -= self.movingSpeed
        self.bgX2 -= self.movingSpeed
        if self.bgX1 <= -self.rectBGimg.width: #Resetting the coordinates of the image if it goes off screen
            self.bgX1 = self.rectBGimg.width
        if self.bgX2 <= -self.rectBGimg.width:
            self.bgX2 = self.rectBGimg.width
    def render(self):
        Screen.blit(self.bgimage, (self.bgX1, self.bgY1)) # Drawing the background to the screen
        Screen.blit(self.bgimage, (self.bgX2, self.bgY2))



class Sprite(pygame.sprite.Sprite):

    def __init__(self,x,y,a,b):
        super().__init__()
        self.image = pygame.Surface([a,b]) # Sets the size
        self.image.fill(purple)
        self.rect = self.image.get_rect() # Hitbox
        self.rect.x = x# Sets the position on the screen
        self.rect.y = y

class Enemy(pygame.sprite.Sprite):

    def __init__(self,x,y,a,b,enemyspeed):
        super().__init__()
        self.image = pygame.Surface([a,b]) # Sets the size
        self.image.fill(red)
        self.rect = self.image.get_rect() # Hitbox
        self.rect.x = x# Sets the position on the screen
        self.rect.y = y
        self.speed = enemyspeed

    def update(self,):
        self.rect.x-=self.speed
    
#############################################################################################################################################################
Player = Sprite(infoObject.current_w/4, (infoObject.current_h*(107/144))-30,30,30)
Enemy = Enemy(infoObject.current_w,  (infoObject.current_h*(107/144))-20,20,20,10)
SpriteGroup = pygame.sprite.Group() # Create a group
EnemyGroup = pygame.sprite.Group()
SpriteGroup.add(Player) # Add object to group
EnemyGroup.add(Enemy)

ground = Background("Bgd_path.png", 5)
##############################################GAMELOOP#######################################################################################################
gameExit = False
while not gameExit:

    for event in pygame.event.get():

        if event.type == pygame.QUIT: # Event quit
            gameExit = True
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: # Quit if ESC key pressed
                gameExit = True
                pygame.quit()
                quit()

    keys = pygame.key.get_pressed()
    if not(Jump):
        if keys[pygame.K_SPACE]:
            Jump = True
    else:
        if jumpCount >=-10:
            Player.rect.y -= jumpCount 
            jumpCount -= 1
        else: # This will execute if our jump is finished
            jumpCount = 10
            Jump = False
            Player.rect.y = (infoObject.current_h*(107/144))-30
            # Resetting our Variables
            
    Screen.fill(DarkRed)
    
    ground.update()
    ground.render()
    

    SpriteGroup.draw(Screen)
    EnemyGroup.draw(Screen)
    EnemyGroup.update()
    
    clock.tick(30)
    pygame.display.update()
