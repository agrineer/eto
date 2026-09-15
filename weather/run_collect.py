#! /usr/bin/env python

'''
@file run_collect.py
@author Scott L. Williams, in collaboration with Elisa Piispa, Israel Pineda, María Solis-Aulestia, Cristina Yánez
@package ETo
@brief Read WRF output and output ETo variables.

@LICENSE
# 
#  run_collect.py Copyright (C) 2020-2026 Scott L. Williams.
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

run_collect_copyright = 'run_collect.py Copyright (c) 2020-2026 Scott L. Williams, released under GNU GPL V3.0'

import os
import sys
import getopt
import itertools
import numpy as np
from ezprint import eprint, eprints

out_dir = '../data/eto/'

# ------------------------------------------------------------------------

# check if files exsis
def check_date_files():

    eprints( myname + ': checking if date files exists ... ' )
    for f in dates_set:

        if not os.path.isfile( f ):
            eprint( myname + ': date file: ', f, ' does not exist...exiting' )
            sys.exit( 1 )
        
        eprints( next(spinner) )
        eprints('\b')
    
    eprint( 'yes' )

def usage():
        
    eprint( '\nusage: run_collect.py' )
    eprint( '       -h, --help' )
    eprint( '       -y year, --year=year # where year is in 2022,2023,2024' )
    eprint( '' )
    sys.exit(0)

def set_params( argv ):
    year = None

    try:                                
        opts, args = getopt.getopt( argv, 'hy:',['help','year='] )
            
    except getopt.GetoptError as e:
        eprint( myname + ': ' + str(e) )
        usage()                          
                   
    for opt, arg in opts:
            
        if opt in ( '-h', '--help' ):      
            usage()                     
 
        if opt in ('-y', '--year' ):
            if arg in ( '2022','2023','2024'):
                year = arg
            else:
                eprint( myname +
                        ': year must be in (2022,2023,2024) .. exiting' )
                usage()

    if year == None:
        eprint( myname + ': must have a year in (2022,2023,2024)' )
        usage()

    return year

# -------------------------------------------------------------------------

# some globals
myname = os.path.basename(__file__)[:-3] # no need for .py suffix
spinner = itertools.cycle( ['\\','-', '|', '-', '/', '-','|'] )

if __name__ == '__main__':

    # declare version
    eprint( myname + ': python version =', sys.version[0:6])
    eprint( myname + ': numpy version  =', np.version.version )

    year = set_params( sys.argv[1:] )

    # list of dates to process, very specific to 2022-2024
    dates_set = [
        '../data/dates/' + year + '/' + year + '-ENE.txt',
        '../data/dates/' + year + '/' + year + '-FEB.txt',
        '../data/dates/' + year + '/' + year + '-MAR.txt',
        '../data/dates/' + year + '/' + year + '-ABR.txt',
        '../data/dates/' + year + '/' + year + '-MAY.txt',
        '../data/dates/' + year + '/' + year + '-JUN.txt',
        '../data/dates/' + year + '/' + year + '-JUL.txt',
        '../data/dates/' + year + '/' + year + '-AGO.txt',
        '../data/dates/' + year + '/' + year + '-SEP.txt',
        '../data/dates/' + year + '/' + year + '-OCT.txt',
        '../data/dates/' + year + '/' + year + '-NOV.txt',
        '../data/dates/' + year + '/' + year + '-DIC.txt'
    ]
 
    check_date_files()
         
    for f in dates_set:

        #year = f[14:18] # years are set in date string, for dates generality
        out_year = out_dir + year + '/'
        if not os.path.isdir( out_year ):
            eprint( '\n' + myname + ': making directory:', out_year )
            os.makedirs( out_year, exist_ok=True )

        month = f[24:27]
        command = '../bin/collect_data.py < ' + f + ' > ' + out_year \
                   +  year + '-' + month + '.npy'
        
        eprint( '\n' + myname + ': running: ', command )
        os.system( command )
    
    eprint( '\n' + myname + ': done' )

