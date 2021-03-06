import os 
import tkinter as tk 
from tkinter import filedialog
from pygame import mixer
from PIL import ImageTk, Image


class Player(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()
        self.playist = ['Please load a song']

        # Init pygame mixer and status of playing song
        mixer.init()
        self.current = 0
        self.paused = True
        self.played = False

        # Init 3 frame for GUI
        self.create_frame()
        self.track_widgets()
        self.control_widgets()
        self.tracklist_widgets()

    def create_frame(self):
        self.track = tk.LabelFrame(self, text="Playing song", bg="#dae2f7", fg="black", bd=5, relief=tk.GROOVE)
        self.track.configure(width=410, height=300)
        self.track.grid(row=0, column=0)
        
        self.tracklist = tk.LabelFrame(self, text=f'Playing list {str(len(self.playist))}', bg="#dae2f7", fg="black", bd=5, relief=tk.GROOVE)
        self.tracklist.configure(width=190, height=410)
        self.tracklist.grid(row=0, column=1, rowspan=3)

        self.controls = tk.LabelFrame(self, bg="#dae2f7", fg="black", bd=2, relief=tk.GROOVE)
        self.controls.configure(width=450, height=80)
        self.controls.grid(row=2, column=0)

    def track_widgets(self):
        self.canvas = tk.Label(self.track, image=main_logo)
        self.canvas.configure(width=400, height=240)
        self.canvas.grid(row=0, column=0)

        self.song_track = tk.Label(self.track, bg="#3365e8", fg="black")
        self.song_track['text'] = "Music player MP3"
        self.song_track.configure(width=30, height=1)
        self.song_track.grid(row=1, column=0)
        
    def control_widgets(self):
        self.loadSongs = tk.Button(self.controls, bg='#dae2f7', relief=tk.GROOVE, activebackground='#dae2f7')
        self.loadSongs['text'] = "Load Songs"
        # self.loadSongs.configure(width=15, height=1)
        self.loadSongs.grid(row=0, column=0, padx=5)
        self.loadSongs['command'] = self.retrieve_songs

        self.prev = tk.Button(self.controls, image=prev_btn, bg='#dae2f7', relief=tk.GROOVE, activebackground='#dae2f7')
        self.prev.grid(row=0, column=1, padx=5, pady=5)
        self.prev['command'] = self.prev_song

        self.pause = tk.Button(self.controls, image=pause_btn, bg='#dae2f7', relief=tk.GROOVE, activebackground='#dae2f7')
        self.pause.grid(row=0, column=2, padx=5, pady=5)
        self.pause['command'] = self.pause_song

        self.next = tk.Button(self.controls, image=next_btn, bg='#dae2f7', relief=tk.GROOVE, activebackground='#dae2f7')
        self.next.grid(row=0, column=3, padx=5, pady=5)
        self.next['command'] = self.next_song

        self.volume = tk.DoubleVar()
        self.slider = tk.Scale(self.controls, from_=0, to=10, orient=tk.HORIZONTAL, bg='#dae2f7')
        self.slider.configure(width=10)
        self.slider['variable'] = self.volume
        self.slider['command'] = self.change_volumn
        self.slider.set(5)
        mixer.music.set_volume(0.5)
        self.slider.grid(row=0, column=4, padx=5, pady=5)

    def tracklist_widgets(self):
        self.scrollbar = tk.Scrollbar(self.tracklist, orient=tk.VERTICAL)
        self.scrollbar.grid(row=0, column=1, rowspan=5, sticky='ns')

        self.list = tk.Listbox(self.tracklist, selectmode=tk.SINGLE, bg='#dae2f7', yscrollcommand=self.scrollbar.set, fg='black', selectbackground='#dae2f7')
        self.list.config(height=22)
        self.list.bind('<Double-1>', self.play_song)
        self.enumerate_song()
        self.scrollbar.config(command=self.list.yview)
        self.list.grid(row=0, column=0, rowspan=5)

    def enumerate_song(self):
        for index, song in enumerate(self.playist):
            self.list.insert(index, os.path.basename(song)) 

    def retrieve_songs(self):
        self.song_list = []
        directory = filedialog.askdirectory()
        for root_, _, files in os.walk(directory):
            for file in files:
                if os.path.splitext(file)[1] == '.mp3':
                    path = (root_ + '/' + file).replace('\\', '/')
                    print(path)
                    self.song_list.append(path)
        
        self.playist = self.song_list
        self.tracklist['text'] = f'Playist - {str(len(self.playist))}'
        self.list.delete(0, tk.END)
        self.enumerate_song()
    
    def play_song(self, event=None):
        if event is not None:
            self.current = self.list.curselection()[0]
            for i in range(len(self.playist)):
                if i != self.current:
                    self.list.itemconfigure(i, fg='black')
            self.list.itemconfigure(self.current, fg='#14e33e') 

        mixer.music.load(self.playist[self.current])
        self.paused = False
        self.played = True
        self.pause['image'] = pause_btn
        self.song_track['anchor'] = 'w'
        self.song_track['text'] = os.path.basename(self.playist[self.current])
        mixer.music.play()

    def pause_song(self):
        if not self.paused:
            self.paused = True
            self.pause['image'] = play_btn
            mixer.music.pause()
        else:
            self.paused = False
            self.pause['image'] = pause_btn
            mixer.music.unpause()

    def prev_song(self):
        if self.current > 0:
            self.current -= 1
        else:
            self.current = 0
        for i in range(len(self.playist)):
            if i != self.current:
                self.list.itemconfigure(i, fg='black')
        self.list.itemconfigure(self.current, fg='#14e33e') 
        self.play_song()

    def next_song(self):
        if self.current < len(self.playist) - 1:
            self.current += 1
        else:
            self.current = len(self.playist) - 1
        for i in range(len(self.playist)):
            if i != self.current:
                self.list.itemconfigure(i, fg='black')
        self.list.itemconfigure(self.current, fg='#14e33e')  
        self.play_song()

    def change_volumn(self, event=None):
        self.v = self.volume.get()
        mixer.music.set_volume(self.v / 10)

root = tk.Tk()
root.geometry('640x410')
root.wm_title('Music player app')
root.configure(bg='#dae2f7')
# Define image sources:
main_logo = ImageTk.PhotoImage(Image.open("images/main_logo.jpg").resize((390, 230), Image.ANTIALIAS))
next_btn = ImageTk.PhotoImage(Image.open("images/next_btn.png").resize((25, 25), Image.ANTIALIAS))
pause_btn = ImageTk.PhotoImage(Image.open("images/pause_btn.png").resize((25, 25), Image.ANTIALIAS))
prev_btn = ImageTk.PhotoImage(Image.open("images/back_btn.png").resize((25, 25), Image.ANTIALIAS))
play_btn = ImageTk.PhotoImage(Image.open("images/play_btn.png").resize((27, 27), Image.ANTIALIAS))

app = Player(master=root)

app.mainloop()
