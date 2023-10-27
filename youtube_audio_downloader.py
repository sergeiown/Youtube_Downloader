"""
Program Name: Youtube Downloader
Version: 1.0
Developer: Serhii I. Myshko
License: https://github.com/sergeiown/Youtube_Downloader/blob/main/LICENSE
"""

import tkinter as tk
from tkinter import ttk, filedialog
from pytube import YouTube
import validators
import pyperclip
import threading
import os
import webbrowser
import re

# Create a global variable to track the current progress bar
current_progress_bar = None

# Function to update the list of available bitrates


def update_bitrate_list(url):
    global available_bitrates
    available_bitrates = []
    yt = YouTube(url)
    audio_streams = yt.streams.filter(only_audio=True)
    for stream in audio_streams:
        abr = re.search(r'\d+kbps', stream.abr)
        if abr:
            abr = abr.group()
            if abr not in available_bitrates:
                available_bitrates.append(abr)

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
        # Get streams with audio only
        audio_streams = yt.streams.filter(only_audio=True)
        selected_stream = None

        for stream in audio_streams:
            abr = re.search(r'\d+kbps', stream.abr)
            if abr:
                abr = abr.group()
                if abr == bitrate:
                    selected_stream = stream
                    break

        if not selected_stream:
            status_label.config(text="Selected bitrate not available!")
            return

        download_button.config(state="disabled")
        status_label.config(text="Downloading in progress...")
        progress_bar.start()
        filename = get_valid_filename(yt.title) + f"_{bitrate}.mp3"
        filetypes = [("MP3 files", "*.mp3")]
        save_path = filedialog.asksaveasfilename(
            defaultextension=".mp3", initialfile=filename, filetypes=filetypes)
        if save_path:
            selected_stream.download(output_path=os.path.dirname(
                save_path), filename=os.path.basename(save_path))
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
        if 'selected_stream' in locals():
            progress_bar.pack_forget()

# Function to paste a link from the clipboard


def paste_from_clipboard():
    clipboard_data = pyperclip.paste()
    if validators.url(clipboard_data):
        if "youtube" in clipboard_data:  # Check if the link contains "youtube"
            entry.config(state="normal")
            entry.delete("1.0", tk.END)
            entry.insert(tk.END, clipboard_data)
            entry.config(state="disabled")
            # Update the list of available bitrates
            update_bitrate_list(clipboard_data)
            update_bitrate_combobox()  # Update the Combobox with bitrates
            update_buttons()
        else:
            status_label.config(text="Invalid link (not a YouTube link)!")
            window.after(2000, lambda: status_label.config(text=""))
    else:
        status_label.config(text="Invalid link!")
        window.after(2000, lambda: status_label.config(text=""))


# Function to clear the entry field and handle invalid link logic


def clear_entry():
    entry.config(state="normal")
    entry.delete("1.0", tk.END)
    entry.config(state="disabled")
    update_buttons()

# Function to update the bitrate Combobox with available bitrates


def update_bitrate_combobox():
    bitrate_combobox['values'] = available_bitrates
    if available_bitrates:
        bitrate_var.set(available_bitrates[0])
    else:
        # Protected default value if the list is empty
        bitrate_var.set("")

# Function to set the maximum width for error messages and wrap text if needed


def set_max_error_label_width():
    max_width = window.winfo_width() - window.winfo_width() // 20
    error_label.config(wraplength=max_width)

# Function to sanitize a filename by removing invalid characters


def get_valid_filename(s):
    s = str(s).strip().replace(" ", "_")
    return "".join(c for c in s if c.isalnum() or c in ('_', '.', '-'))

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

# Function to open the GitHub repository's license URL


def open_license_url(event):
    webbrowser.open_new(
        "https://github.com/sergeiown/Youtube_Downloader/blob/main/LICENSE")


# Create the window
window = tk.Tk()
window.title("YouTube Audio Downloader")
window.iconbitmap(default="youtube_downloader.ico")
window.resizable(False, False)

# Get the screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Set the window size to 30% of the screen width and 50% height
window_width = int(screen_width * 0.30)
window_height = int(screen_height * 0.50)
window.geometry(f"{window_width}x{window_height}")

# Label for choosing audio bitrate
bitrate_label = tk.Label(
    window, text="Choose audio bitrate (kbps):", font=("Helvetica", 16))
bitrate_label.pack(pady=10)

# Options for audio bitrate
available_bitrates = []  # Список доступних бітрейтів
bitrate_options = []

# Combobox for selecting audio bitrate
bitrate_var = tk.StringVar()
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

# Add a label for the Copyright information at the bottom
copyright_label = tk.Label(
    window, text="Copyright (c) 2023 Serhii I. Myshko", font=("Helvetica", 10), fg="gray", anchor="e")
copyright_label.pack(side="bottom", pady=3, fill="x")
copyright_label.bind("<Button-1>", open_license_url)

# Add a line beneath the text
line_frame = tk.Frame(window, height=1, background="lightgray")
line_frame.pack(side="bottom", fill="x")

window.mainloop()
