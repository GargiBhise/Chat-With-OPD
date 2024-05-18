'''File Upload, Chat GUI Module'''

import tkinter as tk
from tkinter import filedialog, ttk, simpledialog, scrolledtext
from PreProcess import download_pdf, open_and_read_pdf
import os

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chat with multiple PDFs")
        self.geometry("1000x600")   # Sets the size of the window to be 1000 pixels wide and 600 pixels tall.
        self.configure(bg="black")

        self.uploaded_files = []  # To keep track of uploaded files
        self.combined_text = []   # Contains List of Dictionaries | Each Dictionary contains Metadata and Contents of Page.
        # self.combined_text wil be sent to LLM to generate embeddings of the text.
        self.download_folder = "downloaded_pdfs"  # Folder to store downloaded PDFs

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

        self.file_list_frame = tk.Frame(self.sidebar_frame, bg="#1E1E1E")
        self.file_list_frame.pack(padx=10, pady=10, fill="both", expand=True)

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

    def browse_files(self):  #  interacts with the user by opening a file dialog and allowing the user to select files.
        filetypes = (("PDF files", "*.pdf"), ("All files", "*.*"))  # user can select PDF files or any type of file.
        filenames = filedialog.askopenfilenames(title="Select files", filetypes=filetypes)  # opens a file dialog where the user can select one or more files
        for filename in filenames:
            self.add_file_to_list(filename)

    def process_files(self):
        self.display_message("System", "Begin process_files method.")
        for file in self.uploaded_files:
            if not os.path.exists(file):
                url = simpledialog.askstring("Input", f"File {file} not found. Please enter the URL to download:")
                if url:
                    local_path = download_pdf(self.download_folder, url)
                    if local_path:
                        self.display_message("System", f"File has been successfully downloaded: {local_path}")
                        self.combined_text = open_and_read_pdf(local_path)
            else:
                self.combined_text = open_and_read_pdf(file)
        self.display_message("System", "PDFs processed successfully. You can now ask questions.")

    def add_file_to_list(self, filename):
        self.uploaded_files.append(filename)
        file_frame = tk.Frame(self.file_list_frame, bg="#1E1E1E")
        file_frame.pack(fill="x", pady=2)

        file_label = tk.Label(file_frame, text=filename, fg="white", bg="#1E1E1E", anchor="w")
        file_label.pack(side="left", padx=10, fill="x", expand=True)

        remove_button = tk.Button(file_frame, text="X", command=lambda: self.remove_file_from_list(filename, file_frame), bg="red", fg="white", width=2)
        remove_button.pack(side="right", padx=10)

    def remove_file_from_list(self, filename, frame):
        self.uploaded_files.remove(filename)
        frame.destroy()

    def add_url(self):
        url = self.url_entry.get()
        if url:
            filename = url.split("/")[-1]
            local_path = os.path.join(os.getcwd(), filename)
            success = download_pdf(local_path, url)
            if success:
                self.add_file_to_list(local_path)
                self.url_entry.delete(0, tk.END)

    def ask_question(self, event=None):
        question = self.entry.get()
        if question.strip():
            self.entry.delete(0, tk.END)
            self.display_message("You", question)
            response = self.get_response(question)
            self.display_message("Bot", response)

    def get_response(self, question):
        if "first amendment" in question.lower():
            return "The First Amendment prohibits the making of any law respecting an establishment of religion, impeding the free exercise of religion, abridging the freedom of speech, infringing on the freedom of the press, interfering with the right to peaceably assemble, or prohibiting the petitioning for a governmental redress of grievances."
        return "This is a placeholder response based on the combined text of the uploaded PDFs."

    def display_message(self, sender, message):
        self.chat_box.config(state="normal")
        self.chat_box.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_box.config(state="disabled")
        self.chat_box.yview(tk.END)

if __name__ == "__main__":
    app = App()
    app.mainloop()