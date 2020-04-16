#################################################
# Term Project 1:
#
# Your name: Shamini Wadhwani
# Your andrew id: swadhwan
#
#################################################
#PYTHON 3.7.7
import module_manager #https://www.cs.cmu.edu/~112/
module_manager.review() 
import math, random
from cmu_112_graphics import * #https://www.cs.cmu.edu/~112/
from PIL import Image
import string
import os
import tkinter
from pygame import mixer
from aubio import source, tempo
from numpy import median, diff

#Source for readFile and writeFile
#https://www.cs.cmu.edu/~112/notes/notes-strings.html
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "a+") as f:
        f.write(contents)

#Source to get dir_path:
#https://stackoverflow.com/questions/3430372/how-do-i-get-the-full-path-of-the-current-files-directory
dir_path = os.path.dirname(os.path.realpath(__file__))

def getSonglist():
    filesList = os.listdir(dir_path)
    songlist = []
    for fileName in filesList:
        if(".wav" in fileName):
            songlist.append(fileName)
    if(len(songlist) == 0):
        songlist.append('None')
    return songlist

#Source for getBeatsList:
#https://github.com/aubio/aubio/blob/master/python/demos/demo_tempo.py
def getBeatsList(name):
    filename = name
    #test song file #downloaded from itunes then converted to wave
    samplerate = 44100 #default samplerate
    win_s = 512 #default win_s
    hop_s = 256 #default hop_s
    s = source(filename, samplerate, hop_s)
    samplerate = s.samplerate
    o = tempo("default", win_s, hop_s, samplerate)
    beatsList = []
    total_frames = 0
    while True:
        samples, read = s()
        is_beat = o(samples)
        if is_beat:
            this_beat = o.get_last_s()
            beatsList.append(this_beat)
        total_frames += read
        if read < hop_s:
            break
    return beatsList

def getNewBeatsList(beatsList):
    newBeatsList = []
    #gets rid of half the beats sorts in columns
    for beat in beatsList:
        num = random.randint(0,5)
        time = beat
        cy = 220
        if(num == 1):
            cx = 425
            color = "green"
            newBeatsList.append((color, cx, cy, time))
        elif(num == 3):
            cx = 400
            color = "red"
            newBeatsList.append((color, cx, cy, time))
        elif(num == 5):
            cx = 375
            color = "blue"
            newBeatsList.append((color, cx, cy, time))
        else:
            pass
    return newBeatsList

def play_music(mode, song):
    mixer.init()
    mixer.music.load(song)
    mixer.music.play()

def loadMusic(mode, path=None):
    if (path is None):
        return None
    else:
        mixer.init()
        song = mixer.music.load(filename)
    return song

def playSong(mode, song):
    return mixer.music.play()

def stopSong(mode, song):
    return mixer.music.stop()

def checkSongPlayingStatus(mode, song):
    return mixer.music.get_busy()

class Obstacle(object):
    def __init__(self, cx, cy, radius, color):
        self.cx = cx
        self.cy = cy
        self.radius = radius
        self.color = color

    def getCollisionBounds(self):
        left = self.cx - self.radius
        right = self.cx + self.radius
        top = self.cy + self.radius
        bottom = self.cy - self.radius

class BollywoodRun(ModalApp):
    def appStarted(app):
        app.home = Home()
        app.selection = Selection()
        app.game = Game()
        app.help = Help()
        app.filename = ''
        app.playerScore = 0
        app.scores = HighScores()
        app.leaderboard = Leaderboard()
        app.setActiveMode(app.home)

class Home(Mode):
    def appStarted(mode):
        mode.image1 = mode.loadImage('Bollywood.png') #Created on: https://maketext.io
        mode.image2 = mode.loadImage('Run.png') #Created on: https://maketext.io
        mode.image3 = mode.loadImage('Enter.png') #Created on: https://maketext.io
        mode.image4 = mode.loadImage('srk.png') #Downloaded from: https://www.uihere.com
        mode.image5 = mode.loadImage('ranbir.png') #Downloaded from: https://www.uihere.com
        mode.image4 = mode.scaleImage(mode.image4, 1/1.5)
        mode.image5 = mode.scaleImage(mode.image5, 1/2.5)
        mode.image5 = mode.image5.transpose(Image.FLIP_LEFT_RIGHT)
        mode.image6 = mode.loadImage('fire.png') #https://cdn131.picsart.com/267730478008211.png?to=min&r=640
        
    def mousePressed(mode, event):
        if((event.x <= 565) and (event.x >= 250) and (event.y <= 575) and (event.y >= 500)):
            mode.app.setActiveMode(mode.app.selection)

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = "black")
        canvas.create_image(mode.width//2, mode.height//3, image=ImageTk.PhotoImage(mode.image2))
        canvas.create_image(mode.width//2, mode.height//6, image=ImageTk.PhotoImage(mode.image1))
        canvas.create_image(mode.width//2, mode.height//1.5, image=ImageTk.PhotoImage(mode.image3))
        canvas.create_image(mode.width//2, mode.height//1.2, image=ImageTk.PhotoImage(mode.image6))
        canvas.create_image(mode.width//8, mode.height//1.2, image=ImageTk.PhotoImage(mode.image4))
        canvas.create_image(mode.width//1.15, mode.height//1.25, image=ImageTk.PhotoImage(mode.image5))

class Selection(Mode):
    def appStarted(mode):
        mode.message = ""
        mode.songList = getSonglist()
        mode.index = 0
        mode.songName = mode.songList[mode.index]
        mode.image1 = mode.loadImage('arrow.jpg') #https://www.pngitem.com/pimgs/m/338-3389718_right-side-bar-touch-arrow-comments-triangle-play.png
        mode.image1 = mode.scaleImage(mode.image1, 1/25)
        mode.image2 = mode.image1.transpose(Image.FLIP_LEFT_RIGHT)
        mode.image3 = mode.loadImage('Select.png') #Created on: https://maketext.io
        mode.image4 = mode.loadImage('Song.png') #Created on: https://maketext.io
        mode.image5 = mode.loadImage('akshay.png') #Downloaded from: https://www.uihere.com
        mode.image5 = mode.scaleImage(mode.image5, 1/1.5)
        mode.image6 = mode.loadImage('fire.png') #https://cdn131.picsart.com/267730478008211.png?to=min&r=640

    def keyPressed(mode, event):
        if(event.key == "Left"):
            if(mode.index > 0):
                mode.index -=1
                mode.songName = mode.songList[mode.index]

        if(event.key == "Right"):
            if(mode.index < len(mode.songList) - 1):
                mode.index +=1
                mode.songName = mode.songList[mode.index]

        if(event.key == "Enter"):
            # app.filename = mode.songName
            mode.app.filename = mode.songName
            mode.app.setActiveMode(mode.app.game)

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = "black")
        canvas.create_image(mode.width//2, mode.height//3, image=ImageTk.PhotoImage(mode.image4))
        canvas.create_image(mode.width//2, mode.height//6, image=ImageTk.PhotoImage(mode.image3))
        canvas.create_rectangle(100, mode.height//2 + 25, mode.width - 75, mode.height//2 + -25, fill = "white")
        canvas.create_image(mode.width - 95, mode.height//2, image=ImageTk.PhotoImage(mode.image1))
        canvas.create_image(120, mode.height//2, image=ImageTk.PhotoImage(mode.image2))
        canvas.create_text(mode.width//2, mode.height//2, text = mode.songName, font = "Arial 20", fill = "black")
        canvas.create_text(mode.width//2, mode.height//1.75, text = "Use the Left/Right Keyboard Arrows to Switch Between Songs", font = "Arial 20", fill = "white")
        canvas.create_text(mode.width//2, mode.height//1.65, text = "Press Enter on your Keyboard to Choose Song and Start the Game", font = "Arial 20", fill = "white")
        canvas.create_image(mode.width//2, mode.height//1.2, image=ImageTk.PhotoImage(mode.image6))
        canvas.create_image(mode.width//2, mode.height//1.1, image=ImageTk.PhotoImage(mode.image5))

class Game(Mode):
    def appStarted(mode):
        mode.fileName = mode.app.filename
        mode.isGameOver = False
        mode.score = 0
        mode.scrollY = 0
        mode.delta = 50
        mode.waitingForPlay = True
        mode.waitingForFirstPlay = True
        mode.r = 5
        mode.image1 = mode.loadImage('fret3.jpg') 
        #Image Source: tinyurl.com/SWadhwanTPImage1
        #Imaged edited on preview
        mode.image2 = mode.scaleImage(mode.image1, 2/3)
        mode.characterImages = []
        mode.counter = 0
        mode.lineCounter = 0
        mode.beats = getNewBeatsList(getBeatsList(mode.fileName))
        mode.image3 = mode.loadImage('spriteNew.png') #https://www.seekpng.com/png/full/230-2302939_joining-images-to-create-sprite-sheet-donald-trump.png
        mode.characterImages = [ ]
        for i in range(6):
            sprite = mode.image3.crop((0+100*i, 0, 100+100*i, 100))
            newSprite = mode.scaleImage(sprite, 1)
            mode.characterImages.append(newSprite)
        mode.positionx = mode.width//2
        mode.positiony = mode.height*(4/5)
        mode.circleCenters = []
        mode.musicIsPaused = False
        mode.linePoints = []
        mode.jump = False
        mode.jumpTime = 0
        mode.lineScroll = 0
        mode.lineTime = 0
        mode.placeLines()
        mode.songPlaying = False

    def mousePressed(mode, event):
        print((event.x, event.y))

    def keyPressed(mode, event):
        if (mode.waitingForFirstPlay == True):
            mode.waitingForFirstPlay = False
            play_music(mode, mode.fileName)
            mode.songPlaying = False
        if(mode.waitingForPlay == True):
            if(event.key == 'Space'):
                mode.waitingForPlay = False
                mixer.music.unpause()
        elif(event.key == 'q'):
            stopSong(mode, mode.fileName)
        elif(event.key == 'p'):
            if(mode.musicIsPaused == False):
                mixer.music.pause()
            else:
                mixer.music.unpause()
            mode.musicIsPaused = not mode.musicIsPaused
        elif(event.key == 'Left'):
            mode.positionx -= 200
            if(mode.positionx < (mode.width//2 - 200)):
                mode.positionx += 200
        elif(event.key == 'Right'):
            mode.positionx += 200
            if(mode.positionx > (mode.width//2 + 200)):
                mode.positionx -= 200
        elif(event.key == 'Down'):
            mode.positiony += 100 #tesing purposes
        elif(event.key == 'h'):
            mode.app.setActiveMode(mode.app.help)
            mixer.music.pause() 
        elif(event.key == 's'):
            mode.app.setActiveMode(mode.app.scores)
            mixer.music.pause() 
        elif(mode.jump == False):
            if(event.key == 'Up'):
                mode.positiony = mode.height*(4/5) - 150
                mode.jump = True

    def timerFired(mode):
        if mode.isGameOver or mode.waitingForPlay: return
        mode.counter = (1 + mode.counter) % len(mode.characterImages)
        mode.placeLines()
        mode.lineTime += 1
        mode.scrollY += 5
        mode.lineScroll += 5
        mode.app.playerScore = mode.score
        if(len(mode.beats) > 0):
            newBeat = mode.beats[0]
            mode.circleCenters.append(newBeat)
            mode.beats.pop(0)
        if mode.jump == True:
            mode.jumpTime +=1
        if(mode.jumpTime == 2):
            mode.positiony = mode.height*(4/5)
            mode.jump = False
            mode.jumpTime = 0
        if(mode.lineTime > 70):
            mode.lineTime = 0
            mode.lineScroll = 0
        if(checkSongPlayingStatus(mode, mode.fileName) == 0):
            mode.songPlaying = False
            mode.isGameOver = True

    def placeLines(mode):
        mode.linePoints.append((115, 750, 685, 750))
        mode.linePoints.append((175, 630, 625, 630))
        mode.linePoints.append((235, 510, 565, 510))
        mode.linePoints.append((295, 390, 505, 390))
        mode.linePoints.append((355, 270, 445, 270))
        mode.linePoints.append((415, 150, 385, 150))
        mode.linePoints.append((475, 30, 325, 30))

    def getPersonCollisionBounds(mode):
        left = mode.positionx - 50
        right = mode.positionx + 50
        top = mode.positiony - 50
        bottom = mode.positiony + 50
        return (left, right, top, bottom)

    def detectBeatCollision(mode, cx, cy):
        left = mode.getPersonCollisionBounds()[0]
        right = mode.getPersonCollisionBounds()[1]
        top = mode.getPersonCollisionBounds()[2]
        bottom = mode.getPersonCollisionBounds()[3]
        if(cx >= left and cx <= right and cy >= top and cy <= bottom):
            return True
        else:
            return False

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = "black")
        canvas.create_image(mode.width//2, mode.height//2, image=ImageTk.PhotoImage(mode.image1))
        for (color, cx, cy, time) in mode.circleCenters:
            if(color == "red"):
                cy -= time*mode.delta 
                cy += mode.scrollY
                value = mode.detectBeatCollision(cx, cy)
                # bounds = mode.getPersonCollisionBounds()
                # if(cy > 300):
                #     print(bounds, "bounds")
                #     print(value, "value")
                #     print(cx, "cx")
                #     print(cy, "cy")
                if(value == True and cy >= 310):
                    canvas.create_oval(cx-mode.r, cy-mode.r, cx+mode.r, cy+mode.r, fill="yellow")
                if(value == False and cy >= 310):
                    canvas.create_oval(cx-mode.r, cy-mode.r, cx+mode.r, cy+mode.r, fill=color)
        for (color, cx, cy, time) in mode.circleCenters:
            if(color == "green"):
                cy -= time*mode.delta
                cx += time*mode.delta//2 
                cy += mode.scrollY
                cx -= mode.scrollY//2
                if(cy >= 310):
                    canvas.create_oval(cx-mode.r, cy-mode.r, cx+mode.r, cy+mode.r, fill=color)
            if(color == "blue"):
                cy -= time*mode.delta 
                cx -= time*mode.delta//2 
                cy += mode.scrollY
                cx += mode.scrollY//2
                if(cy >= 310):
                    canvas.create_oval(cx-mode.r, cy-mode.r, cx+mode.r, cy+mode.r, fill=color)
        for (lx, ly, lx2, ly2) in mode.linePoints:
            ly += mode.lineScroll
            ly2 += mode.lineScroll
            lx -= mode.lineScroll//2
            lx2 += mode.lineScroll//2
            if(ly2 >= 330 and ly >= 330):
                canvas.create_line(lx, ly, lx2, ly2, fill = "grey")
        sprite = mode.characterImages[mode.counter]
        canvas.create_image(mode.positionx, mode.positiony, image=ImageTk.PhotoImage(sprite))

class Help(Mode):
    def appStarted(mode):
        mode.image1 = mode.loadImage('arrowKeys.png') #https://i.ya-webdesign.com/images/arrow-keys-png-image-5.png
        mode.image2 = mode.scaleImage(mode.image1, 2/3)
        mode.image6 = mode.loadImage('fire.png') #https://cdn131.picsart.com/267730478008211.png?to=min&r=640

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = "black")
        canvas.create_text(mode.width//2, mode.height//6, text = "Help Screen", font = "Arial 40 bold", fill="white")
        canvas.create_text(mode.width//2, mode.height//2, text = "h - help", font = "Arial 20", fill="white")
        canvas.create_text(mode.width//2, mode.height//2 + 25, text = "p - pause/unpause music", font = "Arial 20", fill="white")
        canvas.create_text(mode.width//2, mode.height//2 + 50, text = "r - restart", font = "Arial 20", fill="white")
        canvas.create_text(mode.width//2, mode.height//2 + 75, text = "q - quit", font = "Arial 20", fill="white")
        canvas.create_text(mode.width//2, mode.height//3, text = "Collect music beats as you go and watch out for obstacles!", font = "Arial 20", fill="white")
        canvas.create_text(mode.width//2, mode.height//3 + 50, text = "Press Enter to Return to the Game", font = "Arial 20", fill="white")
        canvas.create_text(mode.width//2 - 125, mode.height//1.18, text = "Left", font = "Arial 20", fill="white")
        canvas.create_text(mode.width//2 + 135, mode.height//1.18, text = "Right", font = "Arial 20", fill="white")
        canvas.create_text(mode.width//2, mode.height//1.45, text = "Jump", font = "Arial 20", fill="white")
        canvas.create_image(mode.width//2, mode.height//1.1, image=ImageTk.PhotoImage(mode.image6))
        canvas.create_image(mode.width//2, mode.height//1.25, image=ImageTk.PhotoImage(mode.image2))

    def keyPressed(mode, event):
        if(event.key == "Enter"):
            mode.app.setActiveMode(mode.app.game)

class HighScores(Mode):
    def appStarted(mode):
        mode.message = ''
        mode.typing = False
        mode.image1 = mode.loadImage('Salman.png') #Downloaded from: https://www.uihere.com
        mode.image1 = mode.scaleImage(mode.image1, 1/2)
        mode.image6 = mode.loadImage('fire.png') #https://cdn131.picsart.com/267730478008211.png?to=min&r=640
        mode.score = mode.app.playerScore

    def mousePressed(mode, event):
        if(event.x > 100 and event.x < (mode.height-100) and event.y > mode.height//2 -25 and event.y < mode.height//2 + 25):
            mode.typing = True

    def keyPressed(mode, event):
        if(event.key == "Enter"):
            contentsToWrite = (mode.message + f',{mode.score}' + "/n")
            writeFile("HighScores.txt", contentsToWrite)
            mode.app.setActiveMode(mode.app.leaderboard)
        if(mode.typing == True):
            if((f"{event.key}" in string.ascii_letters) or (f"{event.key}" in string.digits)) :
                mode.message += f"{event.key}"
            if(event.key == "Delete"):
                mode.message = mode.message[:-1]

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = "black")
        canvas.create_text(mode.width//2, mode.height//6, text = "High Scores", font = "Arial 40 bold", fill="white")
        canvas.create_text(mode.width//2, mode.height//3, text = "Your Score Is:", font = "Arial 20", fill="white")
        canvas.create_text(mode.width//2, mode.height//3 + 25, text = "Click Inside the Textbox to Input your Name", font = "Arial 20", fill="white")
        canvas.create_text(mode.width//2, mode.height//3 + 50, text = "Press Enter to Continue", font = "Arial 20", fill = "white")
        canvas.create_rectangle(100, mode.height//2 - 25, mode.width - 100, mode.height//2 + 25, fill = "white")
        canvas.create_text(mode.width//2, mode.height//2, text = mode.message, font = "Arial 20")
        canvas.create_image(mode.width//2, mode.height//1.2, image=ImageTk.PhotoImage(mode.image6))
        canvas.create_image(mode.width//2, mode.height//1.2, image=ImageTk.PhotoImage(mode.image1))

class Leaderboard(Mode):
    def appStarted(mode):
        mode.image1 = mode.loadImage('Amitabh.png') #Downloaded from: https://www.uihere.com
        mode.image6 = mode.loadImage('fire.png') #https://cdn131.picsart.com/267730478008211.png?to=min&r=640
    
    def keyPressed(mode, event):
        if((event.key == "q") or (event.key == "Enter")):
            mode.app.setActiveMode(mode.app.home)

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = "black")
        canvas.create_text(mode.width//2, mode.height//6, text = "Leaderboard", font = "Arial 40 bold", fill="white")
        canvas.create_image(mode.width//2, mode.height//1.2, image=ImageTk.PhotoImage(mode.image6))
        canvas.create_image(mode.width//2, mode.height//1.18, image=ImageTk.PhotoImage(mode.image1))
        contentsRead = readFile("HighScores.txt")
        count = -1
        for line in contentsRead.splitlines():
            name = line.split(",")[0]
            score = line.split(",")[1]
            count +=1
            if(count < 10):
                canvas.create_text(300, mode.height//3.5 + 30*count, text = name, font = "Arial 20", fill = "white")
                canvas.create_text(mode.width - 300, mode.height//3.5 + 30*count, text = score, font = "Arial 20", fill = "white")

app = BollywoodRun(width=800, height=800)
