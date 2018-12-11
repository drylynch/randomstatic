# makes a bunch of pseudo random monochrome noise images, at given width/height

from pathlib import Path
from PIL import Image
import random
import sys


SAVE_DIR = Path(__file__).resolve().parent / '# randoms #'
EXTENSION = '.png'  # can make a lossy jpg if you're a maniac


def random_binary_bytes(length):
    """ return length bytes, only 0x00 and 0xff """
    out = ''
    while len(out) < length:  # TODO make this less shitty
        out = '{0:b}'.format(random.getrandbits(length))  # sometimes retrurns fewer bits than necessary???
    out = out[:length]  # cut off to correct length
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
            go(*args)


if __name__ == '__main__':
    main()
