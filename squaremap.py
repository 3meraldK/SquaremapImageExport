# /// script
# dependencies = [
#     "Pillow",
#     "aiohttp",
#     "munch"
# ]
# ///

from os import path, mkdir
from time import time
from math import log2, floor
from shutil import rmtree
from re import split
from PIL import Image
from munch import Munch
from aiohttp import ClientSession, ClientTimeout
from asyncio import gather, run

async def download_tile(session, url, path):
	global downloaded
	async with session.get(url, timeout=ClientTimeout(total=3)) as response:
		if response.status != 200: return
		with open(path, 'wb') as file:
			downloaded += 1
			file.write(await response.read())

async def download_tiles(tiles):
	async with ClientSession() as session:
		tasks = []
		for x, z in tiles:
			url = f'{link}/tiles/{world}/{zoom}/{x}_{z}.png'
			path = f'{zoom}-{now}/{x}_{z}.png'
			tasks.append(download_tile(session, url, path))
		await gather(*tasks)

async def get_world():
	global world, link
	async with ClientSession() as session:
		try:
			async with session.get(f'{link}/tiles/settings.json', timeout=ClientTimeout(total=3)) as response:
				if response.status != 200:
					exit('The map website isn\'t responding (try later), exiting..\n')
				settings = await response.json()
				settings = Munch.fromDict(settings)
				print('\nAvailable worlds:')
				options = []
				worlds = []
				for i, _world in enumerate(settings.worlds):
					options.append(f'  {i+1}. {_world.name}')
					worlds.append(_world.name)
				print('\n'.join(options))
		except:
			exit('Response or website URL is invalid, exiting..\n')

		try:
			world = int(input('Enter your choice (number): '))
			if world < 1: raise Exception
			world = worlds[world-1]
		except:
			exit('Input should be one of possible choices, exiting..\n')

async def get_max_zoom():
	global world, link, max_zoom
	async with ClientSession() as session:
		try:
			async with session.get(f'{link}/tiles/{world}/settings.json', timeout=ClientTimeout(total=3)) as response:
				if response.status != 200:
					exit('The map website isn\'t responding (try later), exiting..\n')
				settings = await response.json()
				settings = Munch.fromDict(settings)
				max_zoom = int(settings.zoom.max)
		except:
			exit('Response or website URL is invalid, exiting..\n')

print('\nSquaremap Image Export by 3meraldK')

link = input('Enter the map URL: ')
link = ''.join(split('(/)', link)[0:5])
if link.startswith('https://') == False:
	exit('The map URL should start with https://, exiting..\n')

run(get_world())
run(get_max_zoom())

scales = [2**n for n in range(0, max_zoom+1)]
print(f'\nHow many blocks should be 1 pixel on image? Available options: {', '.join([f'{n}' for n in scales])}')
try:
	scale = int(input('Enter your choice: '))
	if scale not in scales: raise Exception
except:
	exit('Input should be one of possible choices, exiting..\n')

print('')
corners = []
try:
	for (i, x) in [(1, 'x'), (1, 'z'), (2, 'x'), (2, 'z')]:
		corners.append(int(input(f'Enter corner {i} {x}-coordinate: ')))
except:
	exit('Corner coordinates should be whole numbers, exiting..\n')

zoom = int(max_zoom - log2(scale))
blocks_per_tile = 2 ** (9 + max_zoom - zoom)
tile_corners = [floor(corner / blocks_per_tile) for corner in corners]

now = int(time())
if not path.exists(f'{zoom}-{now}'):
	mkdir(f'{zoom}-{now}')

print('\nDownloading tiles..')
download_start = time()
downloaded = 0
# range(start, end, step) step must be -1 if start <= end
range_x_step = 1 if tile_corners[0] <= tile_corners[2] else -1
range_z_step = 1 if tile_corners[1] <= tile_corners[3] else -1
range_x = range(tile_corners[0], tile_corners[2] + 1, range_x_step)
range_z = range(tile_corners[1], tile_corners[3] + 1, range_z_step)
tiles = [(x, z) for x in range_x for z in range_z]
if len(tiles) == 0:
	rmtree(f'{zoom}-{now}')
	exit('Corner coordinates are invalid, exiting..\n')

try:
	run(download_tiles(tiles))
except:
	rmtree(f'{zoom}-{now}')
	exit('URL is wrong or map website is not responding, exiting..\n')

if len(tiles) != downloaded:
	print(f'Program failed to download {len(tiles) - downloaded} of {len(tiles)} tiles, continuing..')
download_stop = time()
print(f'Downloading {downloaded} tiles took {round(download_stop - download_start, 2)}s')

print(f'Merging {downloaded} tiles..')
merge_start = time()
width = 512 * len(range_x)
height = 512 * len(range_z)
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

merge_stop = time()
rmtree(f'{zoom}-{now}')
print(f'Merging {downloaded} tiles took {round(merge_stop - merge_start, 2)}s')

print('Saving output map..')
save_start = time()
try:
	output.save(f'map-{now}.png')
except:
	exit('Could not save the image, exiting..\n')

size = round(path.getsize(f'map-{now}.png') / (1024 ** 2), 2)
save_stop = time()
print(f'Saving took {round(save_stop - save_start, 2)}s')
print(f'Total processing time was {round(save_stop - download_start, 2)}s')
print(f'Output saved as map-{now}.png')
print(f'Map is {width} x {height} px and weighs {size} MB.\n')
