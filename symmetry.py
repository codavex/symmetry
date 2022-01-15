#!/bin/python3

import getopt
import os
import sys
from PIL import Image
from PIL import UnidentifiedImageError
from PIL.ImageOps import flip
from PIL.ImageOps import mirror

def main(argv):
    inputfile = ''
    outputfile = ''
    vertical = False
    horizontal = False

    try:
        opts, args = getopt.getopt(argv, "i:o:vh", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('symmetry.py -i <inputfile> [-o <outputfile> -h -v]')
        sys.exit(2)

    # sort out options
    for opt, arg in opts:
        if opt in ("-i", "--ifile"):
            inputfile = arg
            outputfile = arg + '.out'  # default output file name
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt == '-h':
            horizontal = True
        elif opt == '-v':
            vertical = True

    # some validation
    if inputfile == '':
        print('must specify input file')
        sys.exit()
    if horizontal is False and vertical is False:
        print('must specify horizontal and/or vertical symmetry')
        sys.exit()

    print('Processing...')
    print('Input file: ', inputfile)
    # load in image
    try:
        inFile = Image.open(inputfile)
    except FileNotFoundError:
        print('Cant find input file')
        sys.exit()
    except UnidentifiedImageError:
        print('do not understand file format')
        sys.exit()
    outFile = None
    if horizontal is True:
        print('Flipping horizontal')
        # flip
        width, height = inFile.size
        outFile = Image.new(inFile.mode, (2*width, height))
        outFile.paste(inFile, (0, 0))
        outFile.paste(mirror(inFile), (width, 0))
        inFile = outFile
    if vertical is True:
        print('Flipping vertical')
        # flip
        width, height = inFile.size
        outFile = Image.new(inFile.mode, (width, 2*height))
        outFile.paste(inFile, (0, 0))
        outFile.paste(flip(inFile), (0, height))
    print('Output file: ', outputfile)
    # write out image
    outFile.save(outputfile)


if __name__ == "__main__":
    main(sys.argv[1:])
