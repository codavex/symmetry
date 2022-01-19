#!/bin/python3

import getopt
import os
import sys
import PIL
import PIL.ImageOps


def stack_horizontal(mode, left, right):
    temp = PIL.Image.new(mode, (left.width + right.width, left.height))
    temp.paste(left, (0, 0))
    temp.paste(right, (left.width, 0))
    return temp


def stack_vertical(mode, top, bottom):
    temp = PIL.Image.new(mode, (top.width, top.height + bottom.height))
    temp.paste(top, (0, 0))
    temp.paste(bottom, (0, top.height))
    return temp


def main(argv):
    inputFile = ''
    outputFile = ''
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
            inputFile = arg
            if outputFile == '':
                outputFile = arg + '.out'  # default output file name
        elif opt in ("-o", "--ofile"):
            outputFile = arg
        elif opt == '-l':
            left = True
        elif opt == '-r':
            right = True
        elif opt == '-u':
            up = True
        elif opt == '-d':
            down = True

    # some validation
    if inputFile == '':
        print('Must specify input file')
        sys.exit()
    if left is False and right is False and up is False and down is False:
        print('Must specify horizontal and/or vertical symmetry')
        sys.exit()

    print('Processing...')
    print('Input file: ', inputFile)
    # load in image
    try:
        image = PIL.Image.open(inputFile)
        mode = image.mode
    except FileNotFoundError:
        print('Cant find input file')
        sys.exit()
    except PIL.UnidentifiedImageError:
        print('Do not understand file format')
        sys.exit()

    # fill in the canvas
    mirror = PIL.ImageOps.mirror(image)
    if left:
        print('Mirroring left')
        image = stack_horizontal(mode, mirror, image)
    if right:
        print('Mirroring right')
        image = stack_horizontal(mode, image, mirror)

    flip = PIL.ImageOps.flip(image)
    if up:
        print('Flipping up')
        image = stack_vertical(mode, flip, image)
    if down:
        print('Flipping down')
        image = stack_vertical(mode, image, flip)

    print('Output file: ', outputFile)
    # write out image
    image.save(outputFile)


if __name__ == "__main__":
    main(sys.argv[1:])
