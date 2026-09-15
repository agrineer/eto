#! /usr/bin/env python

'''
@file run_plot_diffs.py
@author Scott L. Williams, in collaboration with Elisa Piispa, Israel Pineda, María Solis-Aulestia, Cristina Yánez
@package ETo
@brief run a series of image bar plots
@LICENSE
# 
#  run_plot_diffs.py Copyright (C) 2020-2026 Scott L. Williams.
# 
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
'''

# generate pixel images from sample points

run_plot_diffs_copyright = 'run_plot_diffs.py Copyright (c) 2020-2026 Scott L. Williams, released under GNU GPL V3.0'

import os
import sys
import getopt
from ezprint import eprint, eprints

# pixel image sample pixels
ps = [(0,0), (0,57), (0,141),(0,170),
      (57,0), (57,57), (57,141), (57,170),
      (87,0), (87,87), (87,170),
      (141,0), (141,57), (141,141), (141,170),
      (170,0), (170,57), (170,141), (170,170) ]

sday = '300'
eday = '364'
prefix = 'binary_'
#prefix = 'row_hamming_5_'
#prefix = 'col_hamming_9_'

indir = '../../data/graphics/samples/2022/'
outdir = '../../data/graphics/plots/2022/bars/' + prefix[:-1] + \
    '/' + sday + '_' + eday + '/'

thead = '"Imagen Binaria"'
#thead = '"Filas Suavizadas con Kernel Hamming de 5 Píxeles"'
#thead = '"Columnas Suavizadas con Kernel Hamming de 9 Píxeles"'

# ------------------------------------------------------------------------

myname = os.path.basename(__file__)[:-3] # no need for .py suffix
#spinner = itertools.cycle( ['\\','-', '|', '-', '/', '-','|'] ) # spinner chars

if __name__ == '__main__':

    for s in ps:
        y = str(s[0])
        x = str(s[1])
        pix = y +','+x
        command = './plot_image_bars.py -s ' + sday + \
            ' -e ' +  eday + ' -l ' + pix + ' -p ' + prefix + \
            ' -t ' + thead + ' -i ' + indir + ' -o ' + outdir
        eprint( myname + ': running command: ' + command )
        os.system( command )
