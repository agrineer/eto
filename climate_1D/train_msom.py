#! /usr/bin/env python3

'''
@file train_msom.py
@author Scott L. Williams, in collaboration with Elisa Piispa, Israel Pineda, María Solis-Aulestia, Cristina Yánez
@package ETo
@brief #  POLI batch implementation to train SOM and writes out labels
@LICENSE
# 
#  train_msom.py Copyright (C) 2020-2026 Scott L. Williams.
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
#  poli batch implementation to train SOM and write out labels

train_msom_copyright = 'train_msom.py Copyright (c) 2020-2026 Scott L. Williams, released under GNU GPL V3.0'

import os
import sys
import getopt
from msom import msom
from npy_src import npy_src
from ezprint import eprint, eprints

mmap = False                     # use memory map?

# instantiate the operators

# numpy source
src = npy_src.npy_src()         # instantiate image source
src.p.mmap = mmap               

# mini-som
ms = msom.msom()                # instantiate
ms.p.mmap = mmap                # use memory map
ms.p.shape = (3,4)              # neural net grid shape
ms.p.sigma = 1.5                # ~ 1/2 min grid size    
                                      
#ms.p.nepochs = 5                # number of epochs. an epoch
                                # is a full sampling of the data.
                                # multiple epochs allow for pixel
                                # reconsideration and node reassignment
                                      
ms.p.show_progress = False

ms.p.init_weights = 'pca'             # random or pca
ms.p.neighborhood_function = 'gaussian'
ms.p.topology = 'hexagonal'      
ms.p.activation_distance = 'euclidean' 
ms.p.output_type = 'labels'

ms.p.apply_classification = False
ms.p.rorder = True              # sample at random
ms.p.seed = None                # None means generate a seed.
                                # no fair assigning one
                                
ms.p.decay_function = 'exponential' # exponential or linear
ms.p.calc_epoch_errors = True

#------------------------------------------------------------

def usage():
        
    eprint( '\nusage: train_som.py' )
    eprint( '       -h, --help' )
    eprint( '       -d decay, --decay=decay # decay in (linear,exponential)')
    eprint( '       -e nepochs, --epochs=nepochs' )
    eprint( '       -i, --init=[random,pca]' )
    eprint( '       -o outdir, --outdir=outdir' )
    eprint( '       -r lrate, --rate=lrate' )  
    eprint( '       -s sigma, --suffix=sigma' )
    eprint( '       -t, --tail=tail # series number' )
    sys.exit( 1 )
    
def set_params( argv ):
    
    odir = None
    tail = None
    ms.p.decay_function = None
    src.p.filepath = None
    ms.p.init_weights = None
    ms.p.sigma = None
    ms.p.nepochs = None
    ms.p.rate = None

    try:                                
        opts, args = getopt.getopt( argv, 'hd:e:f:i:o:r:s:t:y:',
                                    ['help', 'epoch=','file=','init=',
                                     'rate=','sigma=', 'tail=', 'outdir='] )
            
    except getopt.GetoptError as e:
        eprint( 'train_msom: ' + str(e) )
        self.usage()                          
        sys.exit( 2 )  
                   
    for opt, arg in opts:
            
        if opt in ( '-h', '--help' ):      
            self.usage()                     

        if opt in ('-d', '--decay'):
            if arg not in ('linear','exponential'):
                eprint( 'train_msom: unknown decay function:', arg, '...exiting' )
                usage()
            ms.p.decay_function = arg

        if opt in ('-e', '--epochs'):
            ms.p.nepochs = int( arg )

        if opt in ('-f', '--file'):
            if not os.path.isfile( arg ):
                eprint( 'train_msom: file not found:', arg, 'exiting' )
                usage()
            src.p.filepath = arg
            
        if opt in ('-o', '--outdir'):
            outdir = arg
 
        if opt in ('-r', '--rate'):
            ms.p.rate = float( arg )
            
        if opt in ('-i', '--init'):
            if arg not in ('random','pca' ):
                eprint( 'train_msom: bad init value:', arg, 'exiting' )
                usage()
            ms.p.init_weights = arg

        if opt in ('-y', '--year' ):
            year = arg

        if opt in ('-t', '--tail' ):
            tail = arg

        if opt in ('-s', '--sigma' ):
            ms.p.sigma = float(arg)

    if outdir == None:
        eprint( 'train_msom: must have output dir ...exiting' )
        usage()
        
    if tail == None:
        eprint( 'train_msom: must have tail serial number...exiting' )
        usage()
        
    if src.p.filepath == None:
        eprint( 'train_msom: input data file path not given...exiting' )
        usage()

    if ms.p.decay_function == None:
        eprint( 'train_msom: must have decay_function...exiting' )
        usage()

    if ms.p.sigma == None:
        eprint( 'train_msom: must have sigma...exiting' )
        usage()

    if ms.p.nepochs == None:
        eprint( 'train_msom: must have number of epochs...exiting' )
        usage()

    if ms.p.rate == None:
        eprint( 'train_msom: must have learning rate...exiting' )
        usage()

    if ms.p.init_weights == None:
        eprint( 'train_msom: must have learning rate...exiting' )
        usage()

    return outdir, tail

# -------------------------------------------------------------------------

outdir, tail = set_params( sys.argv[1:] )

# adjust parameters
#year_dir = '../data/2D/' + year + '/'
#target_dir = year_dir + 'msom/' + '%.6f'%float( ms.p.rate )  + \
#    '_' + str( ms.p.nepochs ) + '/'

eprint( ': output directory: ' + outdir )
if not os.path.isdir( outdir ):
    eprint( 'train_msom: making directory' + outdir )
    os.makedirs( outdir, exist_ok=True )

ms.p.labels_prefix = outdir + '/%.6f'%float( ms.p.rate ) + \
    '_' + str( ms.p.nepochs ) + '_' + tail

# read the training data
eprints( 'reading datafile: ' + src.p.filepath + '...' )
src.run()
eprint( ' done' )

# link src output to msom input and run
eprint( 'training ...' )
ms.source = src.sink
ms.run() # train it here
eprint( 'training done' )
