import os
import shutil
import tkinter as tk
from tkinter import filedialog

def sort_files_by_extension(directory_path):
    # Convert to absolute path
    directory = os.path.abspath(directory_path)
    
    # Check if directory exists
    if not os.path.isdir(directory):
        return f"Error: {directory} is not a valid directory"
    
    # Get all files in the directory
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    if not files:
        return "No files found to sort."
    
    # Dictionary to keep track of created folders
    folders_created = {}
    results = []
    
    for file in files:
        # Get file extension without the dot
        file_path = os.path.join(directory, file)
        extension = os.path.splitext(file)[1][1:].lower()
        
        # Use "no_extension" for files without extension
        if not extension:
            extension = "no_extension"
        
        # Create folder for extension if it doesn't exist
        extension_folder = os.path.join(directory, extension)
        if extension not in folders_created:
            os.makedirs(extension_folder, exist_ok=True)
            folders_created[extension] = True
        
        # Move the file to its corresponding folder
        destination = os.path.join(extension_folder, file)
        try:
            shutil.move(file_path, destination)
            results.append(f"Moved: {file} → {extension}/{file}")
        except Exception as e:
            results.append(f"Error moving {file}: {e}")
    
    return "\n".join(results)

class FileSorterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Sorter")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Directory path frame
        self.path_frame = tk.Frame(root)
        self.path_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.path_label = tk.Label(self.path_frame, text="Directory Path:")
        self.path_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.path_entry = tk.Entry(self.path_frame)
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.browse_button = tk.Button(self.path_frame, text="Browse", command=self.browse_directory)
        self.browse_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Sort button
        self.sort_button = tk.Button(root, text="Sort Files", command=self.sort_files, height=2)
        self.sort_button.pack(fill=tk.X, padx=20, pady=10)
        
        # Results area
        self.results_label = tk.Label(root, text="Results:")
        self.results_label.pack(anchor=tk.W, padx=20, pady=(10, 0))
        
        self.results_frame = tk.Frame(root)
        self.results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.scrollbar = tk.Scrollbar(self.results_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.results_text = tk.Text(self.results_frame)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        self.scrollbar.config(command=self.results_text.yview)
        self.results_text.config(yscrollcommand=self.scrollbar.set)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, directory)

    def sort_files(self):
        directory = self.path_entry.get().strip()
        if not directory:
            directory = os.getcwd()
            self.path_entry.insert(0, directory)
        
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"Sorting files in: {directory}\n\n")
        
        # Perform sorting
        results = sort_files_by_extension(directory)
        self.results_text.insert(tk.END, results)
        self.results_text.insert(tk.END, "\n\nSorting complete!")
        self.results_text.see(tk.END)  # Scroll to bottom

if __name__ == "__main__":
    root = tk.Tk()
    app = FileSorterApp(root)
    root.mainloop()