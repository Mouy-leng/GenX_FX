' A6-9V Silent Launcher for Windows Startup
' This VBScript launches the Enhanced Master Launcher silently without showing console windows
' Organization: A6-9V

Set objShell = CreateObject("WScript.Shell")

' Get the directory where this script is located
strScriptPath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)

' Path to the Enhanced Master Launcher batch file
strBatchFile = strScriptPath & "\A6-9V_Enhanced_Master_Launcher.bat"

' Check if the batch file exists
If CreateObject("Scripting.FileSystemObject").FileExists(strBatchFile) Then
    ' Run the batch file hidden (0 = hidden window, False = don't wait for completion)
    ' Using 0 for hidden, False for not waiting allows the script to exit immediately
    objShell.Run """" & strBatchFile & """", 0, False
Else
    ' If batch file not found, show error message
    MsgBox "Error: A6-9V_Enhanced_Master_Launcher.bat not found in " & strScriptPath, vbCritical, "A6-9V Startup Error"
End If

Set objShell = Nothing
