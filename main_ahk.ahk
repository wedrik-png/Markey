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
    Run "pythonw.exe addFromUI.py", A_ScriptDir
}