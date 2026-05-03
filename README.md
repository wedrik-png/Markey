# Markey

Markey is a lightweight bookmark manager that combines Python and AutoHotkey to quickly add, list, and open bookmarks without leaving your workflow.  
Originally built entirely in AutoHotkey, the latest version has been mostly rewritten in Python for better performance and more features.

---

## ✨ Features
- **Quick Bookmarking** — Add bookmarks instantly via a hotkey.
- **Organization** — Choose or create new tags while bookmarking for better organization.
- **Fast Access** — Search and open bookmarks directly from a tray menu or hotkey. Filter by tags.
- **Lightweight & Portable** — No heavy database or server required.
- **Open with key** - A unique feature that lets you open a bookmark in a second.

---

## 📦 Installation

---

## For general users
If you just want to **use** Markey without touching the code:

1. **Download the latest release** from the [Releases page](https://github.com/Markey/releases).
2. Extract the downloaded zip.
3. Run `main.exe`
4. Enjoy fast, simple bookmark management from your system tray.

> No installation required — Markey is fully portable.

---
## For developers

### 1. Clone the Repository
```bash
git clone https://github.com/wedrik-png/Markey.git
cd Markey
```
### 2. Create virtual environment

```bash
python -m create venv venv
venv/Scripts/activate
```

### 2. Install Python Requirements
```bash
pip install -r requirements.txt
```

### 3. Install AutoHotkey v2
- Download from: [https://www.autohotkey.com/](https://www.autohotkey.com/)

---

## 🚀 Usage

### **1. Start the Main App**
```bash
python main.pyw
```
Or, if you’re using the compiled `.exe` from the [Releases page](https://github.com/Markey/releases)., just run:
```
Main.exe
```

### **2. Hotkeys**
- **Add Bookmark** → `Ctrl + Shift + Alt + B`
- **Open Bookmark (quick: only uses the key)** → `Ctrl + Shift + B`
  - **Open with key** → On adding a bookmark, you choose a *key* (a number) for that website. You can launch it quickly by triggering the hotkey and entering the corresponding key.
- **Open Bookmark (detailed: preferred for managing bookmarks)** → `Ctrl + Alt + B`  
   - **Search bar** → Search for a bookmark  
   - **Filter by tag** → Quickly filter the bookmark list by a specific tag  
   - **Edit/delete bookmark** → Right clicking a bookmark opens menu to edit a bookmark  
   - **Open with key** → same feature as the quick mode
*(You can change them in the `.ahk` script.)*


## 📄 License
This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## 🤝 Contributing
Pull requests are welcome!  
For major changes, please open an issue first to discuss what you’d like to change.

---

## 💬 Contact
Created by **Manan Juneja**  
GitHub: [https://github.com/wedrik-png](https://github.com/wedrik-png)
