import keyboard, subprocess, os, sys, shutil, threading, json
from pathlib import Path
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
import win32com.client
from PyQt5.QtWidgets import QApplication
from markey import MyApp as MarkeyWindow
from addFromUI import MyApp_2, getLink
from PyQt5.QtCore import Qt
from dict_to_ahk_arr import write_json_to_files

with open("bookmarks.json") as f: #load json
    book = json.load(f)


write_json_to_files(book)

subprocess.Popen(["AutoHotkey.exe", "main_ahk.ahk"], shell=True)
app_dir = Path(__file__).parent.absolute()
os.chdir(app_dir)

def runScript(path):
    subprocess.Popen(["python", path], shell = True)
    #subprocess.Popen([sys.executable, path], 
                #creationflags=subprocess.DETACHED_PROCESS)
    #subprocess.Popen(["launch_markey.bat"], shell=True)



def open_addfromui():
    link = getLink()
    uw = MyApp_2(book, link)
    uw.setWindowFlags(uw.windowFlags() | Qt.WindowStaysOnTopHint)
    uw.show()
    uw.raise_()
    uw.activateWindow()



def main():
        def get_startup_shortcut_path():
            startup_folder = os.path.join(os.environ["APPDATA"], r"Microsoft\Windows\Start Menu\Programs\Startup")
            return os.path.join(startup_folder, "TrayAppShortcut.lnk")

        def is_startup_enabled():
            return os.path.exists(get_startup_shortcut_path())

        def enable_startup():
            shortcut_path = get_startup_shortcut_path()

            # Detect path of currently running file (exe or py)
            target = sys.executable  # If .py → python.exe; if .exe → yourapp.exe
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
            shortcut.IconLocation = script
            shortcut.save()

        def disable_startup():
            shortcut_path = get_startup_shortcut_path()
            if os.path.exists(shortcut_path):
                os.remove(shortcut_path)

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
        icon = QIcon("icon2.ico")
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

        markey_action.triggered.connect(lambda: runScript("Markey.py"))
        startup_action.triggered.connect(toggle_startup)
        exit_action.triggered.connect(close_app)

        #keyboard.add_hotkey("ctrl+shift+alt+B", lambda: runScript("markey.py"))
        #keyboard.add_hotkey("ctrl+shift+B", lambda: runScript("addFromUI.py"))
        
        app.exec_()
        


#keyboard.add_hotkey("ctrl+shift+alt+B", lambda: runScript("markey.py"))
#keyboard.add_hotkey("ctrl+shift+B", lambda: runScript("addFromUI.py"))

if __name__ == "__main__":
    main()
