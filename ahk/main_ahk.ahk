#Requires AutoHotkey v2.0
#SingleInstance Force
#NoTrayIcon
+Esc::ExitApp  


SetWorkingDir A_ScriptDir "\.."

^+b::
{
    ;markeyPath := A_ScriptDir "\markey.py"
    ;Run markeyPath
    ;Run "pythonw.exe markey.py", A_ScriptDir
    Run A_ScriptDir "\markey_quick.ahk"
}
^!b::
{
    Run '"pythonw.exe" "src\markey.py"'
}
^+!b::
{
    Send "^l"
    Sleep 1000
    Send "^c"
    ClipWait

    url := A_Clipboard

    Run 'pythonw.exe src/addFromUI.py "' url '"'
}