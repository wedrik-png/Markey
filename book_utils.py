import json, subprocess
from dict_to_ahk_arr import write_json_to_files



book = None


def getBook(book_s):
    global book
    book = book_s

def addBook(link, title, nkey, tag = "unset"):   #add a bookmark
    global book
    for key in book.keys():
        if book[key]["link"] == link:
            print("Same website is already added!\n")
            print("Original bookmark:")
            printBook(key)
            return "error_link"
        elif title == key:
            print("A bookmark is already added with the same title\n")
            printBook(key)
            return "error_title"
        elif book[key]["nkey"] == nkey:
            print("key needs to be unique!!!\n")
            printBook(key)
            return "error_nkey"
    max_index = 0
    for key in book.keys():
        if book[key]["index"] > max_index:
            max_index = book[key]["index"]

    book[title] = {"link": link, "nkey": nkey, "tag": tag, "index": (max_index+1)}
    overwriteBook()





def deleteBook(x):
    if x in book.keys():
        rem = book[x]
        del book[x]
        print("Bookmark deleted! --", rem)
    elif isinstance(x, int):    
        for key in book.keys():
            if book[key]["nkey"] == x:
                rem = book[key]
                del book[key]
                print("Bookmark deleted! --", rem)
                return
        print("No bookmark with that key!")
    overwriteBook()


    
def overwriteBook():        #overwrite the json
    with open("bookmarks.json", "w") as f:
        json.dump(book, f, indent=4)
    write_json_to_files(book)



def printBook(key):
    print(key, ' ',  book[key]["link"], ' ', book[key]["nkey"], ' ', book[key]["tag"])

def openBook(key):
    toOpen = book[key]["link"]
    subprocess.Popen(f"start {toOpen}", shell = True)

def editBook(key, updatedKey, updatedNKey, updatedTag):
    global book
    link = book[key]["link"]
    
    if key == updatedKey and book[key]["nkey"] == updatedNKey and book[key]["tag"] == updatedTag:
        return "no_change"
    else:
        del book[key]
        return_from_addBook = addBook(link, updatedKey, updatedNKey, updatedTag)
        if return_from_addBook == "error_nkey": 
            return "error_nkey"
        elif return_from_addBook == "error_key":
            return "error_key"
        