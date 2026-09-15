#! /usr/bin/env python3

'''
@file run_apply.py
@author Scott L. Williams, in collaboration with Elisa Piispa, Israel Pineda, María Solis-Aulestia, Cristina Yánez
@package ETo
@brief Compare multiple SOMs with each other using Cramer-V similarity measure.
@LICENSE
# 
#  Copyright (C) 2026 Scott L. Williams.
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

# run collect_data on smaller datasets

run_apply_copyright = 'run_apply.py Copyright (c) 2026 Scott L. Williams, released under GNU GPL V3.0'

import os
import sys
import itertools
import numpy as np
from ezprint import eprint, eprints

# list of normalized ETo variables to classify
data_set = [ './2022-2024_dw.npy' ]

'''
data_set = [
    '../data/cnorm/2022/2022-ENE.npy', '../data/cnorm/2022/2022-FEB.npy',
    '../data/cnorm/2022/2022-MAR.npy', '../data/cnorm/2022/2022-ABR.npy',
    '../data/cnorm/2022/2022-MAY.npy', '../data/cnorm/2022/2022-JUN.npy',
    '../data/cnorm/2022/2022-JUL.npy', '../data/cnorm/2022/2022-AGO.npy',
    '../data/cnorm/2022/2022-SEP.npy', '../data/cnorm/2022/2022-OCT.npy',
    '../data/cnorm/2022/2022-NOV.npy', '../data/cnorm/2022/2022-DIC.npy',
    
    '../data/cnorm/2023/2023-ENE.npy', '../data/cnorm/2023/2023-FEB.npy',
    '../data/cnorm/2023/2023-MAR.npy', '../data/cnorm/2023/2023-ABR.npy',
    '../data/cnorm/2023/2023-MAY.npy', '../data/cnorm/2023/2023-JUN.npy',
    '../data/cnorm/2023/2023-JUL.npy', '../data/cnorm/2023/2023-AGO.npy',
    '../data/cnorm/2023/2023-SEP.npy', '../data/cnorm/2023/2023-OCT.npy',
    '../data/cnorm/2023/2023-NOV.npy', '../data/cnorm/2023/2023-DIC.npy',
    
    '../data/cnorm/2024/2024-ENE.npy', '../data/cnorm/2024/2024-FEB.npy',
    '../data/cnorm/2024/2024-MAR.npy', '../data/cnorm/2024/2024-ABR.npy',
    '../data/cnorm/2024/2024-MAY.npy', '../data/cnorm/2024/2024-JUN.npy',
    '../data/cnorm/2024/2024-JUL.npy', '../data/cnorm/2024/2024-AGO.npy',
    '../data/cnorm/2024/2024-SEP.npy', '../data/cnorm/2024/2024-OCT.npy',
    '../data/cnorm/2024/2024-NOV.npy', '../data/cnorm/2024/2024-DIC.npy',
           ]
'''
out_dir = '../data/classes/'
lfile = '2022-2024_sparse.labels'

# ------------------------------------------------------------------------

# terminal spinner characters
spinner = itertools.cycle( ['\\','-', '|', '-', '/', '-','|'] )

# check if files exsis
def check_data_files():

    eprints( 'run_apply: checking if data files exists ... ' )
    for f in data_set:

        if not os.path.isfile( f ):
            eprint( 'run_apply: data file: ', f, ' does not exist...exiting' )
            sys.exit( 1 )
        
        eprints( next(spinner) )
        eprints('\b')
    
    eprint( 'yes' )

# -------------------------------------------------------------------------

if __name__ == '__main__':

    # declare version
    eprint( 'run_apply: python version =', sys.version[0:6])
    eprint( 'run_apply: numpy version  =', np.version.version )

    check_data_files()
    
    for f in data_set:

        year = f[14:18] # KLUDGE: ojo:  years are set in date string
        out_year = out_dir + year + '/'

        if not os.path.isdir( out_year ):
            eprint( '\nrun_apply: making directory:', out_year )
            os.makedirs( out_year, exist_ok=True )

        month = f[24:27]
        command = 'somclass -f ' + lfile + ' < ' + f + ' > ' \
                  + out_year +  year + '-' + month + '.npy'
        
        eprint( '\nrun_apply: running: ', command )
        os.system( command )
    
    eprint( '\nrun_apply: done' )

