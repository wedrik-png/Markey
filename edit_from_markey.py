import pyperclip, time, json, book_utils, sys
from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QSpinBox, QComboBox, QApplication, QHBoxLayout, QPushButton, QMessageBox, QDialog
from PyQt5.QtCore import Qt

with open("bookmarks.json", "r") as f:    #load the json
    book = json.load(f)
book_utils.getBook(book)

class MyApp_3(QDialog):
    def __init__(self, book, key_to_edit): 
        super().__init__()

        self.key_to_edit = key_to_edit

        self.setWindowTitle("Edit bookmark")
        self.setGeometry(500, 500, 400, 100)
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)

        layout = QFormLayout()

        #title
        self.title_input = QLineEdit()    
        self.title_input.setText(key_to_edit)
        self.title_input.selectAll()

        #link
        self.nkey_input = QSpinBox()
        self.nkey_input.setValue(book[key_to_edit]["nkey"])

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
        self.tag_dropdown.setCurrentText(book[key_to_edit]["tag"])
        
       
        #add tag button
        self.tag_button = QPushButton("+")
        self.tag_button.setFixedSize(24, 24)
        self.tag_button.clicked.connect(self.show_input_box)

        #save and cancel button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.add_to_editBook)
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
            self.add_to_editBook();
        elif event.key() == Qt.Key_Escape:
            self.exit_app()

    def show_error(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error")
        msg.setText(message)
        msg.exec_()

    def add_to_editBook(self):
        title = self.title_input.text()
        nkey = self.nkey_input.value()

        if self.tag_input.isVisible() and self.tag_input.text().strip():
          tag = self.tag_input.text().strip()
        else:
            tag = self.tag_dropdown.currentText()

        error_edit = book_utils.editBook(self.key_to_edit, title, nkey, tag)
        if error_edit == "no_change":
            self.show_error("No change")
        elif error_edit == "error_key":
            self.show_error("Error: title already exists")
        elif error_edit == "error_nkey":
            self.show_error("Error: nkey already exists")
        else:
            
            self.close()
        
        
"""
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp_3(book, key_to_edit="")
    window.show()
    window.activateWindow()
    window.raise_()
    window.setWindowState(window.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
    sys.exit(app.exec_())
"""