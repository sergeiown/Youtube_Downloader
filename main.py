import tkinter as tk
from pytube import YouTube

# Function for downloading videos


def download_video():
    url = entry.get()
    yt = YouTube(url)
    stream = yt.streams.get_highest_resolution()
    stream.download()
    status_label.config(text="Відео завантажено!")


# Creating a window
window = tk.Tk()
window.title("Завантажити відео з YouTube")

# Get the screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Set the window size to 25% of the screen width and height
window_width = int(screen_width * 0.25)
window_height = int(screen_height * 0.25)
window.geometry(f"{window_width}x{window_height}")

# Label for entering a link
label = tk.Label(
    window, text="Введіть посилання на відео YouTube:", font=("Helvetica", 16))
label.pack(pady=20)

# Entry field for the link
entry = tk.Entry(window, width=40)
entry.pack(fill=tk.X, padx=20, pady=20)

# Button for downloading
download_button = tk.Button(window, text="Завантажити", command=download_video)
download_button.pack(pady=20)

# Label for the status
status_label = tk.Label(window, text="")
status_label.pack()

window.mainloop()
