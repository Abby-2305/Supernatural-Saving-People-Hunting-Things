from guizero import App, Text, TitleBox, Box, TextBox, CheckBox, PushButton
app = App(title="Restaurante")
app.width = 1280
topHeight = 100
middleHeight = 500
bottomHeight = 100
app.height = topHeight + middleHeight + bottomHeight
rightWidth = 380
leftWidth = 900
app.width = rightWidth + leftWidth
paddingHeight = 1

topBox = Box(app, align="top", width= "fill", height= topHeight, border= True)
padding01 = Text(topBox, text="", height = paddingHeight)
message = Text(topBox, text="TOP BOX", align="top", height = 1, size = 18)
padding02 = Text(topBox, text="", height = paddingHeight)
#messagel = Text(app, text="DeLeitese con nuestros exquisitos pLatos")

middleBox = Box(app, align="top", width= "fill", height= middleHeight, border= True)
leftBox = Box(middleBox, width= leftWidth, height= middleHeight, border= True, align="left", layout="grid")
inputLabel01 = Text(leftBox, text="Input01", grid=[0,0], width = 20, size = 14, align="left")
inputText01 = TextBox(leftBox, text="Type Input01 here", width = 40, grid=[1,0])
inputLabel02 = Text(leftBox, text="Inp02", grid=[0,1], width = 20, size = 14, align="left")
inputText02 = TextBox(leftBox, text="Type Inp02 here", width = 40, grid=[1,1])
inputLabel03 = Text(leftBox, text="Input03", grid=[0,2], width = 20, size = 14, align="left")
inputText03 = TextBox(leftBox, text="Type Input03 here", width = 40, grid=[1,2])

rightBox = Box(middleBox, width= rightWidth, height=middleHeight, border= True, layout="grid")
option01 = CheckBox (rightBox, text="", width = 2, grid=[0,0])
option01Text = Text (rightBox, text="Option01                      ", width = 30, align="left", grid=[1,0])
paddingOpt01 = Text(topBox, text="", height = paddingHeight)
option02 = CheckBox (rightBox, text="", width = 2, grid=[0,1])
option02Text = Text (rightBox, text="Option02 is really gigantic   ", width = 30, align="left", grid=[1,1])
paddingOpt02 = Text(topBox, text="", height = paddingHeight)
option03 = CheckBox (rightBox, text="", width = 2, grid=[0,2])
option03Text = Text (rightBox, text="Option03                      ", width = 30, align="left", grid=[1,2])
paddingOpt03 = Text(topBox, text="", height = paddingHeight)

bottomBox = Box(app, align="top", width= "fill", height= bottomHeight, border= True)
leftBottomBox = Box(bottomBox, align= "left",width= leftWidth, height= bottomHeight, border= True, layout = "grid")
paddingBot00 = Text(leftBottomBox, text="", width = 20, height = paddingHeight, grid = [0,0])
paddingBot10 = Text(leftBottomBox, text="", width = 20, height = paddingHeight, grid = [1,0])
message = Text(leftBottomBox, text="LEFT BOTTOM BOX", grid = [2,0])
paddingBot01 = Text(leftBottomBox, text="", width = 20, height = paddingHeight, grid = [0,1])
buttonOK = PushButton(leftBottomBox, text="OK", width = 20, height = 1, grid = [1,1])
paddingBot21 = Text(leftBottomBox, text="", width = 20, height = paddingHeight, grid = [2,1])
buttonCancel = PushButton(leftBottomBox, text="Cancel", width = 20, height = 1, grid = [3,1])
rightBottomBox = Box(bottomBox, align= "right",width= rightWidth, height=bottomHeight, border= True)
message = Text(rightBottomBox, text="RIGHT BOTTOM BOX")
app.display()
