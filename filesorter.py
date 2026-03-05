import os
import shutil
import threading
import tkinter as tk
from tkinter import filedialog, font  
from tkinter import ttk


def set_app_user_model_id(app_id="grassrune.file.sorter"):
    try:
        import ctypes

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    except Exception:
        pass


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


def _rounded_rect_points(x1, y1, x2, y2, r):
    r = min(r, (x2 - x1) / 2, (y2 - y1) / 2)
    return [
        x1 + r, y1,
        x2 - r, y1,
        x2, y1,
        x2, y1 + r,
        x2, y2 - r,
        x2, y2,
        x2 - r, y2,
        x1 + r, y2,
        x1, y2,
        x1, y2 - r,
        x1, y1 + r,
        x1, y1,
    ]


class RoundedButton(tk.Canvas):
    def __init__(self, master, text, command, colors, width=130, height=36, radius=10, **kwargs):
        bg = colors.get("surface", "#161b22")
        super().__init__(master, width=width, height=height, highlightthickness=0, bd=0, bg=bg, **kwargs)
        self.command = command
        self.colors = colors
        self.radius = radius
        self.state_disabled = False
        self.fill = colors["accent"]
        self.outline = colors["accent"]
        self.text = text
        self.font = ("Segoe UI", 10, "bold")

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

        self._draw(self.fill)

    def _draw(self, fill):
        self.delete("all")
        w = int(self.cget("width"))
        h = int(self.cget("height"))
        pts = _rounded_rect_points(1, 1, w - 1, h - 1, self.radius)
        self.create_polygon(pts, smooth=True, splinesteps=36, fill=fill, outline=self.colors["border"], width=1)
        self.create_text(w // 2, h // 2, text=self.text, fill=self.colors["background"], font=self.font)

    def set_enabled(self, enabled: bool):
        self.state_disabled = not enabled
        if enabled:
            self._draw(self.colors["accent"])
        else:
            self._draw(self.colors["border"])

    def _on_enter(self, _):
        if self.state_disabled:
            return
        self._draw(self.colors["accent_hover"])

    def _on_leave(self, _):
        if self.state_disabled:
            return
        self._draw(self.colors["accent"])

    def _on_press(self, _):
        if self.state_disabled:
            return
        self._draw(self.colors["accent_active"])

    def _on_release(self, event):
        if self.state_disabled:
            return
        self._draw(self.colors["accent"])
        if self.command and self.winfo_containing(event.x_root, event.y_root) == self:
            self.command()


class RoundedEntry(tk.Frame):
    def __init__(self, master, colors, height=34, radius=10, padding=8, **entry_kwargs):
        bg = colors.get("surface", "#161b22")
        super().__init__(master, highlightthickness=0, bd=0, bg=bg)
        self.colors = colors
        self.radius = radius
        self.padding = padding
        self.height = height

        self.canvas = tk.Canvas(self, highlightthickness=0, bd=0, bg=bg, height=height)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        entry_kwargs.setdefault("relief", tk.FLAT)
        entry_kwargs.setdefault("bd", 0)
        entry_kwargs.setdefault("highlightthickness", 0)
        entry_kwargs.setdefault("background", colors["surface"])
        entry_kwargs.setdefault("foreground", colors["text"])
        entry_kwargs.setdefault("insertbackground", colors["accent"])
        self.entry = tk.Entry(self, **entry_kwargs)

        self.bind("<Configure>", self._resize)
        self.entry.bind("<FocusIn>", self._focus_in)
        self.entry.bind("<FocusOut>", self._focus_out)

    def _draw_bg(self, focus=False):
        self.canvas.delete("bg")
        w = self.canvas.winfo_width() or 0
        h = self.height
        pts = _rounded_rect_points(1, 1, w - 2, h - 2, self.radius)
        outline = self.colors["accent"] if focus else self.colors["border"]
        self.canvas.create_polygon(pts, smooth=True, splinesteps=36, fill=self.colors["surface"], outline=outline, width=1, tags="bg")

    def _resize(self, event):
        self._draw_bg()
        pad = self.padding
        self.entry.place(x=pad, y=(self.height - 24) // 2, width=event.width - 2 * pad, height=24)

    def _focus_in(self, _):
        self._draw_bg(focus=True)

    def _focus_out(self, _):
        self._draw_bg(focus=False)


class FileSorterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("grassrune the file sorter")
        self.root.geometry("700x520")
        self.root.minsize(620, 420)

        self.colors = {
            "background": "#0d1117",
            "surface": "#161b22",
            "border": "#30363d",
            "text": "#f0f6fc",
            "muted": "#8b949e",
            "accent": "#2ea043",
            "accent_hover": "#3fb950",
            "accent_active": "#2ea043",
            "disabled": "#5c6370",
        }

        self.entry_font = font.Font(family="Segoe UI", size=10)
        self.results_font = font.Font(family="Consolas", size=10)

        self._apply_icon()
        self._apply_theme()
        self.root.after(50, self._apply_dark_titlebar)

        top = ttk.Frame(root, padding=(18, 14, 18, 6))
        top.pack(fill=tk.X)

        header = ttk.Label(top, text="grassrune the file sorter", style="Header.TLabel", anchor=tk.CENTER, justify=tk.CENTER)
        header.pack(fill=tk.X)

        path_frame = ttk.Frame(top)
        path_frame.pack(fill=tk.X, pady=(10, 0))

        path_label = ttk.Label(path_frame, text="Directory:")
        path_label.pack(side=tk.LEFT, padx=(0, 8))

        self.path_entry_wrapper = RoundedEntry(path_frame, colors=self.colors, height=38, radius=12, padding=10, font=self.entry_font)
        self.path_entry_wrapper.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.path_entry = self.path_entry_wrapper.entry

        browse_btn = RoundedButton(path_frame, text="Browse", command=self.browse_directory, colors=self.colors, height=36, radius=12)
        browse_btn.pack(side=tk.LEFT, padx=(10, 0))
        self.browse_button = browse_btn

        action_frame = ttk.Frame(root, padding=(18, 8, 18, 8))
        action_frame.pack(fill=tk.X)

        self.sort_button = RoundedButton(action_frame, text="Sort Files", command=self.start_sort_thread, colors=self.colors, height=36, radius=12)
        self.sort_button.pack(side=tk.LEFT)

        self.clear_button = RoundedButton(action_frame, text="Clear Results", command=self.clear_results, colors=self.colors, height=36, radius=12)
        self.clear_button.pack(side=tk.LEFT, padx=(10,0))

        results_label = ttk.Label(root, text="Results:")
        results_label.pack(anchor=tk.W, padx=18, pady=(8, 0))

        results_container = ttk.Frame(root, padding=(18, 8, 18, 18))
        results_container.pack(fill=tk.BOTH, expand=True)

        text_frame = ttk.Frame(results_container, style="Surface.TFrame")
        text_frame.pack(fill=tk.BOTH, expand=True)

        self.results_text = tk.Text(
            text_frame,
            wrap=tk.WORD,
            font=self.results_font,
            background=self.colors["surface"],
            foreground=self.colors["text"],
            insertbackground=self.colors["accent"],
            selectbackground=self.colors["accent"],
            selectforeground=self.colors["background"],
            borderwidth=1,
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground=self.colors["border"],
            highlightcolor=self.colors["accent"],
        )

        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.results_text.yview, style="Vertical.TScrollbar")
        self.results_text.configure(yscrollcommand=scrollbar.set)

        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _apply_theme(self):
        style = ttk.Style()
        for theme in ("clam", "vista", "default"):
            try:
                style.theme_use(theme)
                break
            except Exception:
                continue

        c = self.colors
        self.root.configure(background=c["background"])
        self.root.option_add("*background", c["surface"])
        self.root.option_add("*foreground", c["text"])
        self.root.option_add("*highlightColor", c["accent"])
        self.root.option_add("*activeBackground", c["accent"])
        self.root.option_add("*activeForeground", c["background"])

        style.configure("TFrame", background=c["surface"], borderwidth=0)
        style.configure("Surface.TFrame", background=c["surface"], borderwidth=0)
        style.configure("TLabel", background=c["surface"], foreground=c["text"], font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), foreground=c["text"])

        style.configure(
            "TButton",
            padding=8,
            background=c["accent"],
            foreground=c["background"],
            bordercolor=c["border"],
            focusthickness=1,
            focuscolor=c["accent"],
        )
        style.map(
            "TButton",
            background=[("active", c["accent_hover"]), ("pressed", c["accent_active"]), ("disabled", c["border"])],
            foreground=[("disabled", c["disabled"])],
            relief=[("pressed", "sunken"), ("!pressed", "raised")],
        )

        style.configure(
            "TEntry",
            padding=6,
            fieldbackground=c["surface"],
            foreground=c["text"],
            insertcolor=c["accent"],
            bordercolor=c["border"],
            lightcolor=c["border"],
            darkcolor=c["border"],
        )
        style.map(
            "TEntry",
            fieldbackground=[("focus", c["background"]), ("!focus", c["surface"])],
            bordercolor=[("focus", c["accent"]), ("!focus", c["border"])],
        )

        style.configure("TScrollbar", troughcolor=c["surface"], bordercolor=c["border"], arrowcolor=c["text"], gripcount=0)
        style.map("TScrollbar", background=[("active", c["accent_hover"]), ("!active", c["border"])])

    def _apply_dark_titlebar(self):
        try:
            import ctypes

            hwnd = self.root.winfo_id()
            if not hwnd:
                return

            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_20H1 = 19
            WCA_USEDARKMODECOLORS = 26

            def _dwm_set(attr):
                value = ctypes.c_int(1)
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    ctypes.c_void_p(hwnd),
                    ctypes.c_uint(attr),
                    ctypes.byref(value),
                    ctypes.sizeof(value),
                )

            try:
                _dwm_set(DWMWA_USE_IMMERSIVE_DARK_MODE)
            except Exception:
                try:
                    _dwm_set(DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_20H1)
                except Exception:
                    pass

            try:
                class WINDOWCOMPOSITIONATTRIBDATA(ctypes.Structure):
                    _fields_ = [
                        ("Attribute", ctypes.c_int),
                        ("Data", ctypes.c_void_p),
                        ("SizeOfData", ctypes.c_size_t),
                    ]

                data = ctypes.c_int(1)
                data_struct = WINDOWCOMPOSITIONATTRIBDATA(
                    Attribute=WCA_USEDARKMODECOLORS,
                    Data=ctypes.byref(data),
                    SizeOfData=ctypes.sizeof(data),
                )
                ctypes.windll.user32.SetWindowCompositionAttribute(ctypes.c_void_p(hwnd), ctypes.byref(data_struct))
            except Exception:
                pass
        except Exception:
            pass

    def _apply_icon(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(current_dir, "app.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(default=icon_path)
                try:
                    self._icon_image = tk.PhotoImage(file=icon_path)
                    self.root.iconphoto(True, self._icon_image)
                except Exception:
                    pass
        except Exception:
            pass

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

        self.sort_button.set_enabled(False)
        self.clear_button.set_enabled(False)

        thread = threading.Thread(target=self._run_sort, args=(directory,), daemon=True)
        thread.start()

    def _run_sort(self, directory):
        results = sort_files_by_extension(directory)
        self.root.after(0, self._finish_sort, results)

    def _finish_sort(self, results):
        self.sort_button.set_enabled(True)
        self.clear_button.set_enabled(True)

        self.results_text.configure(state=tk.NORMAL)
        self.results_text.insert(tk.END, results + "\n\nSorting complete!\n")
        self.results_text.see(tk.END)
        self.results_text.configure(state=tk.NORMAL)

if __name__ == "__main__":
    set_app_user_model_id()
    root = tk.Tk()
    app = FileSorterApp(root)
    root.mainloop()