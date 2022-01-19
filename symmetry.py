#!/bin/python3

import getopt
import os
import sys
import PIL
import PIL.ImageOps


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
        temp = PIL.Image.new(mode, (image.width + mirror.width, image.height))
        temp.paste(mirror, (0, 0))
        temp.paste(image, (mirror.width, 0))
        image = temp
    if right:
        print('Mirroring right')
        temp = PIL.Image.new(mode, (image.width + mirror.width, image.height))
        temp.paste(image, (0, 0))
        temp.paste(mirror, (image.width, 0))
        image = temp

    flip = PIL.ImageOps.flip(image)
    if up:
        print('Flipping up')
        temp = PIL.Image.new(mode, (image.width, image.height + flip.height))
        temp.paste(flip, (0, 0))
        temp.paste(image, (0, flip.height))
        image = temp
    if down:
        print('Flipping down')
        temp = PIL.Image.new(mode, (image.width, image.height + flip.height))
        temp.paste(image, (0, 0))
        temp.paste(flip, (0, image.height))
        image = temp

    print('Output file: ', outputFile)
    # write out image
    image.save(outputFile)


if __name__ == "__main__":
    main(sys.argv[1:])
