#!/usr/bin/env python

'''
@file brute_diff.py
@author Scott L. Williams, in collaboration with Elisa Piispa, Israel Pineda, María Solis-Aulestia, Cristina Yánez
@package ETo
@brief show the pixel difference between two differently labeled images
@LICENSE
#
#  brute_diff.py Copyright (C) 2026 Scott L. Williams. 
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
brute_diff_copyright = 'brute_diff.py Copyright (c) 2026 Scott L. Williams, released under GNU GPL V3.0'

# show the pixel difference between two differently labeled images
# by cycling through all lut possibilties and to keep the lut with
# minimum difference

import os
import sys
import math
import getopt
import pickle
import numpy as np

from render import render
from npy_src import npy_src
from ezprint import eprint, eprints

from itertools import permutations, cycle

brute_diff_copyright = 'brute_diff.py Copyright (c) 2020-2026 Scott L. Williams, released under GNU GPL V3.0'

# exhaustively run through LUT permutations for least pixel
# difference between cluster images.
#
# however the brute force approach takes (lots of) time.
# ie. for a lut of 12 elements it takes 12! (479,001,600) iterations
def compare_luts( image1, image2, nlabels ):

    pxtotal = image1.shape[0] * image1.shape[1]
    
    # generate unique LUT values, ie. 0,1,2,3,...,N-1
    labels = [ i for i in range(nlabels) ]   # find unique permutations # for this array
    eprint( myname + ': using label array:\n', labels )
    
    mindiff = math.inf
    minlut = None
 
    total = str( math.factorial( nclasses ) )
    i = 0

    # test each LUT for minimum pixel difference
    for l in permutations( labels ):

        if i%100000 == 0:
            eprints( "\x1b[2K" )  # clear the terminal line
            eprints( '\r' + myname + ': i =', i,
                     'of ' + total + ' %done =', '%6.3f,'%(i/float(total)*100.0),
                     'min diff = ' + str( mindiff),
                     '%diff =', '%6.3f'%(mindiff/float(pxtotal)*100.0) + ' ' )
 
        # get the LUT permutation
        lut = np.array( l )
        
        # transcribe labels from first run for comparison
        transcribed = lut[ second ].astype( np.uint8 )

        # take the difference
        diff = first - transcribed     # doesn't matter if it wraps around
        mask = (diff != 0)             # mask is logical False, True

        # highlight pixels in white that are different
        out = np.zeros( first.shape, dtype=np.uint8 )
        np.putmask( out, mask, 255 )

        count = np.count_nonzero( out )
        if count < mindiff:
            minlut = lut;
            mindiff = count

        eprints( next(spinner) )
        eprints('\b')
 
        i += 1
        
    return minlut

# make data into an image
def render_image( data, path ):

    eprints( myname + ': writing image to: ' + path + ' ...' )

    # render the image
    rndr.source = data
    rndr.p.filepath = path
    rndr.run()
    eprint( ' done' )
    
def usage():
        
    eprint( '\nusage: brute_diff.py' )
    eprint( '       -h, --help' )
    eprint( '       -n nclasses, --nclasses=nclasses # where nclasses > 1' )
    eprint( '       -f file, --first=file       # first input image' )
    eprint( '       -s file, --second=file      # second input image' )
    eprint( '' )
    sys.exit(0)
    
def set_params( argv ):
    
    first_path = None
    second_path = None
    nclasses = None
    
    try:                                
        opts, args = getopt.getopt( argv, 'hn:f:s:', ['help','nclasses=','first=','second='] )
            
    except getopt.GetoptError as e:
        eprint( myname + ': ' + str(e) )
        usage()                          
                   
    for opt, arg in opts:
            
        if opt in ( '-h', '--help' ):      
            usage()                     

        if opt in ('-n', '--nclasses'):
            nclasses = int(arg)

            if nclasses <= 1:
                eprint( myname + ': number of class must be > 1' )
                usage()

        if opt in ('-f', '--first'):               
            if not os.path.isfile( arg ):
                eprint( myname + ': file: ' + arg + ' not found ... exiting' )
                usage()

            first_path = arg

        if opt in ('-s', '--second'):
            if not os.path.isfile( arg ):
                eprint( myname + ': file: ' + arg + ' not found ... exiting' )
                usage()

            second_path = arg
            
    if first_path == None:
        eprint( myname + ': first image file path not given ... exiting' )
        usage()
        
    if second_path == None:
        eprint( myname + ': second image file path not given ... exiting' )
        usage()
        
    if nclasses == None:
        eprint( myname + ': number of classes not classes not given ... exiting' )
        usage()

    eprint( myname + ': using parameters:')
    eprint('       first image path = ' + first_path )
    eprint('      second image path = ' + second_path )
    eprint('      number of classes = ' + str(nclasses) )
 
    return first_path, second_path, nclasses

#-----------------------------------------------------------------

# some globals
myname = os.path.basename(__file__) # no need for .py suffix
spinner = cycle( ['\\','-', '|', '-', '/', '-','|'] ) # spinner chars
rndr = render.render( 'render' )
rndr.p.verbose = False

if __name__ == '__main__':

    # declare versions
    eprint( myname + ': python version =', sys.version[0:6])
    eprint( myname + ': numpy version  =', np.version.version )

    first_path, second_path, nclasses  = set_params( sys.argv[1:] )

    # read images
    src1 = npy_src.npy_src( 'npy_src' )  # first image
    src1.p.filepath = first_path
    src1.run()
    first = src1.sink # for readabilty

    src2 = npy_src.npy_src( 'npy_src' )  # second image
    src2.p.filepath = second_path
    src2.run()
    second = src2.sink
    
    if first.shape != second.shape:
        eprint( myname + ': image sizes do not match..exiting.' )
        sys.exit( 2 )

    eprint( myname + ': comparing images:', first_path, 'and', second_path )

    lut = compare_luts( first, second, nclasses )
    #lut = [0,1,2,3,4,5,6,7,8,9,10,11]
    #lut = np.array( lut )
    eprint( myname + ': LUT = ', lut )
    
    # render the first image
    rndr.readlut( '../data/luts/cetin.lut' ) 
    render_image( first, 'first.jpg' )

    # render the second image, keep cetin lut
    render_image( second, 'second.jpg' )

    transcribed = lut[ second ].astype( np.uint8 ) # transcribe classes

    # render the transcribed image
    render_image( transcribed, 'transcribed.jpg' )
 
    # take the difference
    diff = transcribed - first     # wrap around ok
    mask = (diff != 0)             # mask is logical False, True

    # highlight pixels in white (255) that are different
    out = np.zeros( first.shape, dtype=np.uint8 )
    np.putmask( out, mask, 255 )

    # show the difference image, black/white pixels
    rndr.readlut( '../data/luts/ramp.lut' )
    render_image( out, 'diff.jpg' ) 

    # report to terminal
    count = np.count_nonzero( out )
        
    # number pixels =  nx*ny
    npix = first.shape[0]*first.shape[1]
    pcent = (count/float(npix))*100

    ostr = myname + ': num of diff pixels=' + '%d,'%count + ' % diff=' + '%.2f'%pcent
    eprint( ostr )
