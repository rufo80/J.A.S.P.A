import pygame
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
import os
import random


# Funzione per selezionare una cartella contenente file audio
def scegli_cartella():
    global folder_path, audio_files
    folder_path = filedialog.askdirectory(title="Scegli una cartella")
    if folder_path:
        audio_files = [f for f in os.listdir(folder_path) if f.endswith(('.mp3', '.wav', '.ogg'))]
        aggiorna_lista()

# Funzione per aggiornare la lista di file audio
def aggiorna_lista():
    listbox_files.delete(0, END)  # Pulisce la lista attuale
    for file in audio_files:
        listbox_files.insert(END, file)  # Inserisce i file audio nella listbox
        
def on_closing():
    player.stop_audio()  # Ferma l'audio prima di chiudere
    root.destroy() 

class Player():
    def __init__(self):
        self.i = 0
        self.playing = False
        self.update_thread = None
        
    # Funzione per riprodurre l'audio
    def play_audio(self):
        try:
            if audio_files:
                self.num_file = len(audio_files)
                pygame.mixer.music.load(os.path.join(folder_path, audio_files[self.i]))
                pygame.mixer.music.play()
                status_bar.config(text="Riproduzione in corso: " + audio_files[self.i])
        except Exception as e:
            messagebox.showerror("Errore nella riproduzione", f"{e}")

    # Funzione per fermare l'audio
    def stop_audio(self):
        pygame.mixer.music.stop()
        self.playing = False
        status_bar.config(text="Riproduzione fermata")

    # Funzione per mettere in pausa
    def pause_audio(self):
        pygame.mixer.music.pause()
        self.playing = False
        status_bar.config(text="Audio in pausa : " + audio_files[self.i])

    # Funzione per riprendere l'audio
    def resume_audio(self):
        pygame.mixer.music.unpause()
        self.playing = True
        status_bar.config(text="Riproduzione in corso: " + audio_files[self.i])
        
    def next_song(self):
        self.i = self.i + 1
        if self.i > self.num_file-1 :
            self.i = self.i -1
            messagebox.showinfo("Errore Playlist", "Impossibile riprodurre brano")
            return None
        else:
            pygame.mixer.music.load(os.path.join(folder_path, audio_files[self.i]))
            pygame.mixer.music.play()
            status_bar.config(text="Riproduzione in corso: " + audio_files[self.i])
        return 0
        
    def prev_song(self):
        self.i = self.i - 1
        if self.i < 0 :
            self.i = self.i +1
            messagebox.showinfo("Errore Playlist", "Impossibile riprodurre brano")
            return None
        else:
            pygame.mixer.music.load(os.path.join(folder_path, audio_files[self.i]))
            pygame.mixer.music.play()
            status_bar.config(text="Riproduzione in corso: " + audio_files[self.i])
        return 0
    
    # Funzione per aggiornare il volume
    def set_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume) / 100)  # Converte il valore da 0-100 a 0.0-1.0
        
    def casuale(self):
        print(audio_files)
        random.shuffle(audio_files)
        print(audio_files)
        self.play_audio()


# Inizializza Pygame Mixer
pygame.mixer.init()

#Oggetto player
player = Player()

root = Tk()
root.title("J.A.P.A")
root.geometry("508x410")
root.configure(bg="SALMON")
#root.iconbitmap("img/favicon/speaker.ico")
root.resizable(False, False)

root.protocol("WM_DELETE_WINDOW", on_closing)

menu = tk.Menu(root)
file_menu = tk.Menu(menu, tearoff=False)
file_menu.add_command(label="Scegli Cartella", command=scegli_cartella)
file_menu.add_separator()
file_menu.add_command(label="Random", command=player.casuale)
file_menu.add_separator()
file_menu.add_command(label="Esci", command=on_closing)
menu.add_cascade(label="File", menu=file_menu)
root.config(menu=menu)

# Variabile globale per la cartella e file audio
folder_path = ""
audio_files = []

frame_pulsanti = tk.LabelFrame(root, text="Comandi", bg="SALMON")
frame_pulsanti.pack(fill="x", expand="no", padx=10, pady=10)
# Pulsanti per il player audio
prev_button = Button(frame_pulsanti, text="<<", width=10, command=player.prev_song)
prev_button.grid(row=0, column=0)

play_button = Button(frame_pulsanti, text="Play", width=10, command=player.play_audio)
play_button.grid(row=0, column=1)

stop_button = Button(frame_pulsanti, text="Stop", width=10, command=player.stop_audio)
stop_button.grid(row=0, column=2)

pause_button = Button(frame_pulsanti, text="Pausa", width=10, command=player.pause_audio)
pause_button.grid(row=0, column=3)

resume_button = Button(frame_pulsanti, text="Riprendi", width=10, command=player.resume_audio)
resume_button.grid(row=0, column=4)

next_button = Button(frame_pulsanti, text=">>", width=10, command=player.next_song)
next_button.grid(row=0, column=5)

frame_volume = tk.LabelFrame(root, text="Volume", bg="SALMON")
frame_volume.pack(fill="x", expand="no", padx=10, pady=10)
volume_slider = Scale(frame_volume, from_=0, to=100, orient=HORIZONTAL, command=player.set_volume)
volume_slider.set(50)  # Imposta il volume iniziale al 50%
volume_slider.pack(fill="x", padx=20)

frame_lista = tk.LabelFrame(root, text="Canzoni", bg="SALMON")
frame_lista.pack(fill="x", expand="no", padx=10, pady=10)
listbox_files = tk.Listbox(frame_lista, height=10, width=70)
listbox_files.grid(row=1, column=0, columnspan=5)
scrollbar = tk.Scrollbar(frame_lista, orient=tk.VERTICAL)
scrollbar.grid(row=1, column=5, rowspan=4, sticky="NS")
scrollbar.config(command=listbox_files.yview)
listbox_files.config(yscrollcommand=scrollbar.set)

status_bar = tk.Label(root, text="", bd=2, width=200, relief="sunken", anchor='w', bg="SALMON", fg='BLUE')
status_bar.pack(fill="x", expand="no", padx=10, pady=10)

root.mainloop()
