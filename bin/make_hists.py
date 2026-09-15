#! /usr/bin/env python3

'''
@file make_hists.py
@author Scott L. Williams, in collaboration with Elisa Piispa, Israel Pineda, María Solis-Aulestia, Cristina Yánez
@package ETo
@brief Read labeled images and construct a weather histogram for each pixel
@LICENSE
# 
#  make_hists.py Copyright (C) 2020-2026 Scott L. Williams.
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

make_hists_copyright = 'make_hists.py Copyright (c) 2020-2026 Scott L. Williams, released under GNU GPL V3.0'

import os
import sys
import glob
import getopt
import pickle
import itertools

import numpy as np
from npy_src import npy_src
from ezprint import eprint, eprints

# ------------------------------------------------------------------------

# check if data files exist
def check_datafiles( datafiles ):

    eprints( myname + 
             ': checking if data files exist ... ' )
    
    for f in datafiles:

        if not os.path.isfile( f ):
            eprint( '\n' + myname +
                    ': data file:', f, 'does not exist...exiting' )
            sys.exit( 1 )

        eprints( next(spinner) )
        eprints('\b')
    
    eprint( 'yes' )
    
def error_checks( image ):
    
    # error checks
    if image.dtype != np.uint8:
        eprint( myname +
                ': image type is not uint8...exiting' )
        sys.exit( 1 )
                
    # get size of input image
    sizey, sizex, nbands = image.shape
    if (sizex != 171) or (nbands != 1):
        eprint( myname +
                ': wrong data sizes...exiting')
        sys.exit(1 )

    # check if more than 25 classes
    if np.max( image ) > 24: # zero indexed
        eprint( myname +
                ': image contains values greater than 24...exiting' )
        sys.exit( 1 )

    # check if y size is evenly divisible by 171
    if sizey%171 != 0:
        eprint( myname +
                ': image ysize not divisible by 171 ...exiting' )
        sys.exit( 1 )

    ndays = int( sizey/171 )
    return ndays

def usage():
        
    eprint( '\nusage: ' + myname + '.py' )
    eprint( '       -h, --help' )
    eprint( '       -o outfile, --outfile=outfile' )
    eprint( '       -y years, --years=years' )
    eprint( ' where years is a comma separated list containing 2022,2023,2024' )
    eprint( '' )
    sys.exit(0)

def set_params( argv ):
    outfile = None
    years = None
    
    try:                                
        opts, args = getopt.getopt( argv, 'hy:o:',
                                    ['help','years=','outfile='] )
            
    except getopt.GetoptError as e:
        eprint( myname + ': ' + str(e) )
        usage()                          
                   
    for opt, arg in opts:
            
        if opt in ( '-h', '--help' ):      
            usage()                     

        if opt in ( '-o', '--outfile' ):
            outfile = arg
            
        if opt in ( '-y', '--years' ):
            years = arg.split(',')
            nyears = len( years )
            for i in range( nyears ):
                if years[i] not in ( '2022','2023','2024'):
                    eprint( myname +
                        ': year must be in (2022,2023,2024)' )
                    eprint( myname + ': got ' + years[i] + '.. exiting' )
                    usage()

    if years == None:
        eprint( myname + ': must have a year in (2022,2023,2024)' )
        usage()
       
    if outfile == None:
        eprint( myname + ': must have an outfile ... exiting' )
        usage()

    return years, outfile

# -----------------------------------------------------------------------------

# some globals
myname = os.path.basename(__file__)[:-3] # no need for .py suffix
spinner = itertools.cycle( ['\\','-', '|', '-', '/', '-','|'] ) # spinner chars
src = npy_src.npy_src() # instantiate the numpy source
                                   # object and reuse
if __name__ == '__main__':

    datafiles = []

    # declare version
    eprint( myname + ': python version =', sys.version[0:6])
    eprint( myname + ': numpy version  =', np.version.version )

    years, outfile = set_params( sys.argv[1:] )
    dd = '../data/classes/'
    
    for i in range( len(years) ):

        # be specific about files
        for j in ['-ENE','-FEB','-MAR','-ABR','-MAY','-JUN',
                  '-JUL','-AGO','-SEP','-OCT','-NOV','-DIC'] :
            
            datafiles.append( dd + years[i] + '/' + years[i] + j + '.npy'  )

    check_datafiles( datafiles )

    outdir = os.path.dirname( outfile )
    if not os.path.isdir( outdir ):
        eprint( '\n' + myname + ': making directory:', outdir )
        os.makedirs( outdir, exist_ok=True )

    # fixed array size and number of classes
    hist = np.zeros( shape=(171,171,25), dtype=np.uint16 )
    
    for f in datafiles:

        # read the file
        src.p.filepath = f
        src.run()
            
        image = src.sink
        ndays = error_checks( image )
            
        eprints( '\r' + myname + ': processing', f, ' ' )
            
        for k in range(0,ndays):
                
            day = image[ 171*k:171*(k+1),:,: ] # get day chunk
            
            for j in range(0,171):      # TODO: might try 'fancy' indexing
                for i in range( 0,171 ):
                        
                    hist[j,i,image[j,i]] += 1
                    
                    eprints( next(spinner) )
                    eprints('\b')


    eprints( '\x1b[2K' )  # clear the line
    eprints( '\r' + myname + ': processing ... done' )
    eprints( '\n' + myname + ': outputing data ... ' )

    out = open( outfile, 'wb' )
    pickle.dump( hist, file=out, protocol=4 )
    out.close()
    eprint( myname + ': done' )
