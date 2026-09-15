#! /usr/bin/env python

'''
@file run_synoptics.py
@author Scott L. Williams, in collaboration with Elisa Piispa, Israel Pineda, María Solis-Aulestia, Cristina Yánez
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
#komment = '"Las muestras de Píxeles Apilados por Filas"'
komment = '"Pixel Sample Data Stacked by Row,      Pre-processing: None\nLearning Rate=0.30000  Nepochs=50"'

# pixel difference per cent
P = [ '25.55', '25.12', '13.70', '28.61', '3.88',
       '8.09', '28.76', '28.63', '25.68' ]

# cramer values
C = [ '0.8784', '0.8786', '0.8956', '0.8557', '0.9630',
      '0.9222', '0.8540', '0.8556', '0.8775' ]

prefix = '0.300000_50_'
indir  = '../../data/2D/2022/msom_examples/0.300000_50_cdw/'
outdir = '../../data/graphics/2D/2022/synoptics/0.300000_50_cdw/'
srcfile= '../data/2D/2022/2022_cdw.npy'
lut = '../../data/luts/cetin.hex'
'''

''' 2
#komment = '"Las muestras de Píxeles Apilados por Columnas"'
komment = '"Pixel Sample Data Stacked by Column,   Pre-processing: None\nLearning Rate=0.30000  Nepochs=50"'

# pixel difference per cent
P = [ '25.36', '11.41', '0.40', '24.69', '5.13',
      '25.51', '1.30', '28.27', '1.33' ]

# cramer values
C = [ '0.8798', '0.9017', '0.9966', '0.8751', '0.9513',
      '0.8783', '0.9909', '0.8559', '0.9910' ]

prefix = '0.300000_50_'
indir  = '../../data/2D/2022/msom_examples/0.300000_50_fdw/'
outdir = '../../data/graphics/2D/2022/synoptics/0.300000_50_fdw/'
srcfile= '../data/2D/2022/2022_fdw.npy'
'''

''' 3
#komment = '"Filas Suavizado con un Kernel Hamming de 5 Píxeles "'
komment = '"Pixel Sample Data Stacked by Row,      Pre-processing: Row Hamming 5 Pixels\nLearning Rate=0.30000  Nepochs=50"'

# pixel difference per cent
P = [ '16.89', '17.18', '1.24', '16.97', '1.46',
      '0.59', '0.62', '17.00', '16.99' ]

# cramer values
C = [ '0.8901', '0.8873', '0.9894', '0.8889', '0.9882',
      '0.9944', '0.9948', '0.8882', '0.8887' ]

prefix = '0.300000_50_'
indir  = '../../data/2D/2022/msom_examples/0.300000_50_h5cdw/'
outdir = '../../data/graphics/2D/2022/synoptics/0.300000_50_h5cdw/'
srcfile= '../data/2D/2022/2022_h5cdw.npy'
'''

''' 4 ABERRANT START
#komment = '"Columnas Suavizado con Salida Aberrante"'
komment = '"Pixel Sample Data Stacked by Column,      Pre-processing: Column Hamming 9 Pixels\nLearning Rate=0.30000  Nepochs=50       Aberrant Start"'

# pixel difference per cent
P = [ '9.50', '9.27', '8.73', '9.61', '9.46',
      '9.18', '9.36', '9.11', '9.32' ]

# cramer values
C = [ '0.9177', '0.9190', '0.9216', '0.9182', '0.9176',
      '0.9200', '0.9190', '0.9203', '0.9186' ]

prefix = '0.300000_50_'
indir  = '../../data/2D/2022/msom_examples/0.300000_50_h9f_aberrant_start/'
outdir = '../../data/graphics/2D/2022/synoptics/0.300000_50_h9f_aberrant_start/'
srcfile= '../data/2D/2022/2022_h9fdw.npy'
'''

''' 5 First Runs
#komment = '"Columnas Suavizando con un Kernel Hamming de 9 Píxeles"'
komment =  '"Pixel Sample Data Stacked by Column,      Pre-processing: Column Hamming 9 Pixels\nLearning Rate=0.30000  Nepochs=50       First Run"'
# pixel difference per cent
P = [ '0.41', '0.54', '0.68', '0.52', '0.45',
      '0.68', '0.57', '0.23', '0.80' ]

# cramer values
C = [ '0.9972', '0.9966', '0.9955', '0.9961', '0.9958',
      '0.9953', '0.9963', '0.9975', '0.9952' ]

prefix = '0.300000_50_'
indir  = '../../data/2D/2022/msom_examples/0.300000_50_h9fdw_1st/'
outdir = '../../data/graphics/2D/2022/synoptics/0.300000_50_h9fdw_1st/'
srcfile= '../data/2D/2022/2022_h9fdw.npy'
'''

''' 6 Second Runs
#komment = '"Columnas Suavizado con un Kernel Hamming de 9 Píxeles"'
komment =  '"Pixel Sample Data Stacked by Column,      Pre-processing: Column Hamming 9 Pixels\nLearning Rate=0.30000  Nepochs=50       Second Run"'

# pixel difference per cent
P = [ '0.25', '0.37', '0.69', '0.69', '0.39',
      '0.49', '0.38', '0.63', '0.44' ]

# cramer values
C = [ '0.9970', '0.9974', '0.9950', '0.9951', '0.9974',
      '0.9961', '0.9971', '0.9954', '0.9971' ]

prefix = '0.300000_50_'
indir  = '../../data/2D/2022/msom_examples/0.300000_50_h9fdw_2nd/'
outdir = '../../data/graphics/2D/2022/synoptics/0.300000_50_h9fdw_2nd/'
srcfile= '../data/2D/2022/2022_h9fdw.npy'
'''

''' 7 Runs with a Miss
#komment = '"Columnas Suavizado con un Kernel Hamming de 9 Píxeles"'
komment =  '"Pixel Sample Data Stacked by Column,      Pre-processing: Column Hamming 9 Pixels\nLearning Rate=0.30000  Nepochs=50       Run with a Miss"'

# pixel difference per cent
P = [ '28.40', '0.55', '0.22', '0.55', '0.74',
       '0.52', '0.75', '0.79', '0.49' ]

# cramer values
C = [ '0.8968', '0.9957', '0.9977', '0.9966', '0.9951',
      '0.9961', '0.9942', '0.9942', '0.9954' ]

prefix = '0.300000_50_'
indir  = '../../data/2D/2022/msom_examples/0.300000_50_h9fdw_miss/'
outdir = '../../data/graphics/2D/2022/synoptics/0.300000_50_h9fdw_miss/'
srcfile= '../data/2D/2022/2022_h9fdw.npy'
'''

''' 8
#komment = '"Columnas Suavizado con un Kernel Hamming de 9 Píxeles"'
komment =  '"Pixel Sample Data Stacked by Column,      Pre-processing: Column Hamming 9 Pixels\nLearning Rate=0.35000  Nepochs=50       1st Run"'

# pixel difference per cent
P = [ '1.40', '0.83', '0.59', '0.76', '0.67',
       '0.64', '0.81', '0.65', '0.65' ]

# cramer values
C = [ '0.9900', '0.9935', '0.9941', '0.9938', '0.9946',
      '0.9946', '0.9943', '0.9937', '0.9947' ]

prefix = '0.350000_25_'
indir  = '../../data/2D/2022/msom_examples/0.350000_25_h9fdw/'
outdir = '../../data/graphics/2D/2022/synoptics/0.350000_25_h9fdw/'
srcfile= '../data/2D/2022/2022_h9fdw.npy'
'''

#''' 9
#komment = '"Columnas Suavizado con un Kernel Hamming de 9 Píxeles"'
komment =  '"Pixel Sample Data Stacked by Column,      Pre-processing: Column Hamming 9 Pixels\nLearning Rate=0.35000  Nepochs=50       2nd Run"'


# pixel difference per cent
P = [ '0.99', '0.50', '0.54', '0.44', '0.38',
       '0.51', '0.67', '0.34', '0.30' ]

# cramer values
C = [ '0.9941', '0.9967', '0.9959', '0.9965', '0.9971',
      '0.9965', '0.9955', '0.9971', '0.9976' ]

prefix = '0.350000_50_'
indir  = '../../data/2D/2022/msom_examples/0.350000_50_h9fdw/'
outdir = '../../data/graphics/2D/2022/synoptics/0.350000_50_h9fdw/'
srcfile= '../data/2D/2022/2022_h9fdw.npy'
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
