import tkinter as tk
from tkinter import messagebox
import os
import yt_dlp

def select_option(option):
    global selected_option
    selected_option = option
    update_buttons()

def update_buttons():
    """Update colors for selected/unselected options"""
    if selected_option == "audio":
        audio_btn.config(bg="#007bff", fg="white")
        video_btn.config(bg="#cce5ff", fg="#555555")
    else:
        audio_btn.config(bg="#cce5ff", fg="#555555")
        video_btn.config(bg="#007bff", fg="white")

def download():
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube link.")
        return

    output_folder = "downloads"
    os.makedirs(output_folder, exist_ok=True)

    if selected_option == "audio":
        template = os.path.join(output_folder, "%(title)s_audio.%(ext)s")
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': template,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        dtype = "Audio"
    else:
        template = os.path.join(output_folder, "%(title)s_video.%(ext)s")
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': template,
        }
        dtype = "Video"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Success", f"{dtype} downloaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Download failed:\n{e}")

# --- GUI ---
root = tk.Tk()
root.title("YouTube Downloader")
root.geometry("600x350")
root.minsize(600, 350)  # increased minimum size
root.configure(bg="#f5f5f5")  # background color

# Title
tk.Label(root, text="YouTube Downloader", font=("Helvetica", 20, "bold"),
         bg="#f5f5f5", fg="#2a6f97").pack(pady=(15,10))

# Link Entry
entry_frame = tk.Frame(root, bg="#f5f5f5")
entry_frame.pack(fill="x", padx=20, pady=10)
url_entry = tk.Entry(entry_frame, font=("Helvetica", 14))
url_entry.pack(fill="x", ipady=8, padx=5)

# Audio/Video Options
option_frame = tk.Frame(root, bg="#f5f5f5")
option_frame.pack(pady=15, fill="x")
option_frame.columnconfigure(0, weight=1)
option_frame.columnconfigure(1, weight=1)

selected_option = "video"  # default

audio_btn = tk.Button(option_frame, text="Audio", font=("Helvetica",14,"bold"),
                      width=14, height=2, command=lambda: select_option("audio"))
audio_btn.grid(row=0, column=0, padx=15, sticky="ew")

video_btn = tk.Button(option_frame, text="Video", font=("Helvetica",14,"bold"),
                      width=14, height=2, command=lambda: select_option("video"))
video_btn.grid(row=0, column=1, padx=15, sticky="ew")

update_buttons()  # set initial colors

# Download Button
download_btn = tk.Button(root, text="Download", font=("Helvetica",16,"bold"),
                         bg="#28a745", fg="white", width=30, height=2,
                         command=download)
download_btn.pack(pady=20, fill="x", padx=50)

# Make window resize properly
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

root.mainloop()
