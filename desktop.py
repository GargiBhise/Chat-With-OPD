import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from threading import *
import customtkinter

def verify(folder_path):
    print(folder_path)

    
app = customtkinter.CTk()
app.geometry('600x500')

labelFont=customtkinter.CTkFont(family='',size=15)

customtkinter.CTkLabel(app, text="Select Source Folder:", font=labelFont).grid(row=4,column=2,pady=10, padx=15)
folder_path = tk.StringVar()

customtkinter.CTkEntry(app, textvariable=folder_path).grid(row=6, column=4,pady=10)


open_File_Directory=customtkinter.CTkButton(app, text="Browse", command=lambda: folder_path.set(filedialog.askdirectory())).grid(row=6,column=2,pady=10)
customtkinter.CTkButton(app, text="Start Translation", command=lambda: verify(folder_path.get())).grid(row=14, column=2, pady=10)
customtkinter.CTkButton(app, text="Exit", command=app.quit).grid(row=15, column=3,pady=10)

app.mainloop()
