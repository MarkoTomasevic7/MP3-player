import pygame
import tkinter as tk
from tkinter import *
import os

#---------------------------------------------- CONSTANTS -------------------------------------------
current_directory_path = r"C:\Users\Marko\Music\Converted by MediaHuman"
#path for next song in line
next_path = r""
#original item names (after shortening ones longer than 30 chars
original_item_name = ""
#storing contents of each new folder, ie. listbox screen
contents = []
#dict for storing original directory content names
original_items_dict = {}
#after item is clicked, a new playlist if formed with item paths after the clicked one
playlist = []


#----------------------------------------  HANDLING MUSIC FILES -------------------------------------------------------------

# BUDI SVJESTAN DA KAD BUDEŠ PUŠTAO PREKO RASP I NEKIH ZVUČNIKA, MOŽDA ĆEŠ MORAT PROMJENIT DEVICE NA IME TOG ZVUČNIKA!!

#initialising mixer module and its basic arguments
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024, devicename=None, allowedchanges=0)
#verifying mixer is indeed initialised
pygame.mixer.get_init()


#variables to track playback state

playing = False
paused = False

# toggle function, tracks whether music is playing, if not, uses play, if not paused, use pause, and if paused, use pause
def toggle_playlist():
    global playing,paused
    global play_pause_button

    if not playing:
        pygame.mixer.music.play()
        playing = True
        play_pause_button.config(image=pause_img)
    elif not paused:
        pygame.mixer.music.pause()
        paused = True
        play_pause_button.config(image=play_img)
    else:
        pygame.mixer.music.unpause()
        paused = False
        play_pause_button.config(image=pause_img)



def stop_music():
    global playing, paused
    global play_pause_button
    pygame.mixer.music.stop()
    play_pause_button.config(image=play_img)
    paused = False
    playing = False



def turn_off():
    pygame.mixer.music.stop()
    pygame.quit()
    window.destroy()

def navigate_to_parent_directory():
    global current_directory_path
    parent_directory = os.path.dirname(current_directory_path)
    if parent_directory != current_directory_path:  # Ensure not at root
        current_directory_path = parent_directory
        listbox.delete(0, tk.END)
        populate_listbox()


#shows list of directory content on screen
def populate_listbox():
    global current_directory_path, original_items_dict, contents

    contents = os.listdir(current_directory_path)
    print(f"Contents: {contents}")
    max_length = 30
    suffix = "..."
    for item in contents:
        full_path = os.path.join(current_directory_path, item)
        if len(item) <= max_length:
            if os.path.isdir(full_path):
                item_display = item.upper()  # Uppercase for directories
            else:
                item_display = item.lower()  # Lowercase for files
        else:

            item_display = item[:max_length] + suffix  # if item name >30 chars, shorten and add suffix

            if os.path.isdir(full_path):
                item_display = item_display.upper()  # Uppercase for directories
            else:
                item_display = item_display.lower()  # Lowercase for files
        original_items_dict[item_display] = item     # populate a dict with keys of shortened item names, and values of original item names
        listbox.insert(tk.END, item_display)


#
def item_double_clicked(event):
    global current_directory_path, is_dir,is_file, original_item_name, contents, playlist


    index = listbox.curselection()[0]                                         #get item index
    item_display = listbox.get(index)                                         #get changed item text
    original_item_name = original_items_dict[item_display]                    #find the original item name by tapping into a dict whos keys are changed item names
    selected_path = os.path.join(current_directory_path,original_item_name)   #make a directory path with original item name


    if os.path.isdir(selected_path):                                          #if folder, delete current listbox contents
                                                                              # and populate with content within it
        current_directory_path = selected_path
        listbox.delete(0, tk.END)
        populate_listbox()
    elif os.path.isfile(selected_path):                                       #if file,stop current song, unload it, load selected, create a new
                                                                              #playlist of songs that come after it, then run toggle playlist
        if playing or paused:
            stop_music()
            pygame.mixer.music.unload()
        pygame.mixer.music.load(selected_path)
        playlist = [os.path.join(current_directory_path, item) for item in contents[index + 1:]]
        print(f"New playlist: {playlist}")
        toggle_playlist()

"""
# Function to play the playlist
def play_playlist(playlist):
    for track in playlist:
        # Load the current track
        pygame.mixer.music.load(track)
        # Play the track
        pygame.mixer.music.play()
        # Wait until the track is finished
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
"""

#----------------------------------------- DISPLAYING THE MUSIC PLAYER ---------------------------------------------------



#basic window setup
window = tk.Tk()
window.geometry("400x400")
window.title("RASPBERRRRRY MP3 PLAYER")

#image paths
play_img = PhotoImage(file=r"C:\Users\Marko\Desktop\MUSIC PLAYER PROJEKT\icons\play-button.png")
pause_img = PhotoImage(file=r"C:\Users\Marko\Desktop\MUSIC PLAYER PROJEKT\icons\pause-button.png")
stop_img = PhotoImage(file=r"C:\Users\Marko\Desktop\MUSIC PLAYER PROJEKT\icons\stop-button.png")
next_img = PhotoImage(file=r"C:\Users\Marko\Desktop\MUSIC PLAYER PROJEKT\icons\next-song-button.png")
previous_img = PhotoImage(file=r"C:\Users\Marko\Desktop\MUSIC PLAYER PROJEKT\icons\previous-song-button.png")
quit_img = PhotoImage(file=r"C:\Users\Marko\Desktop\MUSIC PLAYER PROJEKT\icons\turn-off-button.png")
back_img = PhotoImage(file=r"C:\Users\Marko\Desktop\MUSIC PLAYER PROJEKT\icons\back-button.png")

#frames
frame_buttons = Frame(window)
frame_listbox = Frame(window)

#buttons
play_pause_button = Button(frame_buttons, image=play_img, command=toggle_playlist)
stop_button = Button(frame_buttons, image=stop_img, command=stop_music)
quit_button = Button(frame_buttons, image=quit_img, command=turn_off)
back_button = Button(frame_listbox,image=back_img)
"""
next_button = Button(window,image=next_img,command=next_song)
previous_button = Button(window,image=previous_img,command=previous_song)
"""

#scrollbar for scrolling the listbox
scrollbar = Scrollbar(frame_listbox, orient=VERTICAL)

#listbox for displaying files and folders
listbox = Listbox(frame_listbox, height=25,
                  yscrollcommand=scrollbar.set)



scrollbar.config(command=listbox.yview)

#positioning frames and widgets
frame_buttons.pack(side=LEFT)
frame_listbox.pack(side=RIGHT)
play_pause_button.pack(side=TOP)
stop_button.pack(side=TOP)
quit_button.pack(side=TOP)
listbox.pack(side=RIGHT)
scrollbar.pack(side=RIGHT,fill=Y)
back_button.pack(side=RIGHT)
"""
next_button.grid(row=1,column=0)
previous_button.grid(row=1,column=2)
"""



listbox.bind("<Double-Button-1>", item_double_clicked)

back_button.config(command=navigate_to_parent_directory)

populate_listbox()


window.mainloop()




