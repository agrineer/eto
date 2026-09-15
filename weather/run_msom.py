#! /usr/bin/env python

'''
@file run_msom.py
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
# poli batch implementation to train SOM and writes out labels
# basically sets up msom parameters.

run_msom_copyright = 'run_msom.py Copyright (c) 2020-2026 Scott L. Williams, released under GNU GPL V3.0'

import os
import sys
import getopt
from msom import msom
from npy_src import npy_src
from ezprint import eprint, eprints

mmap = False                                # use memory map?

# instantiate the operators

# numpy source
src = npy_src.npy_src()         # instantiate image source
src.p.filepath = './3day_norm.npy'         # data to train on
src.p.mmap = mmap               

# mini-som
ms = msom.msom( 'msom' )        # instantiate
ms.p.mmap = mmap                # use memory map
ms.p.shape = (5,5)              # neural net grid shape
ms.p.sigma = 2.5                
                                      
ms.p.nepochs = 4                # number of epochs. an epoch
                                # is a full sampling of the data.
                                # multiple epochs allow for pixel
                                # reconsideration and node reassignment
                                      
ms.p.rate = 0.00724             # learning rate
ms.p.show_progress = True

ms.p.init_weights = 'random'       # random or pca
ms.p.neighborhood_function = 'gaussian'
ms.p.topology = 'hexagonal'      
ms.p.activation_distance = 'euclidean' 
ms.p.output_type = 'labels'
ms.p.mapfile_prefix = '3day'

ms.p.apply_classification = False
ms.p.rorder = True              # sample at random
ms.p.seed = None                # None means generate a seed.
                                # no fair assigning one
ms.p.decay_function = 'inverse' 
ms.p.calc_epoch_errors = False 

#------------------------------------------------------------

# print the (partial) parameters
eprint( '\nparameters for run_msom:')
eprint( 'number of epochs = ', ms.p.nepochs )
eprint( '   learning rate = ', ms.p.rate )
eprint( '      memory map = ', ms.p.mmap )
eprint( '        filepath = ', src.p.filepath )
eprint( '   init_weuights = ', ms.p.init_weights )
eprint( '    neighborhood = ', ms.p.neighborhood_function )
eprint( '        topology = ', ms.p.topology )     
eprint( '   act._distance = ', ms.p.activation_distance ) 
eprint( '     output type = ', ms.p.output_type )
eprint( '  mapfile_prefix = ', ms.p.mapfile_prefix )
eprint( '    random order = ', ms.p.rorder )
eprint( '            seed = ', ms.p.seed )
eprint( '  decay function = ', ms.p.decay_function, '\n' )

# read the training data
eprints( 'reading datafile: ' + src.p.filepath + '...' )
src.run()
eprint( ' done' )

# link src output to msom input and run
eprint( 'training ...' )
ms.source = src.sink
ms.run() # train it here
eprint( 'training done' )
