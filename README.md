# SquaremapImageExport
Python script to generate the Squaremap's (not Dynmap) map image, with [astral-sh/uv](https://github.com/astral-sh/uv) support. Tested on Windows 10 & 11 with Python 3.13.13 on EarthMC Minecraft server.

## Installation

### 1. Prerequisites
1. Download [`squaremap.py`](https://raw.githubusercontent.com/3meraldK/SquaremapImageExport/main/squaremap.py) to a directory of choice.
2. Open a terminal of choice (e.g. the Command Prompt) and navigate to the directory.

### 2.a. Classic way
1. Download Python, preferably 3.13.13 or newer.
2. Download [`requirements.txt`](https://raw.githubusercontent.com/3meraldK/SquaremapImageExport/main/requirements.txt) to the directory of the script.
3. In the terminal you opened before, run `pip install -r requirements.txt` to download required dependencies.
4. Run `python squaremap.py`.

### 2.b. astral.sh/uv
1. Install [astral-sh/uv](https://docs.astral.sh/uv/#installation) with Python, preferably 3.13.13 or newer.
2. In the terminal you opened before, run `uv run squaremap.py`.

### 3. What to expect
It will run a wizard where you input a map URL (https://themapurl.com), scale and map bounds.

## Downloaded example
![image](https://github.com/3meraldK/SquaremapImageExport/assets/48335651/2c08b50f-8d18-4a86-a75a-adcc7021a125)
