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

# Label and field for entering a link
label = tk.Label(window, text="Введіть посилання на відео YouTube:")
label.pack()
entry = tk.Entry(window)
entry.pack()

# Button for downloading
download_button = tk.Button(window, text="Завантажити", command=download_video)
download_button.pack()

# Label for the status
status_label = tk.Label(window, text="")
status_label.pack()

window.mainloop()
