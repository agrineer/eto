#!/usr/bin/env python3
'''
@file mpi_diff.py
@author Scott L. Williams, in collaboration with Elisa Piispa, Israel Pineda, María Solis-Aulestia, Cristina Yánez
@package ETo
@brief cycle through all lut possibilties and keep the lut with minimum difference
@LICENSE
# 
#  mpi_diff.py Copyright (C) 2020-2026 Scott L. Williams.
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
# cycle through all lut possibilties and keep the lut with minimum difference

import os
import sys
import math
import getopt
import mpi4py
import pickle
import numpy as np

from mpi4py import MPI
from render import render
from npy_src import npy_src
from ezprint import eprint, eprints

from itertools import permutations, cycle
from more_itertools import nth_permutation

mpi_diff_copyright = 'mpi_diff.py Copyright (c) 2020-2026 Scott L. Williams, released under GNU GPL V3.0'

# exhaustively run through LUT permutations for least pixel
# difference between clustered images.
#
# however the brute force approach takes (lots of) time.
# ie. for a lut of 12 elements it takes 12! (479,001,600) iterations
def compare_luts( image1, image2, nlabels, index, niter ):
    '''
    lut = [0,1,2,3,4,5,6,7,8,9,10,11 ]
    lut = np.array( lut ).astype(np.uint8)
    return rank, lut
    '''
    pxtotal = image1.shape[0] * image1.shape[1]
    sniter = str( niter )
                   
    # generate unique LUT values, ie. 0,1,2,3,...,N-1
    labels = [ i for i in range(nlabels) ]   # find unique permutations for this array
    
    mindiff = math.inf
    minlut = None
 
    i = 0
    end = index + niter
    
    # test each LUT for minimum pixel difference
    for i in range( index, end ):
        
        if i%100000 == 0 and rank == 0:
            eprints( "\x1b[2K" )  # clear the terminal line
            eprints( '\r' + myname + 'i =', i,
                     'of ' + sniter + ' %done =', '%6.3f,'%(i/float(niter)*100.0),
                     'min diff = ' + str(mindiff),
                     '%diff =', '%6.3f'%(mindiff/float(pxtotal)*100.0) + ' ' )
        
        # get the LUT permutation
        l = nth_permutation( labels, 12, i )
        lut = np.array( l ).astype( np.uint8 )
        
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

        if rank == 0:
            eprints( next(spinner) )
            eprints('\b')
 
        i += 1

    if rank == 0:
        eprint( '\n' )
        
    return mindiff, minlut

# make data into an image
def render_image( rndr, data, path ):

    eprints( myname + ': writing image to: ' + path + ' ...' )

    # render the image
    rndr.source = data
    rndr.p.filepath = path
    rndr.run()
    eprint( ' done' )

# setup variables, etc. for rank == 0
def set_up():

    # declare versions
    eprint( myname + ':    python version =', sys.version[0:6])
    eprint( myname + ':     numpy version =', np.version.version )
    eprint( myname + ':    mpi4py version =', mpi4py.__version__ )
    eprint( myname + ':      num of ranks =', size )

    first_path, second_path, nclasses = set_params( sys.argv[1:] )

    # how big? split up iterations
    total = math.factorial( nclasses )
    eprint( myname + ':   number of iterations =', total )

    chunk = int(total/size)
    remainder = total%size

    # send values to other ranks
    for i in range( 1, size ):

        comm.send( nclasses, dest=i, tag=11 )

        index = chunk*i
        comm.send( index, dest=i, tag=12 )

        if i == size-1:
            niter = chunk + remainder
            comm.send( niter, dest=i, tag=13 )
 
        else:
            niter = chunk
            comm.send( niter, dest=i, tag=13 )

    # read images
    src1 = npy_src.npy_src()  # first image
    src1.p.verbose = False
    src1.p.filepath = first_path
    src1.run()
    first = src1.sink # for readabilty

    src2 = npy_src.npy_src()  # second image
    src2.p.verbose = False
    src2.p.filepath = second_path
    src2.run()
    second = src2.sink
    
    if first.shape != second.shape:
        eprint( myname + ': image sizes do not match..exiting.' )
        sys.exit( 2 )

    for i in range( 1, size ):
        comm.Send( [first, MPI.BYTE], dest=i, tag=77 )
        comm.Send( [second, MPI.BYTE], dest=i, tag=78 )

    return first, second, nclasses, chunk

def show_results( first, second, lut ):

    rndr = render.render()
    rndr.p.verbose = False

    # render the first image
    rndr.readlut( '/home/agrineer/poli/luts/cetin.lut' ) 
    render_image( rndr, first, 'first.jpg' )

    # render the second image, keep cetin lut
    render_image( rndr, second, 'second.jpg' )

    transcribed = lut[ second ].astype( np.uint8 ) # transcribe classes

    # render the transcribed image
    render_image( rndr, transcribed, 'transcribed.jpg' )
 
    # take the difference
    diff = transcribed - first     # wrap around ok
    mask = (diff != 0)             # mask is logical False, True

    # highlight pixels in white (255) that are different
    out = np.zeros( first.shape, dtype=np.uint8 )
    np.putmask( out, mask, 255 )

    # show the difference image, black/white pixels
    rndr.readlut( '/home/agrineer/poli/luts/ramp.lut' )
    render_image( rndr, out, 'diff.jpg' )

    count = np.count_nonzero( out )
    return count

def wrap_up( first, second, mindiff, minlut ):

    # root (rank==0) values
    diff = mindiff
    lut = minlut 
    eprint( myname + ': rank 0 diff = ', mindiff, 'lut = ', minlut )
    
    # get other ranks values and find minimum
    for i in range(1,size):
        
        mindiff = comm.recv( source=i, tag=81 )
        minlut = np.empty( (nclasses), dtype=np.uint8 )
        comm.Recv([minlut, MPI.BYTE], source=i, tag=82)

        eprint( myname + ': rank', i, 'diff = ', mindiff, 'lut = ', minlut )

        if mindiff < diff:
            diff = mindiff
            lut = minlut
            
    eprint( myname + ': minimum difference: ' + str(diff) )
    eprint( myname + ': minimum LUT: ', lut )

    count = show_results( first, second, lut )
    
    # number pixels ==  nx*ny
    npix = first.shape[0]*first.shape[1]
    pcent = (count/float(npix))*100

    # report to terminal
    ostr = myname + ': num of diff pixels=' + '%d,'%count + ' % diff=' + '%.2f'%pcent
    eprint( ostr )
    
def usage():
        
    eprint( '\nusage: mpi_diff.py' )
    eprint( '       -h, --help' )
    eprint( '       -c num_classes, --classes=num_classes' )
    eprint( '       -f file, --first=file       # first input numpy image' )
    eprint( '       -s file, --second=file      # second input numpy image' )
    eprint( '' )
    sys.exit(0)
    
def set_params( argv ):
    
    first_path = None
    second_path = None
    nclasses = None
    
    try:                                
        opts, args = getopt.getopt( argv, 'hc:f:s:', ['help','classes=',
                                                      'first=','second='] )
            
    except getopt.GetoptError as e:
        eprint( myname + ': ' + str(e) )
        usage()                          
                   
    for opt, arg in opts:
            
        if opt in ( '-h', '--help' ):      
            usage()                     

        if opt in ('-c', '--classes'):
            nclasses = int(arg)

            if nclasses <= 1:
                eprint( myname + ': number of class must be > 0' )
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
        eprint( myname + ': number of classes not  given ... exiting' )
        usage()

    eprint( myname + ': using parameters:')
    eprint('       first image path = ' + first_path )
    eprint('      second image path = ' + second_path )
    eprint('      number of classes = ' + str(nclasses) )
 
    return first_path, second_path, nclasses

#-----------------------------------------------------------------

# some globals
spinner = cycle( ['\\','-', '|', '-', '/', '-','|'] ) # spinner chars

# get oriented
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

myname = os.path.basename(__file__)[:-3]+  ': rank ' + str(rank) + ': '

if rank == 0:

    # get images, num classes, calculate iteration chunks
    first, second, nclasses, chunk = set_up()
    
    # this rank's index and iteration size
    index = 0
    niter = chunk
else:

    # get data from root
    nclasses = comm.recv( source=0, tag=11 )
    index = comm.recv( source=0, tag=12 )
    niter = comm.recv( source=0, tag=13 )

    # images to compare
    first = np.empty((171,171,1), dtype=np.uint8)
    comm.Recv([first, MPI.BYTE], source=0, tag=77)
 
    second = np.empty((171,171,1), dtype=np.uint8)
    comm.Recv([second, MPI.BYTE], source=0, tag=78)

# all ranks
comm.Barrier()

# heavy lifting here
mindiff, minlut = compare_luts( first, second, nclasses, index, niter )

if rank == 0:
    eprint( myname + ': waiting for all ranks to finish ...' )

# wait for all ranks to finish
comm.Barrier()

# phone home
if rank != 0:
    comm.send( mindiff, dest=0, tag=81 )
    comm.Send( [minlut, MPI.BYTE], dest=0, tag=82 )

# gather diff, luts and find minimum
if rank == 0:
    wrap_up( first, second, mindiff, minlut )

MPI.Finalize()
