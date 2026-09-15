#! /usr/bin/env python

'''
@file run_sample_pix.py
@author Scott L. Williams, in collaboration with Elisa Piispa, Israel Pineda, María Solis-Aulestia, Cristina Yánez
@package ETo
@brief generate a series of pixel image plots at given pixel locations.
@LICENSE
# 
#  run_sample_pix.py Copyright (C) 2020-2026 Scott L. Williams.
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

# generate pixel images from sample points using sample_pix.py

run_sample_pix_copyright = 'run_sample_pix.py Copyright (c) 2020-2026 Scott L. Williams, released under GNU GPL V3.0'

import os
import sys
import getopt
from ezprint import eprint, eprints

# pixel image sample pixels (16,46) is Yachay
ps = [(16,46),
      (0,0), (0,57), (0,141),(0,170),
      (57,0), (57,57), (57,141), (57,170),
      (87,0), (87,87), (87,170),
      (141,0), (141,57), (141,141), (141,170),
      (170,0), (170,57), (170,141), (170,170) ]

append = 'C'
#prefix = 'binary_'
#inpath = '../../data/2D/2022/2022_fdw.npy'
#prefix = 'col_hamming_9_'
#inpath = '../../data/2D/2022/2022_h9fdw.npy'
prefix = 'row_hamming_5_'
inpath = '../../data/2D/2022/2022_h5cdw.npy'

outdir = '../../data/graphics/samples/2022/'

# ------------------------------------------------------------------------
myname = os.path.basename(__file__)[:-3] # no need for .py suffix

if __name__ == '__main__':

    for p in ps:

        command = './sample_pix.py -a ' + append + '  -c ' + \
            str( p[0] ) + ',' + str( p[1] ) +  ' -p ' + prefix +  \
            ' -i ' + inpath + ' -o ' + outdir
        
        eprint( myname + ': running command: ' + command )
        os.system( command )
