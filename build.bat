@echo off
REM Quick build script for Galactic Combat with icon (Windows)

echo.
echo 🎮 Galactic Combat - Build with Icon
echo =====================================
echo.

REM Check if icon exists
if not exist "assets\image.ico" (
    echo ⚠️  Warning: assets\image.ico not found!
    echo The executable will use default icon.
    echo.
    set /p continue="Continue anyway? (y/n): "
    if not "%continue%"=="y" (
        echo Cancelled.
        exit /b 1
    )
    set ICON_FLAG=
) else (
    echo ✓ Found icon: assets\image.ico
    set ICON_FLAG=--icon=assets\image.ico
)

REM Check if PyInstaller is installed
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo.
    echo 📦 Installing PyInstaller...
    python -m pip install pyinstaller
    if errorlevel 1 (
        echo ❌ Failed to install PyInstaller
        pause
        exit /b 1
    )
    echo ✓ PyInstaller installed
)

echo.
echo 🔨 Building executable...
echo.

REM Build command
python -m PyInstaller main.py ^
    --onefile ^
    --windowed ^
    --add-data "assets;assets" ^
    %ICON_FLAG% ^
    --name="GalacticCombat" ^
    --clean

if errorlevel 0 (
    echo.
    echo ✅ Build successful!
    echo.
    echo 📁 Your game is ready:
    echo    dist\GalacticCombat.exe
    echo.
    echo 🚀 To test:
    echo    Double-click dist\GalacticCombat.exe
    echo.
    echo 📤 To share:
    echo    - Upload to Itch.io
    echo    - Share via Google Drive
    echo    - Send to friends!
    echo.
) else (
    echo.
    echo ❌ Build failed!
    echo Check the errors above
)

pause