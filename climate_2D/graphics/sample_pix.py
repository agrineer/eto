#! /usr/bin/env python

'''
@file sample_pix.py
@author Scott L. Williams, in collaboration with Elisa Piispa, Israel Pineda, María Solis-Aulestia, Cristina Yánez
@package ETo
@brief populate regional pixels with temporal weather signals for discrimation
@LICENSE
# 
#  sample_pix.py Copyright (C) 2026 Scott L. Williams.
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

# sample a pixel for its 2D image

sample_pix_copyright = 'sample_pix.py Copyright (c) 2026 Scott L. Williams, released under GNU GPL V3.0'

import os
import sys
import getopt
import pickle

import numpy as np
from norm import norm
from render import render
from npy_src import npy_src
from ezprint import eprint, eprints

# ------------------------------------------------------------------------

# make pixel vector into an image
def render_image( image, path ):

    eprints( myname + ': writing image to: ' + path + ' ...' )

    # normalize since uin8 values don't get stretched
    n = norm.norm()
    n.source = image
    n.verbose = False
    n.run()
    
    rndr = render.render()

    rndr.source = n.sink
    rndr.p.filepath = path
    rndr.p.greybuf = 0
    rndr.p.RGB = False
    rndr.p.verbose = False

    rndr.run()
    eprint( ' done' )

def error_checks( data ):
                   
    # get size of input image
    sizey, sizex, nbands = data.shape
    
    if (sizey != 171) or (sizex != 171 ) or (nbands != 9125 ):
        eprint( '\n' + myname +
                ': wrong data size...exiting' )
        sys.exit(1 )

    # check if more than 25 classes
    if np.max( data ) > 24:
        eprint( '\n' + myname +
                ': data contains values greater than 24...exiting' )
        sys.exit( 1 )

def usage():
        
    eprint( '\nusage: ' + myname + '.py' )
    eprint( '       -h, --help' )
    eprint( '       -a flag, --append=flag' )
    eprint( "         where flag is one of 'C','F'" )
    eprint( "         'C' indicates row append (C language type)" )
    eprint( "         'F' indicates column append (Fortran type)" )
    eprint( '       -c y,x, --coord=y,x' )
    eprint( '       -i infile, --infile=infile' )
    eprint( '       -p file_prefix, --prefix=file_prefix' )
    eprint( '       -o outdir, --outdir=outdir' )
    eprint( '' )
    sys.exit( 1 )

def set_params( argv ):
    
    append = None
    infile = None
    outdir = None
    prefix = None
    py = None
    px = None
     
    try:                                
        opts, args = getopt.getopt( argv, 'ha:c:i:o:p:',
                                    ['help','append=','coord',
                                     'infile=','outfile=','prefix=' ])
            
    except getopt.GetoptError as e:
        eprint( myname + ': ' + str(e) )
        usage()                          
                   
    for opt, arg in opts:
            
        if opt in ( '-h', '--help' ):      
            usage()
            
        if opt in ( '-a', '--append' ):
            append = arg
            if append not in ( 'C', 'c', 'F', 'f' ):
                eprint( myname + \
                        ": append flag must be in ('C','c','F','f') ... exiting.")
                usage()

        if opt in ( '-c', '--coord' ):
            c = arg.split(',')
            py = int( c[0] )
            px = int( c[1] )

            if py < 0 or py > 170:
                eprint( myname + \
                        ': pixel y cannot be out of range (0..170) ... exiting' )
                usage()
                
            if px < 0 or px > 170:
                eprint( myname + \
                        ': pixel x cannot be out of range (0..170) ... exiting' )
                usage()
                
        if opt in ( '-i','--infile'):
            infile = arg
            if not os.path.isfile( infile ):
                eprint( myname + \
                        ': input file: ' + infile + \
                        ' does not exist ... exiting.')
                usage()               

        if opt in ( '-p','--prefix'):
            prefix = arg
            
        if opt in ( '-o', '--outdir' ):
            outdir = arg
            if not os.path.isdir( outdir ):
                eprint( '\n' + myname + ': making directory:', outdir )
                os.makedirs( outdir, exist_ok=True )

    if append == None:
        eprint( myname + ": must have append type: 'C' or 'F' ... exiting" )
        usage()

    if py == None:
        eprint( myname + ': must have pixel coordinates ... exiting' )
        
    if infile == None:
        eprint( myname + ': must have an input file ... exiting' )
        usage()

    if prefix == None:
        eprint( myname + ': must have an output file prefix ... exiting' )
        usage()
 
    if outdir == None:
        eprint( myname + ': must have an output directory ... exiting' )
        usage()

    eprint( myname + ': using parameters:' )
    eprint( '           append type =', append )
    eprint( '                    py =', py )
    eprint( '                    px =', px )
    eprint( '                prefix =', prefix )
    eprint( '                infile =', infile )
    eprint( '                outdir =', outdir )

    return append, px, py, infile, outdir, prefix

#-----------------------------------------------------------------------------

# some globals
myname = os.path.basename(__file__)[:-3] # no need for .py suffix
#spinner = itertools.cycle( ['\\','-', '|', '-', '/', '-','|'] ) # spinner chars
                                    
if __name__ == '__main__':

    # declare versions
    eprint( myname + ': python version =', sys.version[0:6])
    eprint( myname + ': numpy version  =', np.version.version )

    append, px, py, infile, outdir, prefix = set_params( sys.argv[1:] )

    # get the input data
    src = npy_src.npy_src() # instantiate the numpy source
    src.p.verbose = False
    src.p.filepath = infile
    src.run()
    data = src.sink

    error_checks( data )
    
    # get pixel vector
    pixel = data[py,px]
    
    if append == 'F':
        image = pixel.reshape( 365, 25, 1, order='F' )
        
    elif append == 'C':
        image = pixel.reshape( 365, 25, 1, order='C' )
        
    else:
        eprint( myname + ': unknown stack (append) flag ... exiting' )
        usage()
        
    outfile = outdir + '/' + prefix + str(py) + '_' + str(px) + '.npy'
    eprints( myname + ': outputting numpy data: ' + outfile + ' ... ' )

    # needs to be protocol = 4
    out = open( outfile, 'wb' )
    pickle.dump( image, file=out, protocol=4 )
    out.close()
    eprint( ' done' )

    # png image
    outfile = outdir + '/' + prefix + str(py) + '_' + str(px) + '.png'
    render_image( image, outfile )

    eprint( myname + ': done' )
