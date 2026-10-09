@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
  py -3 -m venv .venv
  if errorlevel 1 goto error
)
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto error
.venv\Scripts\python.exe -m pip install "pyinstaller>=6.16,<7"
if errorlevel 1 goto error
.venv\Scripts\python.exe -m PyInstaller --clean --noconfirm --onefile --windowed --name Zekon_RFQ --collect-all tkinterdnd2 zekon_rfq.py
if errorlevel 1 goto error
 echo Gotowe: dist\Zekon_RFQ.exe
 pause
 exit /b 0
:error
 echo Kompilacja przerwana. Przeczytaj komunikaty powyzej.
 pause
 exit /b 1
