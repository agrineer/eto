#! /usr/bin/env python3

'''
@file make_dwdata.py
@author Scott L. Williams, in collaboration with Elisa Piispa, Israel Pineda, María Solis-Aulestia, Cristina Yánez
@package ETo
@brief populate regional pixels with temporal weather signals for discrimation
@LICENSE
# 
#  make_dwdata.py Copyright (C) 2026 Scott L. Williams.
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

# read label images and construct a timelime of weather class values a
# histogram for each regional pixel

make_tw_copyright = 'make_dwdata.py Copyright (c) 2026 Scott L. Williams, released under GNU GPL V3.0'

import os
import sys
import getopt
import pickle
import tempfile
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
        eprint( '\n' + myname +
                ': image type not uint8...exiting' )
        sys.exit( 1 )
                
    # get size of input image
    sizey, sizex, nbands = image.shape
    if (sizex != 171) or (nbands != 1):   # poli assigns a band (z-buffer)
                                          # to 2-D image
        eprint( '\n' + myname +
                ': wrong image sizes...exiting' )
        sys.exit(1 )

    # check if more than 25 classes
    if np.max( image ) > 24:
        eprint( '\n' + myname +
                ': image contains values greater than 24...exiting' )
        sys.exit( 1 )

    # check if y size is evenly divisible by 171
    if sizey%171 != 0:
        eprint( '\n' + myname +
                ': image ysize not divisible by 171 ...exiting' )
        sys.exit( 1 )

    ndays = int( sizey/171 )
    
    return ndays

# return total number of days
def get_tdays( datafiles ):

    eprints( myname +
             ': checking files and getting total number of days ... ' )

    # read numpy files to get info
    tdays = 0
        
    for f in datafiles:
        src.p.filepath = f
        src.run()
        tdays += error_checks( src.sink )
        eprints( next(spinner) )
        eprints('\b')

    eprint( 'done' )
    return tdays        

# from scipy cookbook
def smooth_vector( z, wlen=11, window='hanning' ):
    """smooth the data using a window with requested size.
    
    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal 
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.
    
    input:
        z: the input signal 
        window_len: the dimension of the smoothing window; should be an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett',
                'blackman'. flat window will produce a moving average smoothing.

    output:
        the smoothed signal
        
    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)
    
    see also: 
    
    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter
 
    TODO: the window parameter could be the window itself if an array instead of a string
    NOTE: length(output) != length(input)
          to correct this: return y[(window_len/2-1):-(window_len/2-1)] instead of just y.
    """
    
    if z.ndim != 1:
        raise ValueError( myname + ": Smooth only accepts 1 dimension arrays.")

    if z.size < wlen:
        raise ValueError( myname + ": Input vector needs to be bigger than window size." )

    if wlen < 3:
        raise ValueError( myname + ": Window size must => 3." )

    if wlen%2 != 1:
        raise ValueError( myname + ": Window size must be an odd value." )     

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError( "Window is either 'flat','hanning','hamming','bartlett','blackman'" )

    s = np.r_[z[wlen-1:0:-1],z,z[-2:-wlen-1:-1]] # reflect ends

    if window == 'flat': # moving average
        w = np.ones( wlen, 'd' )
    else:
        w = eval( 'np.' + window +'(wlen)')

    y = np.convolve( w/w.sum(), s, mode='valid' )

    # return same size as input signal
    hwl = int( (wlen-1)/2 )
    return y[ hwl:-hwl ]

def smooth_classes( dw_data, window, length ):

    numy, numx, ndays, nclasses = dw_data.shape

    # allocate smoothed day-weather buffer
    smap = tempfile.NamedTemporaryFile( delete_on_close=True )
    sdata = np.memmap( smap, dtype=np.float32, mode='w+',
                       shape=(numy,numx,ndays,nclasses) )

    eprint( myname + ': smoothing class columns with window=' + \
            window + ', and length=' +  str(length) )

    for j in range( 0, numy ):
        for i in range( 0, numx ):
            
            eprints( "\x1b[2K" )  # clear the terminal line
            eprints( '\r' + myname + ': smoothing pixel = '
                     + str(j) + ',' + str(i) + ' ' )
            
            # smooth this pixel's class columns
            # NOTE: convoluting a kernel across the class days
            #       will radiate values into neighboring days. 
            #
            #       TODO: look into SOM neighbor similarity map and see
            #             if this can be used to make an improvement.
            #             for example, rearrange the class grid so that
            #             instead of 3x4 neural grid, it has a 1x12 grid so that
            #             when incorporating as an axis the neighbor points
            #             are more closely similar, and with similarity better
            #             expressed as 1D neighbors. then smoothing in 2D before
            #
            for k in range( nclasses ):
                sdata[j,i,:,k] = smooth_vector( dw_data[j,i,:,k], length, window )
                #eprints( next(spinner) )
                #eprints('\b')
            
    eprints( "\x1b[2K" )  # clear the line
    eprint( '\r' + myname + ': smoothing ... done' )

    return sdata

def smooth_days( dw_data, window, length ):

    numy, numx, ndays, nclasses = dw_data.shape

    # allocate smoothed day-weather buffer
    smap = tempfile.NamedTemporaryFile( delete_on_close=True )
    sdata = np.memmap( smap, dtype=np.float32, mode='w+',
                       shape=(numy,numx,ndays,nclasses) )

    eprint( myname + ': smoothing day rows with window=' + window + \
            ', and length=' +  str(length) )
    for j in range( 0, numy ):
        for i in range( 0, numx ):
            
            eprints( "\x1b[2K" )  # clear the terminal line
            eprints( '\r' + myname + ': smoothing pixel = '
                     + str(j) + ',' + str(i) + ' ' )
            
            # NOTE: convoluting a kernel across the class impulses in the day row
            #       will radiate values into neighbor classes and does not
            #       radiate into the previous or future days. 
            #
 
            for k in range( ndays ):
                sdata[j,i,k,:] = smooth_vector( dw_data[j,i,k,:], length, window )
                #eprints( next(spinner) )
                #eprints('\b')
            
    eprints( "\x1b[2K" )  # clear the line
    eprint( '\r' + myname + ': smoothing ... done' )

    return sdata

def usage():
        
    eprint( '\nusage: ' + myname + '.py' )
    eprint( '       -h, --help' )
    eprint( '       -a flag, --append=flag' )
    eprint( "         where flag is one of 'C','F'" )
    eprint( "         'C' indicates row append (C language type)" )
    eprint( "         'F' indicates column append (Fortran type)" )
    eprint( '          where flag is true or false' )
    eprint( '       -o outfile, --outfile=outfile' )
    eprint( '       -s C/F --smooth=C/F # where C->row and F->columns smoothing')
    eprint( '       -w window, --window=window' )
    eprint( "         where window is either 'flat','hanning','hamming','bartlett','blackman'" )
    eprint( '       -l window_length, --length=window_length # must be odd' )
    eprint( '       -y years, --years=years' )
    eprint( '       where years is a comma separated list containing 2022,2023,2024' )

    eprint( '' )
    sys.exit( 1 )

def set_params( argv ):

    # must specify all (for the moment)
    outfile = None
    years = None
    length = None
    window = None
    smooth = None
    append = None
   
    try:                                
        opts, args = getopt.getopt( argv, 'ha:l:o:s:w:y:',
                                    ['help','append=','length=','muestra=','outfile= ',
                                     'smooth=','window','years='] )
            
    except getopt.GetoptError as e:
        eprint( myname + ': ' + str(e) )
        usage()                          
                   
    for opt, arg in opts:
            
        if opt in ( '-h', '--help' ):      
            usage()
            
        if opt in ( '-a', '--append' ):
            if arg not in ( 'C', 'c', 'F', 'f' ):
                eprint( myname + ": append flag must be in ('C','c','F','f') ... exiting.")
                usage()
            append = arg
  
        if opt in ( '-o', '--outfile' ):
            outfile = arg

        if opt in ('-l', '--length'):
            
            length = int( arg )
            if length%2 == 0 or length < 3:
                eprint( myname + ': length must be >= 3 and odd, got: ' +
                        arg + ' exiting...' )
                usage()

        if opt in ('-s', '--smooth'):
 
            if arg in ( 'c', 'C' ):
                smooth = 'C'
                
            elif arg in ( 'f','F' ):
                smooth = 'F'
                
            else:
                eprint( myname +
                        ': smooth option must be "C" or "F" ... got: ', arg,
                        ' exiting...' )
                usage()

        if opt in ('-w','--window'):
 
            if arg not in ('flat', 'hanning', 'hamming', 'bartlett', 'blackman'):
                eprint( myname +
                        ": window must be 'flat', 'hanning', 'hamming','bartlett', or 'blackman' ... exiting" )
                usage()
                
            window = arg

        if opt in ( '-y', '--years' ):
            years = arg.split(',')
            nyears = len( years )
            for i in range( nyears ):

                if years[i] not in ( '2022','2023','2024'):
                    eprint( myname +
                        ': year must be in (2022,2023,2024)' )
                    eprint( myname + ': got ' + years[i] + '.. exiting' )
                    usage()
            years = sorted( years ) # make sequential

    if append == None:
        eprint( myname + ": must have append type: 'C' or 'F' ... exiting" )
        usage()

    if years == None:
        eprint( myname + ': must have a year in (2022,2023,2024)' )
        usage()
       
    if outfile == None:
        eprint( myname + ': must have an outfile ... exiting' )
        usage()

    if smooth != None:
        
        if window == None:
            eprint( myname + ': must have a window for smoothing ... exiting' )
            usage()
            
        if length == None:
            eprint( myname + ': must have a a window length for smoothing ... exiting' )
            usage()

    eprint( myname + ': using parameters:' )
    eprint( '           append type =', append )
    eprint( '               outfile =', outfile )
    eprint( '                 years =', years )
    eprint( '                smooth =', smooth )
    eprint( '                window =', window )
    eprint( '                length =', length )

    return years, outfile, smooth, window, length, append

#-----------------------------------------------------------------------------

# some globals
myname = os.path.basename(__file__)[:-3] # no need for .py suffix
spinner = itertools.cycle( ['\\','-', '|', '-', '/', '-','|'] ) # spinner chars
src = npy_src.npy_src() # instantiate the numpy source
src.p.verbose = False

if __name__ == '__main__':

    # declare versions
    eprint( myname + ': python version =', sys.version[0:6])
    eprint( myname + ': numpy version  =', np.version.version )

    years, outfile, smooth, window, length, append = set_params( sys.argv[1:] )

    datafiles = []

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

    tdays = get_tdays( datafiles ) # error checks and get total number of days

    # construct temporal class assigment as a 2D array for each pixel.
    # 25 weather classes on one axis (x) and days on the other (y)
    # even though it gets flattened for machine learning purposes.
    
    # allocate day-weather data, memory map it
    dw_mmap = tempfile.NamedTemporaryFile( delete_on_close=True )
    dw_data = np.memmap( dw_mmap, dtype=np.uint8, mode='w+',
                         shape=(171,171,tdays,25) )
    
    # initialize with zeros
    dw_data[:,:,:,:] = 0
    day = 0
    
    for f in datafiles:

        # read the month class file
        src.p.filepath = f
        src.run()
            
        clabels = src.sink          # image of month class labels
        msizey = clabels.shape[0]   # get number of days for this month
        ndays = int( msizey/171 )
 
        for k in range(0,ndays):

            cday = clabels[ 171*k:171*(k+1),:,: ] # get day chunk

            # for each pixel populate the day's weather class
            # note that there is only one weather class per day
            #
            # TODO: for faster execution try array masking and/or
            #       'fancy' array indexing, meanwhile
            #       we have a working protype
            for j in range(0,171):          
                for i in range(0,171):
                    
                    dw_data[j,i,day,cday[j,i]] = 1
                   
                    eprints( next(spinner) )
                    eprints('\b')
                    
            day += 1
            eprints( '\r' + myname + ': processing ' + f +
                     ' day=' + str(day) + ' of ' + str(tdays) + ' ' )
                                
    eprints( "\x1b[2K" )  # clear the line
    eprint( '\r' + myname + ': processing ... done' )
 
    if smooth == 'F':

        # smooth the class columns
        dw_data = smooth_classes( dw_data, window, length,  )

    elif smooth == 'C':

        # smooth the day rows
        dw_data = smooth_days( dw_data, window, length,  )
         
    else:
        eprint( myname + ': no smoothing given' )

    # report max, min values
    minv = np.min( dw_data )
    maxv = np.max( dw_data )
    eprint( myname + ': max value = ' + str( maxv ) )
    eprint( myname + ': min value = ' + str( minv ) )
    
    # prepare for msom by flattening the array
    if append == 'C' :
        
        # row appended for each day
        stacked = dw_data.reshape( 171, 171, tdays*25, order='C' )
        
    elif append == 'F':
        
        # column appended for each class
        stacked = dw_data.reshape( 171, 171, tdays*25, order='F' )
        
    else :
        eprint( myname + ': bad append value ... exiting' )
        usage() 
    
    eprints( myname + ': outputting data ... ' )

    # needs to be protocol = 4
    out = open( outfile, 'wb' )
    pickle.dump( stacked, file=out, protocol=4 )
    out.close()
    eprint( 'done' )
