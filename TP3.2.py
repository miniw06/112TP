#################################################
# Term Project 3:
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

#Used to calculate pitch - https://en.wikipedia.org/wiki/Pitch_class
def convertToPitches(list1):
    beats = list1
    beatsList = []
    currBeat = 0
    for beat in beats:
        period = abs(beat - currBeat)
        timeInSeconds = period/1000
        frequency = 1/timeInSeconds
        pitch = 9 + 12*math.log2(frequency/440)
        pitch = (round(pitch, 3))
        beatsList.append(pitch)
        currBeat = beat
    return beatsList

def getNewerBeatsList(list1, list2):
    beats = list1
    pitchList = list2
    s = set(pitchList)
    elementsList = []
    for key in s:
        value = random.randint(1,3)
        elementsList.append((key, value))
    d = dict(elementsList)
    newCombinedList = []
    for index in range(len(beats)):
        collision = False
        time = beats[index]
        pitch = pitchList[index]
        value = d[pitch]
        cy = 220
        if(value == 1):
            color = 'green'
            cx = 425
        elif(value == 2):
            color = 'red'
            cx = 400
        else:
            color = 'blue'
            cx = 375
        newCombinedList.append((color, cx, cy, time, collision, index))
    return newCombinedList

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
        app.filename = ''
        app.playerScore = 0
        app.player2Score = 0
        app.home = Home()
        app.selection = Selection()
        app.chooseMode = SelectMode()
        app.help = Help()
        app.statistics = Statistics()
        app.oneStats = StatisticsOne()
        app.twoStats = StatisticsTwo()
        app.compStats = StatisticsComp()
        app.scores = HighScores()
        app.leaderboard = Leaderboard()
        app.twoPlayer = GameTwoPlayer()
        app.onePlayer = GameOnePlayer()
        app.computerPlayer = GameComputerPlayer()
        app.modeSelection = 0
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
            mode.app.filename = mode.songName
            mode.app.setActiveMode(mode.app.chooseMode)

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

class SelectMode(Mode):
    def appStarted(mode):
        mode.image3 = mode.loadImage('Select.png') #Created on: https://maketext.io
        mode.image4 = mode.loadImage('Mode.png') #Created on: https://maketext.io
        mode.image5 = mode.loadImage('varun.png') #Downloaded from: https://www.pngguru.com 
        mode.image5 = mode.scaleImage(mode.image5, 1/1.5)
        mode.image6 = mode.loadImage('fire.png') #https://cdn131.picsart.com/267730478008211.png?to=min&r=640
        mode.image1 = mode.loadImage('one.png') #Created on: https://maketext.io
        mode.image1 = mode.scaleImage(mode.image1, 1/3)
        mode.image2 = mode.loadImage('two.png') #Created on: https://maketext.io
        mode.image2 = mode.scaleImage(mode.image2, 1/3)
        mode.image7 = mode.loadImage('comp.png') #Created on: https://maketext.io
        mode.image7 = mode.scaleImage(mode.image7, 1/3)

    def mousePressed(mode, event):
        print((event.x, event.y))
        if((event.x <= 230) and (event.x >= 70) and (event.y <= 470) and (event.y >= 430)):
            mode.app.setActiveMode(mode.app.onePlayer)
            mode.app.modeSelection = 1
        elif((event.x <= 480) and (event.x >= 320) and (event.y <= 470) and (event.y >= 430)):
            mode.app.setActiveMode(mode.app.twoPlayer)
            mode.app.modeSelection = 2
        elif((event.x <= 740) and (event.x >= 560) and (event.y <= 470) and (event.y >= 430)):
            mode.app.setActiveMode(mode.app.computerPlayer)
            mode.app.modeSelection = 3

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = "black")
        canvas.create_image(mode.width//2 - 250, mode.height//1.8, image=ImageTk.PhotoImage(mode.image1))
        canvas.create_image(mode.width//2, mode.height//1.8, image=ImageTk.PhotoImage(mode.image2))
        canvas.create_image(mode.width//2 + 250, mode.height//1.8, image=ImageTk.PhotoImage(mode.image7))
        canvas.create_image(mode.width//2, mode.height//3, image=ImageTk.PhotoImage(mode.image4))
        canvas.create_image(mode.width//2, mode.height//6, image=ImageTk.PhotoImage(mode.image3))
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
        mode.image1 = mode.loadImage('fret3.jpg') #Image Source: tinyurl.com/SWadhwanTPImage1  #Imaged edited on preview
        mode.image2 = mode.scaleImage(mode.image1, 2/3)
        mode.characterImages = []
        mode.counter = 0
        mode.counter1 =  0
        mode.lineCounter = 0
        mode.beatsList = getBeatsList(mode.fileName)
        mode.pitchList = convertToPitches(getBeatsList(mode.fileName))
        mode.beats = getNewerBeatsList(mode.beatsList, mode.pitchList)
        mode.image10 = mode.loadImage('enemySprite.png') #https://www.seekpng.com/png/full/230-2302939_joining-images-to-create-sprite-sheet-donald-trump.png #Image edited on preview
        mode.characterImages1 = []
        for i in range(6):
            sprite1 = mode.image10.crop((0+100*i, 0, 100+100*i, 100))
            newSprite1= mode.scaleImage(sprite1, 1)
            mode.characterImages1.append(newSprite1)
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
        mode.image4 = mode.loadImage('spike.png') #https://scribblenauts.fandom.com/wiki/Long_Spike_Row
        mode.image4 = mode.scaleImage(mode.image4, 1/3)
        mode.image6 = mode.loadImage('icebolt.png') #https://www.wpclipart.com/weather/ice_cold/ice_bolt.png
        mode.image6 = mode.scaleImage(mode.image6, 1/15)
        mode.image7 = mode.loadImage('boost.png') #https://cascade.zendesk.com/hc/article_attachments/360014069454/Boost_Score_multiplier.png
        mode.image7 = mode.scaleImage(mode.image7, 1/6)
        mode.image8 = mode.loadImage('ice.png') #http://clipart-library.com/blue-rectangle-cliparts.html
        mode.image8 = mode.scaleImage(mode.image8, 1/6)
        mode.image9 = mode.loadImage('star2.png') #https://www.jing.fm/iclip/u2q8r5r5q8t4i1q8_yellow-star-png-yellow-star-transparent-background/
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
        mode.frozenMissed = []
        mode.allDots = []
        mode.pointsLost = 0

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
            app = BollywoodRun(width=800, height=800)
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
            if(mode.app.modeSelection == 1):
                mode.app.setActiveMode(mode.app.oneStats)
            elif(mode.app.modeSelection == 2):
                mode.app.setActiveMode(mode.app.twoStats)
            elif(mode.app.modeSelection == 3):
                mode.app.setActiveMode(mode.app.compStats)
            stopSong(mode, mode.fileName)

    def timerFired(mode):
        if mode.isGameOver or mode.waitingForPlay or mode.musicIsPaused: return
        mode.counter = (1 + mode.counter) % len(mode.characterImages)
        mode.counter1= (1 + mode.counter1) % len(mode.characterImages1)
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
            mode.subtractScore(1, 100)
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

    def getPlayerCollision(mode, player):
        left = mode.getPersonCollisionBounds(player)[0]
        right = mode.getPersonCollisionBounds(player)[1]
        top = mode.getPersonCollisionBounds(player)[2]
        bottom = mode.getPersonCollisionBounds(player)[3]
        if(player == 1):
            if(mode.position2x >= left and mode.position2x <= right and mode.position2y >= top and mode.position2y <= bottom):
                return True
            else:
                return False  
        elif(player == 2):
            if(mode.positionx >= left and mode.positionx <= right and mode.positiony >= top and mode.positiony <= bottom):
                return True
            else:
                return False  

    def getPersonCollisionBounds(mode, player):
        if(player == 1):
            left = mode.positionx - 50
            right = mode.positionx + 50
            top = mode.positiony
            bottom = mode.positiony + 50
        elif(player == 2):
            left = mode.position2x - 50
            right = mode.position2x + 50
            top = mode.position2y
            bottom = mode.position2y + 50
        return (left, right, top, bottom)

    def detectBeatCollision(mode, player, cx, cy):
        left = mode.getPersonCollisionBounds(player)[0]
        right = mode.getPersonCollisionBounds(player)[1]
        top = mode.getPersonCollisionBounds(player)[2]
        bottom = mode.getPersonCollisionBounds(player)[3]
        if(cx >= left and cx <= right and cy >= top and cy <= bottom):
            return True
        else:
            return False    

    def detectObjectCollision(mode, player, cx, cy):
        left = mode.getPersonCollisionBounds(player)[0]
        right = mode.getPersonCollisionBounds(player)[1]
        top = mode.getPersonCollisionBounds(player)[2]
        bottom = mode.getPersonCollisionBounds(player)[3]
        if(cx >= left and cx <= right and cy >= top and cy <= bottom):
            return True
        else:
            return False    

    def gameOver(mode):
        mode.isGameOver = True

    def freeze(mode, player, index):
        mode.iceSeen.append(index)
        if(player == 1):
            mode.frozen = True
        else:
            mode.frozenTwo = True

    def boost(mode, player, index):
        mode.boostsSeen.append(index)
        if(player == 1):
            mode.boostScore = True
        else:
            mode.boostScoreTwo = True

    def subtractScore(mode, player, value):
        if(player == 1):
            mode.score -= value
            mode.pointsLost += value
        elif(player == 2):
            mode.score2 -= value
            mode.pointsLost += value

    def addSeenDot(mode, index):
        mode.dotsSeen.append(index)

    def addFrozenMissedDot(mode, index):
        mode.frozenMissed.append(index)

    def addMissedDot(mode, index):
        mode.dotsMissed.append(index)

    def addAllDots(mode, index, time, color, value):
        mode.allDots.append([index, time, color, value])

    def addScore(mode, player, value):
        if(player == 1):
            if(mode.boostScore == True):
                mode.score += 2*value
            else:
                mode.score += value
        elif(player == 2):
            if(mode.boostScoreTwo == True):
                mode.score2 += 2*value
            else:
                mode.score2 += value

    def addSpike(mode, player, index):
        mode.spikesSeen.append(index)
        if(player == 1):
            mode.enemyAwake = True
        else:
            mode.enemy2Awake = True

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
        for (lx, ly, lx2, ly2) in mode.linePoints:
            ly += mode.lineScroll
            ly2 += mode.lineScroll
            lx -= mode.lineScroll//2
            lx2 += mode.lineScroll//2
            if(ly2 >= 330 and ly >= 330 and ly <= 750 and ly2 <=750):
                canvas.create_line(lx, ly, lx2, ly2, fill = "grey")
        if(mode.waitingForFirstPlay == True):
            canvas.create_text(mode.width//2, mode.height//2, text = "Press Space to Play", font = "Arial 30 bold", fill="white")

class GameTwoPlayer(Game):
    def appStarted(mode):
        super().appStarted()
        mode.counter2 = 0
        mode.characterImages2 = []
        mode.image11 = mode.loadImage('player1.png') #https://www.seekpng.com/png/full/230-2302939_joining-images-to-create-sprite-sheet-donald-trump.png
        mode.characterImages2 = [ ]
        for i in range(6):
            sprite2 = mode.image11.crop((0+100*i, 0, 100+100*i, 100))
            newSprite2 = mode.scaleImage(sprite2, 1)
            mode.characterImages2.append(newSprite2)
        mode.positionx = mode.width//2 + 200
        mode.score2 = 0
        mode.position2x = mode.width//2 - 200
        mode.position2y = mode.height*(4/5)
        mode.frozenTwo = False
        mode.jumpTwo = False
        mode.jumpTimeTwo = 0
        mode.iceTimerTwo = 0
        mode.boostScoreTwo = False
        mode.boostScoreTimerTwo = 0
        mode.enemy2Awake = False
        mode.enemy2Timer = 0
        mode.nextDots = []
        mode.nextDotIndexes = []
        mode.nextObstacles = []
        mode.nextObstacleIndexes = []
        mode.nextAll = []

    def keyPressed(mode, event):
        super().keyPressed(event)
        if(mode.frozen == False):
            if(event.key == 'Left'):
                mode.positionx -= 200
                if(mode.positionx < (mode.width//2 - 200)):
                    mode.positionx += 200
                if(mode.getPlayerCollision(1) == True):
                    mode.position2x -= 200
            elif(event.key == 'Right'):
                mode.positionx += 200
                if(mode.positionx > (mode.width//2 + 200)):
                    mode.positionx -= 200
                if(mode.getPlayerCollision(1) == True):
                    mode.position2x += 200
            elif(mode.jump == False):
                if(event.key == 'Up'):
                    mode.positiony = mode.height*(4/5) - 150
                    mode.jump = True
        if(mode.frozenTwo == False):
            if(event.key == 'a'):
                mode.position2x -= 200
                if(mode.position2x < (mode.width//2 - 200)):
                    mode.position2x += 200
                if(mode.getPlayerCollision(2) == True):
                    mode.positionx -= 200
            elif(event.key == 'd'):
                mode.position2x += 200
                if(mode.position2x > (mode.width//2 + 200)):
                    mode.position2x -= 200
                if(mode.getPlayerCollision(2) == True):
                    mode.positionx += 200
            elif(mode.jumpTwo == False):
                if(event.key == 'w'):
                    mode.position2y = mode.height*(4/5) - 150
                    mode.jumpTwo = True

    def timerFired(mode):
        super().timerFired()
        if mode.isGameOver or mode.waitingForPlay or mode.musicIsPaused: return 
        mode.counter2= (1 + mode.counter2) % len(mode.characterImages2)
        mode.app.player2Score = mode.score2
        if mode.jumpTwo == True:
            mode.jumpTimeTwo +=1
        if(mode.jumpTimeTwo == 15):
            mode.position2y = mode.height*(4/5)
            mode.jumpTwo = False
            mode.jumpTimeTwo = 0
        if(mode.enemy2Awake == True):
            mode.enemy2Timer += 1
        if(mode.enemy2Timer == 50):
            mode.enemy2Timer = 0
            mode.subtractScore(2, 100)
            mode.enemy2Awake = False
        if(mode.frozenTwo == True):
            mode.iceTimerTwo += 1
        if(mode.iceTimerTwo == 50):
            mode.iceTimerTwo = 0
            mode.frozenTwo = False
        if(mode.boostScoreTwo == True):
            mode.boostScoreTimerTwo += 1
        if(mode.boostScoreTimerTwo == 50):
            mode.boostScoreTimerTwo = 0
            mode.boostScoreTwo = False

    def placeObstacle(mode):
        if((mode.score + mode.score2) < 500):
            objects = ["boost", "ice", "spike", "boost"]
        elif((mode.score + mode.score2) > 1000):
            objects = ["boost", "ice", "spike", "ice", "spike"]
        elif((mode.score + mode.score2) > 2000):
            objects = ["ice", "spike", "ice", "spike"]
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

    def addNextDots(mode, column):
        mode.nextDots.append(column)

    def addNextDotIndexes(mode, index):
        mode.nextDotIndexes.append(index)

    def addNextObstacles(mode, column):
        mode.nextObstacles.append(column)

    def addNextObstacleIndexes(mode, index):
        mode.nextObstacleIndexes.append(index)

    def addNextAll(mode, column):
        mode.nextAll.append(column)

    def redrawAll(mode, canvas):
        super().redrawAll(canvas)
        for (color, cx, cy, time, collision, index) in mode.circleCenters:
            if(color == "red"):
                cy -= time*mode.delta 
                cy += mode.scrollY
                value = mode.detectBeatCollision(1, cx, cy)
                value2 = mode.detectBeatCollision(2, cx, cy)
                if(cy >= 620 and (index not in mode.nextDotIndexes)):
                    mode.addNextDots(2)
                    mode.addNextDotIndexes(index)
                    mode.addNextAll(["red", 2])
                if(cy >= 750 and (index not in mode.dotsSeen) and (index not in mode.dotsMissed) and mode.frozen == False):
                    mode.addMissedDot(index)
                    mode.addAllDots(index, time, "red", False)
                    mode.subtractScore(1, 20)
                    mode.subtractScore(2, 20)
                    mode.addMissed("red")    
                if(cy >= 750 and (index not in mode.dotsSeen) and (index not in mode.dotsMissed) and mode.frozen == True):
                    mode.addMissedDot(index)
                    mode.addAllDots(index, time, "red", False)
                    mode.subtractScore(1, 20)
                    mode.subtractScore(2, 20)
                    mode.addMissed("red") 
                    mode.addFrozenMissedDot(index)
                if(value == True and (index not in mode.dotsSeen)):
                    mode.addSeenDot(index)
                    mode.addAllDots(index, time, "red", True)
                    mode.addScore(1, 10)
                    mode.addCollected("red")
                    if(mode.frozen == True):
                        mode.addFrozenMissedDot(index)
                if(value2 == True and (index not in mode.dotsSeen)):
                    mode.addSeenDot(index)
                    mode.addAllDots(index, time, "red", True)
                    mode.addScore(2, 10)
                    mode.addCollected("red")
                    if(mode.frozen == True):
                        mode.addFrozenMissedDot(index)
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
                if(cy >= 620 and (index not in mode.nextDotIndexes)):
                    mode.addNextDots(1)
                    mode.addNextDotIndexes(index)
                    mode.addNextAll(["green", 1])
                value = mode.detectBeatCollision(1, cx, cy)
                value2 = mode.detectBeatCollision(2, cx, cy)
                if(cy >= 750 and (index not in mode.dotsSeen) and (index not in mode.dotsMissed) and mode.frozen == False):
                    mode.addMissedDot(index)
                    mode.addAllDots(index, time, "green", False)
                    mode.subtractScore(1, 10)
                    mode.subtractScore(2, 10)
                    mode.addMissed("green")    
                if(cy >= 750 and (index not in mode.dotsSeen) and (index not in mode.dotsMissed) and mode.frozen == True):
                    mode.addMissedDot(index)
                    mode.addAllDots(index, time, "green", False)
                    mode.subtractScore(1, 10)
                    mode.subtractScore(2, 10)
                    mode.addMissed("green")   
                    mode.addFrozenMissedDot(index)
                if(value == True and (index not in mode.dotsSeen)):
                    mode.addSeenDot(index)
                    mode.addAllDots(index, time, "green", True)
                    mode.addScore(1, 20)
                    mode.addCollected("green")
                    if(mode.frozen == True):
                        mode.addFrozenMissedDot(index)
                if(value2 == True and (index not in mode.dotsSeen)):
                    mode.addSeenDot(index)
                    mode.addAllDots(index, time, "green", True)
                    mode.addScore(2, 20)
                    mode.addCollected("green")
                    if(mode.frozen == True):
                        mode.addFrozenMissedDot(index)
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
                if(cy >= 620 and (index not in mode.nextDotIndexes)):
                    mode.addNextDots(3)
                    mode.addNextDotIndexes(index)
                    mode.addNextAll(["blue", 3])
                value = mode.detectBeatCollision(1, cx, cy)
                value2 = mode.detectBeatCollision(2, cx, cy)
                if(cy >= 750 and (index not in mode.dotsSeen) and (index not in mode.dotsMissed) and mode.frozen == False):
                    mode.addMissedDot(index)
                    mode.addAllDots(index, time, "blue", False)
                    mode.subtractScore(1, 10)
                    mode.subtractScore(2, 10)
                    mode.addMissed("blue")    
                if(cy >= 750 and (index not in mode.dotsSeen) and (index not in mode.dotsMissed) and mode.frozen == True):
                    mode.addMissedDot(index)
                    mode.addAllDots(index, time, "blue", False)
                    mode.subtractScore(1, 10)
                    mode.subtractScore(2, 10)
                    mode.addMissed("blue")   
                    mode.addFrozenMissedDot(index) 
                if(value == True and (index not in mode.dotsSeen)):
                    mode.addSeenDot(index)
                    mode.addAllDots(index, time, "blue", True)
                    mode.addScore(1, 20)
                    mode.addCollected("blue")
                    if(mode.frozen == True):
                        mode.addFrozenMissedDot(index)
                if(value2 == True and (index not in mode.dotsSeen)):
                    mode.addSeenDot(index)
                    mode.addAllDots(index, time, "blue", True)
                    mode.addScore(2, 20)
                    mode.addCollected("blue")
                    if(mode.frozen == True):
                        mode.addFrozenMissedDot(index)
                if(cy >= 310 and cy <= 750 and (index not in mode.dotsSeen) and mode.songPlaying == True):
                    mode.addPrintedDot(index)
                    canvas.create_oval(cx-mode.r, cy-mode.r, cx+mode.r, cy+mode.r, fill=color)
                if(cy >= 310 and cy <= 750 and (index not in mode.dotsSeen) and (index in mode.dotsPrinted) and mode.songPlaying == False):
                    canvas.create_oval(cx-mode.r, cy-mode.r, cx+mode.r, cy+mode.r, fill=color)
        
        for (cx, cy, name, column, index) in mode.obstacles:
            if(column == 1):
                cy += mode.obstacleScroll
                cx += mode.obstacleScroll//2
            elif(column == 3):
                cy += mode.obstacleScroll
                cx -= mode.obstacleScroll//2
            else:
                cy += mode.obstacleScroll
            value = mode.detectObjectCollision(1, cx, cy)
            value2 = mode.detectObjectCollision(2, cx, cy)
            if(cy >= 630 and (index not in mode.nextObstacleIndexes)):
                mode.addNextObstacles(column)
                mode.addNextObstacleIndexes(index)
                mode.addNextAll([name, column])
            if(name == "spike" and cy <= 750):
                if(mode.enemyAwake == True and value == True and (index not in mode.spikesSeen)):
                    mode.addSpike(1, index)
                    mode.gameOver()
                    canvas.create_image(cx, cy, image=ImageTk.PhotoImage(mode.image4))
                if(mode.enemy2Awake == True and value2 == True and (index not in mode.spikesSeen)):
                    mode.addSpike(2, index)
                    mode.gameOver()
                    canvas.create_image(cx, cy, image=ImageTk.PhotoImage(mode.image4))
                elif(value ==  True and (index not in mode.spikesSeen)):
                    mode.addSpike(1, index)
                    canvas.create_image(cx, cy, image=ImageTk.PhotoImage(mode.image4))
                elif(value2 ==  True and (index not in mode.spikesSeen)):
                    mode.addSpike(2, index)
                    canvas.create_image(cx, cy, image=ImageTk.PhotoImage(mode.image4))
                elif((index in mode.spikesSeen)):
                    pass
                else:
                    canvas.create_image(cx, cy, image=ImageTk.PhotoImage(mode.image4))
            if(name == "ice" and cy <= 750):
                if(value ==  True and (index not in mode.iceSeen)):
                    mode.freeze(1, index)
                    canvas.create_image(cx, cy, image=ImageTk.PhotoImage(mode.image6))
                if(value2 ==  True and (index not in mode.iceSeen)):
                    mode.freeze(2, index)
                    canvas.create_image(cx, cy, image=ImageTk.PhotoImage(mode.image6))
                elif((index in mode.iceSeen)):
                    pass
                else:
                    canvas.create_image(cx, cy, image=ImageTk.PhotoImage(mode.image6))
            if(name == "boost" and cy <= 750):
                if(value ==  True and (index not in mode.boostsSeen)):
                    mode.boost(1, index)
                    canvas.create_image(cx, cy, image=ImageTk.PhotoImage(mode.image7))
                if(value2 ==  True and (index not in mode.boostsSeen)):
                    mode.boost(2, index)
                    canvas.create_image(cx, cy, image=ImageTk.PhotoImage(mode.image7))
                elif((index in mode.boostsSeen)):
                    pass
                else:
                    canvas.create_image(cx, cy, image=ImageTk.PhotoImage(mode.image7))               

            if(mode.enemyAwake == True):
                y = mode.height*(4/5) + 100
                sprite1 = mode.characterImages1[mode.counter1]
                canvas.create_image(mode.positionx, y, image=ImageTk.PhotoImage(sprite1))
                canvas.create_rectangle(mode.width - 100, mode.height//2 - 250, mode.width - 70, mode.height//2 + 250, fill = "black", outline="white")
                canvas.create_rectangle(mode.width - 100, mode.height//2 - 250, mode.width - 70, (mode.height//2 - 250) + 500*mode.enemyTimer/50, fill = "white", outline = "black")

            if(mode.enemy2Awake == True):
                y = mode.height*(4/5) + 100
                sprite1 = mode.characterImages1[mode.counter1]
                canvas.create_image(mode.position2x, y, image=ImageTk.PhotoImage(sprite1))
                canvas.create_rectangle(mode.width - 100, mode.height//2 - 250, mode.width - 70, mode.height//2 + 250, fill = "black", outline="white")
                canvas.create_rectangle(mode.width - 100, mode.height//2 - 250, mode.width - 70, (mode.height//2 - 250) + 500*mode.enemy2Timer/50, fill = "white", outline = "black")

            if(mode.frozen == True):
                canvas.create_image(mode.positionx, mode.positiony, image=ImageTk.PhotoImage(mode.image8))
                canvas.create_rectangle(mode.width - 100, mode.height//2 - 250, mode.width - 70, mode.height//2 + 250, fill = "black", outline="white")
                canvas.create_rectangle(mode.width - 100, mode.height//2 - 250, mode.width - 70, (mode.height//2 - 250) + 500*mode.iceTimer/50, fill = "white", outline = "black")

            if(mode.frozenTwo == True):
                canvas.create_image(mode.position2x, mode.position2y, image=ImageTk.PhotoImage(mode.image8))
                canvas.create_rectangle(mode.width - 100, mode.height//2 - 250, mode.width - 70, mode.height//2 + 250, fill = "black", outline="white")
                canvas.create_rectangle(mode.width - 100, mode.height//2 - 250, mode.width - 70, (mode.height//2 - 250) + 500*mode.iceTimerTwo/50, fill = "white", outline = "black")

            if(mode.boostScore == True):
                canvas.create_image(mode.positionx, mode.positiony, image=ImageTk.PhotoImage(mode.image9))
                canvas.create_rectangle(mode.width - 100, mode.height//2 - 250, mode.width - 70, mode.height//2 + 250, fill = "black", outline="white")
                canvas.create_rectangle(mode.width - 100, mode.height//2 - 250, mode.width - 70, (mode.height//2 - 250) + 500*mode.boostScoreTimer/50, fill = "white", outline = "black")

            if(mode.boostScoreTwo == True):
                canvas.create_image(mode.position2x, mode.position2y, image=ImageTk.PhotoImage(mode.image9))
                canvas.create_rectangle(mode.width - 100, mode.height//2 - 250, mode.width - 70, mode.height//2 + 250, fill = "black", outline="white")
                canvas.create_rectangle(mode.width - 100, mode.height//2 - 250, mode.width - 70, (mode.height//2 - 250) + 500*mode.boostScoreTimerTwo/50, fill = "white", outline = "black")

        sprite = mode.characterImages[mode.counter]
        canvas.create_image(mode.positionx, mode.positiony, image=ImageTk.PhotoImage(sprite))
        canvas.create_text(mode.width//6, mode.height//8, text = f'Player 1 Score: {mode.score}', font = "Arial 24 bold", fill="white")

        sprite2 = mode.characterImages2[mode.counter2]
        canvas.create_image(mode.position2x, mode.position2y, image=ImageTk.PhotoImage(sprite2))
        if(mode.app.modeSelection == 3):
            canvas.create_text(mode.width//6, mode.height//8 + 100, text = f'Computer Score: {mode.score2}', font = "Arial 24 bold", fill="white")
        else:
            canvas.create_text(mode.width//6, mode.height//8 + 100, text = f'Player 2 Score: {mode.score2}', font = "Arial 24 bold", fill="white")

        if(mode.isGameOver == True):
            canvas.create_text(mode.width//2, mode.height//2, text = "Game Over", font = "Arial 30 bold", fill="white")
            canvas.create_text(mode.width//2, mode.height//2 + 100, text="Press Enter to Continue", font="Arial 20 bold", fill = "white")

class GameOnePlayer(Game):
    def appStarted(mode):
        super().appStarted()

    def keyPressed(mode, event):
        super().keyPressed(event)
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

    def placeObstacle(mode):
        if(mode.score < 0):
            objects = ["boost", "ice", "spike", "boost"]
        elif(mode.score > 500):
            objects = ["boost", "ice", "spike", "ice", "spike"]
        elif(mode.score > 1000):
            objects = ["ice", "spike", "ice", "spike"]
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

    def redrawAll(mode, canvas):
        super().redrawAll(canvas)
        for (color, cx, cy, time, collision, index) in mode.circleCenters:
            if(color == "red"):
                cy -= time*mode.delta 
                cy += mode.scrollY
                value = mode.detectBeatCollision(1, cx, cy)
                if(cy >= 750 and (index not in mode.dotsSeen) and (index not in mode.dotsMissed) and mode.frozen == False):
                    mode.addMissedDot(index)
                    mode.addAllDots(index, time, "red", False)
                    mode.subtractScore(1, 20)
                    mode.addMissed("red")    
                if(cy >= 750 and (index not in mode.dotsSeen) and (index not in mode.dotsMissed) and mode.frozen == True):
                    mode.addMissedDot(index)
                    mode.addAllDots(index, time, "red", False)
                    mode.subtractScore(1, 20)
                    mode.addMissed("red") 
                    mode.addFrozenMissedDot(index)
                if(value == True and (index not in mode.dotsSeen)):
                    mode.addSeenDot(index)
                    mode.addAllDots(index, time, "red", True)
                    mode.addScore(1, 10)
                    mode.addCollected("red")
                    if(mode.frozen == True):
                        mode.addFrozenMissedDot(index)
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
                value = mode.detectBeatCollision(1, cx, cy)
                if(cy >= 750 and (index not in mode.dotsSeen) and (index not in mode.dotsMissed) and mode.frozen == False):
                    mode.addMissedDot(index)
                    mode.addAllDots(index, time, "green", False)
                    mode.subtractScore(1, 10)
                    mode.addMissed("green")    
                if(cy >= 750 and (index not in mode.dotsSeen) and (index not in mode.dotsMissed) and mode.frozen == True):
                    mode.addMissedDot(index)
                    mode.addAllDots(index, time, "green", False)
                    mode.subtractScore(1, 10)
                    mode.addMissed("green")   
                    mode.addFrozenMissedDot(index)
                if(value == True and (index not in mode.dotsSeen)):
                    mode.addSeenDot(index)
                    mode.addAllDots(index, time, "green", True)
                    mode.addScore(1, 20)
                    mode.addCollected("green")
                    if(mode.frozen == True):
                        mode.addFrozenMissedDot(index)
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
                value = mode.detectBeatCollision(1, cx, cy)
                if(cy >= 750 and (index not in mode.dotsSeen) and (index not in mode.dotsMissed) and mode.frozen == False):
                    mode.addMissedDot(index)
                    mode.addAllDots(index, time, "blue", False)
                    mode.subtractScore(1, 10)
                    mode.addMissed("blue")    
                if(cy >= 750 and (index not in mode.dotsSeen) and (index not in mode.dotsMissed) and mode.frozen == True):
                    mode.addMissedDot(index)
                    mode.addAllDots(index, time, "blue", False)
                    mode.subtractScore(1, 10)
                    mode.addMissed("blue")   
                    mode.addFrozenMissedDot(index) 
                if(value == True and (index not in mode.dotsSeen)):
                    mode.addSeenDot(index)
                    mode.addAllDots(index, time, "blue", True)
                    mode.addScore(1, 20)
                    mode.addCollected("blue")
                    if(mode.frozen == True):
                        mode.addFrozenMissedDot(index)
                if(cy >= 310 and cy <= 750 and (index not in mode.dotsSeen) and mode.songPlaying == True):
                    mode.addPrintedDot(index)
                    canvas.create_oval(cx-mode.r, cy-mode.r, cx+mode.r, cy+mode.r, fill=color)
                if(cy >= 310 and cy <= 750 and (index not in mode.dotsSeen) and (index in mode.dotsPrinted) and mode.songPlaying == False):
                    canvas.create_oval(cx-mode.r, cy-mode.r, cx+mode.r, cy+mode.r, fill=color)
        
        for (cx, cy, name, column, index) in mode.obstacles:
            if(column == 1):
                cy += mode.obstacleScroll
                cx += mode.obstacleScroll//2
            elif(column == 3):
                cy += mode.obstacleScroll
                cx -= mode.obstacleScroll//2
            else:
                cy += mode.obstacleScroll
            value = mode.detectObjectCollision(1, cx, cy)
            if(name == "spike" and cy <= 750):
                if(mode.enemyAwake == True and value == True and (index not in mode.spikesSeen)):
                    mode.addSpike(1, index)
                    mode.gameOver()
                    canvas.create_image(cx, cy, image=ImageTk.PhotoImage(mode.image4))
                elif(value ==  True and (index not in mode.spikesSeen)):
                    mode.addSpike(1, index)
                    canvas.create_image(cx, cy, image=ImageTk.PhotoImage(mode.image4))
                elif((index in mode.spikesSeen)):
                    pass
                else:
                    canvas.create_image(cx, cy, image=ImageTk.PhotoImage(mode.image4))
            if(name == "ice" and cy <= 750):
                if(value ==  True and (index not in mode.iceSeen)):
                    mode.freeze(1, index)
                    canvas.create_image(cx, cy, image=ImageTk.PhotoImage(mode.image6))
                elif((index in mode.iceSeen)):
                    pass
                else:
                    canvas.create_image(cx, cy, image=ImageTk.PhotoImage(mode.image6))
            if(name == "boost" and cy <= 750):
                if(value ==  True and (index not in mode.boostsSeen)):
                    mode.boost(1, index)
                    canvas.create_image(cx, cy, image=ImageTk.PhotoImage(mode.image7))
                elif((index in mode.boostsSeen)):
                    pass
                else:
                    canvas.create_image(cx, cy, image=ImageTk.PhotoImage(mode.image7))               

            if(mode.enemyAwake == True):
                y = mode.height*(4/5) + 100
                sprite1 = mode.characterImages1[mode.counter1]
                canvas.create_image(mode.positionx, y, image=ImageTk.PhotoImage(sprite1))
                canvas.create_rectangle(mode.width - 100, mode.height//2 - 250, mode.width - 70, mode.height//2 + 250, fill = "black", outline="white")
                canvas.create_rectangle(mode.width - 100, mode.height//2 - 250, mode.width - 70, (mode.height//2 - 250) + 500*mode.enemyTimer/50, fill = "white", outline = "black")

            if(mode.frozen == True):
                canvas.create_image(mode.positionx, mode.positiony, image=ImageTk.PhotoImage(mode.image8))
                canvas.create_rectangle(mode.width - 100, mode.height//2 - 250, mode.width - 70, mode.height//2 + 250, fill = "black", outline="white")
                canvas.create_rectangle(mode.width - 100, mode.height//2 - 250, mode.width - 70, (mode.height//2 - 250) + 500*mode.iceTimer/50, fill = "white", outline = "black")

            if(mode.boostScore == True):
                canvas.create_image(mode.positionx, mode.positiony, image=ImageTk.PhotoImage(mode.image9))
                canvas.create_rectangle(mode.width - 100, mode.height//2 - 250, mode.width - 70, mode.height//2 + 250, fill = "black", outline="white")
                canvas.create_rectangle(mode.width - 100, mode.height//2 - 250, mode.width - 70, (mode.height//2 - 250) + 500*mode.boostScoreTimer/50, fill = "white", outline = "black")

        sprite = mode.characterImages[mode.counter]
        canvas.create_image(mode.positionx, mode.positiony, image=ImageTk.PhotoImage(sprite))
        canvas.create_text(mode.width//6, mode.height//8, text = f'Score: {mode.score}', font = "Arial 24 bold", fill="white")

        if(mode.isGameOver == True):
            canvas.create_text(mode.width//2, mode.height//2, text = "Game Over", font = "Arial 30 bold", fill="white")
            canvas.create_text(mode.width//2, mode.height//2 + 100, text="Press Enter to Continue", font="Arial 20 bold", fill = "white")

class GameComputerPlayer(GameTwoPlayer):
    def appStarted(mode):
        super().appStarted()

    def timerFired(mode):
        super().timerFired()
        mode.moveComputerAI()

    def keyPressed(mode, event):
        if(event.key == 'a'):
            return
        if(event.key == 'd'):
            return
        if(event.key == 'w'):
            return
        super().keyPressed(event)
    
#jump - -50
#jump on + 200

    def moveComputerAI(mode):
        if(mode.frozenTwo == False and mode.jumpTwo == False):
            if(mode.position2x  == mode.width//2 - 400):
                mode.position2x += 200
                if(mode.getPlayerCollision(2) == True):
                    mode.positionx += 200
            if(mode.position2x  == mode.width//2 + 400):
                mode.position2x -= 200
                if(mode.getPlayerCollision(2) == True):
                    mode.positionx -= 200
            if(len(mode.nextAll) > 0):
                nextItem = mode.nextAll[0]
                name = nextItem[0]
                column = nextItem[1]
                if(name == "green"):
                    mode.collectGreenDot()
                elif(name == "red"):
                    mode.collectRedDot()
                elif(name == "blue"):
                    mode.collectBlueDot()
                elif(name == "boost"):
                    mode.collectBoost(column)
                elif(name == "spike"):
                    mode.avoid(column)
                elif(name == "ice"):
                    mode.avoid(column)
                mode.nextAll.pop(0)

    def collectGreenDot(mode):                
        if(mode.position2x == mode.width//2):
            mode.position2x -= 200
            if(mode.getPlayerCollision(2) == True):
                mode.positionx -= 200
        elif(mode.position2x == mode.width//2 + 200):
            mode.position2x -= 200
            if(mode.getPlayerCollision(2) == True):
                mode.positionx -= 200
            mode.position2x -= 200
            if(mode.getPlayerCollision(2) == True):
                mode.positionx -= 200

    def collectRedDot(mode):
        if(mode.position2x == mode.width//2 - 200):
            mode.position2x += 200
            if(mode.getPlayerCollision(2) == True):
                mode.positionx += 200
        elif(mode.position2x == mode.width//2 + 200):
            mode.position2x -= 200
            if(mode.getPlayerCollision(2) == True):
                mode.positionx -= 200

    def collectBlueDot(mode):
        if(mode.position2x == mode.width//2):
            mode.position2x += 200
            if(mode.getPlayerCollision(2) == True):
                mode.positionx += 200
        elif(mode.position2x == mode.width//2 - 200):
            mode.position2x += 200
            if(mode.getPlayerCollision(2) == True):
                mode.positionx += 200
            mode.position2x += 200
            if(mode.getPlayerCollision(2) == True):
                mode.positionx += 200 

    def collectBoost(mode, column):
        if(column == 3):
            if(mode.position2x == mode.width//2):
                mode.position2x -= 200
                if(mode.getPlayerCollision(2) == True):
                    mode.positionx -= 200
            elif(mode.position2x == mode.width//2 + 200):
                mode.position2x -= 200
                if(mode.getPlayerCollision(2) == True):
                    mode.positionx -= 200
                mode.position2x -= 200
                if(mode.getPlayerCollision(2) == True):
                    mode.positionx -= 200
        elif(column == 2):
            if(mode.position2x == mode.width//2 - 200):
                mode.position2x += 200
                if(mode.getPlayerCollision(2) == True):
                    mode.positionx += 200
            elif(mode.position2x == mode.width//2 + 200):
                mode.position2x -= 200
                if(mode.getPlayerCollision(2) == True):
                    mode.positionx -= 200
        elif(column == 1):
            if(mode.position2x == mode.width//2):
                mode.position2x += 200
                if(mode.getPlayerCollision(2) == True):
                    mode.positionx += 200
            elif(mode.position2x == mode.width//2 - 200):
                mode.position2x += 200
                if(mode.getPlayerCollision(2) == True):
                    mode.positionx += 200
                mode.position2x += 200
                if(mode.getPlayerCollision(2) == True):
                    mode.positionx += 200

    def avoid(mode, column):
        if(column == 3):
            if(mode.position2x == mode.width//2 - 200):
                mode.jumpOver()
            elif((mode.positionx == mode.width//2) and (mode.position2x == mode.width//2 + 200)):
                mode.position2x -= 200
                if(mode.getPlayerCollision(2) == True):
                    mode.positionx -= 200
        elif(column == 2):
            if(mode.position2x == mode.width//2 - 200):
                mode.jumpOver()
        elif(column == 1):
            if(mode.position2x == mode.width//2 + 200):
                mode.jumpOver()
            elif((mode.positionx == mode.width//2) and (mode.position2x == mode.width//2 - 200)):
                mode.position2x += 200
                if(mode.getPlayerCollision(2) == True):
                    mode.positionx += 200

    def jumpOver(mode):
        mode.position2y = mode.height*(4/5) - 150
        mode.jumpTwo = True        

        
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
        canvas.create_text(mode.width//2, mode.height//2 + 50, text = "q - quit", font = "Arial 20", fill="white")
        canvas.create_text(mode.width//2, mode.height//3, text = "Collect music beats as you go and watch out for obstacles!", font = "Arial 20", fill="white")
        canvas.create_text(mode.width//2, mode.height//3 + 50, text = "Press Enter to Return to the Game", font = "Arial 20", fill="white")
        canvas.create_text(mode.width//2 - 125, mode.height//1.18, text = "Left", font = "Arial 20", fill="white")
        canvas.create_text(mode.width//2 + 135, mode.height//1.18, text = "Right", font = "Arial 20", fill="white")
        canvas.create_text(mode.width//2, mode.height//1.45, text = "Jump", font = "Arial 20", fill="white")
        canvas.create_image(mode.width//2, mode.height//1.1, image=ImageTk.PhotoImage(mode.image6))
        canvas.create_image(mode.width//2, mode.height//1.25, image=ImageTk.PhotoImage(mode.image2))

    def keyPressed(mode, event):
        if(event.key == "Enter"):
            mixer.music.unpause()
            if(mode.app.modeSelection == 1):
                mode.app.setActiveMode(mode.app.onePlayer)
            elif(mode.app.modeSelection == 2):
                mode.app.setActiveMode(mode.app.twoPlayer)
            elif(mode.app.modeSelection == 3):
                mode.app.setActiveMode(mode.app.computerPlayer)

class Statistics(Mode):
    def appStarted(mode):
        mode.image1 = mode.loadImage('fire.png') #https://cdn131.picsart.com/267730478008211.png?to=min&r=640
        mode.redDrawn = 0
        mode.greenDrawn = 0
        mode.blueDrawn = 0
        mode.spikeCounter = 0
        mode.iceCounter = 0
        mode.boostCounter = 0
        mode.image2 = mode.loadImage('spike.png') #https://scribblenauts.fandom.com/wiki/Long_Spike_Row
        mode.image2 = mode.scaleImage(mode.image2, 2/3)
        mode.image3 = mode.loadImage('icebolt.png') #https://www.wpclipart.com/weather/ice_cold/ice_bolt.png
        mode.image3 = mode.scaleImage(mode.image3, 1/15)
        mode.image4 = mode.loadImage('boost.png') #https://cascade.zendesk.com/hc/article_attachments/360014069454/Boost_Score_multiplier.png
        mode.image4 = mode.scaleImage(mode.image4, 1/6)

    def keyPressed(mode, event):
        if(event.key == "Enter"):
            mode.app.setActiveMode(mode.app.scores)

    def calculateRedPercent(mode):
        if(mode.redTotal != 0):
            redPercent = ((mode.redCollected)/(mode.redTotal) * 100)//1
        else:
            redPercent = 0
        return redPercent
    
    def calculateGreenPercent(mode):
        if(mode.greenTotal != 0):
            greenPercent = ((mode.greenCollected)/(mode.greenTotal) * 100)//1
        else:
            greenPercent = 0
        return greenPercent
    
    def calculateBluePercent(mode):
        if(mode.blueTotal != 0):
            bluePercent = ((mode.blueCollected)/(mode.blueTotal) * 100)//1
        else:
            bluePercent = 0
        return bluePercent

    def returnAverageTime(mode):
        currVal = None
        currBeat = 0
        currTime = 0
        timeDistances = []
        averageTimeDifference = 0
        for beat in mode.allDots:
            time = beat[1]
            value = beat[3]
            if(value == True):
                currVal = value
                currBeat = beat
                currTime = time
            elif(value == False):
                timeDiff = abs(time - currTime)
                timeDistances.append(timeDiff)
        for timeDifference in timeDistances:
            averageTimeDifference += timeDifference
        if(len(timeDistances) == 0):
            averageTimeDifference = 0
        else:
            averageTimeDifference = averageTimeDifference/len(timeDistances)
        return averageTimeDifference

    def returnAverageDist(mode):
        currVal = None
        currBeat = 0
        currColor = 'red'
        colorDistances = []
        averageColorDifference = 0
        for beat in mode.allDots:
            colorDist = -1
            color = beat[2]
            value = beat[3]
            if(value == True):
                currVal = value
                currBeat = beat
                currColor = color
            elif(value == False):
                if(currColor == 'red' and color == 'red'):
                    colorDist = 0
                elif(currColor == 'red' and color == 'green'):
                    colorDist = 1
                elif(currColor == 'red' and color == 'blue'):
                    colorDist = 1
                elif(currColor == 'green' and color == 'red'):
                    colorDist = 1
                elif(currColor == 'green' and color == 'green'):
                    colorDist = 0
                elif(currColor == 'green' and color == 'blue'):
                    colorDist = 2
                if(currColor == 'blue' and color == 'red'):
                    colorDist = 1
                elif(currColor == 'blue' and color == 'green'):
                    colorDist = 2
                elif(currColor == 'blue' and color == 'blue'):
                    colorDist = 0
            if(colorDist >= 0):
                colorDistances.append(colorDist)
        for colorDifference in colorDistances:
            averageColorDifference += (colorDifference*200)
        if(len(colorDistances) == 0):
            averageColorDifference = 0
        else:
            averageColorDifference = averageColorDifference/len(colorDistances)
        return averageColorDifference

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

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = "black")
        canvas.create_text(mode.width//2, mode.height//6, text = "Statistics", font = "Arial 40 bold", fill="white")
        canvas.create_text(mode.width//2, mode.height//2 - 145, text = "Total Beats Collected", font = "Arial 20", fill="white")

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

        canvas.create_image(mode.width//2 - 250, mode.height//1.6, image=ImageTk.PhotoImage(mode.image2))
        canvas.create_text(mode.width//2 - 150, mode.height//1.6, text = f'{mode.spikeCounter}x', font = "Arial 30 bold", fill="red")

        canvas.create_image(mode.width//2 - 250, mode.height//1.6 + 100, image=ImageTk.PhotoImage(mode.image4))
        canvas.create_text(mode.width//2 - 150, mode.height//1.6 + 100, text = f'{mode.boostCounter}x', font = "Arial 30 bold", fill="green")

        canvas.create_image(mode.width//2 - 250, mode.height//1.6 + 200, image=ImageTk.PhotoImage(mode.image3))
        canvas.create_text(mode.width//2 - 150, mode.height//1.6 + 200, text = f'{mode.iceCounter}x', font = "Arial 30 bold", fill="red")

        canvas.create_text(mode.width//2 + 200, mode.height//1.6, text = f'Total Points Lost: {mode.pointsLost}', font = "Arial 16", fill="white")

        canvas.create_text(mode.width//2 + 200, mode.height//1.6 + 100, text = f'Average Time Between Beats Missed: {mode.averageTimeDifference}', font = "Arial 16", fill="white")

        canvas.create_text(mode.width//2 + 200, mode.height//1.6 + 200, text = f'Average Distance Between Beats Missed: {mode.averageColorDifference}', font = "Arial 16", fill="white")

class StatisticsOne(Statistics):
    def appStarted(mode):
        super().appStarted()
        mode.score = mode.app.playerScore
        mode.redCollected = mode.app.onePlayer.collectedRed
        mode.greenCollected = mode.app.onePlayer.collectedGreen
        mode.blueCollected = mode.app.onePlayer.collectedBlue
        mode.redMissed = mode.app.onePlayer.missedRedCount
        mode.blueMissed = mode.app.onePlayer.missedBlueCount
        mode.greenMissed = mode.app.onePlayer.missedGreenCount
        mode.redTotal = (mode.redCollected + mode.redMissed)
        mode.greenTotal = (mode.greenCollected + mode.greenMissed)
        mode.blueTotal = (mode.blueCollected + mode.blueMissed)
        mode.redPercent = mode.calculateRedPercent()
        mode.greenPercent = mode.calculateGreenPercent()
        mode.bluePercent = mode.calculateBluePercent()
        mode.spikeCount = len(mode.app.onePlayer.spikesSeen)    
        mode.iceCount = len(mode.app.onePlayer.iceSeen)
        mode.boostCount = len(mode.app.onePlayer.boostsSeen)
        mode.allDots = mode.app.onePlayer.allDots
        mode.averageTimeDifference = round(mode.returnAverageTime(), 4)
        mode.averageColorDifference = round(mode.returnAverageDist(), 4)
        mode.pointsLost = mode.app.onePlayer.pointsLost

    def redrawAll(mode, canvas):
        super().redrawAll(canvas)
        canvas.create_text(mode.width//2, mode.height//4, text = f'Your score is: {mode.score}', font = "Arial 20", fill="white")

class StatisticsTwo(Statistics):
    def appStarted(mode):
        super().appStarted()
        mode.score = mode.app.playerScore
        mode.score2 = mode.app.player2Score
        mode.redCollected = mode.app.twoPlayer.collectedRed
        mode.greenCollected = mode.app.twoPlayer.collectedGreen
        mode.blueCollected = mode.app.twoPlayer.collectedBlue
        mode.redMissed = mode.app.twoPlayer.missedRedCount
        mode.blueMissed = mode.app.twoPlayer.missedBlueCount
        mode.greenMissed = mode.app.twoPlayer.missedGreenCount
        mode.redTotal = (mode.redCollected + mode.redMissed)
        mode.greenTotal = (mode.greenCollected + mode.greenMissed)
        mode.blueTotal = (mode.blueCollected + mode.blueMissed)
        mode.redPercent = mode.calculateRedPercent()
        mode.greenPercent = mode.calculateGreenPercent()
        mode.bluePercent = mode.calculateBluePercent()
        mode.spikeCount = len(mode.app.twoPlayer.spikesSeen)    
        mode.iceCount = len(mode.app.twoPlayer.iceSeen)
        mode.boostCount = len(mode.app.twoPlayer.boostsSeen)
        mode.allDots = mode.app.twoPlayer.allDots
        mode.averageTimeDifference = round(mode.returnAverageTime(), 4)
        mode.averageColorDifference = round(mode.returnAverageDist(), 2)
        mode.pointsLost = mode.app.twoPlayer.pointsLost

    def redrawAll(mode, canvas):
        super().redrawAll(canvas)
        canvas.create_text(mode.width//2, mode.height//4, text = f'Your scores are: {mode.score}, {mode.score2}', font = "Arial 20", fill="white")

class StatisticsComp(Statistics):
    def appStarted(mode):
        super().appStarted()
        mode.score = mode.app.playerScore
        mode.score2 = mode.app.player2Score
        mode.redCollected = mode.app.computerPlayer.collectedRed
        mode.greenCollected = mode.app.computerPlayer.collectedGreen
        mode.blueCollected = mode.app.computerPlayer.collectedBlue
        mode.redMissed = mode.app.computerPlayer.missedRedCount
        mode.blueMissed = mode.app.computerPlayer.missedBlueCount
        mode.greenMissed = mode.app.computerPlayer.missedGreenCount
        mode.redTotal = (mode.redCollected + mode.redMissed)
        mode.greenTotal = (mode.greenCollected + mode.greenMissed)
        mode.blueTotal = (mode.blueCollected + mode.blueMissed)
        mode.redPercent = mode.calculateRedPercent()
        mode.greenPercent = mode.calculateGreenPercent()
        mode.bluePercent = mode.calculateBluePercent()
        mode.spikeCount = len(mode.app.computerPlayer.spikesSeen)    
        mode.iceCount = len(mode.app.computerPlayer.iceSeen)
        mode.boostCount = len(mode.app.computerPlayer.boostsSeen)
        mode.allDots = mode.app.computerPlayer.allDots
        mode.averageTimeDifference = round(mode.returnAverageTime(), 4)
        mode.averageColorDifference = round(mode.returnAverageDist(), 2)
        mode.pointsLost = mode.app.computerPlayer.pointsLost

    def redrawAll(mode, canvas):
        super().redrawAll(canvas)
        canvas.create_text(mode.width//2, mode.height//4, text = f'Your scores is: {mode.score}', font = "Arial 20", fill="white")


class HighScores(Mode):
    def appStarted(mode):
        mode.message = ''
        mode.typing = False
        mode.image1 = mode.loadImage('Salman.png') #Downloaded from: https://www.uihere.com
        mode.image1 = mode.scaleImage(mode.image1, 1/2)
        mode.image6 = mode.loadImage('fire.png') #https://cdn131.picsart.com/267730478008211.png?to=min&r=640
        mode.score = mode.app.playerScore
        mode.score2 = mode.app.player2Score
        mode.highestScore = mode.returnHighScore()

    def returnHighScore(mode):
        if(mode.score > mode.score2):
            mode.highestScore = 1
        else:
            mode.highestScore = 2
        return mode.highestScore

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
        canvas.create_text(mode.width//2, mode.height//3 + 50, text = "Press Enter to Continue", font = "Arial 20", fill = "white")
        canvas.create_rectangle(100, mode.height//2 - 25, mode.width - 100, mode.height//2 + 25, fill = "white")
        canvas.create_text(mode.width//2, mode.height//2, text = mode.message, font = "Arial 20")
        canvas.create_image(mode.width//2, mode.height//1.2, image=ImageTk.PhotoImage(mode.image6))
        canvas.create_image(mode.width//2, mode.height//1.2, image=ImageTk.PhotoImage(mode.image1))
        if(mode.app.modeSelection == 2):
            if(mode.highestScore == 2):
                canvas.create_text(mode.width//2, mode.height//3, text = f'Player 2 Wins! Score is: {mode.score2}', font = "Arial 20", fill="white")
                canvas.create_text(mode.width//2, mode.height//3 + 25, text = "Click Inside the Textbox to Input Player 2 Name", font = "Arial 20", fill="white")

            else:
                canvas.create_text(mode.width//2, mode.height//3, text = f'Player 1 Wins! Score is: {mode.score}', font = "Arial 20", fill="white")
                canvas.create_text(mode.width//2, mode.height//3 + 25, text = "Click Inside the Textbox to Input Player 1 Name", font = "Arial 20", fill="white")

        else:
            canvas.create_text(mode.width//2, mode.height//3, text = f'Your score is: {mode.score}', font = "Arial 20", fill="white")
            canvas.create_text(mode.width//2, mode.height//3 + 25, text = "Click Inside the Textbox to Input your Name", font = "Arial 20", fill="white")



class Leaderboard(Mode):
    def appStarted(mode):
        mode.image1 = mode.loadImage('Amitabh.png') #Downloaded from: https://www.uihere.com
        mode.image6 = mode.loadImage('fire.png') #https://cdn131.picsart.com/267730478008211.png?to=min&r=640
    
    def keyPressed(mode, event):
        if((event.key == "q") or (event.key == "Enter")):
            mode.app.setActiveMode(mode.app.home)
            app = BollywoodRun(width=800, height=800)

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