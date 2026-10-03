import subprocess, os, sys, shutil, threading, json, winreg
from pathlib import Path

app_dir = Path(__file__).parent.absolute()
os.chdir(app_dir)
sys.path.insert(0, str(app_dir))

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
import win32com.client   
from PyQt5.QtWidgets import QApplication
from src.markey import MyApp as MarkeyWindow
#from addFromUI import MyApp_2, getLink
from PyQt5.QtCore import Qt
from src.dict_to_ahk_arr import load_bookmarks, write_json_to_files

book = load_bookmarks()
write_json_to_files(book)

pythonw = Path(sys.executable)
if pythonw.name.lower() == "python.exe":
    candidate = pythonw.with_name("pythonw.exe")
    if candidate.exists():
        pythonw = candidate
ahk_exe = app_dir / "AutoHotkey.exe"
ahk_script = app_dir / "ahk" / "main_ahk.ahk"
subprocess.Popen([str(ahk_exe), str(ahk_script), str(pythonw)], cwd=str(app_dir))

def runScript(path):
    subprocess.Popen([sys.executable, path])

"""
def open_addfromui():
    link = getLink()
    uw = MyApp_2(book, link)
    uw.setWindowFlags(uw.windowFlags() | Qt.WindowStaysOnTopHint)
    uw.show()
    uw.raise_()
    uw.activateWindow()
"""



def main():
        STARTUP_SHORTCUT_NAME = "Markey.lnk"
        STARTUP_APPROVED_KEY = r"Software\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\StartupFolder"
        LEGACY_STARTUP_NAMES = ("TrayAppShortcut.lnk",)

        def startup_folder():
            return os.path.join(os.environ["APPDATA"], r"Microsoft\Windows\Start Menu\Programs\Startup")

        def get_startup_shortcut_path(name=STARTUP_SHORTCUT_NAME):
            return os.path.join(startup_folder(), name)

        def is_startup_enabled():
            return os.path.exists(get_startup_shortcut_path())

        def set_startup_approved(enabled):
            # Task Manager's Enabled/Disabled flag lives here, separate from the .lnk file
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, STARTUP_APPROVED_KEY)
            try:
                names = (STARTUP_SHORTCUT_NAME,) + LEGACY_STARTUP_NAMES
                if enabled:
                    winreg.SetValueEx(
                        key,
                        STARTUP_SHORTCUT_NAME,
                        0,
                        winreg.REG_BINARY,
                        bytes([0x02, 0x00, 0x00, 0x00]) + b"\x00" * 8,
                    )
                else:
                    for name in names:
                        try:
                            winreg.DeleteValue(key, name)
                        except FileNotFoundError:
                            pass
            finally:
                winreg.CloseKey(key)

        def enable_startup():
            for name in LEGACY_STARTUP_NAMES:
                legacy = get_startup_shortcut_path(name)
                if os.path.exists(legacy):
                    os.remove(legacy)

            shortcut_path = get_startup_shortcut_path()

            # Detect path of currently running file (exe or py)
            target = sys.executable  # If .py → python.exe; if .exe → yourapp.exe
            # Prefer pythonw so a console does not appear on login
            if target.lower().endswith("python.exe"):
                pythonw = os.path.join(os.path.dirname(target), "pythonw.exe")
                if os.path.exists(pythonw):
                    target = pythonw
            script = os.path.abspath(sys.argv[0])  # Actual script or exe file

            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(shortcut_path)

            # If it's a .py script → use python.exe + script.py
            # If it's an .exe → target *is* the app, no extra script argument needed
            if script.endswith(".py") or script.endswith(".pyw"):
               shortcut.Targetpath = target
               shortcut.Arguments = f'"{script}"'
            else:
               shortcut.Targetpath = script
               shortcut.Arguments = ""  # No need to add anything

            shortcut.WorkingDirectory = os.path.dirname(script)
            icon = os.path.join(os.path.dirname(script), "icon_markey_tray.ico")
            shortcut.IconLocation = icon if os.path.exists(icon) else target
            shortcut.Description = "Markey"
            shortcut.save()
            set_startup_approved(True)

        def disable_startup():
            for name in (STARTUP_SHORTCUT_NAME,) + LEGACY_STARTUP_NAMES:
                shortcut_path = get_startup_shortcut_path(name)
                if os.path.exists(shortcut_path):
                    os.remove(shortcut_path)
            set_startup_approved(False)

        def toggle_startup():
            if startup_action.isChecked():
                enable_startup()
            else:
                disable_startup()

        def close_app():
            try:
                subprocess.run(["taskkill", "/f", "/im", "main_ahk.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception:
                pass
            sys.exit()
        
        print("Working directory: ", os.getcwd())
        app = QApplication([])
        app.setQuitOnLastWindowClosed(False)
        icon = QIcon("icon_markey_tray.ico")
        tray = QSystemTrayIcon(icon)
        tray.setToolTip("Markey")

        #initiate a QMenu
        menu = QMenu()

        markey_action = QAction("Open Bookmarks")
        startup_action = QAction("Run on Startup")
        startup_action.setCheckable(True)
        startup_action.setChecked(is_startup_enabled())
        exit_action = QAction("Exit")

        menu.addAction(markey_action)
        menu.addAction(startup_action)
        menu.addAction(exit_action)

        tray.setContextMenu(menu)
        tray.show()

        markey_action.triggered.connect(lambda: runScript("src/Markey.py"))
        startup_action.triggered.connect(toggle_startup)
        exit_action.triggered.connect(close_app)

        #keyboard.add_hotkey("ctrl+shift+alt+B", lambda: runScript("markey.py"))
        #keyboard.add_hotkey("ctrl+shift+B", lambda: runScript("addFromUI.py"))
        
        app.exec_()
        


#keyboard.add_hotkey("ctrl+shift+alt+B", lambda: runScript("markey.py"))
#keyboard.add_hotkey("ctrl+shift+B", lambda: runScript("addFromUI.py"))

if __name__ == "__main__":
    main()
