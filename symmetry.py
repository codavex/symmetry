#!/bin/python3

import getopt
import sys
import PIL
import PIL.ImageOps


def stack_horizontal(left, right):
    temp = PIL.Image.new(left.mode, (left.width + right.width, left.height))
    temp.paste(left, (0, 0))
    temp.paste(right, (left.width, 0))
    return temp


def stack_vertical(top, bottom):
    temp = PIL.Image.new(top.mode, (top.width, top.height + bottom.height))
    temp.paste(top, (0, 0))
    temp.paste(bottom, (0, top.height))
    return temp


def main(argv):
    inputfile = ''
    outputfile = ''
    left = False
    right = False
    up = False
    down = False

    try:
        opts, args = getopt.getopt(argv, "i:o:lrud", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('symmetry.py -i <infile> [-o <outfile>] [-l] [-r] [-u] [-d]')
        sys.exit()

    # sort out options
    for opt, arg in opts:
        if opt in ("-i", "--ifile"):
            inputfile = arg
            if '' == outputfile:
                outputfile = arg + '.out'  # default output file name
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif '-l' == opt:
            left = True
        elif '-r' == opt:
            right = True
        elif '-u' == opt:
            up = True
        elif '-d' == opt:
            down = True

    # some validation
    if '' == inputfile:
        print('Must specify input file')
        sys.exit()
    if left is False and right is False and up is False and down is False:
        print('Must specify horizontal and/or vertical symmetry')
        sys.exit()

    print('Processing...')
    print('Input file: ', inputfile)
    # load in image
    try:
        image = PIL.Image.open(inputfile)
    except FileNotFoundError:
        print('Cant find input file')
        sys.exit()
    except PIL.UnidentifiedImageError:
        print('Do not understand file format')
        sys.exit()

    # fill in the canvas
    # start off with mirror image of the original input image
    # to add left or right if needed
    mirror = PIL.ImageOps.mirror(image)
    if left:
        print('Mirroring left')
        image = stack_horizontal(mirror, image)
    if right:
        print('Mirroring right')
        image = stack_horizontal(image, mirror)

    # now we have horizontal sorted, find mirror ('flipped') image
    # to add above or below if needed
    flip = PIL.ImageOps.flip(image)
    if up:
        print('Flipping up')
        image = stack_vertical(flip, image)
    if down:
        print('Flipping down')
        image = stack_vertical(image, flip)

    print('Output file: ', outputfile)
    # write out image
    image.save(outputfile)


if __name__ == "__main__":
    main(sys.argv[1:])
