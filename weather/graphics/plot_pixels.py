#! /usr/bin/env python3

'''
@file plot_pixels.py
@author Scott L. Williams, in collaboration with Elisa Piispa, Israel Pineda, María Solis-Aulestia, Cristina Yánez
@package ETO_WEATHER
@brief Plot selected pixel values as bars.
@LICENSE
# 
#  Copyright (C) 2010-2026 Scott L. Williams.
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
# plot selected pixel values as bars.

plot_pixels_copyright = 'plot_pixels.py Copyright (c) 2010-2026 Scott L. Williams, released under GNU GPL V3.0'

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D

# define hours of interest
#start = 11*8                  # 12 noon      ( 1 hour )
#end = start + 1*8

start = 9*8                  # 10am - 2pm
end = start + 4*8

#start = 0                    # all day
#end = start + 24*8

# first read the sample file
infile = open( 'jan-mar_2019.csv' )
srcfile = './jan-mar_2019.npy'
outpath = 'ETo_4HR.pdf'
#title = 'Normalized ETo Weather Variables for 6 Pixels\nJan. 1, 2019\n12:00pm - 1:00pm'
title = 'Normalized ETo Weather Variables for 6 Pixels\nJan. 1, 2019\n10:00am - 2:00pm'
#title = 'Normalized ETo Weather Variables for 6 Pixels\nJan. 1, 2019\nAll Day'

# ------------------------------------------------------------------------

def make_legend( colors, labels ):
    
    # match jpg colors with a legend label
    handles = []
    for i in range( len(bands) ):
        
        patch = mpatches.Patch( color=colors[i], label=labels[i] )
        handles.append( patch )

        #count = count+1
       
    plt.legend( handles=handles, ncols=1, title='ETo Weather\nVariables',
                bbox_to_anchor=( 0.025,0.7),fontsize=7 )# bbox_to_anchor=(0.1,1.1), )


srcfile = infile.readline()              # get source filename

values = []                              # array of variable value arrays
xpixpos = []                             # array of sampled pixel x positions
for line in infile:
    
    items = line.split( ',' )            # parse out values from text line
    xpixpos.append( int( items[0] ) )    # grab pixel x position
    
    varvalues = []                       # array of variable values 
    for i in range(2,len(items)):      
        varvalues.append( float(items[i].strip()) )

    values.append( varvalues[::-1] )     # reverse order of values to make
                                         # graph more intiutive when rotated

# set up plot
figure = plt.figure()
ax = figure.add_subplot(111, projection='3d')

# lengths colors has to match number of samples
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple','tab:brown','tab:pink', 'tab:grey' ]

# run through x positions
for j in range( 0, len(xpixpos) ):

    # plot variable values for each pixel
    for i in range( start, end ):

        # plot the bar graph 
        #xs = range( len(values[i][start:end]) )
        ax.bar3d( i, xpixpos[j], 0, 0.25, 0.25, # 5.0, # use for 1HR
                  values[j][i], shade=False, color=colors[i%8], alpha=0.5)
 
    #ax.bar( xs, values[i][start:end],  zs=xpixpos[i], zdir='y',
    #        color=colors[::-1], alpha=0.7)

ax.set_xlabel('\nETo Variables',linespacing=1)
ax.set_ylabel('\nPixel X position\nY=0',linespacing=1)
ax.set_zlabel('\nNormalized ETo Variable value',linespacing=1)

# band labels
#bands = ['Rn', 'G', 'T', 'D', 'g', 'es', 'ea', 'u2']
bands = ['u', 'ea', 'es', '\u03B3', '\u0394', 'T', 'G', 'Rn']
labels = ['u   Wind', 'ea  Vapour Press.', 'es  Sat. Vapour Press.', '\u03B3    Psych. Const', '\u0394    Sat. Slope', 'T    Temp', 'G    Ground Heat Flux', 'Rn  Net Radiation.']
# NOTE: band labels should be used only on the single hour.
#       gets messy otherwise
if end-start == 8:
    
    # must be done before tick label
    ax.set_xticks( range(start,end) )
    ax.set_xticklabels( bands )       # prints out band labels
else:
    ax.set_xticklabels( [] )          # prints empty tick marks; hours > 1

make_legend( colors, labels )
figure.text( 0.01, 0.05, 'Source File: ' + srcfile, fontsize=7 )
figure.text( 0.01, 0.04, 'ETo Project, Yachay Tech University, July 2026',
                 fontsize=7 )

plt.title( title, y=0.9985 )

plt.savefig( outpath ) #, bbox_inches='tight' ) # bbox_inches removes extra white spaces

#plt.show()
