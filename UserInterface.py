'''File Upload, Chat GUI Module'''

import tkinter as tk
from tkinter import filedialog, ttk, simpledialog, scrolledtext
import os


""" tkinter: standard Python interface to the Tk GUI toolkit.
filedialog: Provides dialogs for file selection.
ttk: Provides themed widget set for Tkinter.
simpledialog: Provides simple dialogs for getting user input.
scrolledtext: Provides a text widget with a vertical scroll bar.
os: Provides functions to interact with the operating system."""

class App(tk.Tk):   # Creates main window for the application
    def __init__(self): 
        super().__init__()  
        self.title("Chat with multiple PDFs")
        self.geometry("1000x600")   # Sets the size of the window to be 1000 pixels wide and 600 pixels tall.
        self.configure(bg="black")

        self.uploaded_files = []  # To keep track of uploaded files that the user uploads to the application.
        self.combined_text = ""   # To store combined text from all PDFs

        # Sidebar frame
        self.sidebar_frame = tk.Frame(self, bg="#1E1E1E", width=250)
        self.sidebar_frame.pack(side="left", fill="y")

        # Main frame
        self.main_frame = tk.Frame(self, bg="black")
        self.main_frame.pack(side="right", expand=True, fill="both")

        # Sidebar content
        self.sidebar_title = tk.Label(self.sidebar_frame, text="Your documents", fg="white", bg="#1E1E1E", font=("Helvetica", 14, "bold"))
        self.sidebar_title.pack(pady=10)

        self.upload_instruction = tk.Label(self.sidebar_frame, text="Upload your PDFs here and click on 'Process'", fg="white", bg="#1E1E1E", wraplength=200)
        self.upload_instruction.pack(pady=5)

        self.file_frame = tk.Frame(self.sidebar_frame, bg="#1E1E1E", bd=2, relief="sunken")
        self.file_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.file_label = tk.Label(self.file_frame, text="Drag and drop files here\nLimit 200MB per file", fg="white", bg="black")
        self.file_label.pack(padx=10, pady=10, fill="both", expand=True)

        self.browse_button = tk.Button(self.sidebar_frame, text="Browse files", command=self.browse_files, bg="red", fg="white")
        self.browse_button.pack(pady=10)

        self.url_label = tk.Label(self.sidebar_frame, text="Or enter a PDF URL:", fg="white", bg="#1E1E1E", wraplength=200)
        self.url_label.pack(pady=5)

        self.url_entry = ttk.Entry(self.sidebar_frame)
        self.url_entry.pack(pady=5, padx=10, fill="x")

        self.add_url_button = tk.Button(self.sidebar_frame, text="Add URL", command=self.add_url, bg="blue", fg="white")
        self.add_url_button.pack(pady=10)

        self.process_button = tk.Button(self.sidebar_frame, text="Process", command=self.process_files, bg="green", fg="white")
        self.process_button.pack(pady=10)

         # Main content
        self.heading_frame = tk.Frame(self.main_frame, bg="black")
        self.heading_frame.pack(pady=10, anchor="w", padx=20)

        self.heading_label = tk.Label(self.heading_frame, text="Chat with multiple PDFs", fg="white", bg="black", font=("Helvetica", 24, "bold"))
        self.heading_label.pack(side="left")

        self.icon_image = tk.PhotoImage(file=r"./icons/DB_Icon.png").subsample(8, 8) 
        self.icon_label = tk.Label(self.heading_frame, image=self.icon_image, bg="black")
        self.icon_label.pack(side="left", padx=(10, 0))

        self.prompt_label = tk.Label(self.main_frame, text="Ask a question about your documents:", fg="white", bg="black", font=("Helvetica", 14))
        self.prompt_label.pack(pady=10, anchor="w", padx=20)

        self.entry = ttk.Entry(self.main_frame, font=("Helvetica", 14))
        self.entry.pack(pady=10, padx=20, fill="x")
        self.entry.bind("<Return>", self.ask_question)

        self.chat_frame = tk.Frame(self.main_frame, bg="black")
        self.chat_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.chat_box = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD, font=("Helvetica", 14), bg="#2E2E2E", fg="white", state="disabled")
        self.chat_box.pack(fill="both", expand=True)