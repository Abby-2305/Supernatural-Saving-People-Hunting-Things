import pygame

pygame.init() # Initialising the modules used

Black = (0,0,0) # Creating the Variables
Purple = (144, 41, 204)
Red = (156, 18, 0)
DarkRed = (30, 0, 0)
Green = (0, 240, 0)
i = 0
Jump = False
jumpCount = 10
Score = 0
EnemyCount = 1


infoObject = pygame.display.Info() # Creating variables of the resolution of the screen
Screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h)) # Creating the canvas

pygame.display.set_caption('Supernatural:"Saving People Hunting Things"') # Set game title

clock = pygame.time.Clock() # Defining pygame clock object

bg_img = pygame.image.load("pixil-frame-0.png")
bg_img = pygame.transform.scale(bg_img,(infoObject.current_w, infoObject.current_h))
###########################################CLASSES##########################################################################################################
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
        self.image.fill(Purple)
        self.rect = self.image.get_rect() # Hitbox
        self.rect.x = x# Sets the position on the screen
        self.rect.y = y
        self.health = 100

class Bar(pygame.sprite.Sprite):

    def __init__(self,x,y,a,b,colour):
        super().__init__()
        self.image = pygame.Surface([a,b]) # Sets the size
        self.image.fill(colour)
        self.rect = self.image.get_rect() # Hitbox
        self.rect.x = x# Sets the position on the screen
        self.rect.y = y

    def update(self):
        self.image = pygame.Surface([Player.health,10])
        self.image.fill(Green)

class Enemy(pygame.sprite.Sprite):

    def __init__(self,x,y,a,b,enemyspeed):
        super().__init__()
        self.image = pygame.Surface([a,b]) # Sets the size
        self.image.fill(Red)
        self.rect = self.image.get_rect() # Hitbox
        
        self.rect.x = x# Sets the position on the screen
        self.rect.y = y
        self.speed = enemyspeed

    def update(self,):
        self.rect.x-=self.speed

class Bullet(pygame.sprite.Sprite):

    def __init__(self,x,y,a,b,color):
        super().__init__()
        self.image = pygame.Surface([a,b]) # Sets the size
        self.image.fill(color)
        self.rect = self.image.get_rect() # Hitbox
        self.rect.x = x# Sets the position on the screen
        self.rect.y = y

    def update(self):
        self.rect.x += 5
#############################################################################################################################################################
Player = Sprite(infoObject.current_w/4, (infoObject.current_h*(107/144))-30,30,30)
HealthBarPt1 = Bar(10,10,100,10,Red)
HealthBarPt2 = Bar(10,10,Player.health,10,Green)

SpriteGroup = pygame.sprite.Group() # Create a group
EnemyGroup = pygame.sprite.Group()
HealthBarGroup = pygame.sprite.Group()
BulletGroup = pygame.sprite.Group()

SpriteGroup.add(Player) # Add object to group
HealthBarGroup.add(HealthBarPt1)
HealthBarGroup.add(HealthBarPt2)

ground = Background("Bgd_path.png", 5)
##############################################GAMELOOP#######################################################################################################
gameExit = False
pressed = False
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
            if event.key == pygame.K_e:
                pressed = True

        if event.type == pygame.KEYUP:
            pressed = False

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

    if EnemyCount>0:
        enemy = Enemy(infoObject.current_w,  (infoObject.current_h*(107/144))-20,20,20,10)
        EnemyGroup.add(enemy)
        EnemyCount -=1
        

    for eachEnemy in EnemyGroup:
        Enemyhits = pygame.sprite.spritecollide(enemy,SpriteGroup, True)
        if eachEnemy.rect.x<0:
            EnemyGroup.remove(eachEnemy)
            EnemyCount+=1  
        if Enemyhits:
            Player.health= 0


    if pressed == True:
        bullet = Bullet(Player.rect.centerx,Player.rect.centery,20,5,Red)
        BulletGroup.add(bullet) # Add bullet to bullet group
        

    for eachBullet in BulletGroup:
        if eachBullet.rect.x > infoObject.current_w:
            BulletGroup.remove(eachBullet)#Kills the bullet if it goes off screen
        BulletHits = pygame.sprite.spritecollide(eachBullet, EnemyGroup, True) #Allows the bullets to collide
        if BulletHits:
            BulletGroup.remove(eachBullet)
            EnemyCount += 1

    Screen.fill(DarkRed)

    ground.update()
    ground.render()

    SpriteGroup.draw(Screen)
    EnemyGroup.draw(Screen)
    HealthBarGroup.draw(Screen)
    BulletGroup.draw(Screen)
    HealthBarPt2.update()
    EnemyGroup.update()
    BulletGroup.update()


    
    clock.tick(30)
    if Player.health == 0:
        SpriteGroup.remove()
        EnemyGroup.remove(eachEnemy)
    pygame.display.update()
