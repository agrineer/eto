#! /usr/bin/env python

'''
@file run_image_bars.py
@author Scott L. Williams, in collaboration with Elisa Piispa, Israel Pineda, María Solis-Aulestia, Cristina Yánez
@package ETo
@brief run a series of image bar plots
@LICENSE
# 
#  run_image_bars.py Copyright (C) 2020-2026 Scott L. Williams.
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

run_image_bars_copyright = 'run_image_bars.py Copyright (c) 2020-2026 Scott L. Williams, released under GNU GPL V3.0'

import os
import sys
import getopt
from ezprint import eprint, eprints
'''
ps = ['0,0']
'''
# pixel image sample pixels 
ps = ['16,46', # yachay tech
      '0,0', '0,57', '0,141','0,170',
      '57,0', '57,57', '57,141', '57,170',
      '87,0', '87,87', '87,170',
      '141,0', '141,57', '141,141', '141,170',
      '170,0', '170,57', '170,141', '170,170' ]
'''
pc = [ '0.899,-79.550']
'''
pc = [ ' 0.404,-78.175', # yachay tech
       ' 0.899,-79.550',' 0.899,-77.840',' 0.899,-75.320',' 0.899,-74.450',
       '-0.810,-79.550','-0.810,-77.840','-0.810,-75.320','-0.810,-74.450',
       '-1.710,-79.550','-1.710,-76.940','-1.710,-74.450',
       '-3.328,-79.550','-3.328,-77.840','-3.328,-75.320','-3.328,-74.450',
       '-4.196,-79.550','-4.196,-77.840','-4.196,-75.320','-4.196,-74.450' ]
#'''
sday = '301'
eday = '364'

#prefix = 'binary_'
#prefix = 'row_hamming_5_'
prefix = 'col_hamming_9_'

indir = '../../data/graphics/2D/2022/samples/'
outdir = '../../data/graphics/2D/2022/plots/bars/' + prefix[:-1] + \
    '/' + sday + '_' + eday + '/'

#thead = '"None"'
#thead = '"Row Hamming 5 Pixels"'
thead = '"Column Hamming 9 Pixels"'

# ------------------------------------------------------------------------

myname = os.path.basename(__file__)[:-3] # no need for .py suffix

if __name__ == '__main__':

    count = len( ps )
    if count != len( pc ):
        eprint( myname + ': size mismatch for locations ... exiting' )
        sys.exit(0)

    for i in range( count ):
        
        command = './plot_image_bars.py -s ' + sday +  ' -e ' +  eday + \
            ' -l ' + ps[i] + ' -p ' + prefix + \
            ' -c ' + pc[i] + \
            ' -t ' + thead + ' -i ' + indir + ' -o ' + outdir
        eprint( myname + ': running command: ' + command )
        os.system( command )
