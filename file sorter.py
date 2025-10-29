import os
import shutil
import threading
import tkinter as tk
from tkinter import filedialog, font
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

def sort_files_by_extension(directory_path):
    directory = os.path.abspath(directory_path)
    if not os.path.isdir(directory):
        return f"Error: {directory} is not a valid directory"

    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    if not files:
        return "No files found to sort."

    folders_created = {}
    results = []
    
    try:
        current_script = os.path.abspath(__file__)
    except NameError:
        current_script = None

    for file in files:
        file_path = os.path.join(directory, file)
        
        if current_script and os.path.abspath(file_path) == current_script:
            results.append(f"Skipped: {file} (this script)")
            continue
        
        if file.lower() == "filesorter.py":
            results.append(f"Skipped: {file} (this script)")
            continue
        
        extension = os.path.splitext(file)[1][1:].lower()
        if not extension:
            extension = "no_extension"

        extension_folder = os.path.join(directory, extension)
        if extension not in folders_created:
            os.makedirs(extension_folder, exist_ok=True)
            folders_created[extension] = True

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
        self.root.geometry("700x520")
        self.root.minsize(600, 400)

        style = ttk.Style()
        for theme in ("vista", "clam", "default"):
            try:
                style.theme_use(theme)
                break
            except Exception:
                pass
        style.configure("TFrame", background="#f5f7fb")
        style.configure("TLabel", background="#f5f7fb", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"))
        style.configure("TButton", padding=6)
        style.map("TButton",
                  background=[("active", "#dbeafe")],
                  foreground=[("disabled", "#888")])

        self.root.configure(background="#f5f7fb")

        self.entry_font = font.Font(family="Segoe UI", size=10)
        self.results_font = font.Font(family="Consolas", size=10)

        top = ttk.Frame(root, padding=(18, 14, 18, 6))
        top.pack(fill=tk.X)

        header = ttk.Label(top, text="File Sorter", style="Header.TLabel")
        header.pack(anchor=tk.W)

        path_frame = ttk.Frame(top)
        path_frame.pack(fill=tk.X, pady=(10, 0))

        path_label = ttk.Label(path_frame, text="Directory:")
        path_label.pack(side=tk.LEFT, padx=(0, 8))

        self.path_entry = ttk.Entry(path_frame, font=self.entry_font)
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        browse_btn = ttk.Button(path_frame, text="Browse", command=self.browse_directory)
        browse_btn.pack(side=tk.LEFT, padx=(10, 0))

        action_frame = ttk.Frame(root, padding=(18, 8, 18, 8))
        action_frame.pack(fill=tk.X)

        self.sort_button = ttk.Button(action_frame, text="Sort Files", command=self.start_sort_thread)
        self.sort_button.pack(side=tk.LEFT)

        self.clear_button = ttk.Button(action_frame, text="Clear Results", command=self.clear_results)
        self.clear_button.pack(side=tk.LEFT, padx=(10,0))

        results_label = ttk.Label(root, text="Results:")
        results_label.pack(anchor=tk.W, padx=18, pady=(8, 0))

        results_container = ttk.Frame(root, padding=(18, 8, 18, 18))
        results_container.pack(fill=tk.BOTH, expand=True)

        self.results_text = ScrolledText(results_container, wrap=tk.WORD, font=self.results_font, relief=tk.FLAT)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        self.results_text.configure(background="#ffffff", borderwidth=1, relief=tk.SOLID)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, directory)

    def clear_results(self):
        self.results_text.configure(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.configure(state=tk.NORMAL)

    def start_sort_thread(self):
        directory = self.path_entry.get().strip()
        if not directory:
            directory = os.getcwd()
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, directory)

        self.sort_button.state(["disabled"])
        self.clear_button.state(["disabled"])

        thread = threading.Thread(target=self._run_sort, args=(directory,), daemon=True)
        thread.start()

    def _run_sort(self, directory):
        results = sort_files_by_extension(directory)
        self.root.after(0, self._finish_sort, results)

    def _finish_sort(self, results):
        self.sort_button.state(["!disabled"])
        self.clear_button.state(["!disabled"])

        self.results_text.configure(state=tk.NORMAL)
        self.results_text.insert(tk.END, results + "\n\nSorting complete!\n")
        self.results_text.see(tk.END)
        self.results_text.configure(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileSorterApp(root)
    root.mainloop()
