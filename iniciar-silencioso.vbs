' Launcher Silencioso para o Kanban Minimalista do Maestri
' Executa o servidor Python sem abrir janela de prompt preta no Windows.

Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

strScriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
strComando = "python """ & strScriptDir & "\kanban.py"" --sem-portal"

WshShell.Run strComando, 0, False
Set WshShell = Nothing
Set fso = Nothing
