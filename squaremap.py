# /// script
# dependencies = [
#     "Pillow",
#     "aiohttp"
# ]
# ///
# astral-sh/uv support above

import sys
import os
import time
import math
import asyncio
import shutil
import aiohttp
import re
from PIL import Image

# Utility functions for asynchronous downloading
async def download_tile(session, url, path):
	global downloaded
	async with session.get(url) as response:
		if response.status != 200: return
		with open(path, 'wb') as file:
			downloaded += 1
			file.write(await response.read())

async def download_tiles(tiles):
	async with aiohttp.ClientSession() as session:
		tasks = []
		for x, z in tiles:
			url = f'{link}/tiles/{world}/{zoom}/{x}_{z}.png'
			path = f'{zoom}-{now}/{x}_{z}.png'
			tasks.append(download_tile(session, url, path))
		await asyncio.gather(*tasks)

print('')
print('Squaremap Image Export by 3meraldK')

# Validating parameters
if len(sys.argv) != 9:
	exit('Usage (read repository\'s readme): python squaremap.py [map url] [world name] [max zoom] [scale] [corner coordinates]\n')

link = ''.join(re.split('(/)', sys.argv[1])[0:5])
if link.startswith('https://') == False:
	exit('The [map url] is invalid, it should start with https://, exiting..\n')

world = sys.argv[2]

try:
	max_zoom = int(sys.argv[3])
	scale = int(sys.argv[4])
	corners = sys.argv[5:9]
	for i, corner in enumerate(corners):
		corners[i] = int(corner)
except ValueError:
	exit('Command parameters [corner coordinates], [scale] or [max zoom] should be whole numbers, exiting..\n')

try:
	if not (math.log2(scale)).is_integer(): raise ValueError
except ValueError:
	exit('Command parameter [scale] is not a power of 2, exiting..\n')

zoom = int(max_zoom - math.log2(scale))
if zoom < 0: exit('Command parameters [scale] or [max zoom] are invalid, exiting..\n')

blocks_per_tile = 2 ** (9 + max_zoom - zoom)
tile_corners = [math.floor(corner / blocks_per_tile) for corner in corners]
now = int(time.time())
if not os.path.exists(f'{zoom}-{now}'):
	os.mkdir(f'{zoom}-{now}')

print('Downloading tiles..')
download_start = time.time()
downloaded = 0
# range(start, end, step) step must be -1 if start <= end
range_x_step = 1 if tile_corners[0] <= tile_corners[2] else -1
range_z_step = 1 if tile_corners[1] <= tile_corners[3] else -1
range_x = range(tile_corners[0], tile_corners[2] + 1, range_x_step)
range_z = range(tile_corners[1], tile_corners[3] + 1, range_z_step)
tiles = [(x, z) for x in range_x for z in range_z]
if len(tiles) == 0:
	shutil.rmtree(f'{zoom}-{now}')
	exit('Command parameter [corner coordinates] is invalid (did you preserve the required format?), exiting..\n')
try:
	asyncio.run(download_tiles(tiles))
except:
	shutil.rmtree(f'{zoom}-{now}')
	exit('URL is wrong or map website is not responding, exiting..\n')
if len(tiles) != downloaded:
	print(f'{len(tiles) - downloaded} of {len(tiles)} tiles were not successfully downloaded, continuing..')
download_stop = time.time()
print(f'Downloading {downloaded} tiles took {round(download_stop - download_start, 2)}s')

print(f'Merging {downloaded} tiles..')
merge_start = time.time()
width = 512 * len(range_x)
height = 512 * len(range_z)
if width <= 0 or height <= 0:
	shutil.rmtree(f'{zoom}-{now}')
	exit('Width or height of image is not positive, exiting..\n')
output = Image.new(mode="RGBA", size=(width, height))
x_px = 0
for x in range_x:
	z_px = 0
	for z in range_z[::range_z_step]:
		try:
			tile = Image.open(f'{zoom}-{now}/{x}_{z}.png')
			output.paste(tile, (x_px, z_px))
		except: pass
		z_px += 512
	x_px += 512
merge_stop = time.time()
shutil.rmtree(f'{zoom}-{now}')
print(f'Merging {downloaded} tiles took {round(merge_stop - merge_start, 2)}s')

print('Saving output map..')
save_start = time.time()
output.save(f'map-{zoom}-{now}.png')
size = round(os.path.getsize(f'map-{zoom}-{now}.png') / (1024 ** 2), 2)
save_stop = time.time()
print(f'Saving took {round(save_stop - save_start, 2)}s')
print(f'Total processing time was {round(save_stop - download_start, 2)}s')
print(f'Output saved as map-{zoom}-{now}.png')
print(f'Map is {width} x {height} px and weighs {size} MB.\n')