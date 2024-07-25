import tkinter as tk
from tkinter import ttk
import yt_dlp


def say_hi():
    print("hi there, everyone!")


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.quit = None
        self.hi_there = None
        self.title = None
        self.frame = None
        self.url_entry = None
        self.video_url = None
        self.progress_label = None
        self.master = master
        self.pack()
        self.width: int = 500
        self.height: int = 500
        self.progress = None
        self.set_icon("./assets/icon.ico")
        self.master.title("Downloader Application")
        self.master["bg"] = "#fafafb"
        self.master.resizable(False, False)
        self.window = tk.Frame(self.master)
        self.window["bg"] = "#21233f"
        self.window.pack(fill="both", expand=True)
        self.create_widgets()
        self.build_quit(self.window)
        self.style = ttk.Style()

    def create_widgets(self):
        self.title = tk.Label(self.window, text="Welcome To Downloader".upper())
        self.title.pack(side="top")
        self.title["font"] = ("Arial", 20, "bold")
        self.title["fg"] = "#f3f3f3"
        self.title["bg"] = "#21233f"

        frame1 = self.create_frames(self.window, self.width, self.height, bg="#21233f")

        frame1["bg"] = "#21233f"

        frame1.pack(padx=3, pady=3, fill="both", expand=False)
        self.build_form(frame1)

    def set_icon(self, icon_path):
        self.master.iconbitmap(icon_path)

    def create_frames(self, notebook, w, h, bg) -> ttk.Frame:
        self.frame = tk.Frame(notebook, relief="sunken")
        self.frame["borderwidth"] = 2
        self.frame["relief"] = "solid"
        self.frame["bg"] = bg

        return self.frame

    def build_form(self, container):
        frame = tk.Frame(container)

        frame.pack(fill="both", expand=True, padx=10, pady=10)
        frame.columnconfigure(1, weight=3)
        frame.columnconfigure(1, weight=4)

        frame["bg"] = "#2b2d50"

        # Create a label and entry widget
        url_label = tk.Label(frame, text="Video URL")
        url_label["font"] = ("Arial", 15, "bold")
        url_label["fg"] = "#f3f3f3"
        url_label["bg"] = "#111827"
        url_label.grid(row=0, column=0, sticky=tk.W)

        self.url_entry = tk.Entry(frame, width=50, borderwidth=2, relief="solid")
        self.url_entry.focus()
        self.url_entry["font"] = ("Arial", 15)
        self.url_entry["fg"] = "#f3f3f3"
        self.url_entry["bg"] = "#374151"
        self.url_entry.grid(row=1, column=0, sticky=tk.W)

        self.progress_bar(container=container)
        # button
        self.hi_there = tk.Button(container)
        self.hi_there["text"] = "Download Video"
        self.hi_there["command"] = self.downloader
        self.hi_there["font"] = ("Arial", 15, "bold")
        self.hi_there["fg"] = "#f3f3f3"
        self.hi_there["bg"] = "#374151"
        self.hi_there["relief"] = "solid"
        self.hi_there["borderwidth"] = 2
        self.hi_there["activebackground"] = "#2b2d50"
        self.hi_there["activeforeground"] = "#f3f3f3"
        self.hi_there.pack(side="top")
        self.hi_there["justify"] = "center"

    def downloader(self):
        video_url = self.url_entry.get()
        self.progress.pack(side="top")
        self.url_entry.delete(0, tk.END)
        ydl_opts = {
            "format": "best",
            "quiet": True,
            'progress_hooks': [self.yt_dlp_hook],
            "outtmpl": "downloads/%(title)s.%(ext)s"
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

    def yt_dlp_hook(self, d):
        if d['status'] == 'finished':
            self.progress.stop()
            print('Done downloading, now converting ...')
        elif d['status'] == 'downloading':
            self.progress.start()
            print(f"Downloading {d['filename']}")

    def build_quit(self, container):
        self.quit = tk.Button(container)
        self.quit["text"] = "SALIR"
        self.quit["command"] = self.master.quit
        self.quit["font"] = ("Arial", 15, "bold")
        self.quit["fg"] = "#f3f3f3"
        self.quit["bg"] = "#374151"
        self.quit["relief"] = "solid"
        self.quit["borderwidth"] = 2
        self.quit["activebackground"] = "#2b2d50"
        self.quit["activeforeground"] = "#f3f3f3"
        self.quit.pack(side="top")
        self.quit["justify"] = "center"

    def progress_bar(self, container=None):
        self.progress = ttk.Progressbar(container, orient="horizontal", length=200, mode="indeterminate")
