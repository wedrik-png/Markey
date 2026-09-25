#Requires AutoHotkey v2.0
#SingleInstance Force
#NoTrayIcon
+Esc::ExitApp

root := A_ScriptDir "\.."
SetWorkingDir root

pythonw := A_Args.Length >= 1 ? A_Args[1] : root "\venv\Scripts\pythonw.exe"
if !FileExist(pythonw) {
    MsgBox "Markey could not find pythonw.exe at:`n" pythonw "`n`nStart Markey with run_markey.vbs so the venv is used.", "Markey", 16
    ExitApp
}

RunPython(script, extraArgs := "") {
    global pythonw, root
    cmd := '"' pythonw '" "' root "\" script '"'
    if extraArgs != ""
        cmd .= " " extraArgs
    Run cmd, root
}

^+b::
{
    Run A_ScriptDir "\markey_quick.ahk"
}
^!b::
{
    RunPython("src\markey.py")
}
^+!b::
{
    Send "^l"
    Sleep 200
    Send "^c"
    if !ClipWait(1) {
        MsgBox "Could not copy the page address. Click the browser first, then try again.", "Markey", 48
        return
    }
    url := Trim(A_Clipboard)
    url := StrReplace(url, '"', '\"')
    RunPython("src\addFromUI.py", '"' url '"')
}