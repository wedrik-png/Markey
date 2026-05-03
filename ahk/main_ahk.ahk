#Requires AutoHotkey v2.0
#SingleInstance Force
#NoTrayIcon
+Esc::ExitApp  


SetWorkingDir A_ScriptDir

^+b::
{
    ;markeyPath := A_ScriptDir "\markey.py"
    ;Run markeyPath
    ;Run "pythonw.exe markey.py", A_ScriptDir
    Run "markey_quick.ahk"
}
^!b::
{
    Run "pythonw.exe markey.py", A_ScriptDir
}
^+!b::
{
    Send "^l"
    Sleep 30
    Send "^c"
    ClipWait 0.5

    url := A_Clipboard

    Run 'pythonw.exe addFromUI.py "' url '"'
}