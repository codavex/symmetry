#!/bin/python3

import sys
import getopt


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
            outputfile = arg + '.out' # default output file name
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
    if horizontal is True:
        print('Flipping horizontal')
        # flip
    if vertical is True:
        print('Flipping vertical')
        # flip
    print('Output file: ', outputfile)
    # write out image


if __name__ == "__main__":
    main(sys.argv[1:])
