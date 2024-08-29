import tkinter as tk
from tkinter import PhotoImage, messagebox
import pandas as pd
import random
import pickle

# Load the dataset
data = pd.read_csv('dataset.csv')

# Load the cosine similarity matrix
with open('model.pkl', 'rb') as f:
    cosine_sim = pickle.load(f)

# Create the Tkinter application
root = tk.Tk()
root.title('Song Recommendation App')
root.geometry('1000x600')  # Set window dimensions

# Set background image
bg_image = PhotoImage(file='background.png')
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=0.7)

# Create a frame for the header
header_frame = tk.Frame(root, bg='black', pady=10)
header_frame.pack(fill='x')

# Header label
header_label = tk.Label(header_frame, text='Song Recommendation App', bg='black', fg='white', font=('Helvetica', 24, 'bold'))
header_label.pack()

# Create a frame for the song selection
selection_frame = tk.Frame(root, bg='black')
selection_frame.pack(pady=20)

# Dropdown for song selection
selected_song = tk.StringVar()
song_selection = tk.OptionMenu(selection_frame, selected_song, *data['song'])
song_selection.config(bg='white', fg='black', font=('Helvetica', 12))
song_selection.pack(side='left', padx=10)

# Submit button for song selection
def submit_song():
    select_song(selected_song.get())

submit_button = tk.Button(selection_frame, text='Submit', command=submit_song, bg='blue', fg='white', font=('Helvetica', 12, 'bold'))
submit_button.pack(side='left', padx=10)

# Button to select a random song
def select_random_song():
    select_song(random.choice(data['song']))

random_button = tk.Button(selection_frame, text='Select Random Song', command=select_random_song, bg='green', fg='white', font=('Helvetica', 12, 'bold'))
random_button.pack(side='right', padx=10)

# Display currently playing song
current_song_label = tk.Label(root, text='Currently Playing:', bg='black', fg='white', font=('Helvetica', 16, 'bold'))
current_song_label.pack()

# Create a frame for recommended songs
recommended_frame = tk.Frame(root, bg='black')
recommended_frame.pack(pady=120)  # Adjust the pady value as needed

# Function to select a song
def select_song(selected_song):
    selected_song_index = data[data['song'] == selected_song].index[0]
    sim_scores = list(cosine_sim[selected_song_index])
    sim_scores_sorted = sorted(range(len(sim_scores)), key=lambda i: sim_scores[i], reverse=True)
    top_20_indices = sim_scores_sorted[1:21]
    recommended_songs = data['song'].iloc[top_20_indices].tolist()
    
    # Display the currently playing song
    current_song_label.config(text=f'Currently Playing: {selected_song}')
    
    # Remove previous recommended songs grid
    for widget in recommended_frame.winfo_children():
        widget.destroy()
    
    # Create new recommended songs grid
    for i, song in enumerate(recommended_songs):
        row = i // 5
        column = i % 5
        button = tk.Button(recommended_frame, text=song, command=lambda song=song: select_song(song), bg='black', fg='white', relief='groove', font=('Helvetica', 10))
        button.grid(row=row, column=column, padx=5, pady=5)

# Start the Tkinter event loop
root.mainloop()
