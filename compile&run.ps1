pip install -r requirements.txt
python3 main.py
python main.py

pyinstaller --noconfirm --onefile --windowed --icon=image.png --add-data "assets:assets" main.py