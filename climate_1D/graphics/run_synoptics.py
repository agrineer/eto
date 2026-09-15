#! /usr/bin/env python

'''
@file run_synoptics.py
@author Scott L. Williams. in collaboration with Cristina Yanez, Israel Pineda
@package ETo
@brief run a series of image bar plots
@LICENSE
# 
#  run_synoptics.py Copyright (C) 2020-2026 Scott L. Williams.
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

run_synoptics_copyright = 'run_synoptics.py Copyright (c) 2020-2026 Scott L. Williams, released under GNU GPL V3.0'

import os
import sys
import getopt
from ezprint import eprint, eprints

''' 1
komment = '"Pixel Histogram as Signal,      Pre-processing: None\nLearning Rate=0.30000         Nepochs=30"'

# pixel difference per cent
P = [ '0.42', '0.75', '1.14', '0.38', '0.33',
       '0.77', '0.57', '0.51', '0.67' ]

# cramer values
C = [ '0.9959', '0.9933', '0.9909', '0.9965', '0.9965',
      '0.9922', '0.9936', '0.9952', '0.9922' ]

prefix = '0.300000_30_'
indir  = '../../data/1D/2022/msom/0.300000_30_linear_nonorm_1st/'
outdir = '../../data/graphics/1D/2022/synoptics/0.300000_30_linear_nonorm_1st/'
srcfile= '../data/1D/2022/2022_hists.npy'
'''

''' 2
komment = '"Pixel Histogram as Signal,      Pre-processing: None\nLearning Rate=0.30000         Nepochs=30"'

# pixel difference per cent
P = [ '0.94', '0.95', '0.40', '0.74', '0.91',
       '0.92', '0.34', '0.45', '0.72' ]

# cramer values
C = [ '0.9918', '0.9916', '0.9960', '0.9931', '0.9921',
      '0.9916', '0.9971', '0.9948', '0.9941' ]

prefix = '0.300000_30_'
indir  = '../../data/1D/2022/msom/0.300000_30_linear_nonorm_2nd/'
outdir = '../../data/graphics/1D/2022/synoptics/0.300000_30_linear_nonorm_2nd/'
srcfile= '../data/1D/2022/2022_hists.npy'
'''

''' 3
komment = '"Pixel Histogram as Signal,      Pre-processing: Normalization\nLearning Rate=0.30000         Nepochs=30"'

# pixel difference per cent
P = [ '0.76', '0.67', '0.43', '0.75', '0.85',
       '1.08', '0.52', '0.41', '0.97' ]

# cramer values
C = [ '0.9977', '0.9922', '0.9947', '0.9873', '0.9867',
      '0.9916', '0.9936', '0.9923', '0.9905' ]

prefix = '0.300000_30_'
indir  = '../../data/1D/2022/msom/0.300000_30_linear_zanorm_1st/'
outdir = '../../data/graphics/1D/2022/synoptics/0.300000_30_linear_zanorm_1st/'
srcfile= '../data/1D/2022/2022_zahists.npy'
'''

#''' 4
komment = '"Pixel Histogram as Signal,      Pre-processing: Normalization\nLearning Rate=0.30000         Nepochs=30"'

# pixel difference per cent
P = [ '0.74', '0.79', '0.43', '12.26', '0.79',
       '1.22', '0.94', '0.62', '0.90' ]

# cramer values
C = [ '0.9915', '0.9877', '0.9922', '0.8732', '0.9928',
      '0.9945', '0.9694', '0.9952', '0.9946' ]

prefix = '0.300000_30_'
indir  = '../../data/1D/2022/msom/0.300000_30_linear_zanorm_2nd/'
outdir = '../../data/graphics/1D/2022/synoptics/0.300000_30_linear_zanorm_2nd/'
srcfile= '../data/1D/2022/2022_zahists.npy'
#''' 

lut = '../../data/luts/cetin.hex'

# ----------------------------------------------------------------
myname = os.path.basename(__file__)[:-3] 

if __name__ == '__main__':

    for i in range( 0, 9 ):
        
        command = './plot_synoptic.py -l ' + lut + ' -c ' + \
           C[i] + ' -p ' + P[i] + \
           ' -f ' + indir + prefix + '0' + '.jpg' + \
           ' -s ' + indir + prefix + str(i+1) + '.jpg' + \
           ' -t ' + indir + prefix + str(i+1) + '_T.jpg' + \
           ' -d ' + indir + 'diff_' + str(i+1) + '-0.jpg' + \
           ' -o ' + outdir + 'synoptic_' + str(i+1) + '-0.pdf' \
           ' -k ' + komment + ' -i ' + srcfile
 
        eprint( myname + ': running command: ' + command )
        os.system( command )
