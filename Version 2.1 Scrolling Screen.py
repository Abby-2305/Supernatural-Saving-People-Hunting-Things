import pygame

pygame.init() # Initialising the modules used

black = (0,0,0) # Creating the colours


infoObject = pygame.display.Info() # Creating variables of the resolution of the screen
Screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h)) # Creating the canvas

pygame.display.set_caption('Supernatural:"Saving People Hunting Things"') # Set game title

clock = pygame.time.Clock() # Defining pygame clock object
############################################CLASSES##########################################################################################################
class Background():
    def __init__(self,image,speed):
        self.bgimage = pygame.image.load(image) # Loading the image
        self.bgimage = pygame.transform.scale(self.bgimage,((infoObject.current_w, infoObject.current_h))) # Fitting the image to the size of the screen
        self.rectBGimg = self.bgimage.get_rect()

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
#############################################################################################################################################################
backgrnd = Background("pixil-frame-0.png", 1) # Creating the background objects
clouds = Background("pixil-layer-1.png", 1)
clouds2 = Background("pixil-layer-2.png", 3)
ground = Background("pixil-layer-3.png", 5)
##############################################GAMELOOP#######################################################################################################
gameExit = False
while not gameExit:    # Start of the Game Loop

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
                
    backgrnd.update()   # Running the class methods
    backgrnd.render()
    clouds.update()
    clouds.render()
    clouds2.update()
    clouds2.render()
    ground.update()
    ground.render()
    
    clock.tick(60) # Setting the FPS
    pygame.display.update() # Update the screen with every loop
