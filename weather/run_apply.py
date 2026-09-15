#! /usr/bin/env python

'''
@file run_apply.py
@author Scott L. Williams, in collaboration with Elisa Piispa, Israel Pineda, María Solis-Aulestia, Cristina Yánez
@package ETo
@brief Classify data using a labels file
@LICENSE
# 
#  run_apply.py Copyright (C) 2020-2026 Scott L. Williams.
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

run_apply_copyright = 'run_apply.py Copyright (c) 2020-2026 Scott L. Williams, released under GNU GPL V3.0'

import os
import sys
import getopt
import itertools
import numpy as np
from ezprint import eprint, eprints

out_dir = '../data/classes/'

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
    eprint( '       -y year, --year=year # where year is in 2022,2023,2024' )
    eprint( '       -f labels, --file=labels' )
    eprint( '' )
    sys.exit(0)

def set_params( argv ):
    year = None
    labels = None

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
            labels = arg

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
        
    if labels == None:
        eprint( myname + ': must have labels file ... exiting' )
        usage()

    return year, labels

# -------------------------------------------------------------------------

myname = os.path.basename(__file__)[:-3] # no need for .py suffix
spinner = itertools.cycle( ['\\','-', '|', '-', '/', '-','|'] )

if __name__ == '__main__':

    # declare version
    eprint( myname + ': python version =', sys.version[0:6])
    eprint( myname + ': numpy version  =', np.version.version )

    year, labels = set_params( sys.argv[1:] )

    data_set = [
        '../data/cnorm/' + year + '/' + year + '-ENE.npy',
        '../data/cnorm/' + year + '/' + year + '-FEB.npy',
        '../data/cnorm/' + year + '/' + year + '-MAR.npy',
        '../data/cnorm/' + year + '/' + year + '-ABR.npy',
        '../data/cnorm/' + year + '/' + year + '-MAY.npy',
        '../data/cnorm/' + year + '/' + year + '-JUN.npy',
        '../data/cnorm/' + year + '/' + year + '-JUL.npy',
        '../data/cnorm/' + year + '/' + year + '-AGO.npy',
        '../data/cnorm/' + year + '/' + year + '-SEP.npy',
        '../data/cnorm/' + year + '/' + year + '-OCT.npy',
        '../data/cnorm/' + year + '/' + year + '-NOV.npy',
        '../data/cnorm/' + year + '/' + year + '-DIC.npy'
    ]

    check_data_files()
    
    for f in data_set:

        #year = f[14:18] # KLUDGE: ojo:  years are set in date string
        out_year = out_dir + year + '/'

        if not os.path.isdir( out_year ):
            eprint( '\n' + myname + ': making directory:', out_year )
            os.makedirs( out_year, exist_ok=True )

        month = f[24:27]
        command = 'somclass -f ' + labels + ' < ' + f + ' > ' \
                  + out_year +  year + '-' + month + '.npy'
        
        eprint( '\n' + myname + ': running: ', command )
        os.system( command )
    
    eprint( '\n' + myname + ': done' )

