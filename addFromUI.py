import pyautogui as pg
import pygetwindow, sys
import pyperclip, time, json, book_utils
from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QSpinBox, QComboBox, QApplication, QHBoxLayout, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

with open("bookmarks.json", "r") as f:    #load the json
    book = json.load(f)

book_utils.getBook(book)

def getDefaultKey(book):
    used = {book[k]["nkey"] for k in book}
    i = 1
    while i in used:
        i += 1
    return i


        

def getTitle(): #get title from window title
    titl = str(pygetwindow.getActiveWindow().title)
    if "- Brave" in titl:
        titl = titl.replace("- Brave", "")
    elif "- Chrome" in titl:
        titl = titl.replace("- Chrome", "")
    elif "- Firefox" in titl:
        titl = titl.replace("- Firefox", "")
    return titl


def getLink(): #get link using pyautoGUI
    #time.sleep(0.2)
    pg.hotkey("alt", "d")
    time.sleep(0.1)
    pg.hotkey("ctrl", "c")
    time.sleep(0.1)
    pg.press('esc')
    return pyperclip.paste()

#Window for save bookmark added from UI
class MyApp_2(QWidget):
    def __init__(self, book, link_str): 
        super().__init__()

        self.setWindowTitle("Save bookmark")
        self.setGeometry(500, 500, 400, 100)

        layout = QFormLayout()

        #title
        self.title_input = QLineEdit()    
        self.title_input.setText(getTitle())
        self.title_input.selectAll()

        #link
        self.nkey_input = QSpinBox()
        self.nkey_input.setValue(getDefaultKey(book))

        #tag (add new tag)
        self.tag_input = QLineEdit()
        self.tag_input.setPlaceholderText("Create new tag")
        self.tag_input.hide()

        #tag dropdown
        self.tag_dropdown = QComboBox()
        seen_tags = set()
        for key in book.keys():
            
            if book[key]["tag"] not in seen_tags:
                self.tag_dropdown.addItem(book[key]["tag"])
                seen_tags.add(book[key]["tag"])
        self.tag_dropdown.addItem("other")
        self.tag_dropdown.setCurrentText("other")
        
       
        #add tag button
        self.tag_button = QPushButton("+")
        self.tag_button.setFixedSize(24, 24)
        self.tag_button.clicked.connect(self.show_input_box)

        #save and cancel button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.add_to_addBook)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.exit_app)

        #container for save and cancel
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.save_button)
        button_container = QWidget()
        button_container.setLayout(button_layout)

        #container for tag dropdown and add tag
        tag_layout = QHBoxLayout()
        tag_layout.addWidget(self.tag_dropdown, stretch = 1)
        tag_layout.addWidget(self.tag_input, stretch=1)
        tag_layout.addWidget(self.tag_button)
        tag_container = QWidget()
        tag_container.setLayout(tag_layout)

        #add to layout
        layout.addRow("Title: ", self.title_input)
        layout.addRow("key: ", self.nkey_input)
        layout.addRow("Tag: ", tag_container)
        layout.addRow("", button_container)

        self.setLayout(layout)

    def show_input_box(self): #show tag input
        self.tag_dropdown.hide()
        self.tag_input.show()
        self.tag_input.setFocus()

    def exit_app(self):
        self.close()

    def keyPressEvent(self, event): #enter - save, esc - cancel
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.add_to_addBook();
        elif event.key() == Qt.Key_Escape:
            self.exit_app()
        

    def add_to_addBook(self):
        title = self.title_input.text()
        nkey = self.nkey_input.value()

        if self.tag_input.isVisible() and self.tag_input.text().strip():
          tag = self.tag_input.text().strip()
        else:
            tag = self.tag_dropdown.currentText()
            
        #if addBook returns error values
        error_state = book_utils.addBook(link = link_str, title=title, nkey=nkey, tag=tag)
        if error_state == "error_link":
            for key in book:
                if book[key]["link"] == link_str:
                    titleOfCommonLink = key
                    nkeyOfCommonLink = book[key]["nkey"]
                    break
            self.show_error(f"Error: This website is already saved with title {titleOfCommonLink} and key: {nkeyOfCommonLink}")
        
        elif error_state == "error_title":
            for key in book:
                if key == title:
                    linkOfCommonTitle = book[key]["link"]
                    nkeyOfCommonTitle = book[key]["nkey"]
                    break
            self.show_error(f"Error: This title is already used for the address {linkOfCommonTitle} and key: {nkeyOfCommonTitle}")
        elif error_state == "error_nkey":
            for key in book:
                if book[key]["nkey"] == nkey:
                    titleOfCommonNkey = key
                    linkOfCommonNkey = book[key]["link"]
                    break
            self.show_error(f"Error: The key is already used for {titleOfCommonNkey} ({linkOfCommonNkey})")
        else:
            self.close()
            
    def show_error(self, message):
       msg = QMessageBox()
       msg.setIcon(QMessageBox.Critical)
       msg.setWindowTitle("Error")
       msg.setText(message)
       msg.exec_()


link_str = str(getLink())
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp_2(book, link_str)
    window.show()
    window.activateWindow()
    window.raise_()
    window.setWindowState(window.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
    sys.exit(app.exec_())