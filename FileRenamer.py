import re, os
import ctypes
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar, Combobox

from tkinter import ttk

#Global variables used in the 'undo' function
global SaveMeIgoofed
global ThisWasAmistake


#The Function that actually renames all the files... aka 'the nuts and bolts of the program'
def FileRenamer():

    global ThisWasAmistake, SaveMeIgoofed
    
    #Episode Sandwitch
    ep = "~"

    try:
        
        #The naming pattern in Richens' computer
        BasePattern = OriginalNamingConvention.get("1.0", "end-1c")


        #The  file extension
        FileType =  FileExtension.get("1.0","end-1c")

        #The new  naming  convention
        NewPattern =  NewNamingConvention.get("1.0", "end-1c")
        
        #The file path  to the episodes
        FilePath = File_Path.get("1.0",'end-1c')
        path = rf"{FilePath}"

        #Check that user actually input a name for each one
        
        if len(FilePath) < 1 and len(BasePattern) < 1 and len(FileType) <  1 and len(NewPattern) < 1:
            EasterEgg()
        
        if len(FilePath) < 1:
            FilePath = "No file path was entered"
        
        if len(BasePattern) < 1:
            BasePattern = "No name was Input"

        if len(FileType) < 1:
            FileType = "No file type was Input"
            
        if len(NewPattern) < 1:
            NewPattern = "No name was input"

        #Grab the parametres to undo everything if this is a goof
        SaveMeIgoofed = BasePattern
        ThisWasAmistake = NewPattern


        #Grab all files in the directory
        fileItems = os.listdir(path)

        #Same as above, but it's been arranged
        fileItems  = sorted(fileItems)

        #Get the episode numbers
        FindOldEpisodeNumber = re.findall(f"{ep}[0-9]*{ep}", BasePattern)
        OldEpisode = int(FindOldEpisodeNumber[0].replace(f"{ep}",""))
        FindNewEpisodeNumber = re.findall(f"{ep}[0-9]*{ep}", NewPattern)
        NewEpisode = int(FindNewEpisodeNumber[0].replace(f"{ep}",""))

        
        #Check if there's going to be a possible name double-up
        #Remove the numbers from each naming type 
        CheckBase = BasePattern.replace(f"{FindOldEpisodeNumber[0]}", "")
        CheckNew = NewPattern.replace(f"{FindNewEpisodeNumber[0]}","")

        #If the names are the same, add a  period '.' to the NewPattern, just to ensure there are no double-ups of names
        if CheckBase == CheckNew:
            NewPattern = f"{NewPattern}."

        #I've  found files don't automatically arrange perfectly, so it can take a few iterations
        counter = 0  #counter is used to trigger 'file not found' error
        for i in range (10):

            #Let's do this!
            for episode in fileItems:

                #Create a version of the basepattern without the signpost, (this is what it'd look like in the files)
                temporaryPattern = BasePattern.replace(f"{ep}", "")
         
                #If we are looking at an episode that  matches the counter (starting from 1) then that's what we want to rename
                if temporaryPattern in episode:
                    counter += 1

                    #The full path to this episode
                    fullPath = os.path.join(path, episode)

                    #Create the new episode new
                    newName = NewPattern.replace(f"{ep}", "")
                    newName = f"{newName}{FileType}"

                    #The full new name (including file path)
                    new_name = os.path.join(path, newName)

                    #Rename the file
                    os.rename(fullPath, new_name)

                    #Add to counter so we can look for the next episode
                    ReplaceOldEpisode = OldEpisode
                    ReplaceNewEpisode = NewEpisode

                    OldEpisode += 1
                    NewEpisode += 1

                    #update the  number in BasePattern
                    BasePattern =  BasePattern.replace(f"{ep}{ReplaceOldEpisode}{ep}", f"{ep}{OldEpisode}{ep}")
                    NewPattern = NewPattern.replace(f"{ep}{ReplaceNewEpisode}{ep}", f"{ep}{NewEpisode}{ep}")

                    
                    
        if counter == 0:
            ErrorPopup(f"Could not find the name: {BasePattern}")
    #except FileNotFoundError:
#        ErrorPopup(f"Could not find: {FilePath}")
    except IndexError:
        ErrorPopup("I'm not psychic,, but it seems your episode number cant be found or wasn't input in either section.")
    except NameError:
        ErrorPopup("Something went wrong, consult the programing gods to figure out what.")

def Undo():


    #Grab the saving grace
    global ThisWasAmistake, SaveMeIgoofed
        
    
    #Episode Sandwich, this is the symbol to surround the episode number
    ep = "~"

    try:
        #The naming pattern in Richens' computer
        BasePattern = ThisWasAmistake

        #The  file extension
        FileType =  FileExtension.get("1.0","end-1c")

        #The new  naming  convention
        NewPattern =  SaveMeIgoofed
        
        #The file path  to the episodes
        FilePath = File_Path.get("1.0",'end-1c')
        path = rf"{FilePath}"

        #Check that user didn't ignore previous error messages...
        if len(FilePath) < 1:
            FilePath = "No file path was entered"
        
        if len(BasePattern) < 1:
            BasePattern = "No name was Input"

        if len(FileType) < 1:
            FileType = "No file type was Input"
            
        if len(NewPattern) < 1:
            NewPattern = "No name was input"


        #Grab all files in the directory
        fileItems = os.listdir(path)

        #Same as above, but it's been arranged
        fileItems  = sorted(fileItems)

        #Get the episode numbers
        FindOldEpisodeNumber = re.findall(f"{ep}[0-9]*{ep}", BasePattern)
        OldEpisode = int(FindOldEpisodeNumber[0][1])
        FindNewEpisodeNumber = re.findall(f"{ep}[0-9]*{ep}", NewPattern)
        NewEpisode = int(FindNewEpisodeNumber[0][1])

        #I've  found files don't automatically arrange perfectly, so it can take a few iterations
        for i in range (10):

            #Let's do this!
            for episode in fileItems:

                #Create a version of the basepattern without the signpost, (this is what it'd look like in the files)
                temporaryPattern = BasePattern.replace(f"{ep}", "")
         
                #If we are looking at an episode that  matches the counter (starting from 1) then that's what we want to rename
                if temporaryPattern in episode:

                    #The full path to this episode
                    fullPath = os.path.join(path, episode)

                    #Create the new episode new
                    newName = NewPattern.replace(f"{ep}", "")
                    newName = f"{newName}{FileType}"

                    #The full new name (including file path)
                    new_name = os.path.join(path, newName)

                    #Rename the file
                    os.rename(fullPath, new_name)

                    #Add to counter so we can look for the next episode
                    ReplaceOldEpisode = OldEpisode
                    ReplaceNewEpisode = NewEpisode

                    OldEpisode += 1
                    NewEpisode += 1

                    #update the  number in BasePattern
                    BasePattern =  BasePattern.replace(f"{ep}{ReplaceOldEpisode}{ep}", f"{ep}{OldEpisode}{ep}")
                    NewPattern = NewPattern.replace(f"{ep}{ReplaceNewEpisode}{ep}", f"{ep}{NewEpisode}{ep}")

    except NameError:
        ErrorPopup("\nDon't press undo when you have nothing to undo, shtuped.\n\n (Or ignore other error messages)")
    except FileNotFoundError:
        ErrorPopup(f"Could not find: {FilePath}")
    except IndexError:
        ErrorPopup("I'm not psychic,, but it seems your episode number cant be found or wasn't input in either section.")


def Help():
    HelpWindow = Tk()
    HelpWindow.title("Help")

    #SetUp the Style of the window
    style = ttk.Style()
    style.theme_use('clam')
    bg_color = 'white'

    instructions = """Instructions
File Path: Enter the file path to the folder that contains your files \n
e.g. /User/Richens/StupidFolder/NarutoIsGay \n
\n
Old Naming Style: Enter the current name style that you want to change, start with the first episode \n
Surround the episode number with a tilde on either side e.g. ~1~\n
e.g. 'Naruto 720p episode  ~1~ \n
or if you were starting  the rename at epsidoe 100 you would enter Naruto 720p episode ~100~\n
\n
New Naming Style\n
Enter the new naming style you want, for the episode number start with the first episode that will be changed.\n
Surround the episode number with a tilde on either side e.g. ~1~\n
e.g. Naruto Episode ~1~ OR Naruto Episode ~100~\n
\n
File Extension\n
This is the file type e.g. .mp4 OR .docx This is mandatory,it ensures your files immediately work\n
NOTES\n
-If you goof up, you can tap 'undo' 
-This program will run until there are no new files e.g. if there are  500  episodees,it will run until episode 500\n
-I am using the term 'episode' but this  can work  for ANY file type\n
-If you  don't surround the episode number with a tilde, it just won't work
-If the Episodee names are the same, the program willl add a period '.' to the end to avoid double ups e.g.\n
      Episod~4~ > Episode~1~ : without the numbers both episodes have  the same naming  style\n
      if this isn't done, files get deleted."""

    HelpInstructions = Label(HelpWindow, text = instructions, font = ('Arial', 14), fg = 'Black', bg = bg_color)
    HelpInstructions.grid(row = 2, column = 1)

def ErrorPopup(errormessage):
    ErrorWindow = Tk()
    ErrorWindow.title("An Error has been encountered")

    
    ErrorLabel = Label(ErrorWindow, text = errormessage, font = ('Arial', 16, 'bold'), fg = 'Black', bg = bg_color)
    ErrorLabel.grid(row = 1, column = 1)

def EasterEgg():
    EasterEgg = Tk()
    EasterEgg.title("Congratulations!!")
    EasterEggText = """You Pressed 'Start' after removing all sample text and DIDN'T input a SINGLE thing\n
NOT A SINGLE THING\n
You are special, numpty\n
\n\n\n\n\n\n And this message is your gift for being so special."""

    
    ErrorLabel = Label(EasterEgg, text = EasterEggText, font = ('Arial', 32, 'bold'), fg = 'Blue', bg = bg_color)
    ErrorLabel.grid(row = 1, column = 1)

##Front End stuff##

#Set up the UI window
fileRenamerWindow = Tk()
fileRenamerWindow.title("Episode Re-Namer")

#Set up any frames
MainFrame = Frame(fileRenamerWindow)
PictureFrame = Frame(fileRenamerWindow)
ButtonFrame =  Frame(fileRenamerWindow)

#SetUp the Style of the window
style = ttk.Style()
style.theme_use('clam')
bg_color = 'WhiteSmoke'
fileRenamerWindow.configure(bg = bg_color)
MainFrame.configure(bg = bg_color)
ButtonFrame.configure(bg = bg_color)

#Bind the 'enter' button to the 'Start' button
fileRenamerWindow.bind('<Return>', FileRenamer)


#The File Path the user will input
FilePathTitle = Label(MainFrame, text = "File Path", font =  ('Arial', 12, 'bold'), fg = 'Black', bg = bg_color)
File_Path = ScrolledText(MainFrame, width = 26,  height = 1,
                        font = ('Arial', 18), bg = 'white', fg = 'Black')

#Original file naming convention
OriginalNameTitle = Label(MainFrame, text = "Old Naming Style", font = ('Arial', 12, 'bold'), fg = 'Black', bg = bg_color)
OriginalNamingConvention = ScrolledText(MainFrame, width = 26,  height = 1,
                        font = ('Arial', 18), bg = 'white', fg = 'Black')

#New Naming Convention
NewNameTitle = Label(MainFrame, text = "New  Naming Style", font = ('Arial', 12, 'bold'), fg = 'Black', bg = bg_color)
NewNamingConvention = ScrolledText(MainFrame, width = 26,  height = 1,
                        font = ('Arial', 18), bg = 'white', fg = 'Black')
#File Extension type
FileExtensionTitle = Label(MainFrame, text = "File Type", font  = ('Arial', 12, 'bold'), fg = 'Black', bg = bg_color)
FileExtension =  ScrolledText(MainFrame, width =5,  height = 1,
                        font = ('Arial', 18), bg = 'white', fg = 'Black')

#Button used to engage  the  program
StartButton = Button(ButtonFrame, text = "Start", command = FileRenamer, 
                        activeforeground = 'Blue', fg = 'black', pady = 3,
                      font = ('Arial', 12), bg = bg_color, borderwidth = 0)

#Help Button to display instructions
HelpButton = Button(ButtonFrame, text = "Help", command = Help,
                    activeforeground = 'Blue', fg = 'black', pady = 3,
                      font = ('Arial', 12), bg = bg_color, borderwidth = 0)

#Undo button if yo done goofed
UndoButton = Button(ButtonFrame, text = "Undo", command = Undo,
                    activeforeground = 'Blue', fg = 'black', pady = 3,
                      font = ('Arial', 12), bg = bg_color, borderwidth = 0)

#Logo: Importing the logo and placing in the logo frame
try:
    logo_image_file = PhotoImage(file = 'logo.png')

    logo_image = Label(PictureFrame, image = logo_image_file, bg = bg_color)

    logo_image.grid(row = 1, column = 2)

except TclError:
    ErrorPopup("The Logo image could not be found.\n This program will still function as normal.\n\n(Just won't be 'peeerrty' UwU)")
    


  


#Positioning Everything in the window

#MainFrame
MainFrame.grid(row = 1, column = 1)

FilePathTitle.grid(row = 1, column = 1)
File_Path.grid(row = 2, column = 1)

OriginalNameTitle.grid(row = 3, column  = 1)
OriginalNamingConvention.grid(row  = 4, column = 1)

NewNameTitle.grid(row = 5, column = 1)
NewNamingConvention.grid(row = 6, column = 1)

FileExtensionTitle.grid(row = 5, column = 2)
FileExtension.grid(row = 6, column = 2)

#Button Frame
ButtonFrame.grid(row = 2, column = 1, sticky = W)
StartButton.grid(row = 1, column = 1, sticky = W)
UndoButton.grid(row = 1, column = 2, sticky = W)
HelpButton.grid(row = 1, column = 3, sticky = W)


#Picture Frame
PictureFrame.grid(row = 1, column = 2)


#Example texts
File_Path.insert("1.0", "/put/filepath/here/like/this")
OriginalNamingConvention.insert("1.0", "Example Show Episode ~1~")
NewNamingConvention.insert("1.0", "Example~1~Episode")
FileExtension.insert("1.0", ".eg")

# Start the event loop to detect user inputs
try:
    fileRenamerWindow.mainloop()

#Print message if user presses CTRL+C
except KeyboardInterrupt:
    print('Goodbye! Episode Renamer will continue to run until closed')
