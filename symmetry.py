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
        inFile = PIL.Image.open(inputfile)
        flip = PIL.ImageOps.flip(inFile)
        mirror = PIL.ImageOps.mirror(inFile)
        flipmirror = PIL.ImageOps.flip(mirror)
    except FileNotFoundError:
        print('Cant find input file')
        sys.exit()
    except PIL.UnidentifiedImageError:
        print('do not understand file format')
        sys.exit()

    # create output file canvas
    width, height = inFile.size
    h_tiles = 1 + (1 if left else 0) + (1 if right else 0)
    v_tiles = 1 + (1 if up else 0) + (1 if down else 0)
    outFile = PIL.Image.new(inFile.mode, (h_tiles*width, v_tiles*height))

    # fill in the canvas
    outFile.paste(inFile, (width if left else 0,
                           height if up else 0))  # original image
    if left:
        outFile.paste(mirror, (0, height if up else 0))
    if right:
        outFile.paste(mirror, (2*width if left else width,
                               height if up else 0))
    if up:
        outFile.paste(flip, (width if left else 0, 0))
    if down:
        outFile.paste(flip, (width if left else 0,
                             2*height if up else height))
    if up and left:
        outFile.paste(flipmirror, (0, 0))
    if up and right:
        outFile.paste(flipmirror, (2*width if left else width, 0))
    if down and left:
        outFile.paste(flipmirror, (0, 2*height if up else height))
    if down and right:
        outFile.paste(flipmirror, (2*width if left else width,
                                   2*height if up else height))

    print('Output file: ', outputfile)
    # write out image
    outFile.save(outputfile)


if __name__ == "__main__":
    main(sys.argv[1:])
