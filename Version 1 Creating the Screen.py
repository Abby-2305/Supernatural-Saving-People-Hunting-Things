import pygame

pygame.init() # Initialising the modules used

black = (0,0,0) # Creating the colours

infoObject = pygame.display.Info() # Creating variables of the resolution of the screen
Screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h)) # Creating the canvas

pygame.display.set_caption('Supernatural:"Saving People Hunting Things"') # Set game title

clock = pygame.time.Clock() # Defining pygame clock object
##############################################################################
gameExit = False
while not gameExit:  # Start of the Game loop

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
            
    Screen.fill(black) # Draw the screen
    pygame.display.update() # Update the screen with every loop
