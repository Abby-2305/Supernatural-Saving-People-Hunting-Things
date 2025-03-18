## Importing the modules used throughout the code
from guizero import App, Box, Combo, Text, TextBox, PushButton, Picture, Window, Slider, ListBox
import sqlite3
import pygame
import random
import time

pygame.init() # Initialising the modules used

Black = (0,0,0) # Creating the Colours
DramaticalRed = (156, 18, 0)
DwarfFortress = (30, 0, 0)
RedSentinel = (188, 7, 12)
DelightfulGreen = (0, 240, 0)
GameBoyContrast = (17, 59, 17)
White = (255, 255, 255)
RushmoreGrey = (181, 177, 165)
Silver = (192, 192, 192)
DeadPixel = (60, 57, 57)
BrilliantLiquorice = (84, 84, 84)
Nero = (38, 38, 38)
Skull = (227, 218, 201)
EmpirePorcelain = (223, 219, 211)

infoObject = pygame.display.Info() # Creating variables of the resolution of the screen
Screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h)) # Creating the canvas

pygame.display.set_caption('Supernatural:"Saving People Hunting Things"') # Set game title

clock = pygame.time.Clock() # Defining pygame clock object

font = pygame.font.SysFont(None, 25) # Import the font
ScoreBoardFont = pygame.font.Font("fnt_HelpMe.ttf", 25) # Creatinge fonts used throughout the program
WeaponFont = pygame.font.Font("fnt_HelpMe.ttf",50)

bg_img = pygame.image.load("pixil-frame-0.png") # Loading the image for the background
bg_img = pygame.transform.scale(bg_img,(infoObject.current_w, infoObject.current_h)) # Scaling the image to fit the screen

# Importing the sounds used throughout the game
pygame.mixer.init() # to play sound
buttonPressedSound = pygame.mixer.Sound("Snd_buttonpressed.WAV") # Imports sound
enemyDiedSound = pygame.mixer.Sound("Snd_dead.WAV")
jumpSound = pygame.mixer.Sound("Snd_jump.WAV")
landSound = pygame.mixer.Sound("Snd_land.WAV")
shootSound = pygame.mixer.Sound("Snd_shot.WAV")
gameMusic = pygame.mixer.music
menuMusic = pygame.mixer.music

weapon_list = pygame.image.load("spr_weapons.png") # Importing the weapon list image that is displayed at the bottom of the screen
weapon_list = pygame.transform.scale(weapon_list, (infoObject.current_w, (infoObject.current_h/489)*21)) # Scaling the image to fit the width of the screen
###########################################CLASSES##########################################################################################################
class Background():
    def __init__(self,image,speed):
        self.bgimage = pygame.image.load(image) # Loading the image
        self.bgimage = pygame.transform.scale(self.bgimage,((infoObject.current_w, infoObject.current_h))) # Scaling the image to fit the size of the screen
        self.rectBGimg= self.bgimage.get_rect()

        self.bgY1 = 0
        self.bgX1 = 0

        self.bgY2 = 0
        self.bgX2 = self.rectBGimg.width # Setting the initial x an y coordinates of the two background images

        self.movingSpeed = speed # setting the speed of the background

    def update(self):
        self.bgX1 -= self.movingSpeed
        self.bgX2 -= self.movingSpeed
        if self.bgX1 <= -self.rectBGimg.width: #Resetting the coordinates of the image if it goes off screen
            self.bgX1 = self.rectBGimg.width
        if self.bgX2 <= -self.rectBGimg.width: # Moving two different backgrounds because one background is the size of the users screen so whenit moves left you want another one right next to it so that th background is covered at all times
            self.bgX2 = self.rectBGimg.width
    def render(self):
        Screen.blit(self.bgimage, (self.bgX1, self.bgY1)) # Drawing the background to the screen
        Screen.blit(self.bgimage, (self.bgX2, self.bgY2))

class Sprite(pygame.sprite.Sprite):

    def __init__(self,xCoordinate,yCoordinate,width,height,startImage):
        super().__init__()
        self.image = pygame.image.load(startImage) # Sets the size
        self.image = pygame.transform.scale(self.image,[width,height]) # scaling the image to the width and height passed up
        self.rect = self.image.get_rect() # Hitbox
        self.rect.x = xCoordinate# Sets the position on the screen
        self.rect.y = yCoordinate
        self.health = 100

class Bar(pygame.sprite.Sprite):

    def __init__(self,xCoordinate,yCoordinate,width,height,colour):
        super().__init__()
        self.image = pygame.Surface([width,height]) # Sets the size
        self.image.fill(colour)
        self.rect = self.image.get_rect() # Hitbox
        self.rect.x = xCoordinate# Sets the position on the screen
        self.rect.y = yCoordinate

    def update(self, Health):
        self.image = pygame.Surface([Health,10]) # Updating the width of the green health bar so it changes size if the users health goes down
        self.image.fill(DelightfulGreen)

class Enemy(pygame.sprite.Sprite):

    def __init__(self,xCoordinate,yCoordinate,width,height,enemyspeed, image, monster):
        super().__init__()
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image,[width,height]) # Sets the size
        self.rect = self.image.get_rect() # Hitbox
        
        self.rect.x = xCoordinate# Sets the position on the screen
        self.rect.y = yCoordinate
        self.speed = enemyspeed
        self.monster = monster
        self.health = 100

    def update(self):
        self.rect.x-=self.speed # Moves the enemy left

class Weapon(pygame.sprite.Sprite):

    def __init__(self,xCoordinate,yCoordinate,width,height,colour, weapon):
        super().__init__()
        self.image = pygame.Surface([width,height]) # Sets the size
        self.image.fill(colour)
        self.rect = self.image.get_rect() # Hitbox
        self.rect.x = xCoordinate# Sets the position on the screen
        self.rect.y = yCoordinate

        self.weapon = weapon

    def update(self):
        self.rect.x += 5 # Moves the bullet right by five pixels

def ScoreText(Text, Colour, xCoordinate, yCoordinate): # Text procedure
    ScreenText = ScoreBoardFont.render(Text, True, Colour)
    Screen.blit(ScreenText,[xCoordinate, yCoordinate])

def WeaponChoiceText(Text, Colour): # Text procedure
    ScreenText = WeaponFont.render(Text, True, Colour)
    textWidth = ScreenText.get_width()
    Screen.blit(ScreenText,[infoObject.current_w/2 - textWidth/2, infoObject.current_h/4])
#############################################################################################################################################################
Player= Sprite(infoObject.current_w/4, (infoObject.current_h*(107/144))-30,30,30,"spr_dean.png") # Creatng the defauult player object

ground = Background("Bgd_path.png", 5)
##############################################GAMELOOP#######################################################################################################
def Game(Name, Difficulty, Hunter):
    i = 0 # Creating the variables used for the game
    Jump = False
    jumpCount = 20
    score = 0
    EnemyCount = 1
    playerweapon = "Scythe"
    weaponcolour = (0,0,0)
    if Difficulty ==1:             # Setting the number of types of enemies based on the difficulty chosen by the user
        typesOfEnemies = 2
    elif Difficulty == 2:
        typesOfEnemies = 5
    elif Difficulty == 3:
        typesOfEnemies = 9

    if Hunter == "Dean Winchester": # Creating the image based on what hunter was chosen
        startImage = "spr_dean.png"
        imageList =  ["spr_dean.png", "spr_dean2.png", "spr_dean.png", "spr_dean3.png"] # Creating an array of images to implement character animation (didn't have enough time to complete)
    if Hunter == "Sam Winchester":
        startImage = "spr_sam.png"
        imageList =  ["spr_sam.png", "spr_sam2.png", "spr_sam.png", "spr_sam3.png"]
    

    ##################################OBJECTS########################################################################################
    Player= Sprite(infoObject.current_w/4, (infoObject.current_h*(107/144))-30,30,30, startImage) # Creating the objects
    HealthBarPt1 = Bar(10,10,100,10,DramaticalRed)
    HealthBarPt2 = Bar(10,10,Player.health,10,DelightfulGreen)

    SpriteGroup = pygame.sprite.Group() # Create a group
    EnemyGroup = pygame.sprite.Group()
    HealthBarGroup = pygame.sprite.Group()
    WeaponGroup = pygame.sprite.Group()

    SpriteGroup.add(Player) # Add object to group
    HealthBarGroup.add(HealthBarPt1)
    HealthBarGroup.add(HealthBarPt2)

    def AddToLeaderboard(Name,Score,Difficulty): # Creating the add to leaderboard procedure
        con = sqlite3.connect('Leaderboard.db') # Opening the leaderboard
        cursorObj = con.cursor()

        entities = (Name, Score, Difficulty)
        cursorObj.execute('INSERT INTO UsersScores (Name, Score, Difficulty) VALUES(?, ?, ?)',entities) # Adding the data into the leaderboard
        
        con.commit()
    
        cursorObj.close()
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
                    shootSound.play() # Playing shoot sound
                    weaponObject = Weapon(Player.rect.centerx,Player.rect.centery,20,5,weaponcolour, playerweapon) # Firing weapon
                    WeaponGroup.add(weaponObject) # Add weapon to weapon group
                if event.key == pygame.K_1:
                    playerweapon = "Scythe"  # setting the weapon and the colour of the weapon based on the the number pressed 
                    weaponcolour = Black
                if event.key == pygame.K_2:
                    playerweapon = "Salt"
                    weaponcolour = White
                if event.key == pygame.K_3:
                    playerweapon = "Machete"
                    weaponcolour = DeadPixel
                if event.key == pygame.K_4:
                    playerweapon = "WitchBullet"
                    weaponcolour = GameBoyContrast 
                if event.key == pygame.K_5:
                    playerweapon = "AngelBlade"
                    weaponcolour = RushmoreGrey
                if event.key == pygame.K_6:
                    playerweapon = "DemonBlade"
                    weaponcolour = BrilliantLiquorice
                if event.key == pygame.K_7:
                    playerweapon = "SilverBullet"
                    weaponcolour = Silver
                if event.key == pygame.K_8:
                    playerweapon = "Colt"
                    weaponcolour = Nero
                if event.key == pygame.K_9:
                    playerweapon = "Bone"
                    weaponcolour = Skull
                if event.key == pygame.K_0:
                    playerweapon = "Borax"
                    weaponcolour = EmpirePorcelain
                    
        keys = pygame.key.get_pressed()
        if not(Jump):
            if keys[pygame.K_SPACE]:
                jumpSound.play()
                Jump = True
        else:
            if jumpCount >=-20:
                Player.rect.y -= jumpCount 
                jumpCount -= 2
            else: # This will execute if our jump is finished
                landSound.play()
                jumpCount = 20
                Jump = False
                Player.rect.y = (infoObject.current_h*(107/144))-30
                # Resetting our Variables

        if EnemyCount>0:
            enemyChoice = random.randint(1,typesOfEnemies) # random number generator so that a random enemy spawns and then a giant if statement setting the enemy object depending on the number from the random number generator
            if enemyChoice == 1:
                enemy = Enemy(infoObject.current_w, (infoObject.current_h*(107/144))-50,30,50,10, "spr_ghost.png", "spirit")
            if enemyChoice == 2:
                enemy = Enemy(infoObject.current_w, (infoObject.current_h*(107/144))-70,30,70,10, "spr_death.png", "death")
            if enemyChoice == 3:
                enemy = Enemy(infoObject.current_w, (infoObject.current_h*(107/144))-50,30,50,10, "spr_angel.png", "angel")
            if enemyChoice == 4:
                enemy = Enemy(infoObject.current_w, (infoObject.current_h*(107/144))-50,30,50,10, "spr_vampire.png", "vampire")
            if enemyChoice == 5:
                enemy = Enemy(infoObject.current_w, (infoObject.current_h*(107/144))-50,30,50,10, "spr_witch.png", "witch")
            if enemyChoice == 6:
                enemy = Enemy(infoObject.current_w, (infoObject.current_h*(107/144))-50,30,50,10, "spr_leviathan.png", "leviathan")
            if enemyChoice == 7:
                enemy = Enemy(infoObject.current_w, (infoObject.current_h*(107/144))-50,30,50,10, "spr_hellhound.png", "hellhound")
            if enemyChoice == 8:
                enemy = Enemy(infoObject.current_w, (infoObject.current_h*(107/144))-50,30,50,10, "spr_werewolf.png", "werewolf")
            if enemyChoice == 9:
                enemy = Enemy(infoObject.current_w, (infoObject.current_h*(107/144))-70,20,70,10, "spr_demon.png", "demon")
            EnemyGroup.add(enemy)
            EnemyCount -=1
            
        for eachEnemy in EnemyGroup:
            Enemyhits = pygame.sprite.spritecollide(eachEnemy,SpriteGroup, True)
            if eachEnemy.rect.x<0: # Checking if the enemy goes off screen
                EnemyGroup.remove(eachEnemy)
                EnemyCount+=1
            if eachEnemy.rect.centerx <= Player.rect.centerx + 5 and eachEnemy.rect.centerx >= Player.rect.centerx -1: # Checking if the player has jumped over the enemy
                score +=10
                Player.health-=10
            if Enemyhits: # Checking if the enemy and player collide
                Player.health= 0

        for eachWeapon in WeaponGroup:
            if eachWeapon.rect.x == infoObject.current_w: # Giant if statement to check if the correct weapon is getting used against the correct enemy
                WeaponGroup.remove(eachWeapon)#Kills the Weapon if it goes off screen
            if eachWeapon.weapon == "Scythe" and enemy.monster == "death":    
                WeaponHits = pygame.sprite.spritecollide(eachWeapon, EnemyGroup, True) #Allows the Weapons to collide 
                if WeaponHits:
                    enemyDiedSound.play()
                    EnemyCount += 1
                    score+=100
            elif eachWeapon.weapon == "Salt" and enemy.monster == "spirit":    
                WeaponHits = pygame.sprite.spritecollide(eachWeapon, EnemyGroup, True) #Allows the Weapons to collide 
                if WeaponHits:
                    enemyDiedSound.play()
                    EnemyCount += 1
                    score+=100
            elif eachWeapon.weapon == "AngelBlade" and enemy.monster == "angel":
                WeaponHits = pygame.sprite.spritecollide(eachWeapon, EnemyGroup, True) #Allows the Weapons to collide 
                if WeaponHits:
                    enemyDiedSound.play()
                    EnemyCount += 1
                    score+=100
            elif (eachWeapon.weapon == "Machete" or eachWeapon.weapon == "Colt") and enemy.monster == "vampire":
                WeaponHits = pygame.sprite.spritecollide(eachWeapon, EnemyGroup, True) #Allows the Weapons to collide 
                if WeaponHits:
                    enemyDiedSound.play()
                    EnemyCount += 1
                    score+=100
            elif eachWeapon.weapon == "WitchBullet" and enemy.monster == "witch":
                WeaponHits = pygame.sprite.spritecollide(eachWeapon, EnemyGroup, True) #Allows the Weapons to collide 
                if WeaponHits:
                    enemyDiedSound.play()
                    EnemyCount += 1
                    score+=100
            elif enemy.monster == "leviathan" and (eachWeapon.weapon =="Bone" or eachWeapon.weapon == "Borax"):
                if eachWeapon.weapon == "Bone":
                    WeaponHits = pygame.sprite.spritecollide(eachWeapon, EnemyGroup, True) #Allows the Weapons to collide 
                    if WeaponHits:
                        enemyDiedSound.play()
                        EnemyCount += 1
                        score+=100
                if eachWeapon.weapon == "Borax":
                    if enemy.health > 10:
                        WeaponHits = pygame.sprite.spritecollide(eachWeapon, EnemyGroup, False) #Allows the Weapons to collide
                        if WeaponHits:
                            enemy.health -=10
                            score+=10
                    elif enemy.health <=10:
                        WeaponHits = pygame.sprite.spritecollide(eachWeapon, EnemyGroup, True) #Allows the Weapons to collide
                        if WeaponHits:
                            enemy.health -=10
                            score+=10
                            EnemyCount+=1
            elif enemy.monster == "hellhound" and (eachWeapon.weapon == "AngelBlade" or eachWeapon.weapon == "DemonBlade" or eachWeapon.weapon == "Colt" or eachWeapon.weapon == "Salt"):
                if eachWeapon.weapon == "AngelBlade" or eachWeapon.weapon == "DemonBlade" or eachWeapon.weapon == "Colt":
                    WeaponHits = pygame.sprite.spritecollide(eachWeapon, EnemyGroup, True) #Allows the Weapons to collide 
                    if WeaponHits:
                        enemyDiedSound.play()
                        EnemyCount += 1
                        score+=100
                if eachWeapon.weapon == "Salt":
                    if enemy.health > 10:
                        WeaponHits = pygame.sprite.spritecollide(eachWeapon, EnemyGroup, False) #Allows the Weapons to collide
                        if WeaponHits:
                            enemy.health -=10
                            score+=10
                    else:
                        BulletHits = pygame.sprite.spritecollide(eachWeapon, EnemyGroup, False) #Allows the bullets to collide 
                        if BulletHits:
                            score-=10
            elif (eachWeapon.weapon == "Machete" or eachWeapon.weapon == "AngelBlade" or eachWeapon.weapon == "SilverWeapon" or eachWeapon.weapon == "Colt") and enemy.monster == "werewolf":
                WeaponHits = pygame.sprite.spritecollide(eachWeapon, EnemyGroup, True) #Allows the Weapons to collide 
                if WeaponHits:
                    enemyDiedSound.play()
                    EnemyCount += 1
                    score+=100
            elif (eachWeapon.weapon == "AngelBlade" or eachWeapon.weapon == "DemonBlade" or eachWeapon.weapon == "Colt") and enemy.monster == "demon":
                WeaponHits = pygame.sprite.spritecollide(eachWeapon, EnemyGroup, True) #Allows the Weapons to collide 
                if WeaponHits:
                    enemyDiedSound.play()
                    EnemyCount += 1
                    score+=100
            else:
                WeaponHits = pygame.sprite.spritecollide(eachWeapon, EnemyGroup, False) #Allows the Weapons to collide 
                if WeaponHits:
                    score-=10
            if WeaponHits:
                WeaponGroup.remove(eachWeapon)

        Screen.fill(DwarfFortress)

        ground.update()
        ground.render() # running the background methods for the auto scrolling background
        
        SpriteGroup.draw(Screen)
        EnemyGroup.draw(Screen)
        HealthBarGroup.draw(Screen)
        WeaponGroup.draw(Screen)
        HealthBarPt2.update(Player.health)
        EnemyGroup.update()
        WeaponGroup.update()

        Screen.blit(weapon_list,(1, infoObject.current_h-((infoObject.current_h/489)*21))) # Displaying the weapon list on the bottom of the screen

        clock.tick(30) # setting the FPS

        ScoreText("Score:",White,10,30)
        ScoreText(str(score),White,110,30) # Displaying the score onto the screen
        WeaponChoiceText(playerweapon,White) # Displaying the equipped weapon on the screen
        
        
        if Player.health == 0:
            SpriteGroup.remove()
            EnemyGroup.remove(eachEnemy)
            AddToLeaderboard(Name, score, Difficulty) # Adding the score to the leaderboard
            gameExit = True
            GameOver(Name, score)
        pygame.display.update() # ensuring all the objects update on the screen after every loop
##############################################MENU###########################################################################################################
def customGame(): # Procedure to hide the main menu and show the customisation menu
    buttonPressedSound.play()
    Menu.hide()
    Customiser()
def loadHowToPlay(): # procedure to hide the main menu and display the how to play menu
    buttonPressedSound.play()
    Menu.hide()
    HowToPlay()
def endgame(): # procedure to end the game
    buttonPressedSound.play()
    endchoice = Menu.yesno("QUIT?", "Are you sure you want to quit?")
    if endchoice == True:
        Menu.warn("Thanks for Playing", "Thank you for playing Supernatural:\"Saving People, Hunting Things\"")
        Menu.destroy()
        pygame.quit()

def ShowLeaderboard(): # procedure to hide the main menu and display the leaderboard menu
    buttonPressedSound.play()
    Menu.hide()
    displayLeaderboard()

Menu = App(title="Supernatural: Saving People Hunting Things", bg = Black) # Creating the main menu
Menu.full_screen = True

MenuHeight = Menu.height
MenuWidth = Menu.width

TitleBox = Box(Menu, width="fill", align="top") # Creating the title box
Background = Picture(Menu, image = "bgd_menu.PNG")

ButtonBox = Box(Menu, width = int(MenuWidth/4), height="fill") # creating all of the buttons displayed on the main menu
button = PushButton(ButtonBox, text ="Play", width = "fill", command=customGame)
button.text_size = int(MenuHeight/30)
button.text_color = RedSentinel
button = PushButton(ButtonBox, text="How To Play", width = "fill", command=loadHowToPlay)
button.text_size = int(MenuHeight/30)
button.text_color = RedSentinel
button = PushButton(ButtonBox, text="Leaderboards", width = "fill", command = ShowLeaderboard)
button.text_size = int(MenuHeight/30)
button.text_color = RedSentinel

ExitBox = Box(Menu, align="bottom", width = "fill") # creating the exit box
button = PushButton(ExitBox, text ="QUIT", align = "right",command = endgame)
button.text_size = int(MenuHeight/30)
button.text_color = RedSentinel
###################################################################################################################################################################################################
def Customiser(): # procedure for the customisation menu
    def GameInformation(): # procedure to hide the customisation menu and display the game
        buttonPressedSound.play()
        Name = NameInput.value
        Difficulty = DifficultyInput.value
        Hunter = HunterInput.value
        print(Name)
        if len(Name) < 3:
            Customiser.error("Name is too short", "The name you have entered is too short. Your name must be 3 characters - 10 characters long.")
        elif len(Name) >10:
            Customiser.error("Name is too long", "The name you have entered is too long. Your name must be 3 characters - 10 characters long.")
        else:
            Customiser.hide()
            gameMusic.load("Snd_GameMusic.WAV")
            gameMusic.play(-1)
            Game(Name, Difficulty, Hunter)
               
    def Back(): # procedure to hide the customisation menu and load the main menu
        buttonPressedSound.play()
        Customiser.hide()
        Menu.show()
    Customiser = Window(Menu, title = "Customisation Menu", bg = Black) # creating the customisation menu
    Customiser.full_screen = True

    CustomiserHeight = Customiser.height
    CustomiserWidth = Customiser.width

    TitleBox2 = Box(Customiser, width="fill", align="top") # creating the title box
    Background2 = Picture(Customiser, image = "bgd_menu.PNG")

    InputsBox = Box(Customiser, width = int(Customiser.width/4), height = "fill") # taking in all of the inputs from the user
    NameText = Text(InputsBox, text = "Enter your name:")
    NameText.text_color = White
    NameText.text_size =15

    NameInput = TextBox(InputsBox, width = "fill")
    NameInput.text_color = White
    NameInput.text_size = 15

    DifficultyText = Text(InputsBox, text = "Difficulty:")
    DifficultyText.text_color = White
    DifficultyText.text_size = 15
    DifficultyInput = Slider(InputsBox, start = 1, end = 3, width = "fill")
    DifficultyInput.text_color = White
    DifficultyInput.text_size = 15

    HunterText = Text(InputsBox, text = "Hunter:")
    HunterText.text_color = White
    HunterText.text_size = 15
    HunterInput = Combo(InputsBox, options = ["Dean Winchester", "Sam Winchester"], width = "fill")
    HunterInput.text_color = White
    HunterInput.text_size = 15

    StartButton = PushButton(InputsBox, text = "START", width = "fill", command = GameInformation) # creating the button to start the game
    StartButton.text_size = int(MenuHeight/30)
    StartButton.text_color = White

    BackBox = Box(Customiser, align="bottom", width = "fill") # creating the button to go back to main menu
    button = PushButton(BackBox, text ="BACK", align = "right", command = Back)
    button.text_size = int(MenuHeight/30)
    button.text_color = RedSentinel
################################################################################
def HowToPlay(): # creating the how to play procedure
    def BackToMain(): # creating a procedure that hides the how to play menu and shows the main menu
        buttonPressedSound.play()
        HowToPlay.hide()
        Menu.show()
    HowToPlay = Window(Menu, title = "Customisation Menu", bg = Black) # creating the how to play menu
    HowToPlay.full_screen = True

    HowToPlayHeight = HowToPlay.height
    HowToPlayWidth = HowToPlay.width

    TitleBox3 = Box(HowToPlay, width="fill", align="top")
    Background2 = Picture(TitleBox3, image = "bgd_menu.PNG")

    HowToPlay1 = Picture(HowToPlay, image = "menu_UseCustomisation.PNG", align = "left") # displaying the images that instruct the user on how to play
    HowToPlay2 = Picture(HowToPlay, image = "menu_PlayMainGame.PNG", align = "left")

    BackBox = Box(HowToPlay, align="bottom", width = "fill") # creating the button that takes the user back to the main menu
    button = PushButton(BackBox, text ="BACK", align = "right", command = BackToMain)
    button.text_size = int(MenuHeight/30)
    button.text_color = RedSentinel
################################################################################
def GameOver(Name, Score): # creating the game over menu procedure
    def MainMenu(): # reating a procedure that hides the game over menu and displays the main menu
        buttonPressedSound.play()
        GameOver.hide()
        menuMusic.load("Snd_MenuMusic.WAV")
        menuMusic.play(-1)
        Menu.show()

    ScoreText = (Name,"your score is", Score) # creating the string to display the score

    GameOver = Window(Menu, title = "Game Over", bg = DwarfFortress)
    GameOver.full_screen = True
    GameOverText = Text(GameOver, text = "Game Over!", width = "fill", height = "fill")
    GameOverText.text_size = 100
    GameOverText.text_color = White
    GameOverTextScore = Text(GameOver, text = ScoreText, width = "fill", height = "fill") # Displaying the score
    GameOverTextScore.text_size = 50
    GameOverTextScore.text_color = White
    GameOverButton = PushButton(GameOver , text="Go back to Main Menu", command = MainMenu) # creating the button that takes the user back to the main menu
    GameOverButton.text_size = 100
    GameOverButton.text_color = White
################################################################################
def displayLeaderboard(): # creating the leaderboard menu procedure
    def BackToMain(): # creating a procedure that hides the leaderboard menu and displays the main menu
        buttonPressedSound.play()
        Leaderboard.hide()
        Menu.show()

    con = sqlite3.connect('Leaderboard.db') # opeing the database that stores the users scores
    cursorObj = con.cursor()

    Leaderboard = Window(Menu, title="Supernatural: Saving People Hunting Things", bg = Black)
    Leaderboard.full_screen = True

    LeaderboardHeight = Leaderboard.height
    LeaderboardWidth = Leaderboard.width

    TitleBox = Box(Leaderboard, width="fill", align="top")
    Background = Picture(TitleBox, image = "Bgd_Leaderboard.PNG", width = LeaderboardWidth)


    EasyBox = Box(Leaderboard, width = int(LeaderboardWidth/3), height=int(LeaderboardWidth*0.8), align = "left")
    EasyBoxNumbers = Box(EasyBox,width = int(LeaderboardWidth/24), height="fill", align = "left") # changed width of numbers box and stats box
    for i in range (1,11): # for loop that displays the numbers 1-10
        PlaceText = Text(EasyBoxNumbers, text = i)
        PlaceText.text_size = int(LeaderboardHeight/30)
        PlaceText.text_color = White
    strSQLEasy = "SELECT Name, Score FROM UsersScores WHERE Difficulty = 1 ORDER BY Score DESC LIMIT 10" # creating a string of the top 10 easy scores
    cursorObj.execute(strSQLEasy)
    rows = cursorObj.fetchall()

    EasyBoxStats = Box(EasyBox, width = int(LeaderboardWidth/3), height="fill", align = "left")
    for row in rows: # Iterating through the easy scores string and displaying it
        EasyText = Text(EasyBoxStats, text = row)
        EasyText.text_size = int(LeaderboardHeight/30)
        EasyText.text_color = White

    MediumBox = Box(Leaderboard, width = int(LeaderboardWidth/3), height=int(LeaderboardWidth*0.8), align = "left")
    MediumBoxNumbers = Box(MediumBox, width = int(LeaderboardWidth/24), height="fill", align = "left")
    for i in range (1,11): # for loop that displays the numbers 1 to 10
        PlaceText = Text(MediumBoxNumbers, text = i)
        PlaceText.text_size = int(LeaderboardHeight/30)
        PlaceText.text_color = White
    strSQLMedium = "SELECT Name, Score FROM UsersScores WHERE Difficulty = 2 ORDER BY Score DESC LIMIT 10" # creating a string that holds the top 10 medium scores
    cursorObj.execute(strSQLMedium)
    rows = cursorObj.fetchall()

    MediumBoxStats = Box(MediumBox, width = int(LeaderboardWidth/3), height="fill", align = "left")
    for row in rows: # iterating through the medium scores string and displaying it to the screen
        MediumText = Text(MediumBoxStats, text = row)
        MediumText.text_size = int(LeaderboardHeight/30)
        MediumText.text_color = White

        
    HardBox = Box(Leaderboard, width = int(LeaderboardWidth/3), height=int(LeaderboardWidth*0.8), align = "left")
    HardBoxNumbers = Box(HardBox, width = int(LeaderboardWidth/24), height = "fill", align = "left")
    for i in range (1,11): # for loop to display the numbers 1 to 10
        PlaceText = Text(HardBoxNumbers, text = i)
        PlaceText.text_size = int(LeaderboardHeight/30)
        PlaceText.text_color = White
    strSQLHard = "SELECT Name, Score FROM UsersScores WHERE Difficulty = 3 ORDER BY Score DESC LIMIT 10" # creating a string with the top 10 hard difficulty scores
    cursorObj.execute(strSQLHard)
    rows = cursorObj.fetchall()

    HardBoxStats = Box(HardBox, width = int(LeaderboardWidth/3), height = "fill", align = "left")
    for row in rows: # iterating through the hard score string and displaying it onto the screen
        HardText = Text(HardBoxStats, text = row)
        HardText.text_size = int(LeaderboardHeight/30)
        HardText.text_color = White

    button = PushButton(HardBoxStats, text ="QUIT", align ="right", command = BackToMain) # creating the button that takes the user back to the main menu
    button.text_size = int(LeaderboardHeight/30)
    button.text_color = White

    cursorObj.close() # closing the database that stores the scores
##################################################################################
menuMusic.load("Snd_MenuMusic.WAV") # playing the main menu music
menuMusic.play(-1) # looping the music
Menu.display() # displaying the main menu
