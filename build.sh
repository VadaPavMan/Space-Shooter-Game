#!/bin/bash
# Quick build script for Galactic Combat with icon

echo "🎮 Galactic Combat - Build with Icon"
echo "====================================="
echo ""

# Check if icon exists
if [ ! -f "assets/image.ico" ]; then
    echo "⚠️  Warning: assets/image.ico not found!"
    echo "The executable will use default icon."
    echo ""
    read -p "Continue anyway? (y/n): " continue
    if [ "$continue" != "y" ]; then
        echo "Cancelled."
        exit 1
    fi
    ICON_FLAG=""
else
    echo "✓ Found icon: assets/image.ico"
    ICON_FLAG="--icon=assets/image.ico"
fi

# Check if PyInstaller is installed
if ! python3 -m pip show pyinstaller &> /dev/null; then
    echo ""
    echo "📦 Installing PyInstaller..."
    python3 -m pip install pyinstaller
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install PyInstaller"
        exit 1
    fi
    echo "✓ PyInstaller installed"
fi

echo ""
echo "🔨 Building executable..."
echo ""

# Build command
python3 -m PyInstaller main.py \
    --onefile \
    --windowed \
    --add-data "assets:assets" \
    $ICON_FLAG \
    --name="GalacticCombat" \
    --clean

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Build successful!"
    echo ""
    echo "📁 Your game is ready:"
    echo "   dist/GalacticCombat"
    echo ""
    echo "🚀 To test:"
    echo "   ./dist/GalacticCombat"
    echo ""
    echo "📤 To share:"
    echo "   - Upload to Itch.io"
    echo "   - Share via Google Drive"
    echo "   - Send to friends!"
    echo ""
else
    echo ""
    echo "❌ Build failed!"
    echo "Check the errors above"
    exit 1
fi