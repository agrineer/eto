#! /usr/bin/env python

'''
@file pixval.py
@author Scott L. Williams, in collaboration with Elisa Piispa, Israel Pineda, María Solis-Aulestia, Cristina Yánez
@package ETo
@brief show the pixel difference between two differently labeled images
@LICENSE

#  pixval.py Copyright (C) 2020-2026 Scott L. Williams.
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
pixval_copyright = 'pixval.py Copyright (c) 2020-2026 Scott L. Williams, released under GNU GPL V3.0'

# retrieve a specified pixel's band values from a numpy file
# and write out the values to a text csv file.

import os
import sys

import ezprint
from npy_src import npy_src

# list pixels to sample (numpy arrays have origin at top left)
# y,x order
pixels = [(16,46), # Yachay Tech
          (0,0), (0,57), (0,141),(0,170),
          (57,0), (57,57), (57,141), (57,170),
          (87,0), (87,87), (87,170),
          (141,0), (141,57), (141,141), (141,170),
          (170,0), (170,57), (170,141), (170,170) ]

# TODO: make these input parameters
inpath = '../../data/1D/2022/2022_hists.npy'
outpath = '../../data/graphics/1D/2022/2022_hists_points.csv'

# ----------------------------------------------------------------
myname = os.path.basename(__file__)[:-3] # no need for .py suffix

results_dir = os.path.dirname( outpath )

if not os.path.isdir( results_dir ):
    eprint( myname + ': making results directory:', results_dir )
    os.makedirs( results_dir )

# instantiate the numpy source operator
src = npy_src.npy_src()
src.p.filepath = inpath 
src.run()   # read the numpy data

# output file
out = open( outpath, 'w' )
out.write( inpath + '\n' ) # report numpy file

# get dimensions
height,width,nbands = src.sink.shape

for i in range( len(pixels) ):
    
    y = pixels[i][0]
    x = pixels[i][1]

    # check if specified pixel is inside numpy array
    if y < 0 or y >= height:
        eprint( 'pixel: ', i, ' has out of range y value: ', y )
        continue

    # check if specified pixel is inside numpy array
    if x < 0 or x >= width:
        eprint( 'pixel: ', i, ' has out of range x value: ', x )
        continue
    
    # report pixel position to file as y,x
    out.write( str(y) +',' + str(x) + ',' )

    # retrieve the specified pixel's data
    v = src.sink[y,x,:] # numpy uses y,x format

    # write out values 
    for k in range( nbands-1 ):
        out.write( str( v[k] ) + ',' )
    
    out.write( str( v[nbands-1] ) + '\n' )
        
out.close()
           


