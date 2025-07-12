#Requires AutoHotkey v2.0
#SingleInstance Force
+Esc::ExitApp   


; ======= AUTO-CONFIG SYSTEM =======
; ======= CLEAN CONFIG SECTION FOR ZIP DISTRIBUTION =======

; All files are assumed to be in the same folder as the .exe
user_folder := A_ScriptDir

; Define file paths
title_txt := user_folder "\title.txt"
address_txt := user_folder "\address.txt"
counter_txt := user_folder "\counter.txt"

; Optional: Verify the required files exist — warn if missing
;missing := ""
;for file in [title_txt, address_txt, counter_txt] {
;    if !FileExist(file)
;        missing .= file "`n"
;}
;if (missing != "") {
;    MsgBox "The following required file(s) are missing:`n" missing "`nPlease re-download the full zip folder.", "Missing Files", 48
;    ExitApp
;}

; ======= END CONFIG SYSTEM =======

^+!b::
{
    ; Initialize variables
    x := "Heck"
    texty := FileOpen(title_txt, "r")

    ; Create GUI with a resizable window
    global MyGui := Gui("+Resize")
    MyGui.Title := "Bookmarks List"

    ; Add a Search Bar
    SearchBar := MyGui.Add("Edit", "w700 vSearchBar")
    SearchBar.OnEvent("Change", SearchList)

    ; Add a ListView
    LV := MyGui.Add("Listview", "Grid -Hdr r20 w700 vMyListView", ["Index"])

    ; Read each line from the texty and add it to the ListView
    while (x != "")
    {
        x := texty.ReadLine()
        if (x != "")
            LV.Add(, x)
    }

    ; Set the column width
    LV.ModifyCol(1, 500)

    ; Show the GUI
    MyGui.Show

    {
        ; Show an input box asking for a number
       Input := InputBox("Enter the number to open, or `n<number> delete` to delete:", "", "x780 y793 w260 h100")
if !Input.Result or Input.Value = ""
{
    MsgBox "No input provided.", "Error", 48
    return
}

inputParts := StrSplit(Input.Value, " ")
index := inputParts[1] + 0
doDelete := (inputParts.Length > 1 && Trim(inputParts[2]) = "delete")

titles := StrSplit(FileRead(title_txt), "`n", "`r")
addresses := StrSplit(FileRead(address_txt), "`n", "`r")

; Cleanup any trailing empties
;titles := titles.filter((line) => line != "")
;addresses := addresses.filter((line) => line != "")

if (index < 1 || index > titles.Length)
{
    MsgBox "Invalid bookmark number: " index, "Error", 48
    return
}

if doDelete
{
    ; Delete bookmark at index
    titles.RemoveAt(index)
    addresses.RemoveAt(index)
    FileDelete(title_txt)
    FileDelete(address_txt)
    newTitles := []
j := 1  ; fresh counter for valid (non-empty) lines

for _, title in titles
{
    cleanTitle := RegExReplace(title, "^\d+\.\s*", "")
    if Trim(cleanTitle) != ""
    {
        newTitles.Push(j ". " cleanTitle)
        j++
    }
}
; After renumbering and rewriting title_txt
FileDelete(counter_txt)
FileAppend(j - 1, counter_txt)  ; j was last used index + 1


FileAppend(Trim(StrJoin("`n", newTitles)), title_txt)

    FileAppend(Trim(StrJoin("`n", addresses)), address_txt)

    MsgBox "Bookmark #" index " deleted successfully!"
}
else
{
    ; Open bookmark at index
    Run addresses[index]
}
MyGui.Destroy()

    }
}

SearchList(*) {
    global MyGui
    SearchBarText := MyGui.Submit(false).SearchBar
    LV := MyGui["MyListView"]

    LV.Modify(0, "-Select")  ; Clear previous selection

    Loop LV.GetCount()
    {
        LVText := LV.GetText(A_Index)
        if InStr(LVText, SearchBarText)
        {
            LV.Modify(A_Index, "Select")  ; Highlight the match
            LV.Modify(A_Index, "Vis")     ; Scroll to the match
            break  ; Stop after first match
        }
    }
} 
^+b::
{
i := 0
Sleep 100
Send "!d"
Sleep 100
Send "^c"
Sleep 100
Result := InputBox("Enter the title", "Bookmark website")
fbook := FileOpen(address_txt, "a")
fhelper := FileOpen(title_txt, "a")
Title := Result.Value


{
fcounter := FileOpen(counter_txt, "rw")
fcounter.Seek(0)
i2 := fcounter.ReadLine()
i2 := i2+0
i2 := i2+1
fcounter.Seek(0)
fcounter.Write(i2)
;Msgbox "i2 = " i2
}

Appendtxtb := A_Clipboard . "`n"
Appendtxth := i2 . ". " . Title . "`n"
fbook.Write(Appendtxtb)
fhelper.Write(Appendtxth)
Msgbox "Saved! " . i2*1 . " " . Title . " " . A_Clipboard
A_Clipboard := ""
}

StrJoin(delimiter, arr) {
    out := ""
    for index, item in arr
        out .= (index > 1 ? delimiter : "") . item
    return out
}
