# File Sorter

A simple Python application that automatically organizes files in a directory by sorting them into folders based on their file extensions.

## Features

- **GUI Interface**: Has an interface that displays the contents of the folder after sorting and which folder each file was moved to.
- **Automatic Sorting**: Organizes files by creating folders named after file extensions
- **Directory Browser**: Built-in directory selection dialog
- **Error Handling**: Gracefully handles missing directories and file operation errors
- **No Extension Support**: Files without extensions are placed in a "no_extension" folder

## Requirements

- Python 3.x
- Tkinter (usually included with Python)
- Standard library modules: `os`, `shutil`

## Installation

1. Clone or download the repository
2. Ensure you have Python 3.x installed
3. No additional dependencies required - uses only standard library modules

## Usage

### Running the Application

```bash
python "file sorter.py"
```

### Using the GUI

1. **Select Directory**: 
   - Enter a directory path manually in the text field, or
   - Click "Browse" to select a directory using the file dialog
   - If no directory is specified, the current directory of the file will be used

2. **Sort Files**: 
   - Click the "Sort Files" button to start the organization process

3. **View Results**: 
   - The results area will show detailed information about each file moved
   - Any errors encountered during the process will also be displayed

### Example Output

```
Sorting files in: /path/directory

Moved: document.pdf → pdf/document.pdf
Moved: image.jpg → jpg/image.jpg
Moved: music.mp3 → mp3/music.mp3
Moved: readme → no_extension/readme

Sorting complete!
```
