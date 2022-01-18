#!/bin/bash

../symmetry.py -i O_3.png -o test_l.png -l
../symmetry.py -i O_3.png -o test_r.png -r
../symmetry.py -i O_3.png -o test_lr.png -l -r

../symmetry.py -i O_3.png -o test_u.png -u
../symmetry.py -i O_3.png -o test_d.png -d
../symmetry.py -i O_3.png -o test_ud.png -u -d

../symmetry.py -i O_3.png -o test_lu.png -l -u
../symmetry.py -i O_3.png -o test_ld.png -l -d
../symmetry.py -i O_3.png -o test_ru.png -r -u
../symmetry.py -i O_3.png -o test_rd.png -r -d

../symmetry.py -i O_3.png -o test_lru.png -l -r -u
../symmetry.py -i O_3.png -o test_lrd.png -l -r -d
../symmetry.py -i O_3.png -o test_lud.png -l -u -d
../symmetry.py -i O_3.png -o test_rud.png -r -u -d

../symmetry.py -i O_3.png -o test_lrud.png -l -r -u -d

