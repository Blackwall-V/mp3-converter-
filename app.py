import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
from yt_dlp import YoutubeDL

class YouTubeToAudioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Audio Downloader")
        self.root.geometry("500x250")
        self.root.resizable(False, False)

        self.target_dir = tk.StringVar(value=os.path.expanduser("~"))

        tk.Label(root, text="YouTube URL:", font=("Arial", 11, "bold")).pack(pady=(15, 2))
        self.url_entry = tk.Entry(root, width=55, font=("Arial", 10))
        self.url_entry.pack(pady=5)

        tk.Label(root, text="Save Target (Select your USB Drive):", font=("Arial", 11, "bold")).pack(pady=(10, 2))
        
        dir_frame = tk.Frame(root)
        dir_frame.pack(pady=5)
        
        self.dir_label = tk.Entry(dir_frame, textvariable=self.target_dir, width=40, state='readonly', font=("Arial", 9))
        self.dir_label.pack(side=tk.LEFT, padx=5)
        
        browse_btn = tk.Button(dir_frame, text="Browse USB", command=self.browse_directory)
        browse_btn.pack(side=tk.LEFT)

        self.download_btn = tk.Button(root, text="Convert & Save Audio", bg="#2ecc71", fg="white", 
                                      font=("Arial", 12, "bold"), command=self.start_download_thread, height=2)
        self.download_btn.pack(pady=20)

        self.status_label = tk.Label(root, text="", fg="blue")
        self.status_label.pack()

    def browse_directory(self):
        selected_dir = filedialog.askdirectory(initialdir=self.target_dir.get(), title="Select USB Drive or Folder")
        if selected_dir:
            self.target_dir.set(selected_dir)

    def start_download_thread(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a valid YouTube URL.")
            return
        
        self.download_btn.config(state=tk.DISABLED, bg="#95a5a6")
        self.status_label.config(text="Processing... please wait.", fg="orange")
        
        threading.Thread(target=self.download_audio, args=(url,), daemon=True).start()

        def download_audio(self, url):
        # We enforce the .mp3 extension framework template
            output_path = os.path.join(self.target_dir.get(), '%(title)s.%(ext)s')
        
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': output_path,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
            }],
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            self.update_ui_success("Success! MP3 saved to your drive.")
        except Exception as e:
            self.update_ui_success(f"Error processing audio.", failed=True)

               
            # UI Updates must be done safely from main thread or handled simply
            self.update_ui_success("Success! Audio saved to your drive.")
        except Exception as e:
            self.update_ui_success(f"Error: Lower quality or invalid link.", failed=True)

    def update_ui_success(self, message, failed=False):
        def callback():
            self.download_btn.config(state=tk.NORMAL, bg="#2ecc71")
            if failed:
                self.status_label.config(text="Download failed.", fg="red")
                messagebox.showerror("Download Failed", message)
            else:
                self.status_label.config(text="Finished!", fg="green")
                messagebox.showinfo("Done", message)
                self.url_entry.delete(0, tk.END)
        self.root.after(0, callback)

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeToAudioApp(root)
    root.mainloop()
