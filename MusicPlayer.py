import os
from tkinter import *
from tkinter import filedialog
from pygame import mixer
import tkinter.messagebox
from mutagen.mp3 import MP3

mixer.init() # initializing the mixer for playing songs

paused = FALSE
muted = FALSE

root = Tk()#main window

root.minsize(400, 100)
root.title("Music player")
root.iconbitmap(r'mainIcon.ico') #r -> raw string

playList = [] #contains the full path - music is played from here
selectedPathBaseName = "" #used for the Selected: songName

def loadInPlaylist(file):
    file = os.path.basename(file)
    index = 0
    songListBox.insert(index, file)
    playList.insert(index, fileName)
    index += 1


def browseFiles():
    global fileName
    fileName = filedialog.askopenfilename()
    loadInPlaylist(fileName)
    #playMusic()


def deleteSong():
    selectedSong = songListBox.curselection()
    selectedSong = int(selectedSong[0])  # index of selected song
    songListBox.delete(selectedSong)
    playList.pop(selectedSong)
    stopMusic()


def showDetails(p):
    global selectedPathBaseName
    selectedPathBaseName = os.path.basename(p)
    fileLabel["text"] = "Selected: " + selectedPathBaseName
    fileData = os.path.splitext(p)
    if fileData[1] == ".mp3":
        aud = MP3(p)
        totalLength = aud.info.length
    else:
        a = mixer.Sound(p)
        totalLength = a.get_length()

    mins, secs = divmod(totalLength, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthLabel['text'] = "Total Length " + timeformat


def playMusic():
    global paused
    if paused:
        mixer.music.unpause()
        paused = FALSE
        statusBar["text"] = "Playing"
        fileLabel["text"] = "Selected " + selectedPathBaseName
    else:
        try:
            selectedSong = songListBox.curselection()
            selectedSong = int(selectedSong[0]) #index of selected song
            play = playList[selectedSong]
            mixer.music.load(play)
            mixer.music.play()
            statusBar["text"] = "Playing"
            showDetails(play)
        except:
            tkinter.messagebox.showerror("Error", "No music file has been selected")


def stopMusic():
    mixer.music.stop()
    statusBar["text"] = "Stopped"
    fileLabel["text"] = "Music player"


def setVolume(val):
    mixer.music.set_volume(int(val)/100) #takes values from 0 to 1


def aboutUs():
    tkinter.messagebox.showinfo("About Music player", "Designed by Georgi V. Tihomirov")


def pauseMusic():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusBar["text"] = "Paused"
    fileLabel["text"] = "Music player"


def rewindMusic():
    playMusic()


def muteUnmuteMusic():
    global muted
    if muted:
        muted = FALSE
        mixer.music.set_volume(0.7)
        volumeSlider.set(70)
        muteUnmuteButton.configure(image=unmuteButtonPhoto)
        statusBar["text"] = "Playing music"
    else:
        mixer.music.set_volume(0)
        volumeSlider.set(0)
        muteUnmuteButton.configure(image=muteButtonPhoto)
        statusBar["text"] = "Muted"
        muted = TRUE


#creating menu bar
menuBar = Menu(root) #creating empty top menu bar
root.config(menu=menuBar)

subMenu = Menu(menuBar, tearoff=0) #drop down sub manu bar
menuBar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open file", command=browseFiles)
subMenu.add_command(label="Exit", command=root.destroy)
menuBar.add_cascade(label="About Us", command=aboutUs)

fileLabel = Label(root, text="Music player")
fileLabel.pack(pady=10)

listframe = Frame(root)
listframe.pack()

songListBox = Listbox(listframe)
songListBox.pack()

addButton = Button(listframe, text="+ Add", command=browseFiles)
addButton.pack(side=LEFT, pady=5)

deleteButton = Button(listframe, text="-Delete", command=deleteSong)
deleteButton.pack(side=RIGHT, pady=5)

lengthLabel = Label(root, text="Total length --:--")
lengthLabel.pack(pady=10)

#middle frame - play, pause, stop
middleFrame = Frame(root)
middleFrame.pack(padx=30, pady=10)


playButtonPhoto = PhotoImage(file="play.png")
playButton = Button(middleFrame, image=playButtonPhoto, command=playMusic)
playButton.grid(row=0, column=0, padx=10)

stopButtonPhoto = PhotoImage(file="stop.png")
stopButton = Button(middleFrame, image=stopButtonPhoto, command=stopMusic)
stopButton.grid(row=0, column=1, padx=10)

pauseButtonPhoto = PhotoImage(file="pause.png")
pauseButton = Button(middleFrame, image=pauseButtonPhoto, command=pauseMusic)
pauseButton.grid(row=0, column=2, padx=10)

#bottom frame - rewind, mute, slider
bottomFrame = Frame(root)
bottomFrame.pack(padx=10, pady=10)

rewindButtonPhoto = PhotoImage(file="rewind.png")
rewindButton = Button(bottomFrame, image=rewindButtonPhoto, command=rewindMusic)
rewindButton.grid(row=0, column=0, padx=10)

muteButtonPhoto = PhotoImage(file="mute.png")
unmuteButtonPhoto = PhotoImage(file="unmute.png")
muteUnmuteButton = Button(bottomFrame, image=unmuteButtonPhoto, command=muteUnmuteMusic)
muteUnmuteButton.grid(row=0, column=1, padx=10)

#volume silder
volumeSlider = Scale(bottomFrame, from_=0, to=100, orient=HORIZONTAL, command=setVolume)
volumeSlider.grid(row=0, column=2, padx=10)
volumeSlider.set(70)
mixer.music.set_volume(0.7)

#status bar - playing, stopped, paused
statusBar = Label(root, anchor=W)
statusBar.pack(side=BOTTOM, fill=X)

#save playlist - open playlist
#web service - download music info by choice

root.mainloop()