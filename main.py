import tkinter as tk
from tkinter import ttk
from pytube import YouTube
import validators
import pyperclip
import threading

# Function to download the video


def download_video():
    url = entry.get("1.0", tk.END).strip()
    if not url or not validators.url(url):
        status_label.config(text="Invalid link!")
        return

    download_thread = threading.Thread(
        target=download_video_thread, args=(url,))
    download_thread.start()

# Function to download the video in a separate thread


def download_video_thread(url):
    progress_bar = ttk.Progressbar(window, mode="indeterminate", length=400)
    progress_bar.pack(pady=20)
    yt = YouTube(url)
    stream = yt.streams.get_highest_resolution()
    status_label.config(text="Downloading in progress...")
    progress_bar.start()
    stream.download()
    progress_bar.stop()
    progress_bar.pack_forget()
    status_label.config(text="Video downloaded!")
    clear_entry()
    update_buttons()
    window.after(2000, lambda: status_label.config(text=""))

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

# Update the state of buttons and the presence of the "Download" button


def update_buttons():
    url = entry.get("1.0", tk.END).strip()
    if validators.url(url):
        if not download_button.winfo_ismapped():
            download_button.pack(pady=20)
        clear_button.pack(pady=5)  # Show the "Clear" button
        paste_button.pack_forget()
    else:
        if download_button.winfo_ismapped():
            download_button.pack_forget()
        clear_button.pack_forget()  # Hide the "Clear" button
        paste_button.pack(pady=20)


# Create the window
window = tk.Tk()
window.title("Download Video from YouTube")

# Get the screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Set the window size to 25% of the screen width and height
window_width = int(screen_width * 0.25)
window_height = int(screen_height * 0.25)
window.geometry(f"{window_width}x{window_height}")

# Label for entering the link
label = tk.Label(
    window, text="Paste a link to a YouTube video:", font=("Helvetica", 16))
label.pack(pady=10)

# Entry field for entering the link
entry = tk.Text(window, height=1, width=40, state="disabled")
entry.pack(padx=10, pady=2)

# Button to download
download_button = tk.Button(
    window, text="Download", command=download_video)
download_button.pack_forget()

# Button to clear the entry field
clear_button = tk.Button(
    window, text="Clear", command=clear_entry)
clear_button.pack(pady=2)  # Adjust the padding as needed

# Label for the status
status_label = tk.Label(window, text="")
status_label.pack()

# Button to paste a link from the clipboard
paste_button = tk.Button(
    window, text="Paste from clipboard", command=paste_from_clipboard)
paste_button.pack(pady=20)

# Update the state of buttons and the presence of the "Download" button at the beginning
update_buttons()

window.mainloop()
