#! /usr/bin/env python

'''
@file run_cnorm.py
@author Scott L. Williams, in collaboration with Elisa Piispa, Israel Pineda, María Solis-Aulestia, Cristina Yánez
@package ETo
@brief Normalize the interlaced ETo variables 
@LICENSE
# 
#  run_cnorm.py Copyright (C) 2020-2026 Scott L. Williams.
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

run_cnorm_copyright = 'run_cnorm.py Copyright (c) 2020-2026 Scott L. Williams, released under GNU GPL V3.0'

import os
import sys
import getopt
import itertools
import numpy as np
from ezprint import eprint, eprints
   
out_dir = '../data/cnorm/'

# ------------------------------------------------------------------------

# check if files exist
def check_data_files():

    eprints( myname + ': checking if data files exists ... ' )
    for f in data_set:

        if not os.path.isfile( f ):
            eprint( myname + ': data file: ', f, ' does not exist...exiting' )
            sys.exit( 1 )
        
        eprints( next(spinner) )
        eprints('\b')
    
    eprint( 'yes' )

def usage():
        
    eprint( '\nusage: ' + myname + '.py' )
    eprint( '       -h, --help' )
    eprint( '       -y year, --year=year     # where year is in 2022,2023,2024')
    eprint( '       -f labels, --file=coeffs' )
    eprint( '' )
    sys.exit(0)

def set_params( argv ):
    year = None
    coeffs = None

    try:                                
        opts, args = getopt.getopt( argv, 'hy:f:',
                                    ['help','year=','file='] )
            
    except getopt.GetoptError as e:
        eprint( myname + ': ' + str(e) )
        usage()                          
                   
    for opt, arg in opts:
            
        if opt in ( '-h', '--help' ):      
            usage()                     

        if opt in ('-f', '--file' ):
            if not os.path.isfile( arg ):
                eprint( myname + ': given file: ' +
                        arg + ' not found ... exiting' )
                sys.exit( 1 )
            coeffs = arg

        if opt in ('-y', '--year' ):
            if arg in ( '2022','2023','2024'):
                year = arg
            else:
                eprint( myname +
                        ': year must be in (2022,2023,2024) .. exiting' )
                usage()

    if year == None:
        eprint( myname + ': must have a year in (2022,2023,2024) ... exiting' )
        usage()
        
    if coeffs == None:
        eprint( myname + ': must have coefficients file ... exiting' )
        usage()

    return year, coeffs

# -------------------------------------------------------------------------

myname = os.path.basename(__file__)[:-3] # no need for .py suffix
spinner = itertools.cycle( ['\\','-', '|', '-', '/', '-','|'] )

if __name__ == '__main__':

    # declare version
    eprint( myname + ': python version =', sys.version[0:6])
    eprint( myname + ': numpy version  =', np.version.version )

    year, coeffs = set_params( sys.argv[1:] )

    # list of numpy ETo variables to normalize
    data_set = [
        '../data/eto/' + year + '/' + year + '-ENE.npy',
        '../data/eto/' + year + '/' + year + '-FEB.npy',
        '../data/eto/' + year + '/' + year + '-MAR.npy',
        '../data/eto/' + year + '/' + year + '-ABR.npy',
        '../data/eto/' + year + '/' + year + '-MAY.npy',
        '../data/eto/' + year + '/' + year + '-JUN.npy',
        '../data/eto/' + year + '/' + year + '-JUL.npy',
        '../data/eto/' + year + '/' + year + '-AGO.npy',
        '../data/eto/' + year + '/' + year + '-SEP.npy',
        '../data/eto/' + year + '/' + year + '-OCT.npy',
        '../data/eto/' + year + '/' + year + '-NOV.npy',
        '../data/eto/' + year + '/' + year + '-DIC.npy'
    ]
   
    check_data_files()
 
    for f in data_set:

        #year = f[12:16] # years are set in date string for data generality
        out_year = out_dir + year + '/'
        if not os.path.isdir( out_year ):
            eprint( '\n' + myname + ': making directory:', out_year )
            os.makedirs( out_year, exist_ok=True )

        month = f[22:25]
        command = 'cnorm -f ' + coeffs + ' -c < ' + f + ' > ' \
                  + out_year +  year + '-' + month + '.npy'
        
        eprint( '\n' + myname + ': running: ', command )
        os.system( command )
    
    eprint( '\n' + myname + ': done' )

