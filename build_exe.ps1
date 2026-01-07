# Build a single-file Windows executable using PyInstaller
# Usage: Open PowerShell, activate your virtualenv, then run:
#   .\build_exe.ps1

# 1) Ensure PyInstaller is installed
python -m pip install --upgrade pyinstaller

# 2) Clean previous builds
if (Test-Path -Path "dist") { Remove-Item -Recurse -Force dist }
if (Test-Path -Path "build") { Remove-Item -Recurse -Force build }
if (Test-Path -Path "gui_expense_tracker.spec") { Remove-Item -Force gui_expense_tracker.spec }

# 3) Run PyInstaller to create a single-file, windowed executable
# Note: --add-data uses a ';' separator on Windows: "source;dest"
pyinstaller --noconfirm --clean --onefile --windowed `
    --name "IODEX_Expense_Tracker" `
    --icon "app.ico" `
    --add-data "photo1.jpg;." `
    gui_expense_tracker.py

Write-Host "Build finished. Check the 'dist' folder for IODEX_Expense_Tracker.exe"