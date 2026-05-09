# PigeonTrans

A minimalist desktop translator built with Python and CustomTkinter. 

This tool uses the [deep-translator-api](https://deep-translator-api.azurewebsites.net/) to provide reliable translations via Google Translate.

## Features
- **Global Hotkey**: Toggle window with `Alt + T`.
- **Persistence**: Automatically saves your language and service settings.
- **Always on Top**: Keeps the window accessible while multitasking.

## How to Use
1. **Download**: Get the latest `PigeonTrans.exe` from [Releases](https://github.com/lk-zx0/PigeonTrans/releases).
2. **Run**: Double-click the EXE (it will create a `src/` folder for settings).
3. **Translate**: Enter text and press `Enter`.

## Development
To run from source:
```bash
pip install -r requirements.txt
python main.py
