#! /usr/bin/env python
'''
@file plot_contours.py
@author Scott L. Williams, in collaboration with Elisa Piispa, Israel Pineda, María Solis-Aulestia, Cristina Yánez
@package ETo
@brief show the pixel difference between two differently labeled images
@LICENSE

#  plot_contours.py
# 
#  Copyright (C) 2020-2026 Scott L. Williams.
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
plot_contours_copyright = 'plot_contours.py Copyright (c) 2020-2026 Scott L. Williams, released under GNU GPL V3.0'

import sys
import numpy as np
from npy_src import npy_src
import matplotlib.pyplot as plt
from ezprint import eprint, eprints
#from scale_pack import scale

#dirpath = './2021/SOM_5x5_9_02_3_1/'
dirpath = './'
nlabels = 12

# numpy source
src = npy_src.npy_src()        # instantiate
src.p.filepath = dirpath + '2022-2024_1_classified.npy'

# read the label image
eprints( 'reading datafile: ' + src.p.filepath + '...' )
src.run()
eprint( 'done' )

'''
# scale it for contouring
sc = scale.scale( 'scale' )                        # instantiate
sc.params.sx = 6.0
sc.params.sy = 6.0
sc.source = src.sink
sc.run()

# contour the scaled image
image = sc.sink[:,:,0]
'''
image = src.sink[:,:,0]

# set up plot
fig,ax = plt.subplots(1,1)
levels = np.arange(1, nlabels, 1.0)
CS = ax.contour( image, levels, linewidths=.05, colors='black' )
#ax.clabel( CS, inline=True, fontsize=10 )

plt.ylim( 171, 0 ) # apparently vertically flips the image

plt.title( 'Source file: ' + src.p.filepath )
plt.show()
