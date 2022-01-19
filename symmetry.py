#!/bin/python3

import getopt
import os
import sys
import PIL
import PIL.ImageOps


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
        sys.exit(2)

    # sort out options
    for opt, arg in opts:
        if opt in ("-i", "--ifile"):
            inputfile = arg
            outputfile = arg + '.out'  # default output file name
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt == '-l':
            left = True
        elif opt == '-r':
            right = True
        elif opt == '-u':
            up = True
        elif opt == '-d':
            down = True

    # some validation
    if inputfile == '':
        print('must specify input file')
        sys.exit()
    if left is False and right is False and up is False and down is False:
        print('must specify horizontal and/or vertical symmetry')
        sys.exit()

    print('Processing...')
    print('Input file: ', inputfile)
    # load in image
    try:
        image = PIL.Image.open(inputfile)
        mode = image.mode
    except FileNotFoundError:
        print('Cant find input file')
        sys.exit()
    except PIL.UnidentifiedImageError:
        print('do not understand file format')
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

    print('Output file: ', outputfile)
    # write out image
    image.save(outputfile)


if __name__ == "__main__":
    main(sys.argv[1:])
