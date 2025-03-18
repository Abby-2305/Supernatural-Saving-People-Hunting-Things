from guizero import App, Box, Text, TextBox, PushButton, Picture


Black = (0,0,0)
White = (255, 255, 255)
DarkRed = (188, 7, 12)



Menu = App(title="Supernatural: Saving People Hunting Things", bg = Black)
Menu.full_screen = True

MenuHeight = Menu.height
MenuWidth = Menu.width

TitleBox = Box(Menu, width="fill", align="top")
Background = Picture(Menu, image = "bgd_menu.PNG")

ButtonBox = Box(Menu, width = int(MenuWidth/4), height="fill")
button = PushButton(ButtonBox, text ="Play", width = "fill")
button.text_size = int(MenuHeight/30)
button.text_color = DarkRed
button = PushButton(ButtonBox, text="How To Play", width = "fill")
button.text_size = int(MenuHeight/30)
button.text_color = DarkRed
button = PushButton(ButtonBox, text="Leaderboards", width = "fill")
button.text_size = int(MenuHeight/30)
button.text_color = DarkRed

ExitBox = Box(Menu, align="bottom", width = "fill")
button = PushButton(ExitBox, text ="QUIT", align = "right")
button.text_size = int(MenuHeight/30)
button.text_color = DarkRed

Menu.display()
