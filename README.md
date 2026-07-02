# SquaremapImageExport
Python script to generate the Squaremap's .png map image, with [the uv](https://github.com/astral-sh/uv) support. Tested on Windows 10 with Python 3.11.5 and 3.13.14 on EarthMC Minecraft server.

## Installation

### 1. Prerequisites
1. Download [`squaremap.py`](https://raw.githubusercontent.com/3meraldK/SquaremapImageExport/main/squaremap.py) to a directory of choice.
2. Open a terminal of choice (e.g. the Command Prompt) and navigate to the directory.

### 2.a. Classic way
1. Download Python, at least 3.11.5.
2. Download [`requirements.txt`](https://raw.githubusercontent.com/3meraldK/SquaremapImageExport/main/requirements.txt) to the same directory.
3. In the terminal you opened before, run `pip install -r requirements.txt` to download required dependencies.
4. Run `python squaremap.py [map url] [world name] [max zoom] [scale] [corner coordinates]`.

### 2.b. astral.sh/uv
1. Follow [official docs](https://docs.astral.sh/uv/#installation) to install uv and Python, at least 3.11.5.
2. In the terminal you opened before, run `uv run squaremap.py [map url] [world name] [max zoom] [scale] [corner coordinates]`.

## Usage
- `[map url]` - URL to the map
- `[world name]` - name of the world you want to get the map of. To get it, click the small link button in bottom-left corner on a website. The page should refresh and the updated URL should include the world's name in it, for example: `?world=world_name`. Alternative way is described below.
- `[max zoom]` - this whole number depends on map. To find out, hop on the map website, open Developer Tools (Ctrl+Shift+I on Windows), go to Network tab, pan around the map while on max zoom and look for requests (do it until you find one) named like x_y.png, where x and y are any numbers. Right click on it and click Copy > Copy URL. URL includes the max zoom by `?zoom=number` and `[world name]` by `?world=world_name`.
- `[scale]` - how many blocks should be 1 pixel. This whole number must be a power of 2 (so 1, 2, 4, 8...). The limit is 2^(max zoom) pixels.
- `[corner coordinates]` - series of whole numbers in format "x1 z1 x2 z2" - there are no restrictions on order or used corners.
- ✅ Good example (test it out!): `python squaremap.py https://map.earthmc.net minecraft_overworld 5 32 -2280 -13344 7720 -6408`
- ⛔ Wrong example: `python squaremap.py map.earthmc.net 2.5 12.5 (-1000, -2000) (1000, 4000)`

## Downloaded example
![image](https://github.com/3meraldK/SquaremapImageExport/assets/48335651/2c08b50f-8d18-4a86-a75a-adcc7021a125)
