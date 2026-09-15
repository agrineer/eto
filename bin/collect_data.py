#! /usr/bin/env python

'''
@file collect_data.py
@author Scott L. Williams, in collaboration with Elisa Piispa, Israel Pineda, María Solis-Aulestia, Cristina Yánez
@package ETo
@brief POLI batch implementation to construct a data set for ETo training
@LICENSE
# 
#  collect_data.py Copyright (C) 2020-2026 Scott L. Williams.
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

# constructs a data set for ETo vars training
# using 24 averaged time-slices on actual variables
# can use memory mapping for large datasets

# an embarrasing top-down, global variable prototype...

collect_data_copyright = 'collect_data.py Copyright (c) 2020-2026 Scott L. Williams, released under GNU GPL V3.0'

import gc
import os
import sys
import glob
import pickle
import tempfile
import itertools
import numpy as np

from wrf_src  import wrf_src
from prep_eto import prep_eto
from ezprint import eprint, eprints

mmap = True  # use memory map?

# USAGE:
#./collect_data.py < ../data/dates/3day.txt > ../data/eto/3day_eto.npy

# ----------------------------------------------------------------------------

def get_dates_file():
    
    # the program needs to 'seek' on the dates file
    # so read from stdin and write to temporary file to be able to seek
    try:

        # can't seem to make it in "ascii' mode
        dates_file = tempfile.NamedTemporaryFile( delete_on_close=True )
        dates_file.write( sys.stdin.buffer.read() )
 
        dates_file.seek( 0, 0 )
        return dates_file
    
    except Exception as e:
        eprint( str(e) )
        sys.exit( 1 )
        
# check if input files exists
def check_data_files( dates_file ):
        
    ndays = 0       # counter for number of days to process

    eprints( 'collect_data: checking if data files exists ... ' )
 
    for f in dates_file:

        f = f.decode()
        
        # check for new line and skip
        if f == '\n':
            continue

        if not os.path.isfile( f.strip() ):
            eprint( 'collect_data: datafile: ', f, ' does not exist...exiting' )
            dates_file.close()
            sys.exit( 1 )

        # day counter
        ndays += 1
        
        eprints( next(spinner) )
        eprints('\b')
    
    eprint( 'yes' )

    # rewind file pointer position for day dates
    dates_file.seek( 0, 0 )

    return ndays

def make_datacube( ndays ):

    # construct output array (geo shape is fixed at 171x171)
    # make attempt to memory map numpy array if swap is not available or
    # too small
    try:
        if mmap:
            collect_mmap = tempfile.NamedTemporaryFile( delete_on_close=True )
            eto_vars = np.memmap( collect_mmap, dtype=np.float32, mode='w+',
                                  shape=(sizey*ndays,sizex,sizez) ) 
            eprint( 'collect_data: using memory mapping' )
            
        else:

            # does not actually allocate at once,
            # instead numpy allocates (appends) as it is needed
            eto_vars = np.empty( shape=(sizey*ndays,sizex,sizez),
                                 dtype=np.float32 )
            eprint( 'collect_data: using ram memory' )
            
        return eto_vars

    except Exception as e:
        
        eprint( str(e) )
        eprint( 'collect_data: cannot allocate output numpy file...exiting ' ) 
        sys.exit( 1 )

# ----------------------------------------------------------------------------

if __name__ == '__main__':

    myname = os.path.basename(__file__)

    # declare version
    eprint( myname + ': python version =', sys.version[0:6])
    eprint( myname + ': numpy version  =', np.version.version )

    # terminal spinner characters
    spinner = itertools.cycle( ['\\','-', '|', '-', '/', '-','|'] )

    nvars = 8    # number of ETo input actual variables
    sizex = 171  # fixed geo sizes; TODO make dynamic
    sizey = 171
    sizez = 192  # 8*24=192   8 vars x 24 hours
 
    # instantiate the operators
    src = wrf_src.wrf_src()
    prep = prep_eto.prep_eto()
    prep.p.mmap = False     # for 171x171 pixels not really needed
                            # to memory map

    dates_file = get_dates_file()
    ndays = check_data_files( dates_file )
    eto_vars = make_datacube( ndays )
 
    # NOTE: time slice 11 corresponds to 12:00pm Ecuador time
    #       time slice  0 corresponds to 01:00am Ecuador time

    # template band string; 0-indexed.
    # string 'ts' gets replaced with actual hour below.
    # band string indicates which bands get extracted from WRF source file
    bandstr = 'TSK:ts,SWDOWN:ts,GLW:ts,GRDFLX:ts,T2:ts,PSFC:ts,Q2:ts,U10:ts,V10:ts'
    day = 0  # day counter
    
    for f in dates_file:

        f = f.decode() # make into real string not encoded
        
        # check for blank line
        if f == '\n':
            continue
        
        f = f.strip()  # remove white spaces
        eprints( '\rcollect_data: processing', f, ' ' )

        # run through hourly slices to augment feature space
        # read two hourly slices and average values over the day
        for i in range( 0, 24 ):

            # replace 'ts' with first time slice value and
            # set wrf_src parameters
            src.p.bandstr = bandstr.replace('ts','%02d'%i )               
            src.p.filepath = f
            src.run()
            wt1 = src.sink   # save first time slice buffers
             
            # get second time slice       
            src.p.bandstr = bandstr.replace('ts','%02d'%(i+1) )
            src.p.filepath = f
            src.run()
            wt2 = src.sink   # save second time slice buffers
 
            # average the values per buffer
            prep.source = (wt1 + wt2)/2.0

            # process raw variables to get input values
            # for Penman-Montieth equation
            prep.run()
            
            # time slice variable augmentation to feature space
            if i == 0: 
                aug = prep.sink
            else:
                aug = np.append( aug, prep.sink, axis=2 )

            ''' same thing done manually                
            for j in range( nvars ):
                   aug[:,:,((i-1)*nvars + j)] = prep.sink[:,:,j]
            '''           
            eprints( next(spinner) )
            eprints('\b')

        # fill in out buffer on daily basis
        yoff = sizey*day
        eto_vars[ yoff:yoff+sizey, :, : ] = aug
        
        day += 1

    # end day loop

    eprints( "\x1b[2K" )  # clear the line
    eprints( '\rcollect_data: processing ... done' )

    # open files are closed on exit by garbage collector
    
    if mmap:
        eto_vars.flush()     # flush values to file
      
    # save eto vars data as numpy file
    eprints( '\ncollect_data: outputing data ... ' )

    # attempts to make output faster
    #sys.stdout.reconfigure( line_buffering=True )
    #sys.stdout = open( sys.stdout.fileno(), "w", buffering=1024 )
    
    # must be pickle protocal=4; eto_vars.dump doesn't work
    pickle.dump( eto_vars, file=sys.stdout.buffer, protocol=4 )
    eprint( 'done' )
    # TODO: get lat lon buffers for each augmentation
    #       throw flag to do so, as it increase space demand
