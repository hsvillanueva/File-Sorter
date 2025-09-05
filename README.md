# File Sorter

A simple Python application that automatically organizes files in a directory by sorting them into folders based on their file extensions.

## Features

- **GUI Interface**: Easy-to-use graphical interface built with Tkinter
- **Automatic Sorting**: Organizes files by creating folders named after file extensions
- **Directory Browser**: Built-in directory selection dialog
- **Real-time Results**: Shows detailed results of the sorting process
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
   - If no directory is specified, the current working directory will be used

2. **Sort Files**: 
   - Click the "Sort Files" button to start the organization process

3. **View Results**: 
   - The results area will show detailed information about each file moved
   - Any errors encountered during the process will also be displayed

### Example Output

```
Sorting files in: /path/to/your/directory

Moved: document.pdf → pdf/document.pdf
Moved: image.jpg → jpg/image.jpg
Moved: music.mp3 → mp3/music.mp3
Moved: readme → no_extension/readme

Sorting complete!
```

## How It Works

The application creates subfolders within the target directory based on file extensions:

- `document.pdf` → moved to `pdf/` folder
- `image.jpg` → moved to `jpg/` folder  
- `song.mp3` → moved to `mp3/` folder
- `file_without_extension` → moved to `no_extension/` folder

**Note**: The application only processes files, not subdirectories.

## File Structure After Sorting

```
your-directory/
├── pdf/
│   ├── document1.pdf
│   └── document2.pdf
├── jpg/
│   ├── photo1.jpg
│   └── photo2.jpg
├── txt/
│   └── notes.txt
└── no_extension/
    └── README
```

## Error Handling

- **Invalid Directory**: Shows error message if specified directory doesn't exist
- **No Files**: Informs user if directory contains no files to sort
- **File Operation Errors**: Displays specific error messages for files that couldn't be moved

## Safety Features

- **Non-destructive**: Only moves files, doesn't delete or modify them
- **Folder Creation**: Automatically creates extension folders as needed using `exist_ok=True`
- **Absolute Paths**: Converts relative paths to absolute paths to avoid confusion

## Customization

The core sorting function `sort_files_by_extension()` can be used independently of the GUI:

```python
from file_sorter import sort_files_by_extension

# Sort files in a specific directory
results = sort_files_by_extension("/path/to/directory")
print(results)
```

## License

This project is open source. Feel free to modify and distribute as needed.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the application.

## Troubleshooting

**Q: The application window doesn't appear**
A: Make sure Tkinter is installed with your Python distribution. On some Linux distributions, you may need to install `python3-tk`.

**Q: Files aren't being moved**
A: Check that you have write permissions for the target directory and that the files aren't currently in use by other applications.

**Q: What happens to files without extensions?**
A: They are moved to a folder called "no_extension".
