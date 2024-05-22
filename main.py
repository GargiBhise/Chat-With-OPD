import os
from tkinter import simpledialog
from GUI import App
from PreProcess import PreProcess


class MainApp:
    def __init__(self):
        self.download_folder = "./"  # replace with your actual path
        self.preprocess = PreProcess(self.download_folder)
        self.app = App(self.process_files_callback, self.get_response_callback)
        self.app.mainloop()

    def process_files_callback(self, uploaded_files):
        combined_text = ""
        for file in uploaded_files:
            if not os.path.exists(file):
                url = simpledialog.askstring("Input", f"File {file} not found. Please enter the URL to download:")
                if url:
                    local_path = self.preprocess.download_pdf(url)
                    if local_path:
                        print(f"File has been successfully downloaded: {local_path}")
                        texts = self.preprocess.open_and_read_pdf(local_path)
                        if isinstance(texts, list):
                            for text_dict in texts:
                                combined_text += text_dict['text'] + ' '
            else:
                texts = self.preprocess.open_and_read_pdf(file)
                if isinstance(texts, list):
                    for text_dict in texts:
                        combined_text += text_dict['text'] + ' '
        print("PDFs processed successfully. You can now ask questions.")
        return combined_text

    def get_response_callback(self, question):
        # This is a placeholder for your actual response generation code
        if "first amendment" in question.lower():
            return "The First Amendment prohibits the..."
        return "This is a placeholder response based on the combined text of the uploaded PDFs."

if __name__ == "__main__":
    MainApp()