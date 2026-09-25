Option Explicit
' Starts Markey with the project venv (no console). Double-click this file.

Dim fso, sh, dir, pythonw, script
Set fso = CreateObject("Scripting.FileSystemObject")
Set sh = CreateObject("WScript.Shell")
dir = fso.GetParentFolderName(WScript.ScriptFullName)
pythonw = dir & "\venv\Scripts\pythonw.exe"
script = dir & "\main.pyw"

If Not fso.FileExists(pythonw) Then
  MsgBox "venv not found at:" & vbCrLf & pythonw & vbCrLf & vbCrLf & _
         "In this folder run:" & vbCrLf & _
         "  python -m venv venv" & vbCrLf & _
         "  venv\Scripts\activate" & vbCrLf & _
         "  pip install -r requirements.txt", 16, "Markey"
  WScript.Quit 1
End If

sh.CurrentDirectory = dir
sh.Run """" & pythonw & """ """ & script & """", 0, False
