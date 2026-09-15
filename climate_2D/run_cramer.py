#! /usr/bin/env python3

'''
@file run_cramer.py
@author Scott L. Williams. in collaboration with Cristina Yanez, Israel Pineda
@package ETo
@brief Compare multiple SOMs with each other using Cramer-V similarity measure.
@LICENSE
# 
#  run_cramer.py Copyright (C) 2020-2026 Scott L. Williams.
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

# compare multiple SOMs with each other using Cramer-V similarity measure.

run_cramer_copyright = 'run_cramer.py Copyright (c) 2020-2026 Scott L. Williams, released under GNU GPL V3.0'

import os
import sys
import getopt
from cramer import cramer
from ezprint import eprint, eprints

mmap = True  # use memory map?

datafile = '../data/2D/2022/2022_h9fdw.npy'
outfile  = '../data/2D/2022/msom_col_stack_h9fdw/0.300000_50_linear_nonorm/cramer/cramer.results'
lutdir   = '../data/2D/2022/msom_col_stack_h9fdw/0.300000_50_linear_nonorm/cramer/luts'

somset = [ '../data/2D/2022/msom_col_stack_h9fdw/0.300000_50_linear_nonorm/0.300000_50_0.labels',
           '../data/2D/2022/msom_col_stack_h9fdw/0.300000_50_linear_nonorm/0.300000_50_1.labels',
           '../data/2D/2022/msom_col_stack_h9fdw/0.300000_50_linear_nonorm/0.300000_50_2.labels',
           '../data/2D/2022/msom_col_stack_h9fdw/0.300000_50_linear_nonorm/0.300000_50_3.labels',
           '../data/2D/2022/msom_col_stack_h9fdw/0.300000_50_linear_nonorm/0.300000_50_4.labels',
           '../data/2D/2022/msom_col_stack_h9fdw/0.300000_50_linear_nonorm/0.300000_50_5.labels',
           '../data/2D/2022/msom_col_stack_h9fdw/0.300000_50_linear_nonorm/0.300000_50_6.labels',
           '../data/2D/2022/msom_col_stack_h9fdw/0.300000_50_linear_nonorm/0.300000_50_7.labels',
           '../data/2D/2022/msom_col_stack_h9fdw/0.300000_50_linear_nonorm/0.300000_50_8.labels',
           '../data/2D/2022/msom_col_stack_h9fdw/0.300000_50_linear_nonorm/0.300000_50_9.labels'
          ] 

# ------------------------------------------------------------------------
myname = os.path.basename(__file__)
#spinner = itertools.cycle( ['\\','-', '|', '-', '/', '-','|'] ) # spinner chars

nsoms = len(somset) # number of soms

if __name__ == '__main__':
    
    # check if files exist
    for i in range( nsoms ):
        if not os.path.isfile( somset[i]):
            eprint( myname + ': file:', somset[i], 'does not exist...exiting' )
            sys.exit( 1 )

    results_dir = os.path.dirname( outfile )
    eprint( myname + ': results directory:', results_dir )
    if not os.path.isdir( results_dir ):
        os.makedirs( results_dir )

    if lutdir != None:
        if not os.path.isdir( lutdir ):
            os.makedirs( lutdir )

    # number of combinations
    total = 0
    for i in range( nsoms ):
        total += i

    results = open( outfile, 'w' )

    eprint( myname + ': comparing', nsoms, 'som mapfiles with each other, for a total of',
            total, ' comparisons.' )
    eprint( myname + ': results are in the file:', outfile )

    k = 0
    for j in range( nsoms ):
        for i in range( j+1, nsoms ):

            eprint( '\ncomparing: ', somset[i], somset[j] )

            # use train run numbers; OJO: must adjust for data dir length
            tag1 = somset[i][-8:-7]
            tag2 = somset[j][-8:-7]
            
            if lutdir != None:
                lutfile = lutdir + '/' + tag1 + '-' + tag2 + '.lut'
            else:
                lutfile = None

            Cv = cramer( datafile, somset[i], somset[j], lutfile, mmap )
            results.write( somset[i] + ' ' +  somset[j] + ' %.4f\n'%Cv )
            results.flush()
            k += 1
            eprint( 'result for', somset[i], ' ',  somset[j],
               ' -> Cv=%.4f'%Cv, ' %d'%k, 'out of %d'%total )

    results.close()


