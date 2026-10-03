# Markey

Markey is a lightweight Windows bookmark manager designed for **fast, keyboard-driven access to your saved websites**.

Each bookmark has a unique **key** (a number). Once a website is saved, you can open it by simply entering its key — without searching through a bookmark list.

## The idea

Markey has three main workflows:

### 1. Save the current page

While browsing, press:

**`Ctrl + Shift + Alt + B`**

Markey opens a save window for the current browser page. You can:

* Change the bookmark title
* Choose its key
* Add an existing tag or create a new one


### 2. Quickly open a bookmark

Press:

**`Ctrl + Shift + B`**

A small window appears asking for a bookmark key.

Enter the key and press Enter, and Markey immediately opens the corresponding website.

No bookmark list. No search. 

This is the fastest way to access bookmarks when you know their keys.

### 3. Manage and browse bookmarks

Press:

**`Ctrl + Alt + B`**

This opens the full bookmark manager.

Here you can:

* View all saved bookmarks
* Search bookmarks
* Filter by tag
* Open a bookmark by clicking it
* Edit bookmarks
* Delete bookmarks
* Enter a key to open a bookmark

Use this window when you don't remember a bookmark's key or when you want to manage your collection.

## Features

* Keyboard-driven bookmark opening
* Assignable numeric keys for bookmarks
* Quick bookmark the current browser page
* Tags for organizing bookmarks
* Edit and delete bookmarks
* System tray operation
* Full bookmark management GUI
* Browser-independent — keep one bookmark collection instead of managing separate bookmarks across browsers and profiles.

## Requirements

* Windows
* Python 3
* AutoHotkey v2

Install AutoHotkey v2 from [autohotkey.com](https://www.autohotkey.com/).

Markey checks for a bundled `AutoHotkey.exe`, then searches `PATH` and common installation folders. You do not need to copy AutoHotkey into the repository if it is installed in one of those locations.

## Install

1. Clone the repository:

   ```powershell
   git clone https://github.com/wedrik-png/Markey.git
   cd Markey
   ```

2. Create a virtual environment:

   ```powershell
   py -m venv venv
   ```

3. Install the dependencies:

   ```powershell
   venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

## Start Markey

Run `run_markey.vbs` from the repository folder.

You can double-click it in File Explorer, or launch it from PowerShell:

```powershell
wscript .\run_markey.vbs
```

The VBS launcher starts Markey using the project's virtual environment without opening a console window. Start Markey this way so its hotkeys use the correct Python environment.

Once running, Markey stays in the system tray.

Right-click the tray icon to:

* Open the bookmark manager
* Enable or disable startup
* Exit Markey

## Keyboard shortcuts

| Shortcut                 | Action                         |
| ------------------------ | ------------------------------ |
| `Ctrl + Shift + Alt + B` | Save the current browser page  |
| `Ctrl + Shift + B`       | Quickly open a bookmark by key |
| `Ctrl + Alt + B`         | Open the full bookmark manager |

## License

Markey is licensed under the MIT License. See [LICENSE](LICENSE).

## Contributing

Contributions are welcome. For substantial changes, please open an issue to discuss the proposal before submitting a pull request.
