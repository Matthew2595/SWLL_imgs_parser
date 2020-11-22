# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2020 Matteo Ingrosso

The images are subject to Copyright and Terms of Use of the site.

This script aims to download SWLL images from AM weather site and save them
locally or on OneDrive folder.
"""

import os
from io import BytesIO
from urllib.request import URLopener
from time import sleep
from PIL import Image
from bs4 import BeautifulSoup
import requests

MAIN_PATH = "http://www.meteoam.it"  # Path of the page to parse.
SAVE_FOLDER = "INSERT YOUR FOLDER HERE"  # Folder used to save imgs.
DELAY = 10  # Seconds to wait after header creation and between subsequent trials.

# Check if already are images in the saving folder, shows them and ask to delete.
existing_imgs = os.listdir(SAVE_FOLDER)
if len(existing_imgs) > 0:
    print('The following images already exist.\n')
    for x in existing_imgs:
        print("---> " + x)
    inp = input('Do you want to remove them? [y/n]: ')
    if inp == 'y':
        for x in existing_imgs:
            os.remove(os.path.join(SAVE_FOLDER, x))
        print('Old images removed.\n')

# Creating the header to later open the images path.
opener = URLopener()
opener.addheader('Referer', "http://www.meteoam.it/prodotti_grafici/bassiStrati")
print('Header created.\n')

# Download the page
print('The page is loading.\n')
PAGE = "http://www.meteoam.it/prodotti_grafici/bassiStrati"
header = {'User-Agent': 'Chrome/87.0.4280.66'}
result = requests.get(PAGE, headers=header)

# Keep repeating until it gets a good output.
while result.status_code != 200:
    print('Code ' + str(result.status_code) + " returned. I'll try again in " +
          str(DELAY) + ' seconds.')
    sleep(DELAY)

# If successful parse the download into a BeautifulSoup object, which allows
# easy manipulation.
soup = BeautifulSoup(result.content, "html.parser")
print('Page loaded successfully.')

# Finding all the images with a width of '160', in this way it is possible to
# select the needed images because are the only ones with this size.
imgs = soup.findAll('img', width='160')
names = []  # Used to store the path of images on the page.

# Loop over the iterable result of the search to get the path from the 'src'
# attribute.
for x in imgs:
    names.append(x['src'])

# Looping over the paths of needed images to read them, open, transform into
# PIL image object and save with proper name.
for x in names:
    img = opener.open(MAIN_PATH + x)
    img = img.read()
    img = Image.open(BytesIO(img))
    IMG_NAME = '_'.join((x[15:25], x[78:80], '00')) + '.gif'
    img.save(os.path.join(SAVE_FOLDER, IMG_NAME))
img.close()
print('Images saved correctly in ' + SAVE_FOLDER)
new_imgs = os.listdir(SAVE_FOLDER)
for img in new_imgs:
    print("---> " + img)

# Just to not directly close the prompt.
input('Press ENTER to exit')
