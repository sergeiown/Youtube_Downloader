import tkinter as tk
import os
import subprocess

# Функція для запуску audio_downloader.py


def run_audio_downloader():
    root.iconify()  # Ховаємо вікно
    subprocess.Popen(['python', 'audio_downloader.py'], shell=True).wait()
    root.deiconify()  # Показуємо вікно знову

# Функція для запуску video_downloader.py


def run_video_downloader():
    root.iconify()  # Ховаємо вікно
    subprocess.Popen(['python', 'video_downloader.py'], shell=True).wait()
    root.deiconify()  # Показуємо вікно знову


# Створюємо головне вікно
root = tk.Tk()
root.title("YouTube Downloader")

# Додаємо напис "Select what to download" зверху
label = tk.Label(root, text="Select what to download")
label.pack()

# Додаємо кнопку для завантаження аудіо
audio_button = tk.Button(root, text="Audio", command=run_audio_downloader)
audio_button.pack()

# Додаємо кнопку для завантаження відео
video_button = tk.Button(root, text="Video", command=run_video_downloader)
video_button.pack()

root.mainloop()
