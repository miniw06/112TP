#################################################
# Term Project 2:
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
        index = beatsList.index(beat)
        collision = False
        num = random.randint(1,3)
        time = beat
        cy = 220
        if(num == 1):
            cx = 425
            color = "green"
            newBeatsList.append((color, cx, cy, time, collision, index))
        elif(num == 2):
            cx = 400
            color = "red"
            newBeatsList.append((color, cx, cy, time, collision, index))
        elif(num == 3):
            cx = 375
            color = "blue"
            newBeatsList.append((color, cx, cy, time, collision, index))
        else:
            pass
    return newBeatsList

def playMusic(mode, song):
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

class BollywoodRun(ModalApp):
    def appStarted(app):
        app.home = Home()
        app.selection = Selection()
        app.game = Game()
        app.help = Help()
        app.filename = ''
        app.playerScore = 0
        app.statistics = Statistics()
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
        mode.app.filename = ''
        
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
            print(mode.songName)
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
        mode.timerDelay = 1
        mode.missedRedCount = 0
        mode.missedBlueCount = 0
        mode.missedGreenCount = 0
        mode.collectedRed = 0
        mode.collectedBlue = 0
        mode.collectedGreen = 0
        mode.currentDot = -1
        mode.dotsSeen = []
        mode.dotsMissed = []
        mode.dotsPrinted = []
        mode.obstacles = []
        mode.image4 = mode.loadImage('spike.png') 
        mode.image4 = mode.scaleImage(mode.image4, 1/3)
        mode.image6 = mode.loadImage('icebolt.png') 
        mode.image6 = mode.scaleImage(mode.image6, 1/15)
        mode.image7 = mode.loadImage('boost.png') 
        mode.image7 = mode.scaleImage(mode.image7, 1/6)
        mode.image8 = mode.loadImage('ice.png') 
        mode.image8 = mode.scaleImage(mode.image8, 1/6)
        mode.image9 = mode.loadImage('star2.png') 
        mode.image9 = mode.scaleImage(mode.image9, 1/12)
        mode.obstalceTimer = 0
        mode.obstaclePlaced = True
        mode.obstacleScroll = 0
        mode.obstacleIndex = 0
        mode.obstaclesSeen = []
        mode.spikesSeen = []
        mode.enemyAwake = False
        mode.enemyTimer = 0
        mode.iceSeen = []
        mode.boostsSeen = []
        mode.frozen = False
        mode.iceTimer = 0
        mode.boostScore = False
        mode.boostScoreTimer = 0
        mode.gameEndTimer = 0

    def mousePressed(mode, event):
        print((event.x, event.y))

    def keyPressed(mode, event):
        if (mode.waitingForFirstPlay == True):
            mode.waitingForFirstPlay = False
            playMusic(mode, mode.fileName)
            mode.songPlaying = True
        if(mode.waitingForPlay == True):
            if(event.key == 'Space'):
                mode.waitingForPlay = False
                mixer.music.unpause()
        elif(event.key == 'q'):
            stopSong(mode, mode.fileName)
            mode.waitingForFirstPlay = True
            mode.waitingForPlay = True
            mode.app.setActiveMode(mode.app.home)
        elif(event.key == 'p'):
            if(mode.musicIsPaused == False):
                mixer.music.pause()
            else:
                mixer.music.unpause()
            mode.musicIsPaused = not mode.musicIsPaused
        elif(event.key == 'h'):
            mode.app.setActiveMode(mode.app.help)
            mixer.music.pause() 
        elif(event.key == 'Enter'):
            mode.app.setActiveMode(mode.app.statistics)
            stopSong(mode, mode.fileName)
        if(mode.frozen == False):
            if(event.key == 'Left'):
                mode.positionx -= 200
                if(mode.positionx < (mode.width//2 - 200)):
                    mode.positionx += 200
            elif(event.key == 'Right'):
                mode.positionx += 200
                if(mode.positionx > (mode.width//2 + 200)):
                    mode.positionx -= 200
            elif(mode.jump == False):
                if(event.key == 'Up'):
                    mode.positiony = mode.height*(4/5) - 150
                    mode.jump = True

    def timerFired(mode):
        if mode.isGameOver or mode.waitingForPlay or mode.musicIsPaused: return
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
        if(mode.jumpTime == 15):
            mode.positiony = mode.height*(4/5)
            mode.jump = False
            mode.jumpTime = 0
        if(mode.lineTime > 70):
            mode.lineTime = 0
            mode.lineScroll = 0
        if(checkSongPlayingStatus(mode, mode.fileName) == 0):
            mode.songPlaying = False
            mode.gameEndTimer += 1
        if(mode.obstaclePlaced == False and mode.gameEndTimer == 0):
            mode.placeObstacle()
            mode.obstaclePlaced = True
        if mode.obstaclePlaced == True:
            mode.obstalceTimer +=1
            mode.obstacleScroll +=5
        if(mode.obstalceTimer == 100):
            mode.obstaclePlaced = False
            mode.obstalceTimer = 0
            mode.obstacleScroll = 0
            mode.obstacleIndex += 1
            if(len(mode.obstacles) > 0):
                mode.obstacles.pop(0)
        if(mode.enemyAwake == True):
            mode.enemyTimer += 1
        if(mode.enemyTimer == 50):
            mode.enemyTimer = 0
            mode.subtractScore(50)
            mode.enemyAwake = False
        if(mode.frozen == True):
            mode.iceTimer += 1
        if(mode.iceTimer == 50):
            mode.iceTimer = 0
            mode.frozen = False
        if(mode.boostScore == True):
            mode.boostScoreTimer += 1
        if(mode.boostScoreTimer == 50):
            mode.boostScoreTimer = 0
            mode.boostScore = False
        if(mode.gameEndTimer == 100):
            mode.isGameOver = True

    def placeLines(mode):
        mode.linePoints.append((115, 750, 685, 750))
        mode.linePoints.append((175, 630, 625, 630))
        mode.linePoints.append((235, 510, 565, 510))
        mode.linePoints.append((295, 390, 505, 390))
        mode.linePoints.append((355, 270, 445, 270))
        mode.linePoints.append((415, 150, 385, 150))
        mode.linePoints.append((475, 30, 325, 30))

    def placeObstacle(mode):
        if(mode.score < 0):
            objects = ["boost", "ice", "spike", "boost"]
        elif(mode.score > 500):
            objects = ["boost", "ice", "spike", "ice", "spike"]
        elif(mode.score > 1000):
            objects = ["ice", "ice", "spike", "ice", "spike"]
        else:
            objects = ["boost", "ice", "spike"]
        cxPositions = [425, 400, 375]
        name = random.choice(objects)
        cx = random.choice(cxPositions)
        cy = 310
        size = 100
        if(cx == 425):
            column = 1
        elif(cx == 400):
            column = 2
        else:
            column = 3
        index = mode.obstacleIndex
        mode.obstacles.append((cx, cy, name, column, index))

    def getPersonCollisionBounds(mode):
        left = mode.positionx - 50
        right = mode.positionx + 50
        top = mode.positiony
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

    def detectObjectCollision(mode, cx, cy):
        left = mode.getPersonCollisionBounds()[0]
        right = mode.getPersonCollisionBounds()[1]
        top = mode.getPersonCollisionBounds()[2]
        bottom = mode.getPersonCollisionBounds()[3]
        if(cx >= left and cx <= right and cy >= top and cy <= bottom):
            return True
        else:
            return False    

    def gameOver(mode):
        mode.isGameOver = True

    def freeze(mode, index):
        mode.iceSeen.append(index)
        mode.frozen = True

    def boost(mode, index):
        mode.boostsSeen.append(index)
        mode.boostScore = True

    def subtractScore(mode, value):
        mode.score -= value

    def addSeenDot(mode, index):
        mode.dotsSeen.append(index)

    def addMissedDot(mode, index):
        mode.dotsMissed.append(index)

    def addScore(mode, value):
        if(mode.boostScore == True):
            mode.score += 2*value
        else:
            mode.score += value

    def addSpike(mode, index):
        mode.spikesSeen.append(index)
        mode.enemyAwake = True

    def addMissed(mode, color):
        if(color == 'red'):
            mode.missedRedCount +=1
        elif(color == 'blue'):
            mode.missedBlueCount +=1
        elif(color == 'green'):
            mode.missedGreenCount +=1

    def addCollected(mode, color):
        if(color == 'red'):
            mode.collectedRed += 1
        elif(color == 'blue'):
            mode.collectedBlue +=1
        elif(color == 'green'):
            mode.collectedGreen +=1

    def addPrintedDot(mode, index):
        mode.dotsPrinted.append(index)

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = "black")
        canvas.create_image(mode.width//2, mode.height//2, image=ImageTk.PhotoImage(mode.image1))
        for (color, cx, cy, time, collision, index) in mode.circleCenters:
            if(color == "red"):
                cy -= time*mode.delta 
                cy += mode.scrollY
                value = mode.detectBeatCollision(cx, cy)
                if(cy >= 750 and (index not in mode.dotsSeen) and (index not in mode.dotsMissed)):
                    mode.addMissedDot(index)
                    mode.subtractScore(20)
                    mode.addMissed("red")    
                if(value == True and (index not in mode.dotsSeen)):
                    mode.addSeenDot(index)
                    mode.addScore(10)
                    mode.addCollected("red")
                if(cy >= 310 and cy <= 750 and (index not in mode.dotsSeen) and mode.songPlaying == True):
                    mode.addPrintedDot(index)
                    canvas.create_oval(cx-mode.r, cy-mode.r, cx+mode.r, cy+mode.r, fill=color)
                if(cy >= 310 and cy <= 750 and (index not in mode.dotsSeen) and (index in mode.dotsPrinted) and mode.songPlaying == False):
                    canvas.create_oval(cx-mode.r, cy-mode.r, cx+mode.r, cy+mode.r, fill=color)
            if(color == "green"):
                cy -= time*mode.delta
                cx += time*mode.delta//2 
                cy += mode.scrollY
                cx -= mode.scrollY//2
                value = mode.detectBeatCollision(cx, cy)
                if(cy >= 750 and (index not in mode.dotsSeen) and (index not in mode.dotsMissed)):
                    mode.addMissedDot(index)
                    mode.subtractScore(10)
                    mode.addMissed("green")    
                if(value == True and (index not in mode.dotsSeen)):
                    mode.addSeenDot(index)
                    mode.addScore(20)
                    mode.addCollected("green")
                if(cy >= 310 and cy <= 750 and (index not in mode.dotsSeen) and mode.songPlaying == True):
                    mode.addPrintedDot(index)
                    canvas.create_oval(cx-mode.r, cy-mode.r, cx+mode.r, cy+mode.r, fill=color)
                if(cy >= 310 and cy <= 750 and (index not in mode.dotsSeen) and (index in mode.dotsPrinted) and mode.songPlaying == False):
                    canvas.create_oval(cx-mode.r, cy-mode.r, cx+mode.r, cy+mode.r, fill=color)
            if(color == "blue"):
                cy -= time*mode.delta 
                cx -= time*mode.delta//2 
                cy += mode.scrollY
                cx += mode.scrollY//2
                value = mode.detectBeatCollision(cx, cy)
                if(cy >= 750 and (index not in mode.dotsSeen) and (index not in mode.dotsMissed)):
                    mode.addMissedDot(index)
                    mode.subtractScore(10)
                    mode.addMissed("blue")    
                if(value == True and (index not in mode.dotsSeen)):
                    mode.addSeenDot(index)
                    mode.addScore(20)
                    mode.addCollected("blue")
                if(cy >= 310 and cy <= 750 and (index not in mode.dotsSeen) and mode.songPlaying == True):
                    mode.addPrintedDot(index)
                    canvas.create_oval(cx-mode.r, cy-mode.r, cx+mode.r, cy+mode.r, fill=color)
                if(cy >= 310 and cy <= 750 and (index not in mode.dotsSeen) and (index in mode.dotsPrinted) and mode.songPlaying == False):
                    canvas.create_oval(cx-mode.r, cy-mode.r, cx+mode.r, cy+mode.r, fill=color)
        for (lx, ly, lx2, ly2) in mode.linePoints:
            ly += mode.lineScroll
            ly2 += mode.lineScroll
            lx -= mode.lineScroll//2
            lx2 += mode.lineScroll//2
            if(ly2 >= 330 and ly >= 330 and ly <= 750 and ly2 <=750):
                canvas.create_line(lx, ly, lx2, ly2, fill = "grey")
        for (cx, cy, name, column, index) in mode.obstacles:
            if(column == 1):
                cy += mode.obstacleScroll
                cx += mode.obstacleScroll//2
            elif(column == 3):
                cy += mode.obstacleScroll
                cx -= mode.obstacleScroll//2
            else:
                cy += mode.obstacleScroll
            value = mode.detectObjectCollision(cx, cy)
            if(name == "spike" and cy <= 750):
                canvas.create_image(cx, cy, image=ImageTk.PhotoImage(mode.image4))
                if(mode.enemyAwake == True and value ==  True and (index not in mode.spikesSeen)):
                        mode.addSpike(index)
                        mode.gameOver()
                elif(value ==  True and (index not in mode.spikesSeen)):
                    mode.addSpike(index)

            if(name == "ice" and cy <= 750):
                canvas.create_image(cx, cy, image=ImageTk.PhotoImage(mode.image6))
                if(value ==  True and (index not in mode.iceSeen)):
                    mode.freeze(index)

            if(name == "boost" and cy <= 750):
                canvas.create_image(cx, cy, image=ImageTk.PhotoImage(mode.image7))
                if(value ==  True and (index not in mode.boostsSeen)):
                    mode.boost(index)
    
            if(mode.enemyAwake == True):
                y = mode.height*(4/5) + 100
                sprite = mode.characterImages[mode.counter]
                canvas.create_image(mode.positionx, y, image=ImageTk.PhotoImage(sprite))

            if(mode.frozen == True):
                canvas.create_image(mode.positionx, mode.positiony, image=ImageTk.PhotoImage(mode.image8))

            if(mode.boostScore == True):
                canvas.create_image(mode.positionx, mode.positiony, image=ImageTk.PhotoImage(mode.image9))

        sprite = mode.characterImages[mode.counter]
        canvas.create_image(mode.positionx, mode.positiony, image=ImageTk.PhotoImage(sprite))
        canvas.create_text(mode.width//6, mode.height//8, text = f'Score: {mode.score}', font = "Arial 30 bold", fill="white")

        if(mode.isGameOver == True):
            canvas.create_text(mode.width//2, mode.height//2, text = "Game Over", font = "Arial 30 bold", fill="white")
            canvas.create_text(mode.width//2, mode.height//2 + 100, text="Press Enter to Continue", font="Arial 20 bold", fill = "white")

class Help(Mode):
    def appStarted(mode):
        mode.image1 = mode.loadImage('arrowKeys.png') #https://i.ya-webdesign.com/images/arrow-keys-png-image-5.png
        mode.image2 = mode.scaleImage(mode.image1, 2/3)
        mode.image6 = mode.loadImage('fire.png') #https://cdn131.picsart.com/267730478008211.png?to=min&r=640

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = "black")
        canvas.create_text(mode.width//2, mode.height//6, text = "Help Screen", font = "Arial 40 bold", fill="white")
        canvas.create_text(mode.width//2, mode.height//2, text = "h - help", font = "Arial 20", fill="white")
        canvas.create_text(mode.width//2, mode.height//2 + 25, text = "p - pause", font = "Arial 20", fill="white")
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

class Statistics(Mode):
    def appStarted(mode):
        mode.image1 = mode.loadImage('fire.png') #https://cdn131.picsart.com/267730478008211.png?to=min&r=640
        mode.score = mode.app.playerScore
        mode.redCollected = mode.app.game.collectedRed
        mode.greenCollected = mode.app.game.collectedGreen
        mode.blueCollected = mode.app.game.collectedBlue
        mode.redMissed = mode.app.game.missedRedCount
        mode.blueMissed = mode.app.game.missedBlueCount
        mode.greenMissed = mode.app.game.missedGreenCount
        mode.redPercent = ((mode.redCollected)/(mode.redCollected + mode.redMissed) * 100)//1
        mode.greenPercent = ((mode.greenCollected)/(mode.greenCollected + mode.greenMissed) * 100)//1
        mode.bluePercent = ((mode.blueCollected)/(mode.blueCollected + mode.blueMissed) * 100)//1
        mode.redDrawn = 0
        mode.greenDrawn = 0
        mode.blueDrawn = 0
        mode.spikeCount = len(mode.app.game.spikesSeen)
        mode.spikeCounter = 0
        mode.iceCount = len(mode.app.game.iceSeen)
        mode.iceCounter = 0
        mode.boostCount = len(mode.app.game.boostsSeen)
        mode.boostCounter = 0
        mode.image2 = mode.loadImage('spike.png') 
        mode.image2 = mode.scaleImage(mode.image2, 2/3)
        mode.image3 = mode.loadImage('icebolt.png') 
        mode.image3 = mode.scaleImage(mode.image3, 1/15)
        mode.image4 = mode.loadImage('boost.png') 
        mode.image4 = mode.scaleImage(mode.image4, 1/6)

    def timerFired(mode):
        if(mode.blueDrawn < mode.bluePercent):
            mode.blueDrawn += 1
        if(mode.greenDrawn < mode.greenPercent):
            mode.greenDrawn += 1
        if(mode.redDrawn < mode.redPercent):
            mode.redDrawn += 1
        if(mode.spikeCounter < mode.spikeCount):
            mode.spikeCounter += 1
        if(mode.iceCounter < mode.iceCount):
            mode.iceCounter += 1
        if(mode.boostCounter < mode.boostCount):
            mode.boostCounter += 1

    def keyPressed(mode, event):
        if(event.key == "Enter"):
            mode.app.setActiveMode(mode.app.scores)

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = "black")
        canvas.create_text(mode.width//2, mode.height//6, text = "Statistics", font = "Arial 40 bold", fill="white")
        canvas.create_text(mode.width//2, mode.height//4, text = f'Your score is: {mode.score}', font = "Arial 20", fill="white")
        canvas.create_text(mode.width//2, mode.height//2 - 145, text = "Beats Collected", font = "Arial 20", fill="white")

        canvas.create_rectangle(100, mode.height//2 - 115, mode.width - 100, mode.height//2 - 85, fill = "black", outline="white")
        canvas.create_rectangle(100, mode.height//2 - 115, 100 + (mode.width - 200)*mode.greenDrawn/100, mode.height//2 - 85, fill = "green", outline = "black")
        if(mode.greenDrawn == mode.greenPercent):
            canvas.create_text(125 + (mode.width - 200)*mode.greenDrawn/100, mode.height//2 - 100, text = f'{mode.greenDrawn}%', font = "Arial 12", fill="white")

        canvas.create_rectangle(100, mode.height//2 - 70, mode.width - 100, mode.height//2 - 40, fill = "black", outline="white")
        canvas.create_rectangle(100, mode.height//2 - 70, 100 + (mode.width - 200)*mode.redDrawn/100, mode.height//2 - 40, fill = "red", outline = "black")
        if(mode.redDrawn == mode.redPercent):
            canvas.create_text(125 + (mode.width - 200)*mode.redDrawn/100, mode.height//2 - 55, text = f'{mode.redDrawn}%', font = "Arial 12", fill="white")

        canvas.create_rectangle(100, mode.height//2 - 25, mode.width - 100, mode.height//2 +5, fill = "black", outline="white")
        canvas.create_rectangle(100, mode.height//2 - 25, 100 + (mode.width - 200)*mode.blueDrawn/100, mode.height//2 +5, fill = "blue", outline = "black")
        if(mode.blueDrawn == mode.bluePercent):
            canvas.create_text(125 + (mode.width - 200)*mode.blueDrawn/100, mode.height//2 - 10, text = f'{mode.blueDrawn}%', font = "Arial 12", fill="white")

        canvas.create_image(mode.width//2, mode.height//1.2, image=ImageTk.PhotoImage(mode.image1))

        canvas.create_image(mode.width//2 - 25, mode.height//1.6, image=ImageTk.PhotoImage(mode.image2))
        canvas.create_text(mode.width//2 + 50, mode.height//1.6, text = f'{mode.spikeCounter}x', font = "Arial 30 bold", fill="red")

        canvas.create_image(mode.width//2 - 25, mode.height//1.6 + 100, image=ImageTk.PhotoImage(mode.image4))
        canvas.create_text(mode.width//2 + 50, mode.height//1.6 + 100, text = f'{mode.boostCounter}x', font = "Arial 30 bold", fill="green")

        canvas.create_image(mode.width//2 - 25, mode.height//1.6 + 200, image=ImageTk.PhotoImage(mode.image3))
        canvas.create_text(mode.width//2 + 50, mode.height//1.6 + 200, text = f'{mode.iceCounter}x', font = "Arial 30 bold", fill="red")

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
            contentsToWrite = (mode.message + f',{mode.score}' + "\n")
            writeFile("HighScores.txt", contentsToWrite)
            mode.app.setActiveMode(mode.app.leaderboard)
        if(mode.typing == True):
            if((f"{event.key}" in string.ascii_letters) or (f"{event.key}" in string.digits)) :
                mode.message += f"{event.key}"
            if(event.key == "Delete"):
                mode.message = mode.message[:-1]
            if(event.key == "Space"):
                mode.message += f" "

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = "black")
        canvas.create_text(mode.width//2, mode.height//6, text = "High Scores", font = "Arial 40 bold", fill="white")
        canvas.create_text(mode.width//2, mode.height//3, text = f'Your score is: {mode.score}', font = "Arial 20", fill="white")
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
        scoreset = []
        for line in contentsRead.splitlines():
            name = line.split(",")[0]
            score = line.split(",")[1]
            scoreset.append([int(score), name])
        sortedset = sorted(scoreset, reverse = True)
        count = -1
        for scorelist in sortedset:
            name = scorelist[1]
            score = str(scorelist[0])
            count += 1
            if(count < 10):
                canvas.create_text(300, mode.height//3.5 + 30*count, text = name, font = "Arial 20", fill = "white")
                canvas.create_text(mode.width - 300, mode.height//3.5 + 30*count, text = score, font = "Arial 20", fill = "white")

app = BollywoodRun(width=800, height=800)

#External files used include songs - downloaded from Itunes converted to wav
#shared with TP mentor on google drive