#Requires AutoHotkey v2.0

cacheDir := A_ScriptDir "\cache_"

;txt -> array
readFileToArray(filePath) {
    arr := []
    file := FileOpen(filePath, "r", "UTF-8")
    while !file.AtEOF {
        line := Trim(file.ReadLine(), "`r`n")
        arr.Push(line)
    }
    file.Close()
    return arr
}

; Read all three files into arrays
titlesArr := readFileToArray(cacheDir "\titles.txt")
nkeysArr  := readFileToArray(cacheDir "\nkeys.txt")
linksArr  := readFileToArray(cacheDir "\links.txt")

; Create GUI with a resizable window
global MyGui := Gui("+Resize")
MyGui.Title := "Markey"


; Show an input box asking for a number (using GUI input, better to do before or in a GUI event)
Input := InputBox("Enter bookmark key:", "", "x780 y793 w260 h100")


if (!Input.Result || Input.Value = "") {
    ;MsgBox("No input provided.", "Error", 48)
    return
}

inputParts := StrSplit(Input.Value, " ")
nkey_inp := inputParts[1] + 0  ; Convert to number

;MsgBox("Input is " nkey_inp)

index_of_nkey := 0

for index, value in nkeysArr {
    if (value + 0 = nkey_inp) {  ; Ensure numeric comparison
        index_of_nkey := index
        break
    }
}

if (index_of_nkey = 0) {
    MsgBox("No bookmark found for this key")
    return
}

; Open bookmark at index
Run(linksArr[index_of_nkey])
Sleep(1000)
; Get list of all windows and activate the topmost one
id := WinGetList()
WinActivate("ahk_id " . id[1])
MyGui.Destroy()

; Optional helper function (unused in your script)
StrJoin(delimiter, arr) {
    out := ""
    for index, item in arr
        out .= (index > 1 ? delimiter : "") . item
    return out
}
