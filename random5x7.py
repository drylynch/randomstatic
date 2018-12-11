# makes a bunch of pseudo random monochrome noise images, at given width/height
# will take a while if you go over 100k imgs, and will kill your drive if you run on an ssd
# so watch out ok buddy

"""
TODO

find a way to generate random binary strings that are always a given length cause padding works but is dumb

"""

from pathlib import Path
from PIL import Image
import random
import sys


SAVE_DIR = Path(__file__).resolve().parent / '# randoms #'
EXTENSION = '.png'  # can make a lossy jpg if you're a maniac
PADDING_SIZE = 20  # extra bits to generate, cause random.getrandbits sometimes doesn't generate enough, never more than 12-13 needed though


def random_binary_bytes(length):
    """ return bytes, only b'0x00' and b'0xff' """
    out = bin(random.getrandbits(length + PADDING_SIZE))[:length]  # add extra padding, then cut down to desired size
    out = bytes(out, encoding='utf8')
    trans = bytearray.maketrans(b'10', b'\xff\x00')  # translate 1 -> FF, 0 -> 00
    out = out.translate(trans)
    return out


def generate(width, height):
    """ return black & white Image of given width & height """
    return Image.frombytes('L', (width, height), random_binary_bytes(width * height))


def go(width, height, how_many):
    """ makes how_many random images """
    SAVE_DIR.mkdir(parents=True, exist_ok=True)  # quietly make save dir if it doesn't exist yet
    for n in range(1, how_many+1):
        img = generate(width, height)
        img.save(SAVE_DIR / (str(n) + EXTENSION))


def main():
    args = sys.argv[1:]
    if not len(args) == 3:
        print('random static generator\n'
              '=======================\n'
              'usage:\n'
              '\trandom5x7.py width height how_many\n')
        input('press enter to exit... ')
    else:
        try:
            args = [int(a) for a in args]
        except ValueError:
            print('ERROR: positive integer inputs only')
        else:
            print('generating images, press CTRL + C to stop...')
            try:
                go(*args)
            except KeyboardInterrupt:
                print('## stopped.')
            else:
                print('done.')


if __name__ == '__main__':
    main()
