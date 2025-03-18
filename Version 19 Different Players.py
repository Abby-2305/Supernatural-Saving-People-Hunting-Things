from guizero import App, Box, Combo, Text, TextBox, PushButton, Picture, Window, Slider, ListBox
import sqlite3
import pygame
import random
import time

pygame.init() # Initialising the modules used

Black = (0,0,0) # Creating the Variables
Purple = (144, 41, 204)
Red = (156, 18, 0)
DarkRed = (30, 0, 0)
DarkRed2 = (188, 7, 12)
Green = (0, 240, 0)
DarkGreen = (17, 59, 17)
White = (255, 255, 255)
Grey = (181, 177, 165)

infoObject = pygame.display.Info() # Creating variables of the resolution of the screen
Screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h)) # Creating the canvas

pygame.display.set_caption('Supernatural:"Saving People Hunting Things"') # Set game title

clock = pygame.time.Clock() # Defining pygame clock object

font = pygame.font.SysFont(None, 25) # Import the font
ScoreBoardFont = pygame.font.Font("fnt_HelpMe.ttf", 25)
WeaponFont = pygame.font.Font("fnt_HelpMe.ttf",50)

bg_img = pygame.image.load("pixil-frame-0.png")
bg_img = pygame.transform.scale(bg_img,(infoObject.current_w, infoObject.current_h))

pygame.mixer.init() # to play sound
buttonPressedSound = pygame.mixer.Sound("Snd_buttonpressed.WAV") # Imports sound
enemyDiedSound = pygame.mixer.Sound("Snd_dead.WAV")
jumpSound = pygame.mixer.Sound("Snd_jump.WAV")
landSound = pygame.mixer.Sound("Snd_land.WAV")
shootSound = pygame.mixer.Sound("Snd_shot.WAV")
gameMusic = pygame.mixer.music
menuMusic = pygame.mixer.music

weapon_list = pygame.image.load("spr_weapons.png")
weapon_list = pygame.transform.scale(weapon_list, (infoObject.current_w, (infoObject.current_h/489)*21))
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

    def __init__(self,x,y,a,b,startImage):
        super().__init__()
        self.image = pygame.image.load(startImage) # Sets the size
        self.image = pygame.transform.scale(self.image,[a,b])
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

    def update(self, Health):
        self.image = pygame.Surface([Health,10])
        self.image.fill(Green)

class Enemy(pygame.sprite.Sprite):

    def __init__(self,x,y,a,b,enemyspeed, image, monster):
        super().__init__()
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image,[a,b]) # Sets the size
        self.rect = self.image.get_rect() # Hitbox
        
        self.rect.x = x# Sets the position on the screen
        self.rect.y = y
        self.speed = enemyspeed
        self.monster = monster
        self.health = 100

    def update(self,):
        self.rect.x-=self.speed

class Bullet(pygame.sprite.Sprite):

    def __init__(self,x,y,a,b,color, weapon):
        super().__init__()
        self.image = pygame.Surface([a,b]) # Sets the size
        self.image.fill(color)
        self.rect = self.image.get_rect() # Hitbox
        self.rect.x = x# Sets the position on the screen
        self.rect.y = y

        self.weapon = weapon

    def update(self):
        self.rect.x += 5

def ScoreText(Text, Colour, x, y): # Text procedure
    ScreenText = ScoreBoardFont.render(Text, True, Colour)
    Screen.blit(ScreenText,[x, y])

def WeaponChoiceText(Text, Colour): # Text procedure
    ScreenText = WeaponFont.render(Text, True, Colour)
    textWidth = ScreenText.get_width()
    Screen.blit(ScreenText,[infoObject.current_w/2 - textWidth/2, infoObject.current_h/4])
#############################################################################################################################################################
Player= Sprite(infoObject.current_w/4, (infoObject.current_h*(107/144))-30,30,30,"spr_dean.png")

ground = Background("Bgd_path.png", 5)
##############################################GAMELOOP#######################################################################################################
def Game(Name, Difficulty, Hunter):
    i = 0
    Jump = False
    jumpCount = 20
    score = 0
    EnemyCount = 1
    playerweapon = "Scythe"
    weaponcolour = (0,0,0)
    if Difficulty ==1:
        typesOfEnemies = 2
    elif Difficulty == 2:
        typesOfEnemies = 5
    elif Difficulty == 3:
        typesOfEnemies = 9

    if Hunter == "Dean Winchester":
        startImage = "spr_dean.png"
        imageList =  ["spr_dean.png", "spr_dean2.png", "spr_dean.png", "spr_dean3.png"]
    if Hunter == "Sam Winchester":
        startImage = "spr_sam.png"
        imageList =  ["spr_sam.png", "spr_sam2.png", "spr_sam.png", "spr_sam3.png"]
    

    #############################################################################################################################################################
    Player= Sprite(infoObject.current_w/4, (infoObject.current_h*(107/144))-30,30,30, startImage)
    HealthBarPt1 = Bar(10,10,100,10,Red)
    HealthBarPt2 = Bar(10,10,Player.health,10,Green)

    SpriteGroup = pygame.sprite.Group() # Create a group
    EnemyGroup = pygame.sprite.Group()
    HealthBarGroup = pygame.sprite.Group()
    BulletGroup = pygame.sprite.Group()

    SpriteGroup.add(Player) # Add object to group
    HealthBarGroup.add(HealthBarPt1)
    HealthBarGroup.add(HealthBarPt2)

    def AddToLeaderboard(Name,Score,Difficulty):
        con = sqlite3.connect('Leaderboard.db')
        cursorObj = con.cursor()

        entities = (Name, Score, Difficulty)
        cursorObj.execute('INSERT INTO UsersScores (Name, Score, Difficulty) VALUES(?, ?, ?)',entities)
        
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
                    shootSound.play()
                    bullet = Bullet(Player.rect.centerx,Player.rect.centery,20,5,weaponcolour, playerweapon)
                    BulletGroup.add(bullet) # Add bullet to bullet group
                if event.key == pygame.K_1:
                    playerweapon = "Scythe"
                    weaponcolour = Black
                if event.key == pygame.K_2:
                    playerweapon = "Salt"
                    weaponcolour = White
                if event.key == pygame.K_3:
                    playerweapon = "Machette"
                    weaponcolour = Black
                if event.key == pygame.K_4:
                    playerweapon = "WitchBullet"
                    weaponcolour = DarkGreen
                if event.key == pygame.K_5:
                    playerweapon = "AngelBlade"
                    weaponcolour = Grey
                if event.key == pygame.K_6:
                    playerweapon = "DemonBlade"
                if event.key == pygame.K_7:
                    playerweapon = "SilverBullet"
                if event.key == pygame.K_8:
                    playerweapon = "Colt"
                    weaponcolour = Grey
                if event.key == pygame.K_9:
                    playerweapon = "Bone"
                if event.key == pygame.K_0:
                    playerweapon = "Borax"

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
            enemyChoice = random.randint(1,typesOfEnemies)
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
            if eachEnemy.rect.x<0:
                EnemyGroup.remove(eachEnemy)
                EnemyCount+=1
            if eachEnemy.rect.centerx <= Player.rect.centerx + 5 and eachEnemy.rect.centerx >= Player.rect.centerx -1:
                score +=10
                Player.health-=10
            if Enemyhits:
                Player.health= 0

        for eachBullet in BulletGroup:
            if eachBullet.rect.x == infoObject.current_w:
                BulletGroup.remove(eachBullet)#Kills the bullet if it goes off screen
            if eachBullet.weapon == "Scythe" and enemy.monster == "death":    
                BulletHits = pygame.sprite.spritecollide(eachBullet, EnemyGroup, True) #Allows the bullets to collide 
                if BulletHits:
                    enemyDiedSound.play()
                    EnemyCount += 1
                    score+=100
            elif eachBullet.weapon == "Salt" and enemy.monster == "spirit":    
                BulletHits = pygame.sprite.spritecollide(eachBullet, EnemyGroup, True) #Allows the bullets to collide 
                if BulletHits:
                    enemyDiedSound.play()
                    EnemyCount += 1
                    score+=100
            elif eachBullet.weapon == "AngelBlade" and enemy.monster == "angel":
                BulletHits = pygame.sprite.spritecollide(eachBullet, EnemyGroup, True) #Allows the bullets to collide 
                if BulletHits:
                    enemyDiedSound.play()
                    EnemyCount += 1
                    score+=100
            elif (eachBullet.weapon == "Machette" or eachBullet.weapon == "Colt") and enemy.monster == "vampire":
                BulletHits = pygame.sprite.spritecollide(eachBullet, EnemyGroup, True) #Allows the bullets to collide 
                if BulletHits:
                    enemyDiedSound.play()
                    EnemyCount += 1
                    score+=100
            elif eachBullet.weapon == "WitchBullet" and enemy.monster == "witch":
                BulletHits = pygame.sprite.spritecollide(eachBullet, EnemyGroup, True) #Allows the bullets to collide 
                if BulletHits:
                    enemyDiedSound.play()
                    EnemyCount += 1
                    score+=100
            elif enemy.monster == "leviathan":
                if eachBullet.weapon == "Bone":
                    BulletHits = pygame.sprite.spritecollide(eachBullet, EnemyGroup, True) #Allows the bullets to collide 
                    if BulletHits:
                        enemyDiedSound.play()
                        EnemyCount += 1
                        score+=100
                if eachBullet.weapon == "Borax":
                    if enemy.health > 10:
                        BulletHits = pygame.sprite.spritecollide(eachBullet, EnemyGroup, False) #Allows the bullets to collide
                        if BulletHits:
                            enemy.health -=10
                            score+=10
                    elif enemy.health <=10:
                        BulletHits = pygame.sprite.spritecollide(eachBullet, EnemyGroup, True) #Allows the bullets to collide
                        if BulletHits:
                            enemy.health -=10
                            score+=10
                            EnemyCount+=1
            elif enemy.monster == "hellhound":
                if eachBullet.weapon == "AngelBlade" or eachBullet.weapon == "DemonBlade" or eachBullet.weapon == "Colt":
                    BulletHits = pygame.sprite.spritecollide(eachBullet, EnemyGroup, True) #Allows the bullets to collide 
                    if BulletHits:
                        enemyDiedSound.play()
                        EnemyCount += 1
                        score+=100
                if eachBullet.weapon == "Salt":
                    if enemy.health > 10:
                        BulletHits = pygame.sprite.spritecollide(eachBullet, EnemyGroup, False) #Allows the bullets to collide
                        if BulletHits:
                            enemy.health -=10
                            score+=10
            elif (eachBullet.weapon == "Machette" or eachBullet.weapon == "AngelBlade" or eachBullet.weapon == "SilverBullet" or eachBullet.weapon == "Colt") and enemy.monster == "werewolf":
                BulletHits = pygame.sprite.spritecollide(eachBullet, EnemyGroup, True) #Allows the bullets to collide 
                if BulletHits:
                    enemyDiedSound.play()
                    EnemyCount += 1
                    score+=100
            elif (eachBullet.weapon == "AngelBlade" or eachBullet.weapon == "DemonBlade" or eachBullet.weapon == "Colt") and enemy.monster == "demon":
                BulletHits = pygame.sprite.spritecollide(eachBullet, EnemyGroup, True) #Allows the bullets to collide 
                if BulletHits:
                    enemyDiedSound.play()
                    EnemyCount += 1
                    score+=100
            else:
                BulletHits = pygame.sprite.spritecollide(eachBullet, EnemyGroup, False) #Allows the bullets to collide 
                if BulletHits:
                    score-=10
            if BulletHits:
                BulletGroup.remove(eachBullet)

        Screen.fill(DarkRed)

        ground.update()
        ground.render()
        
        SpriteGroup.draw(Screen)
        EnemyGroup.draw(Screen)
        HealthBarGroup.draw(Screen)
        BulletGroup.draw(Screen)
        HealthBarPt2.update(Player.health)
        EnemyGroup.update()
        BulletGroup.update()

        Screen.blit(weapon_list,(1, infoObject.current_h-((infoObject.current_h/489)*21)))

        clock.tick(30)

        ScoreText("Score:",White,10,30)
        ScoreText(str(score),White,110,30)

        WeaponChoiceText(playerweapon,White)
        
        
        if Player.health == 0:
            SpriteGroup.remove()
            EnemyGroup.remove(eachEnemy)
            AddToLeaderboard(Name, score, Difficulty)
            gameExit = True
            GameOver(Name, score)
        pygame.display.update()
##############################################MENU###########################################################################################################
def customGame():
    buttonPressedSound.play()
    Menu.hide()
    Customiser()
def loadHowToPlay():
    buttonPressedSound.play()
    Menu.hide()
    HowToPlay()
def endgame():
    buttonPressedSound.play()
    endchoice = Menu.yesno("QUIT?", "Are you sure you want to quit?")
    if endchoice == True:
        Menu.warn("Thanks for Playing", "Thank you for playing Supernatural:\"Saving People, Hunting Things\"")
        Menu.destroy()
        pygame.quit()

def ShowLeaderboard():
    buttonPressedSound.play()
    Menu.hide()
    displayLeaderboard()

Menu = App(title="Supernatural: Saving People Hunting Things", bg = Black)
Menu.full_screen = True

MenuHeight = Menu.height
MenuWidth = Menu.width

TitleBox = Box(Menu, width="fill", align="top")
Background = Picture(Menu, image = "bgd_menu.PNG")

ButtonBox = Box(Menu, width = int(MenuWidth/4), height="fill")
button = PushButton(ButtonBox, text ="Play", width = "fill", command=customGame)
button.text_size = int(MenuHeight/30)
button.text_color = DarkRed2
button = PushButton(ButtonBox, text="How To Play", width = "fill", command=loadHowToPlay)
button.text_size = int(MenuHeight/30)
button.text_color = DarkRed2
button = PushButton(ButtonBox, text="Leaderboards", width = "fill", command = ShowLeaderboard)
button.text_size = int(MenuHeight/30)
button.text_color = DarkRed2

ExitBox = Box(Menu, align="bottom", width = "fill")
button = PushButton(ExitBox, text ="QUIT", align = "right",command = endgame)
button.text_size = int(MenuHeight/30)
button.text_color = DarkRed2
###################################################################################################################################################################################################
def Customiser():
    def GameInformation():
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
               
    def Back():
        buttonPressedSound.play()
        Customiser.hide()
        Menu.show()
    Customiser = Window(Menu, title = "Customisation Menu", bg = Black)
    Customiser.full_screen = True

    CustomiserHeight = Customiser.height
    CustomiserWidth = Customiser.width

    TitleBox2 = Box(Customiser, width="fill", align="top")
    Background2 = Picture(Customiser, image = "bgd_menu.PNG")

    InputsBox = Box(Customiser, width = int(Customiser.width/4), height = "fill")
    NameText = Text(InputsBox, text = "Enter your name:")
    NameText.text_color = White
    NameText.text_size = 20

    NameInput = TextBox(InputsBox, width = "fill")
    NameInput.text_color = White
    NameInput.text_size = 20

    DifficultyText = Text(InputsBox, text = "Difficulty:")
    DifficultyText.text_color = White
    DifficultyText.text_size = 20
    DifficultyInput = Slider(InputsBox, start = 1, end = 3, width = "fill")
    DifficultyInput.text_color = White
    DifficultyInput.text_size = 20

    HunterText = Text(InputsBox, text = "Hunter:")
    HunterText.text_color = White
    HunterText.text_size = 20
    HunterInput = Combo(InputsBox, options = ["Dean Winchester", "Sam Winchester"], width = "fill")
    HunterInput.text_color = White
    HunterInput.text_size = 20

    StartButton = PushButton(InputsBox, text = "START", width = "fill", command = GameInformation)
    StartButton.text_size = int(MenuHeight/30)
    StartButton.text_color = White

    BackBox = Box(Customiser, align="bottom", width = "fill")
    button = PushButton(BackBox, text ="BACK", align = "right", command = Back)
    button.text_size = int(MenuHeight/30)
    button.text_color = DarkRed2
################################################################################
def HowToPlay():
    def BackToMain():
        buttonPressedSound.play()
        HowToPlay.hide()
        Menu.show()
    HowToPlay = Window(Menu, title = "Customisation Menu", bg = Black)
    HowToPlay.full_screen = True

    HowToPlayHeight = HowToPlay.height
    HowToPlayWidth = HowToPlay.width

    TitleBox3 = Box(HowToPlay, width="fill", align="top")
    Background2 = Picture(TitleBox3, image = "bgd_menu.PNG")

    HowToPlay1 = Picture(HowToPlay, image = "menu_UseCustomisation.PNG", align = "left")
    HowToPlay2 = Picture(HowToPlay, image = "menu_PlayMainGame.PNG", align = "left")

    BackBox = Box(HowToPlay, align="bottom", width = "fill")
    button = PushButton(BackBox, text ="BACK", align = "right", command = BackToMain)
    button.text_size = int(MenuHeight/30)
    button.text_color = DarkRed2
################################################################################
def GameOver(Name, Score):
    def MainMenu():
        buttonPressedSound.play()
        GameOver.hide()
        menuMusic.load("Snd_MenuMusic.WAV")
        menuMusic.play(-1)
        Menu.show()

    ScoreText = (Name,"your score is", Score)

    GameOver = Window(Menu, title = "Game Over", bg = DarkRed)
    GameOver.full_screen = True
    GameOverText = Text(GameOver, text = "Game Over!", width = "fill", height = "fill")
    GameOver.text_size = 50
    GameOver.text_color = White
    GameOverText = Text(GameOver, text = ScoreText, width = "fill", height = "fill")
    GameOver.text_size = 100
    GameOver.text_color = White
    GameOverButton = PushButton(GameOver , text="Go back to Main Menu", command = MainMenu)
################################################################################
def displayLeaderboard():
    def BackToMain():
        buttonPressedSound.play()
        Leaderboard.hide()
        Menu.show()

    con = sqlite3.connect('Leaderboard.db')
    cursorObj = con.cursor()

    Leaderboard = Window(Menu, title="Supernatural: Saving People Hunting Things", bg = Black)
    Leaderboard.full_screen = True

    LeaderboardHeight = Leaderboard.height
    LeaderboardWidth = Leaderboard.width

    TitleBox = Box(Leaderboard, width="fill", align="top")
    Background = Picture(TitleBox, image = "Bgd_Leaderboard.PNG", width = LeaderboardWidth)


    EasyBox = Box(Leaderboard, width = int(LeaderboardWidth/3), height=int(LeaderboardWidth*0.8), align = "left")
    EasyBoxNumbers = Box(EasyBox,width = int(LeaderboardWidth/24), height="fill", align = "left") # changed width of numbers box and stats box
    for i in range (1,11):
        PlaceText = Text(EasyBoxNumbers, text = i)
        PlaceText.text_size = int(LeaderboardHeight/30)
        PlaceText.text_color = White
    strSQLEasy = "SELECT Name, Score FROM UsersScores WHERE Difficulty = 1 ORDER BY Score DESC LIMIT 10"
    cursorObj.execute(strSQLEasy)
    rows = cursorObj.fetchall()

    EasyBoxStats = Box(EasyBox, width = int(LeaderboardWidth/3), height="fill", align = "left")
    for row in rows:
        EasyText = Text(EasyBoxStats, text = row)
        EasyText.text_size = int(LeaderboardHeight/30)
        EasyText.text_color = White

    MediumBox = Box(Leaderboard, width = int(LeaderboardWidth/3), height=int(LeaderboardWidth*0.8), align = "left")
    MediumBoxNumbers = Box(MediumBox, width = int(LeaderboardWidth/24), height="fill", align = "left")
    for i in range (1,11):
        PlaceText = Text(MediumBoxNumbers, text = i)
        PlaceText.text_size = int(LeaderboardHeight/30)
        PlaceText.text_color = White
    strSQLMedium = "SELECT Name, Score FROM UsersScores WHERE Difficulty = 2 ORDER BY Score DESC LIMIT 10"
    cursorObj.execute(strSQLMedium)
    rows = cursorObj.fetchall()

    MediumBoxStats = Box(MediumBox, width = int(LeaderboardWidth/3), height="fill", align = "left")
    for row in rows:
        MediumText = Text(MediumBoxStats, text = row)
        MediumText.text_size = int(LeaderboardHeight/30)
        MediumText.text_color = White

        
    HardBox = Box(Leaderboard, width = int(LeaderboardWidth/3), height=int(LeaderboardWidth*0.8), align = "left")
    HardBoxNumbers = Box(HardBox, width = int(LeaderboardWidth/24), height = "fill", align = "left")
    for i in range (1,11):
        PlaceText = Text(HardBoxNumbers, text = i)
        PlaceText.text_size = int(LeaderboardHeight/30)
        PlaceText.text_color = White
    strSQLHard = "SELECT Name, Score FROM UsersScores WHERE Difficulty = 3 ORDER BY Score DESC LIMIT 10"
    cursorObj.execute(strSQLHard)
    rows = cursorObj.fetchall()

    HardBoxStats = Box(HardBox, width = int(LeaderboardWidth/3), height = "fill", align = "left")
    for row in rows:
        HardText = Text(HardBoxStats, text = row)
        HardText.text_size = int(LeaderboardHeight/30)
        HardText.text_color = White

    button = PushButton(HardBoxStats, text ="QUIT", align ="right", command = BackToMain)
    button.text_size = int(LeaderboardHeight/30)
    button.text_color = White

    cursorObj.close()
##################################################################################
menuMusic.load("Snd_MenuMusic.WAV")
menuMusic.play(-1)
Menu.display()
