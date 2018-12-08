# makes a bunch of pseudo random monochrome noise images, at given width/height

from pathlib import Path
from PIL import Image
import random


SAVE_DIR = Path(__file__).resolve().parent / '# randoms #'
EXTENSION = '.png'  # can make a lossy jpg if you're a maniac


def random_binary_bytes(length):
    """ return bytes with only 0x00 and 0xff, of input length """
    bstr = ''
    outbytes = b''
    while len(bstr) < length:
        bstr = '{0:b}'.format(random.getrandbits(length + round((length/5))))  # generate some extras cause they don't show up sometimes for some reason (??)
    bstr = bstr[:length]  # cut off to desired length
    for c in bstr:  # shitty but works \_:^)_/
        if c == '1':
            outbytes += b'\xff'
        else:
            outbytes += b'\x00'
    return outbytes


def bnw_image_from_bytes(inbytes, width, height):
    """ convert input binary bytes to black and white PIL Image """
    return Image.frombytes('L', (width, height), inbytes)


def go(how_many, width, height):
    """ makes how_many random images """
    SAVE_DIR.mkdir(parents=True, exist_ok=True)  # quietly make the save dir if it doesn't exist yet
    for n in range(1, how_many+1):
        img = bnw_image_from_bytes(random_binary_bytes(width*height), width, height)
        img.save(SAVE_DIR / (str(n) + EXTENSION))
    print('donezo')


if __name__ == '__main__':
    go(10, 10, 10)  # !
