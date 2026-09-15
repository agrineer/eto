#! /usr/bin/env python

'''
@file plot_countours.py
@author Scott L. Williams, in collaboration with Elisa Piispa, Israel Pineda, María Solis-Aulestia, Cristina Yánez
@package ETo
@brief show the pixel difference between two differently labeled images
@LICENSE

#  plot_contours.py Copyright (C) 2020-2026 Scott L. Williams
#                   In collaboration with Cristina Yanez and Israel Pineda
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

import os
import sys
import getopt

import matplotlib
import numpy as np
from npy_src import npy_src
from matplotlib import colors
import matplotlib.pyplot as plt
from ezprint import eprint, eprints
import matplotlib.patches as mpatches
from matplotlib.patches import Shadow

# -------------------------------------------------------------------------

def usage():
        
    eprint( '\nusage: ' + myname + '.py' )
    eprint( '       -h, --help' )
    eprint( '       -i inpath, --inpath=inpath' )
    eprint( '       -o outpath, --outpath=outpath' )
    eprint( '       -l lutpath, --lutpath=lutpath' )
    eprint( '       -f true/false, --fill=true/false' )

    eprint( '' )
    sys.exit( 1 )

def set_params( argv ):
    
    inpath = None
    outpath = None
    lutpath = None
    fill = False
    
    try:                                
        opts, args = getopt.getopt( argv, 'hf:i:o:l:',
                                    ['help','inpath=','outpath=','lutpath'] )
            
    except getopt.GetoptError as e:
        eprint( myname + ': ' + str(e) )
        usage()                          
                   
    for opt, arg in opts:
            
        if opt in ( '-h', '--help' ):      
            usage()

        if opt in ( '-f', '--fill' ):
            if arg in ('T','t','True','true'):
                fill = True
            elif arg in ('F','f','False','false' ):
                fill = False
            else:
                eprint( myname + ': unrecognized fill value: ' + arg + ' ... exiting' )

        if opt in ('-i', '--inpath'):

            inpath = arg
            if not os.path.isfile( inpath ):
                eprint( myname + ': input file: ' + infile + \
                        ' does not exists ... exiting' )
                usage()
                
        if opt in ('-o', '--outpath'):            
            outpath = arg  # gets created later if needed

        if opt in ('-l', '--lutpath'):

            lutpath = arg
            if not os.path.isfile( lutpath ):
                eprint( myname + ': lut file: ' + lutpath + \
                        ' does not exists ... exiting' )
                usage()

    if inpath == None:
        eprint( myname + ': must have an input file ... exiting' )
        usage()
        
    if outpath == None:
        eprint( myname + ': must have an output file ... exiting' )
        usage()

    if lutpath == None:
        eprint( myname + ': must have a color lut input file path ... exiting' )
        usage()

    eprint( myname + ': using parameters:' )
    eprint( '                   fill = ', fill )
    eprint( '                 inpath = ', inpath  )
    eprint( '                outpath = ', outpath )
    eprint( '                lutpath = ', lutpath )
    
    outdir = os.path.dirname( outpath )
    if not os.path.isdir( outdir ):
        eprint( myname + ': making directory: ' + outdir )
        os.makedirs( outdir )

    return inpath, outpath, lutpath, fill

#----------------------------------------------------

# some globals
myname = os.path.basename(__file__)[:-3] # no need for .py suffix

def make_ticks( ax ):

   # set tick marks
    ticks = range(0,180,20)
    ax.set_yticks( ticks )
    ax.set_xticks( ticks )

    
def read_data( fpath ):
    
    # read the numpy file
    eprints( myname + ': reading datafile: ' + fpath + '...' )
    src = npy_src.npy_src()
    src.p.filepath = fpath
    src.run()
    eprint( myname + ': reading datafile done' )
    
    image = src.sink[:,:,0] # make 2D
    return image


def make_legend( lut ):
    
    # match jpg colors with a legend label
    handles = []
    count = 0
    #rlut = reversed( llut )
    for c in lut:

        c = c.strip()
        patch = mpatches.Patch( color=c, label=str( count ) )
        handles.append( patch )

        count = count+1
       
    plt.legend( handles=handles,ncols=1,title='ETo\nClimate\nClasses',
                bbox_to_anchor=(-0.15,0.9),fontsize=7 )# bbox_to_anchor=(0.1,1.1), )


def get_lut( path ):

    flut = open( path, 'r' )  # read the look up table file

    lut = []
    for c in flut:
        lut.append( c.strip() )
    #eprint( llut )

    return lut


if __name__ == '__main__':

    # declare versions
    eprint( myname + ':     python version =', sys.version[0:6])
    eprint( myname + ': matplotlib version =', matplotlib.__version__)
    
    inpath, outpath, lutpath, fill = set_params( sys.argv[1:] )
    
    nlabels = 12  # apriori hardwired value

    image = read_data( inpath )  
    lut = get_lut( lutpath )
    
    # set up plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')
    ax.xaxis.set_label_position('top')
    ax.xaxis.set_ticks_position('top')

    cmap = colors.ListedColormap( lut[:nlabels] )
    levels = np.arange( 0, nlabels, 1.0 )

    if fill:
        CS = ax.contourf( image, levels, cmap=cmap )
    else:
        CS = ax.contour( image, levels, linewidths=.05, cmap=cmap )

    plt.ylim( 171, 0 ) # flips the image

    make_legend( lut[:nlabels] )
    make_ticks( ax )
    
    fig.text( 0.38, 0.085, 'Source File: ' + os.path.basename(inpath),
              fontsize=7 )
    fig.text( 0.81, 0.25, 'ETo Project, Yachay Tech University, July 2026',
                  rotation=90, fontsize=7 )
 
    title = 'Contour Image Showing 2D ETo Climate Classes 2024'
    plt.title( title, y=1.07, fontweight ="bold" )
    plt.savefig( outpath ) #, bbox_inches='tight' ) # bbox_inches removes extra white spaces
    #plt.show() # uncomment to see plot on screen

