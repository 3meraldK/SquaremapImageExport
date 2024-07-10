# squaremap
Python script to download a Squaremap map. Tested on Windows 10 with Python 3.11.5.

## Installation and usage
1. Download Python.
2. Download [`squaremap.py`](https://raw.githubusercontent.com/3meraldK/squaremap/main/squaremap.py) and [`requirements.txt`](https://raw.githubusercontent.com/3meraldK/squaremap/main/requirements.txt) by clicking hyperlinks and saving files onto your computer to same directory.
3. Open your desired terminal (e.g. Windows' Command Prompt) and navigate to the directory with downloaded files.
4. Run `pip install -r requirements.txt` to download required modules.
5. Run `squaremap.py` via command:
<pre>python squaremap.py [map url] [world name] [zoom=0..3] (corner coordinates)</pre>
- ✅ Good example (test it out!): `python squaremap.py https://map.earthmc.net minecraft_overworld 0 -2280 -13344 7720 -6408`
- ⛔ Wrong example: `python squaremap.py map.earthmc.net/?x=180&z=500 2.5 (-1000, -2000) (1000, 4000)`
- ℹ️ Corner coordinates are optional. When not passed, script downloads whole world's map.

## Downloaded example