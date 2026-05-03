# Markey

Markey is a lightweight bookmark manager that combines Python and AutoHotkey to quickly add, search, and open bookmarks without leaving your workflow.
Originally built entirely in AutoHotkey, it has now been largely rewritten in Python for better performance and scalability.

---

## ✨ Features

* **Quick Bookmarking** — Add bookmarks instantly using a hotkey
* **Tag Organization** — Assign or create tags while bookmarking
* **Fast Access** — Search and open bookmarks via hotkeys or menu
* **Open with Key** — Launch bookmarks instantly using numeric keys
* **Lightweight & Portable** — No database or server required

---

## 📦 Installation

### For General Users

If you just want to use Markey:

1. Download the latest release from the
   https://github.com/wedrik-png/Markey/releases
2. Extract the ZIP file
3. Run `main.exe`
4. Start using Markey from the system tray

> No installation required — fully portable.

---

### For Developers

#### 1. Clone the Repository

```bash
git clone https://github.com/wedrik-png/Markey.git
cd Markey
```

#### 2. Create a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Install AutoHotkey v2

Download from: https://www.autohotkey.com/

---

## 🚀 Usage

### Start the Application

```bash
python main.pyw
```

Or run the compiled executable:

```
main.exe
```

---

## ⌨️ Hotkeys

* **Add Bookmark** → `Ctrl + Shift + Alt + B`
* **Quick Open (Key-based)** → `Ctrl + Shift + B`
* **Full Manager View** → `Ctrl + Alt + B`

### Features in Manager View

* Search bookmarks
* Filter by tag
* Right-click to edit/delete
* Open bookmarks using assigned keys

---

## 📄 License

Licensed under the MIT License — see [LICENSE](LICENSE)

---

## 🤝 Contributing

Pull requests are welcome.
For major changes, open an issue first to discuss your ideas.

---

## 💬 Contact

Created by Manan Juneja
GitHub: https://github.com/wedrik-png
