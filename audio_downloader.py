"""
Program Name: YouTube MP3 Downloader
Version: 1.0
Developer: Serhii I. Myshko
"""

import tkinter as tk
from tkinter import ttk, filedialog
from pytube import YouTube
import validators
import pyperclip
import threading
import os
import subprocess

# Create a global variable to track the current progress bar
current_progress_bar = None

# Function to download the audio as mp3


def download_mp3():
    url = entry.get("1.0", tk.END).strip()
    if not url or not validators.url(url):
        status_label.config(text="Invalid link!")
        return

    selected_bitrate = bitrate_var.get()
    download_thread = threading.Thread(
        target=download_mp3_thread, args=(url, selected_bitrate))
    download_thread.start()

# Function to download the audio as mp3 in a separate thread


def download_mp3_thread(url, bitrate):
    global current_progress_bar
    # Check if a progress bar is already displayed and remove it
    if current_progress_bar:
        current_progress_bar.pack_forget()

    progress_bar = ttk.Progressbar(window, mode="indeterminate", length=400)
    progress_bar.pack(pady=30)
    current_progress_bar = progress_bar  # Set the current progress bar

    yt = YouTube(url)

    try:
        streams = yt.streams.filter(only_audio=True, abr=bitrate + 'kbps')
        if not streams:
            status_label.config(text="Selected bitrate not available!")
            return

        download_button.config(state="disabled")
        status_label.config(text="Downloading in progress...")
        progress_bar.start()
        audio_stream = streams.first()
        filename = get_valid_filename(yt.title) + f'_{bitrate}kbps.mp3'
        filetypes = [("MP3 files", "*.mp3")]
        save_path = filedialog.asksaveasfilename(
            defaultextension=".mp3", initialfile=filename, filetypes=filetypes)
        if save_path:
            audio_stream.download(output_path=os.path.dirname(
                save_path), filename=os.path.basename(save_path))
            mp4_filename = os.path.join(os.path.dirname(
                save_path), os.path.basename(save_path))
            mp3_filename = os.path.splitext(mp4_filename)[0] + ".mp3"
            convert_to_mp3(mp4_filename, mp3_filename)
            progress_bar.stop()
            progress_bar.pack_forget()
            status_label.config(text="Audio downloaded as MP3!")
            clear_entry()
            update_buttons()
            window.after(2000, lambda: status_label.config(text=""))
            download_button.config(state="normal")
        else:
            status_label.config(text="")
            download_button.config(state="normal")
            clear_entry()
    except Exception as e:
        error_label.config(text=str(e))
        window.after(5000, lambda: error_label.config(text=""))
    finally:
        if 'audio_stream' in locals():
            progress_bar.pack_forget()

# Function to paste a link from the clipboard


def paste_from_clipboard():
    clipboard_data = pyperclip.paste()
    if validators.url(clipboard_data):
        entry.config(state="normal")
        entry.delete("1.0", tk.END)
        entry.insert(tk.END, clipboard_data)
        entry.config(state="disabled")
        update_buttons()
    else:
        status_label.config(text="Invalid link!")
        window.after(2000, lambda: status_label.config(text=""))

# Function to clear the entry field and handle invalid link logic


def clear_entry():
    entry.config(state="normal")
    entry.delete("1.0", tk.END)
    entry.config(state="disabled")
    update_buttons()

# Function to set the maximum width for error messages and wrap text if needed


def set_max_error_label_width():
    max_width = window.winfo_width() - window.winfo_width() // 20
    error_label.config(wraplength=max_width)

# Function to sanitize a filename by removing invalid characters


def get_valid_filename(s):
    s = str(s).strip().replace(" ", "_")
    return "".join(c for c in s if c.isalnum() or c in ('_', '.', '-'))

# Function to convert downloaded mp4 to mp3


def convert_to_mp3(input_file, output_file):
    cmd = f'ffmpeg -i "{input_file}" -q:a 0 -map a "{output_file}"'
    subprocess.call(cmd, shell=True)

# Update the state of buttons and the presence of the "Download" button


def update_buttons():
    global current_progress_bar
    url = entry.get("1.0", tk.END).strip()
    if validators.url(url):
        if not current_progress_bar:  # Only create a new progress bar if none is active
            download_button.pack(pady=15)
        clear_button.pack(pady=5)
        paste_button.pack_forget()
    else:
        if current_progress_bar:
            current_progress_bar.pack_forget()
            current_progress_bar = None  # Reset the current progress bar
        if download_button.winfo_ismapped():
            download_button.pack_forget()
        clear_button.pack_forget()
        paste_button.pack(pady=15)

    set_max_error_label_width()


# Create the window
window = tk.Tk()
window.title("YouTube MP3 Downloader")
window.iconbitmap(default="youtube_downloader.ico")
window.resizable(False, False)

# Get the screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Set the window size to 25% of the screen width and 35% height
window_width = int(screen_width * 0.25)
window_height = int(screen_height * 0.35)
window.geometry(f"{window_width}x{window_height}")

# Label for choosing audio bitrate
bitrate_label = tk.Label(
    window, text="Choose audio bitrate (kbps):", font=("Helvetica", 16))
bitrate_label.pack(pady=10)

# Options for audio bitrate
bitrate_options = ["128", "160", "256", "320"]

# Combobox for selecting audio bitrate
bitrate_var = tk.StringVar()
bitrate_var.set(bitrate_options[0])
bitrate_combobox = ttk.Combobox(
    window, textvariable=bitrate_var, values=bitrate_options, width=25)
bitrate_combobox.pack()

# Label for entering the link
label = tk.Label(
    window, text="Link to a YouTube video:", font=("Helvetica", 16))
label.pack(pady=10)

# Entry field for entering the link
entry = tk.Text(window, height=1, width=50, state="disabled")
entry.pack(padx=10, pady=2)

# Button to download
download_button = tk.Button(
    window, text="Download as MP3", command=download_mp3, width=25)
download_button.pack_forget()

# Button to clear the entry field
clear_button = tk.Button(
    window, text="Clear", command=clear_entry, width=25)
clear_button.pack(pady=2)

# Label for the status
status_label = tk.Label(window, text="")
status_label.pack()

# Label for error messages
error_label = tk.Label(window, text="", fg="red",
                       wraplength=window_width - window_width // 20)
error_label.pack()

# Button to paste a link from the clipboard
paste_button = tk.Button(
    window, text="Paste URL from clipboard", command=paste_from_clipboard, width=25)
paste_button.pack(pady=15)

# Update the state of buttons and the presence of the "Download" button at the beginning
update_buttons()

# Bind a function to window resize event to update the max width for error messages
window.bind("<Configure>", lambda event: set_max_error_label_width())

# Get the center coordinates for the window
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Set the window position
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.mainloop()
