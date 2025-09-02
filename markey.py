import sys, json, subprocess, os, ctypes
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QLineEdit,
    QMessageBox, QVBoxLayout, QWidget, QListWidget, QMenu,
    QHBoxLayout, QComboBox
)
import book_utils
from PyQt5.QtCore import Qt, QTimer
from edit_from_markey import MyApp_3
import win32gui, win32con
from dict_to_ahk_arr import write_json_to_files



print(os.getcwd())

with open("bookmarks.json", "r") as f:    #load the json
    book = json.load(f)
book_utils.getBook(book)
write_json_to_files(book)


def on_item_clicked(item):  #Open the website on clicking
    global keyClicked
    keyClicked = item.text()
    book_utils.openBook(keyClicked)
    print("OPENED")

class MyApp(QMainWindow):
    def __init__(self, book):
        super().__init__()
        self.book = book
        self.original_book = book.copy()  # Keep original for resetting filters

        self.setWindowTitle("Markey")
        self.resize(1000, 650)         
        self.setMinimumSize(400, 500)  
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        


        layout = QVBoxLayout()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Search and filter section
        search_layout = QHBoxLayout()
        
        # Search box
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search bookmarks...")
        self.search_input.textChanged.connect(self.filter_bookmarks)
        
        # Tag filter dropdown
        self.tag_filter = QComboBox()
        self.populate_tag_filter()
        self.tag_filter.currentTextChanged.connect(self.filter_bookmarks)
        
        # Clear filters button
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_filters)
        
        search_layout.addWidget(QLabel("Search:"))
        search_layout.addWidget(self.search_input, stretch=2)
        search_layout.addWidget(QLabel("Tag:"))
        search_layout.addWidget(self.tag_filter, stretch=1)
        search_layout.addWidget(self.clear_button)
        
        search_widget = QWidget()
        search_widget.setLayout(search_layout)

        open_key_layout = QHBoxLayout()
        self.key_input = QLineEdit()
        self.open_key_button = QPushButton("Open by key")
        self.open_key_button.clicked.connect(self.open_with_key)
        self.key_input.returnPressed.connect(self.open_with_key)
        
        

        open_key_layout.addWidget(self.key_input)
        open_key_layout.addWidget(self.open_key_button)

        open_key_widget = QWidget()
        open_key_widget.setLayout(open_key_layout)



        # Create a scrollable, clickable list
        self.list = QListWidget()
        self.populate_list(self.book)
        
        self.list.itemClicked.connect(on_item_clicked)
        self.list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list.customContextMenuRequested.connect(self.show_context_menu)

        layout.addWidget(open_key_widget)
        layout.addWidget(search_widget)
       
        layout.addWidget(self.list)
       
        
        central_widget.setLayout(layout)

        self.list.setStyleSheet("""
    QListWidget {
        font-size: 14px;
        padding: 4px;
    }
    QListWidget::item:selected {
        background-color: #87CEFA;  /* light blue */
        color: black;
    }
    QListWidget::item:hover {
        background-color: #E6F0FF;  /* very light blue */
    }
""")
        self.list.setAlternatingRowColors(True)


    def populate_tag_filter(self):
        """Populate the tag filter dropdown with unique tags"""
        self.tag_filter.clear()
        self.tag_filter.addItem("All Tags")  # Default option
        
        # Get unique tags
        unique_tags = set()
        for key in self.original_book.keys():
            unique_tags.add(self.original_book[key]["tag"])
        
        for tag in sorted(unique_tags):
            self.tag_filter.addItem(tag)

    def populate_list(self, book_data):
        """Populate the list widget with bookmarks"""
        self.list.clear()
        for key in book_data.keys():
            self.list.addItem(key)

    def filter_bookmarks(self):
        """Filter bookmarks based on search text and selected tag"""
        search_text = self.search_input.text().lower()
        selected_tag = self.tag_filter.currentText()
        
        filtered_book = {}
        
        for key, value in self.original_book.items():
            # Check if bookmark matches search criteria
            matches_search = (
                search_text == "" or 
                search_text in key.lower() or 
                search_text in value["link"].lower() or
                search_text in value["tag"].lower()
            )
            
            # Check if bookmark matches tag filter
            matches_tag = (
                selected_tag == "All Tags" or 
                value["tag"] == selected_tag
            )
            
            if matches_search and matches_tag:
                filtered_book[key] = value
        
        self.populate_list(filtered_book)
        self.book = filtered_book  # Update current working book
        
        # Update status (optional - shows count)
        self.setWindowTitle(f"Markey - {len(filtered_book)} bookmarks")

    def clear_filters(self):
        """Clear all filters and show all bookmarks"""
        self.search_input.clear()
        self.tag_filter.setCurrentText("All Tags")
        self.populate_list(self.original_book)
        self.book = self.original_book.copy()
        self.setWindowTitle("Markey")

    # Add this method inside the MyApp class
    def open_with_key(self):
        try:
            nkey_str = self.key_input.text()
            if not nkey_str:
                return # Do nothing if input is empty

            nkey = int(nkey_str)
            title_to_open = None
            for title, data in self.original_book.items():
                if data["nkey"] == nkey:
                    title_to_open = title
                    break

            if title_to_open:
               book_utils.openBook(title_to_open)
               self.close()
               self.key_input.clear() # Clear the input after opening
            else:
              QMessageBox.warning(self, "Error", f"No bookmark found with key: {nkey}")
        except ValueError:
              QMessageBox.warning(self, "Error", "Please enter a valid number for the key.")

    def show_context_menu(self, position):
        item = self.list.itemAt(position)

        if item:
            menu = QMenu()

            open_action = menu.addAction("Open")
            delete_action = menu.addAction("Delete")
            edit_action = menu.addAction("Edit")
            

            action = menu.exec_(self.list.mapToGlobal(position))

            if action == open_action:
                book_utils.openBook(item.text())
            elif action == delete_action:
                # Delete from original book as well
                if item.text() in self.original_book:
                    book_utils.deleteBook(item.text())
                    del self.original_book[item.text()]
                
                # Remove from current view
                self.list.takeItem(self.list.row(item))
                if item.text() in self.book:
                    del self.book[item.text()]
                
                # Refresh tag filter in case this was the last bookmark with this tag
                self.populate_tag_filter()
            elif action == edit_action:      #Open the bookmark in the editor
                self.edit_window = MyApp_3(book, item.text())
                self.edit_window.setWindowFlags(window.windowFlags() | Qt.WindowStaysOnTopHint)                     
                self.edit_window.raise_()
                self.edit_window.activateWindow()
                self.edit_window.exec_()
                self.repaint()
                with open("bookmarks.json", "r") as f:
                    self.original_book = json.load(f)
                    self.book = self.original_book.copy()

                # Refresh tag filter and list
                self.populate_tag_filter()
                self.populate_list(self.book)
           
           
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp(book)
    window.setWindowFlags(window.windowFlags() | Qt.WindowStaysOnTopHint)
    window.show()
    window.raise_()
    window.activateWindow()

    #hwnd = int(window.winId())
    #win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
    #win32gui.SetForegroundWindow(hwnd) 

    sys.exit(app.exec_())



