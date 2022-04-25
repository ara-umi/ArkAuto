@echo off
reg add HKEY_CURRENT_USER\Console /v WindowSize /t REG_DWORD /d 0x1e0078 /f>nul
reg add HKEY_CURRENT_USER\Console /v WindowPosition /t REG_DWORD /d 0x00000000 /f>nul
reg add HKEY_CURRENT_USER\Console /v ScreenBufferSize /t REG_DWORD /d 0x23290078 /f>nul
%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit
cd /d %~dp0
set PYTHONPATH=%~dp0
python arkauto/main.py
pause